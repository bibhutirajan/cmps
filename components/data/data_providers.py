"""
Data Providers for Charge Mapping Application

This module contains the data abstraction layer with providers for different data sources.
Supports LOCAL, SANDBOX, and PRODUCTION environments.
"""

import os
import pandas as pd
import streamlit as st
from abc import ABC, abstractmethod
from typing import Dict, Any
from config import get_snowflake_session


class DataProvider(ABC):
    """Abstract base class for data providers"""
    
    @abstractmethod
    def get_charges(self, customer: str, charge_type: str = None, page: int = 1, page_size: int = 50) -> pd.DataFrame:
        """Get charges data with pagination"""
        pass
    
    @abstractmethod
    def get_rules(self, customer: str) -> pd.DataFrame:
        """Get rules data"""
        pass
    
    @abstractmethod
    def create_rule(self, rule_data: Dict[str, Any]) -> bool:
        """Create a new rule"""
        pass
    
    @abstractmethod
    def update_rule(self, rule_id: str, rule_data: Dict[str, Any]) -> bool:
        """Update an existing rule"""
        pass
    
    @abstractmethod
    def update_priority(self, rule_id: str, new_priority: int) -> bool:
        """Update rule priority"""
        pass


class SnowflakeDataProvider(DataProvider):
    """Snowflake data provider for all environments (LOCAL, SANDBOX, PRODUCTION)"""
    
    def __init__(self, session, database: str = "SANDBOX", schema: str = "BMANOJKUMAR"):
        self.session = session
        self.database = database
        self.schema = schema
        
        # Customer name to organization ID mapping
        self.customer_to_org_id = {
            "Yardi": "75",
            "AmerescoFTP": "1412"
        }
    
    def get_environment(self) -> str:
        """Determine the current environment based on configuration"""
        # Check if we're in production environment
        is_production = (
            os.getenv("ENVIRONMENT", "").upper() == "PRODUCTION" or
            os.getenv("SNOWFLAKE_DATABASE", "").upper() == "ARCADIA" or
            "arcadia.export.hex_uc_charge_mapping_delivery" in os.getenv("CHARGES_TABLE", "")
        )
        
        if is_production:
            return "PRODUCTION"
        else:
            return "SANDBOX"  # LOCAL and SANDBOX both use SANDBOX tables
    
    def get_organization_id(self, customer: str) -> str:
        """Convert customer name to organization ID"""
        return self.customer_to_org_id.get(customer, customer)
    
    def get_charges(self, customer: str, charge_type: str = None, page: int = 1, page_size: int = 50) -> pd.DataFrame:
        """Get charges data from Snowflake based on environment and charge type with pagination"""
        try:
            environment = self.get_environment()
            org_id = self.get_organization_id(customer)
            
            # Build WHERE clause based on charge type
            if charge_type and "Uncategorized" in charge_type:
                where_clause = f"ODIN_ORGANIZATION_ID = '{org_id}' AND (CHARGE_ID IS NULL OR CHARGE_ID = 'ch.uncategorized_charge')"
            else:
                # Default: show all charges for the organization
                where_clause = f"ODIN_ORGANIZATION_ID = '{org_id}'"
                
            # Get table configuration
            table_config = self._get_table_config()
            table_name = table_config['charges_table']
            
            # Calculate offset for pagination
            offset = (page - 1) * page_size
            
            # Build query using table name with pagination
            query = f"""
            SELECT 
                ODIN_STATEMENT_ID as STATEMENT_ID,
                STATEMENT_DATE as STATEMENT_CREATED_DATE,
                UTILITY_PROVIDER_NAME as PROVIDER_NAME,
                NORMALIZED_ACCOUNT_NUMBER as ACCOUNT_NUMBER,
                TARIFF_NAME as CHARGE_NAME,
                CHARGE_ID as CHARGE_ID,
                MEASUREMENT_TYPE as CHARGE_MEASUREMENT,
                SERVICE_TYPE
            FROM {table_name}
                WHERE {where_clause}
                ORDER BY STATEMENT_DATE DESC, ODIN_STATEMENT_ID
            LIMIT {page_size} OFFSET {offset}
                """
            
            return self.session.sql(query).to_pandas()
        except Exception as e:
            st.error(f"Error fetching charges data: {str(e)}")
            return pd.DataFrame()
    
    def get_charges_count(self, customer: str, charge_type: str = None) -> int:
        """Get total count of charges for pagination"""
        try:
            environment = self.get_environment()
            org_id = self.get_organization_id(customer)
            
            # Build WHERE clause based on charge type
            if charge_type and "Uncategorized" in charge_type:
                where_clause = f"ODIN_ORGANIZATION_ID = '{org_id}' AND (CHARGE_ID IS NULL OR CHARGE_ID = 'ch.uncategorized_charge')"
            else:
                # Default: show all charges for the organization
                where_clause = f"ODIN_ORGANIZATION_ID = '{org_id}'"
            
            # Get table configuration
            table_config = self._get_table_config()
            table_name = table_config['charges_table']
            
            # Build count query
            query = f"""
            SELECT COUNT(*) as total_count
            FROM {table_name}
            WHERE {where_clause}
            """
            
            result = self.session.sql(query).to_pandas()
            return int(result.iloc[0]['TOTAL_COUNT']) if not result.empty else 0
        except Exception as e:
            st.error(f"Error fetching charges count: {str(e)}")
            return 0
    
    def _build_where_clause(self, base_where: str, filters: dict) -> str:
        """Build WHERE clause for filtering rules data"""
        where_conditions = [base_where]
        
        # Rule type filter
        if filters.get('rule_type') and filters['rule_type'] != 'All':
            if filters['rule_type'] == 'Custom':
                where_conditions.append("RULE_TYPE = 'Custom'")
            elif filters['rule_type'] == 'Global':
                where_conditions.append("RULE_TYPE = 'Global'")
        
        # Charge ID filter
        if filters.get('charge_id') and filters['charge_id'] != 'All Charge IDs':
            where_conditions.append(f"CHARGE_ID = '{filters['charge_id']}'")
        
        # Provider filter
        if filters.get('provider') and filters['provider'] != 'All Providers':
            where_conditions.append(f"PROVIDER_ALIAS = '{filters['provider']}'")
        
        # Charge name filter (exact matching for both custom and global rules)
        if filters.get('charge_name') and filters['charge_name'] != 'All Charge Names':
            charge_name = filters['charge_name'].replace("'", "''")  # Escape single quotes for SQL
            # For custom rules, filter on CHARGE_MAPPING_RULE
            # For global rules, filter on CHARGE_REGEX_RULE
            rule_type = filters.get('rule_type', 'All')
            if rule_type == "Custom":
                where_conditions.append(f"CHARGE_MAPPING_RULE = '{charge_name}'")
            elif rule_type == "Global":
                where_conditions.append(f"CHARGE_REGEX_RULE = '{charge_name}'")
            # For "All" rule type, we don't add charge name filtering here
            # as it will be handled separately for each table
        
        return " AND ".join(where_conditions)
    
    def _get_table_config(self) -> Dict[str, str]:
        """Get database, schema, and table configuration based on environment"""
        environment = self.get_environment()
        
        # TEMPORARY: Always use PRODUCTION tables (bypassing SANDBOX/LOCAL)
        # TODO: Uncomment the environment-based logic below when ready to revert
        return {
            'database': 'arcadia',
            'schema': 'lakehouse',
            'custom_rules_table': 'f_combined_customer_charge_rules',
            'global_rules_table': 'f_combined_provider_template_charge_rules',
            'charges_table': 'arcadia.export.hex_uc_charge_mapping_delivery'
        }
        
        # COMMENTED OUT - Original environment-based logic:
        # if environment == "PRODUCTION":
        #     return {
        #         'database': 'arcadia',
        #         'schema': 'lakehouse',
        #         'custom_rules_table': 'f_combined_customer_charge_rules',
        #         'global_rules_table': 'f_combined_provider_template_charge_rules',
        #         'charges_table': 'arcadia.export.hex_uc_charge_mapping_delivery'
        #     }
        # else:
        #     # Use SANDBOX tables (for both LOCAL and SANDBOX environments)
        #     return {
        #         'database': 'SANDBOX',
        #         'schema': 'BMANOJKUMAR',
        #         'custom_rules_table': 'f_combined_customer_charge_rules',
        #         'global_rules_table': 'f_combined_provider_template_charge_rules',
        #         'charges_table': 'SANDBOX.BMANOJKUMAR.hex_uc_charge_mapping_delivery'
        #     }
    
    def _build_custom_rules_query(self, table_name: str, customer: str, filters: dict) -> str:
        """Build custom rules query with table name parameter"""
        custom_base_where = f"CUSTOMER_NAME = '{customer}'"
        custom_where = self._build_where_clause(custom_base_where, filters)
        
        # For "All" rule type with charge name filter, add charge name filtering to custom rules
        if filters.get('rule_type') == 'All' and filters.get('charge_name') and filters['charge_name'] != 'All Charge Names':
            charge_name = filters['charge_name'].replace("'", "''")  # Escape single quotes for SQL
            custom_where += f" AND CHARGE_MAPPING_RULE = '{charge_name}'"
        
        return f"""
        SELECT 
            CHIPS_BUSINESS_RULE_ID as RULE_ID,
            CUSTOMER_NAME,
            PRIORITY_ORDER,
            CHARGE_MAPPING_RULE as CHARGE_NAME,
            CHARGE_ID,
            SERVICE_TYPE,
            ACCOUNT_NUMBER,
            PROVIDER_ALIAS as PROVIDER_NAME,
            CREATED_AT as CREATED_DATE,
            UPDATED_AT as MODIFIED_DATE,
            CREATED_BY,
            LAST_MODIFIED_BY as MODIFIED_BY,
            MEASUREMENT_TYPE as CHARGE_MEASUREMENT,
            'Custom' as RULE_TYPE
        FROM {table_name}
        WHERE {custom_where}
        ORDER BY PRIORITY_ORDER
        """
    
    def _build_global_rules_query(self, table_name: str, filters: dict) -> str:
        """Build global rules query with table name parameter"""
        global_base_where = "IS_ENABLED = TRUE"
        global_where = self._build_where_clause(global_base_where, filters)
        
        # For "All" rule type with charge name filter, add charge name filtering to global rules
        if filters.get('rule_type') == 'All' and filters.get('charge_name') and filters['charge_name'] != 'All Charge Names':
            charge_name = filters['charge_name'].replace("'", "''")  # Escape single quotes for SQL
            global_where += f" AND CHARGE_REGEX_RULE = '{charge_name}'"
        
        return f"""
        SELECT 
            CHIPS_EXTRACTION_CHARGE_RULE_ID as RULE_ID,
            'Global' as CUSTOMER_NAME,
            POSITION as PRIORITY_ORDER,
            CHARGE_REGEX_RULE as CHARGE_NAME,
            CHARGE_ID,
            NULL as SERVICE_TYPE,
            ACCOUNT_NUMBER,
            PROVIDER_ALIAS as PROVIDER_NAME,
            CREATED_AT as CREATED_DATE,
            LAST_MODIFIED_AT as MODIFIED_DATE,
            CREATED_BY,
            LAST_MODIFIED_BY as MODIFIED_BY,
            MEASUREMENT_TYPE as CHARGE_MEASUREMENT,
            'Global' as RULE_TYPE
        FROM {table_name}
        WHERE {global_where}
        ORDER BY POSITION
        """

    def get_rules(self, customer: str, filters: Dict[str, str] = None) -> pd.DataFrame:
        """Get rules data from Snowflake based on environment with optional filters"""
        try:
            environment = self.get_environment()
            filters = filters or {}
            
            # Get table configuration
            table_config = self._get_table_config()
            custom_table = f"{table_config['database']}.{table_config['schema']}.{table_config['custom_rules_table']}"
            global_table = f"{table_config['database']}.{table_config['schema']}.{table_config['global_rules_table']}"
            
            # Build queries using table names
            custom_rules_query = self._build_custom_rules_query(custom_table, customer, filters)
            global_rules_query = self._build_global_rules_query(global_table, filters)
            
            # Execute queries
            custom_rules_df = self.session.sql(custom_rules_query).to_pandas()
            global_rules_df = self.session.sql(global_rules_query).to_pandas()
            
            # Combine the dataframes
            if not custom_rules_df.empty and not global_rules_df.empty:
                combined_df = pd.concat([custom_rules_df, global_rules_df], ignore_index=True)
            elif not custom_rules_df.empty:
                combined_df = custom_rules_df
            elif not global_rules_df.empty:
                combined_df = global_rules_df
            else:
                combined_df = pd.DataFrame()
            
            return combined_df
        except Exception as e:
            st.error(f"Error fetching rules data: {str(e)}")
            return pd.DataFrame()
    
    def _build_custom_rules_query_paginated(self, table_name: str, customer: str, filters: dict, page: int, page_size: int) -> str:
        """Build custom rules query with pagination"""
        custom_base_where = f"CUSTOMER_NAME = '{customer}'"
        custom_where = self._build_where_clause(custom_base_where, filters)
        
        # For "All" rule type with charge name filter, add charge name filtering to custom rules
        if filters.get('rule_type') == 'All' and filters.get('charge_name') and filters['charge_name'] != 'All Charge Names':
            charge_name = filters['charge_name'].replace("'", "''")  # Escape single quotes for SQL
            custom_where += f" AND CHARGE_MAPPING_RULE = '{charge_name}'"
        
        # Calculate offset for pagination
        offset = (page - 1) * page_size
        
        return f"""
        SELECT 
            CHIPS_BUSINESS_RULE_ID as RULE_ID,
            CUSTOMER_NAME,
            PRIORITY_ORDER,
            CHARGE_MAPPING_RULE as CHARGE_NAME,
            CHARGE_ID,
            SERVICE_TYPE,
            ACCOUNT_NUMBER,
            PROVIDER_ALIAS as PROVIDER_NAME,
            CREATED_AT as CREATED_DATE,
            UPDATED_AT as MODIFIED_DATE,
            CREATED_BY,
            LAST_MODIFIED_BY as MODIFIED_BY,
            MEASUREMENT_TYPE as CHARGE_MEASUREMENT,
            'Custom' as RULE_TYPE
        FROM {table_name}
        WHERE {custom_where}
        ORDER BY PRIORITY_ORDER
        LIMIT {page_size} OFFSET {offset}
        """
    
    def get_custom_rules(self, customer: str, filters: Dict[str, str] = None, page: int = 1, page_size: int = 50) -> pd.DataFrame:
        """Get custom rules data with pagination"""
        try:
            environment = self.get_environment()
            filters = filters or {}
            
            # Get table configuration
            table_config = self._get_table_config()
            custom_table = f"{table_config['database']}.{table_config['schema']}.{table_config['custom_rules_table']}"
            
            # Build custom rules query with pagination
            custom_rules_query = self._build_custom_rules_query_paginated(custom_table, customer, filters, page, page_size)
            
            # Execute query
            custom_rules_df = self.session.sql(custom_rules_query).to_pandas()
            
            return custom_rules_df
        except Exception as e:
            st.error(f"Error fetching custom rules data: {str(e)}")
            return pd.DataFrame()
    
    def _build_global_rules_query_paginated(self, table_name: str, filters: dict, page: int, page_size: int) -> str:
        """Build global rules query with pagination"""
        global_base_where = "IS_ENABLED = TRUE"
        global_where = self._build_where_clause(global_base_where, filters)
        
        # For "All" rule type with charge name filter, add charge name filtering to global rules
        if filters.get('rule_type') == 'All' and filters.get('charge_name') and filters['charge_name'] != 'All Charge Names':
            charge_name = filters['charge_name'].replace("'", "''")  # Escape single quotes for SQL
            global_where += f" AND CHARGE_REGEX_RULE = '{charge_name}'"
        
        # Calculate offset for pagination
        offset = (page - 1) * page_size
        
        return f"""
        SELECT 
            CHIPS_EXTRACTION_CHARGE_RULE_ID as RULE_ID,
            'Global' as CUSTOMER_NAME,
            POSITION as PRIORITY_ORDER,
            CHARGE_REGEX_RULE as CHARGE_NAME,
            CHARGE_ID,
            NULL as SERVICE_TYPE,
            ACCOUNT_NUMBER,
            PROVIDER_ALIAS as PROVIDER_NAME,
            CREATED_AT as CREATED_DATE,
            LAST_MODIFIED_AT as MODIFIED_DATE,
            CREATED_BY,
            LAST_MODIFIED_BY as MODIFIED_BY,
            MEASUREMENT_TYPE as CHARGE_MEASUREMENT,
            'Global' as RULE_TYPE
        FROM {table_name}
        WHERE {global_where}
        ORDER BY POSITION
        LIMIT {page_size} OFFSET {offset}
        """
    
    def get_global_rules(self, filters: Dict[str, str] = None, page: int = 1, page_size: int = 50) -> pd.DataFrame:
        """Get global rules data with pagination"""
        try:
            environment = self.get_environment()
            filters = filters or {}
            
            # Get table configuration
            table_config = self._get_table_config()
            global_table = f"{table_config['database']}.{table_config['schema']}.{table_config['global_rules_table']}"
            
            # Build global rules query with pagination
            global_rules_query = self._build_global_rules_query_paginated(global_table, filters, page, page_size)
            
            # Execute query
            global_rules_df = self.session.sql(global_rules_query).to_pandas()
            
            return global_rules_df
        except Exception as e:
            st.error(f"Error fetching global rules data: {str(e)}")
            return pd.DataFrame()
    
    def get_custom_rules_count(self, customer: str, filters: Dict[str, str] = None) -> int:
        """Get total count of custom rules"""
        try:
            environment = self.get_environment()
            filters = filters or {}
            
            # Get table configuration
            table_config = self._get_table_config()
            custom_table = f"{table_config['database']}.{table_config['schema']}.{table_config['custom_rules_table']}"
            
            # Build count query for custom rules
            custom_base_where = f"CUSTOMER_NAME = '{customer}'"
            custom_where = self._build_where_clause(custom_base_where, filters)
            
            # For "All" rule type with charge name filter, add charge name filtering to custom rules
            if filters.get('rule_type') == 'All' and filters.get('charge_name') and filters['charge_name'] != 'All Charge Names':
                charge_name = filters['charge_name'].replace("'", "''")  # Escape single quotes for SQL
                custom_where += f" AND CHARGE_MAPPING_RULE = '{charge_name}'"
            
            count_query = f"""
            SELECT COUNT(*) as TOTAL_COUNT
            FROM {custom_table}
            WHERE {custom_where}
            """
            
            result = self.session.sql(count_query).to_pandas()
            return int(result.iloc[0]['TOTAL_COUNT'])
        except Exception as e:
            st.error(f"Error fetching custom rules count: {str(e)}")
            return 0
    
    def get_global_rules_count(self, filters: Dict[str, str] = None) -> int:
        """Get total count of global rules"""
        try:
            environment = self.get_environment()
            filters = filters or {}
            
            # Get table configuration
            table_config = self._get_table_config()
            global_table = f"{table_config['database']}.{table_config['schema']}.{table_config['global_rules_table']}"
            
            # Build count query for global rules
            global_base_where = "IS_ENABLED = TRUE"
            global_where = self._build_where_clause(global_base_where, filters)
            
            # For "All" rule type with charge name filter, add charge name filtering to global rules
            if filters.get('rule_type') == 'All' and filters.get('charge_name') and filters['charge_name'] != 'All Charge Names':
                charge_name = filters['charge_name'].replace("'", "''")  # Escape single quotes for SQL
                global_where += f" AND CHARGE_REGEX_RULE = '{charge_name}'"
            
            count_query = f"""
            SELECT COUNT(*) as TOTAL_COUNT
            FROM {global_table}
            WHERE {global_where}
            """
            
            result = self.session.sql(count_query).to_pandas()
            return int(result.iloc[0]['TOTAL_COUNT'])
        except Exception as e:
            st.error(f"Error fetching global rules count: {str(e)}")
            return 0
    
    def get_filter_options(self, customer: str) -> Dict[str, list]:
        """Get unique filter options from the rules data"""
        try:
            environment = self.get_environment()
            
            # Get table configuration
            table_config = self._get_table_config()
            custom_table = f"{table_config['database']}.{table_config['schema']}.{table_config['custom_rules_table']}"
            global_table = f"{table_config['database']}.{table_config['schema']}.{table_config['global_rules_table']}"
            
            # Build query using table names
            filter_query = f"""
            SELECT DISTINCT 
                CHARGE_ID,
                PROVIDER_ALIAS,
                CHARGE_MAPPING_RULE,
                CHARGE_REGEX_RULE
            FROM (
                SELECT CHARGE_ID, PROVIDER_ALIAS, CHARGE_MAPPING_RULE, NULL as CHARGE_REGEX_RULE
                FROM {custom_table}
                WHERE CUSTOMER_NAME = '{customer}'
                UNION ALL
                SELECT CHARGE_ID, PROVIDER_ALIAS, NULL as CHARGE_MAPPING_RULE, CHARGE_REGEX_RULE
                FROM {global_table}
                WHERE IS_ENABLED = TRUE
            )
            ORDER BY CHARGE_ID, PROVIDER_ALIAS
            """
            
            filter_df = self.session.sql(filter_query).to_pandas()
            
            # Extract unique values with meaningful "no filtering" defaults
            charge_ids = ['All Charge IDs'] + sorted([str(x) for x in filter_df['CHARGE_ID'].dropna().unique() if str(x) != 'nan'])
            providers = ['All Providers'] + sorted([str(x) for x in filter_df['PROVIDER_ALIAS'].dropna().unique() if str(x) != 'nan'])
            
            # Combine charge names from both custom and global rules
            custom_charge_names = [str(x) for x in filter_df['CHARGE_MAPPING_RULE'].dropna().unique() if str(x) != 'nan']
            global_charge_names = [str(x) for x in filter_df['CHARGE_REGEX_RULE'].dropna().unique() if str(x) != 'nan']
            all_charge_names = list(set(custom_charge_names + global_charge_names))
            charge_names = ['All Charge Names'] + sorted(all_charge_names)
            
            return {
                'charge_ids': charge_ids,
                'providers': providers,
                'charge_names': charge_names
            }
            
        except Exception as e:
            st.error(f"Error fetching filter options: {str(e)}")
            return {
                'charge_ids': ['All Charge IDs', 'NewBatch', 'Other'],
                'providers': ['All Providers', 'Atmos', 'Other'],
                'charge_names': ['All Charge Names', 'CHP Rider', 'Other']
            }
    
    def create_rule(self, rule_data: Dict[str, Any]) -> bool:
        """Create a new rule in Snowflake"""
        try:
            environment = self.get_environment()
            
            # Get table configuration
            table_config = self._get_table_config()
            database = table_config['database']
            schema = table_config['schema']
            rules_table = table_config['custom_rules_table']
            
            # Get next rule ID and priority
            customer_name = rule_data.get('customer', '')
            max_rule_id_query = f"""
            SELECT COALESCE(MAX(CHIPS_BUSINESS_RULE_ID), 0) + 1 as NEXT_RULE_ID
            FROM {database}.{schema}.{rules_table}
            WHERE CUSTOMER_NAME = '{customer_name}'
            """
            
            max_priority_query = f"""
            SELECT COALESCE(MAX(PRIORITY_ORDER), 0) + 1 as NEXT_PRIORITY
            FROM {database}.{schema}.{rules_table}
            WHERE CUSTOMER_NAME = '{customer_name}'
            """
            
            next_rule_id = self.session.sql(max_rule_id_query).collect()[0][0]
            next_priority = self.session.sql(max_priority_query).collect()[0][0]
            
            # Determine request type
            request_type_value = 1 if rule_data.get('request_type') == 'NewBatch' else 0
            
            # Insert new rule
            insert_query = f"""
            INSERT INTO {database}.{schema}.{rules_table} (
                CHIPS_BUSINESS_RULE_ID,
                CUSTOMER_NAME,
                PRIORITY_ORDER,
                CHARGE_NAME_MAPPING,
                CHARGE_ID,
                CHARGE_GROUP_HEADING,
                CHARGE_CATEGORY,
                REQUEST_TYPE
            ) VALUES (
                {next_rule_id},
                '{rule_data.get('customer', '')}',
                {next_priority},
                '{rule_data.get('charge_name_mapping', '')}',
                'NewBatch',
                '{rule_data.get('charge_group_heading', '')}',
                '{rule_data.get('charge_category', '')}',
                {request_type_value}
            )
            """
            
            self.session.sql(insert_query).collect()
            st.success(f"🎉 Rule created successfully in {environment} environment!")
            return True
            
        except Exception as e:
            st.error(f"Error creating rule: {str(e)}")
            return False
    
    def update_rule(self, rule_id: str, rule_data: Dict[str, Any]) -> bool:
        """Update an existing rule in Snowflake"""
        try:
            environment = self.get_environment()
            
            # Get table configuration
            table_config = self._get_table_config()
            database = table_config['database']
            schema = table_config['schema']
            rules_table = table_config['custom_rules_table']
            
            # Determine request type
            request_type_value = 1 if rule_data.get('request_type') == 'NewBatch' else 0
            
            # Update rule
            customer_name = rule_data.get('customer', '')
            update_query = f"""
            UPDATE {database}.{schema}.{rules_table}
            SET 
                CHARGE_NAME_MAPPING = '{rule_data.get('charge_name_mapping', '')}',
                CHARGE_GROUP_HEADING = '{rule_data.get('charge_group_heading', '')}',
                CHARGE_CATEGORY = '{rule_data.get('charge_category', '')}',
                REQUEST_TYPE = {request_type_value}
            WHERE CHIPS_BUSINESS_RULE_ID = {rule_id}
            AND CUSTOMER_NAME = '{customer_name}'
            """
            
            self.session.sql(update_query).collect()
            st.success(f"🎉 Rule {rule_id} updated successfully in {environment} environment!")
            return True
                
        except Exception as e:
            st.error(f"Error updating rule: {str(e)}")
            return False
    
    def update_priority(self, rule_id: str, new_priority: int) -> bool:
        """Update rule priority in Snowflake"""
        try:
            environment = self.get_environment()
            
            if environment == "PRODUCTION":
                # Use production tables
                database = "arcadia"
                schema = "lakehouse"
                rules_table = "f_combined_customer_charge_rules"
            else:
                # Use SANDBOX tables
                database = "SANDBOX"
                schema = "BMANOJKUMAR"
                rules_table = "f_combined_customer_charge_rules"
            
            # Update priority
            update_query = f"""
            UPDATE {database}.{schema}.{rules_table}
            SET PRIORITY_ORDER = {new_priority}
            WHERE CHIPS_BUSINESS_RULE_ID = {rule_id}
            """
            
            self.session.sql(update_query).collect()
            st.success(f"🎉 Priority for rule {rule_id} updated to {new_priority} in {environment} environment!")
            return True
            
        except Exception as e:
            st.error(f"Error updating priority: {str(e)}")
            return False


def get_data_provider() -> DataProvider:
    """Factory function to get the appropriate data provider based on configuration"""
    try:
        # Always use Snowflake data provider for all environments
        session = get_snowflake_session()
        database = os.getenv("SNOWFLAKE_DATABASE", "SANDBOX")
        schema = os.getenv("SNOWFLAKE_SCHEMA", "BMANOJKUMAR")
        return SnowflakeDataProvider(session, database, schema)
    except Exception as e:
        st.error(f"Failed to initialize data provider: {str(e)}")
        # Return a minimal provider that shows error
        return SnowflakeDataProvider(None, "SANDBOX", "BMANOJKUMAR")
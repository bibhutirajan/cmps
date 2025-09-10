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
    def get_charges(self, customer: str, charge_type: str = None) -> pd.DataFrame:
        """Get charges data"""
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
    
    def get_charges(self, customer: str, charge_type: str = None) -> pd.DataFrame:
        """Get charges data from Snowflake based on environment and charge type"""
        try:
            environment = self.get_environment()
            org_id = self.get_organization_id(customer)
            
            # Build WHERE clause based on charge type
            if charge_type and "Uncategorized" in charge_type:
                where_clause = f"ODIN_ORGANIZATION_ID = '{org_id}' AND (CHARGE_ID IS NULL OR CHARGE_ID = 'ch.uncategorized_charge')"
            else:
                # Default: show all charges for the organization
                where_clause = f"ODIN_ORGANIZATION_ID = '{org_id}'"
            
            if environment == "PRODUCTION":
                # Use production tables
                query = f"""
                SELECT *
                FROM arcadia.export.hex_uc_charge_mapping_delivery
                WHERE {where_clause}
                ORDER BY STATEMENT_DATE DESC, ODIN_STATEMENT_ID
                LIMIT 1000
                """
            else:
                # Use SANDBOX tables (for both LOCAL and SANDBOX environments)
                query = f"""
                SELECT *
                FROM SANDBOX.BMANOJKUMAR.hex_uc_charge_mapping_delivery
                WHERE {where_clause}
                ORDER BY STATEMENT_DATE DESC, ODIN_STATEMENT_ID
                LIMIT 1000
                """
            
            return self.session.sql(query).to_pandas()
        except Exception as e:
            st.error(f"Error fetching charges data: {str(e)}")
            return pd.DataFrame()
    
    def get_rules(self, customer: str) -> pd.DataFrame:
        """Get rules data from Snowflake based on environment"""
        try:
            environment = self.get_environment()            
            if environment == "PRODUCTION":
                # Use production tables
                # Get custom rules (customer-specific)
                custom_rules_query = f"""
                SELECT *, 'Custom' as RULE_TYPE
                FROM arcadia.lakehouse.f_combined_customer_charge_rules
                WHERE CUSTOMER_NAME = '{customer}'
                ORDER BY PRIORITY_ORDER
                LIMIT 100
                """
                
                # Get global rules (provider template rules)
                global_rules_query = """
                SELECT *, 'Global' as RULE_TYPE
                FROM arcadia.lakehouse.f_combined_provider_template_charge_rules
                WHERE IS_ENABLED = TRUE
                ORDER BY POSITION
                LIMIT 100
                """
            else:
                # Use SANDBOX tables (for both LOCAL and SANDBOX environments)
                # Get custom rules (customer-specific with organization filtering)
                custom_rules_query = f"""
                SELECT *, 'Custom' as RULE_TYPE
                FROM SANDBOX.BMANOJKUMAR.f_combined_customer_charge_rules
                WHERE CUSTOMER_NAME = '{customer}'
                ORDER BY PRIORITY_ORDER
                LIMIT 100
                """
                
                # Get global rules (provider template rules)
                global_rules_query = """
                SELECT *, 'Global' as RULE_TYPE
                FROM SANDBOX.BMANOJKUMAR.f_combined_provider_template_charge_rules
                WHERE IS_ENABLED = TRUE
                ORDER BY POSITION
                LIMIT 100
                """
            
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
    
    def create_rule(self, rule_data: Dict[str, Any]) -> bool:
        """Create a new rule in Snowflake"""
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
            
            # Get next rule ID and priority
            max_rule_id_query = f"""
            SELECT COALESCE(MAX(CHIPS_BUSINESS_RULE_ID), 0) + 1 as NEXT_RULE_ID
            FROM {database}.{schema}.{rules_table}
            WHERE CUSTOMER_NAME = '{customer}'
            """
            
            max_priority_query = f"""
            SELECT COALESCE(MAX(PRIORITY_ORDER), 0) + 1 as NEXT_PRIORITY
            FROM {database}.{schema}.{rules_table}
            WHERE CUSTOMER_NAME = '{customer}'
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
            
            # Determine request type
            request_type_value = 1 if rule_data.get('request_type') == 'NewBatch' else 0
            
            # Update rule
            update_query = f"""
            UPDATE {database}.{schema}.{rules_table}
            SET 
                CHARGE_NAME_MAPPING = '{rule_data.get('charge_name_mapping', '')}',
                CHARGE_GROUP_HEADING = '{rule_data.get('charge_group_heading', '')}',
                CHARGE_CATEGORY = '{rule_data.get('charge_category', '')}',
                REQUEST_TYPE = {request_type_value}
            WHERE CHIPS_BUSINESS_RULE_ID = {rule_id}
            AND CUSTOMER_NAME = '{customer}'
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
        return SnowflakeDataProvider(session)
    except Exception as e:
        st.error(f"Failed to initialize data provider: {str(e)}")
        # Return a minimal provider that shows error
        return SnowflakeDataProvider(None)
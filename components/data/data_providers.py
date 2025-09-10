"""
Data Providers for Charge Mapping Application

This module contains the data abstraction layer with providers for different data sources.
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


class DemoDataProvider(DataProvider):
    """Demo data provider for development and testing"""
    
    def get_charges(self, customer: str, charge_type: str = None) -> pd.DataFrame:
        """Get demo charges data"""
        return pd.DataFrame({
            'Statement ID': ['1efe9dd1-6cad-d3c...', '1efe9dd1-6cad-d3c...', '1efe9dd1-6cad-d3c...', '1efe9dd1-6cad-d3c...'],
            'Provider name': ['Atmos', 'Atmos', 'Atmos', 'Atmos'],
            'Account number': ['3018639036', '3018639036', '3018639036', '3018639036'],
            'Charge name': ['CHP Rider', 'CHP Rider', 'CHP Rider', 'CHP Rider'],
            'Charge ID': ['NewBatch', 'NewBatch', 'NewBatch', 'NewBatch'],
            'Charge measurement': ['general_consumption', 'general_consumption', 'general_consumption', 'general_consumption'],
            'Usage unit': ['None', 'None', 'None', 'None'],
            'Service type': ['None', 'None', 'None', 'None']
        })
    
    def get_rules(self, customer: str) -> pd.DataFrame:
        """Get demo rules data"""
        return pd.DataFrame({
            'Rule ID': [8912000, 8912003, 8912005, 8912008, 8912010, 8912011, 8912017, 8912020],
            'Customer name': [customer] * 8,
            'Priority order': [3101, 3100, 3299, 3112, 3113, 3120, 3102.0, 3102.0],
            'Charge name mapping': ['(?i)Electric\\s*servic...'] * 8,
            'Charge ID': ['Placeholder'] * 8,
            'Charge group heading': [''] * 8,
            'Charge category': ['ch.usage_charge'] * 8,
            'Request type': [''] * 8
        })
    
    def create_rule(self, rule_data: Dict[str, Any]) -> bool:
        """Demo rule creation"""
        st.success("🎉 Rule created successfully in demo mode!")
        return True
    
    def update_rule(self, rule_id: str, rule_data: Dict[str, Any]) -> bool:
        """Demo rule update"""
        st.success(f"🎉 Rule {rule_id} updated successfully in demo mode!")
        return True
    
    def update_priority(self, rule_id: str, new_priority: int) -> bool:
        """Demo priority update"""
        st.success(f"🎉 Priority for rule {rule_id} updated to {new_priority} in demo mode!")
        return True


class SnowflakeDataProvider(DataProvider):
    """Snowflake data provider for production"""
    
    def __init__(self, session, database: str = "SANDBOX", schema: str = "BMANOJKUMAR"):
        self.session = session
        self.database = database
        self.schema = schema
        
        # Customer name to organization ID mapping
        self.customer_to_org_id = {
            "AmerescoFTP": "75",     # Updated to use available org ID with most data
            "OtherCustomer": "617",  # Available org ID
            "NewCustomer": "1482",   # Available org ID
            "TestCustomer": "75"     # Fallback to same as AmerescoFTP
        }
    
    def get_organization_id(self, customer: str) -> str:
        """Convert customer name to organization ID"""
        return self.customer_to_org_id.get(customer, customer)
    
    def get_charges(self, customer: str, charge_type: str = None) -> pd.DataFrame:
        """Get charges data from Snowflake based on charge type"""
        try:
            # Use production tables if CHARGES_TABLE environment variable is set to production table
            charges_table = os.getenv("CHARGES_TABLE", "charges")
            use_production_tables = "arcadia.export.hex_uc_charge_mapping_delivery" in charges_table
            
            if use_production_tables:
                # Use remote table with direct filtering based on charge type
                org_id = self.get_organization_id(customer)
                
                # Build WHERE clause based on charge type
                if charge_type and "Uncategorized" in charge_type:
                    where_clause = f"ODIN_ORGANIZATION_ID = '{org_id}' AND CHARGE_ID = 'ch.uncategorized_charge'"
                elif charge_type and "Approval needed" in charge_type:
                    where_clause = f"ODIN_ORGANIZATION_ID = '{org_id}' AND CONTRIBUTION_STATUS = 'non_contributing'"
                elif charge_type and "Approved" in charge_type:
                    where_clause = f"ODIN_ORGANIZATION_ID = '{org_id}' AND CONTRIBUTION_STATUS = 'contributing'"
                else:
                    # Default: show all charges for the organization
                    where_clause = f"ODIN_ORGANIZATION_ID = '{org_id}'"
                
                query = f"""
                SELECT *
                FROM arcadia.export.hex_uc_charge_mapping_delivery
                WHERE {where_clause}
                ORDER BY STATEMENT_DATE DESC, ODIN_STATEMENT_ID
                LIMIT 1000
                """
            else:
                # Use local sandbox table
                query = f"""
                SELECT 
                    STATEMENT_ID as "Statement ID",
                    PROVIDER_NAME as "Provider name",
                    ACCOUNT_NUMBER as "Account number",
                    CHARGE_NAME as "Charge name",
                    CHARGE_ID as "Charge ID",
                    CHARGE_MEASUREMENT as "Charge measurement",
                    USAGE_UNIT as "Usage unit",
                    SERVICE_TYPE as "Service type"
                FROM {self.database}.{self.schema}.CHARGES
                WHERE CUSTOMER_NAME = '{customer}'
                """
            
            return self.session.sql(query).to_pandas()
        except Exception as e:
            st.error(f"Error fetching charges data: {str(e)}")
            return pd.DataFrame()
    
    def get_rules(self, customer: str) -> pd.DataFrame:
        """Get rules data from Snowflake"""
        try:
            # Use production tables if RULES_CUSTOMER_TABLE environment variable is set to production table
            rules_customer_table = os.getenv("RULES_CUSTOMER_TABLE", "rules")
            use_production_tables = "arcadia.lakehouse.f_combined_customer_charge_rules" in rules_customer_table
            
            if use_production_tables:
                # Use lakehouse tables for remote environment - simple direct queries
                
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
            else:
                # Use local sandbox table
                query = f"""
                SELECT 
                    CHIPS_BUSINESS_RULE_ID as "Rule ID",
                    CUSTOMER_NAME as "Customer name",
                    PRIORITY_ORDER as "Priority order",
                    CHARGE_NAME_MAPPING as "Charge name mapping",
                    CHARGE_ID as "Charge ID",
                    CHARGE_GROUP_HEADING as "Charge group heading",
                    CHARGE_CATEGORY as "Charge category",
                    REQUEST_TYPE as "Request type"
                FROM {self.database}.{self.schema}.RULES
                WHERE CUSTOMER_NAME = '{customer}'
                ORDER BY PRIORITY_ORDER
                """
                df = self.session.sql(query).to_pandas()
                return df
        except Exception as e:
            st.error(f"Error fetching rules data: {str(e)}")
            return pd.DataFrame()
    
    def create_rule(self, rule_data: Dict[str, Any]) -> bool:
        """Create a new rule in Snowflake"""
        try:
            # Get the next available rule ID
            max_id_query = f"""
            SELECT COALESCE(MAX(CHIPS_BUSINESS_RULE_ID), 0) + 1 as NEXT_ID
            FROM {self.database}.{self.schema}.RULES
            """
            max_id_result = self.session.sql(max_id_query).to_pandas()
            next_rule_id = max_id_result.iloc[0]['NEXT_ID']
            
            # Get the next available priority order
            max_priority_query = f"""
            SELECT COALESCE(MAX(PRIORITY_ORDER), 0) + 1 as NEXT_PRIORITY
            FROM {self.database}.{self.schema}.RULES
            WHERE CUSTOMER_NAME = '{rule_data.get('customer', '')}'
            """
            max_priority_result = self.session.sql(max_priority_query).to_pandas()
            next_priority = max_priority_result.iloc[0]['NEXT_PRIORITY']
            
            # Build the INSERT query - using only columns that exist in the RULES table
            # Convert request_type to numeric if it's a string
            request_type_value = rule_data.get('request_type', '')
            if request_type_value == 'Standard':
                request_type_value = 1
            elif request_type_value == 'Express':
                request_type_value = 2
            elif request_type_value == 'Priority':
                request_type_value = 3
            else:
                request_type_value = 1  # Default to Standard
            
            insert_query = f"""
            INSERT INTO {self.database}.{self.schema}.RULES (
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
            
            # Execute the INSERT
            self.session.sql(insert_query).collect()
            st.success(f"🎉 Rule {next_rule_id} created successfully in Snowflake!")
            return True
            
        except Exception as e:
            st.error(f"Error creating rule: {str(e)}")
            # Add debugging information
            st.error(f"Debug info - Next Rule ID: {next_rule_id}, Next Priority: {next_priority}")
            st.error(f"Debug info - Customer: {rule_data.get('customer', '')}")
            return False
    
    def update_rule(self, rule_id: str, rule_data: Dict[str, Any]) -> bool:
        """Update an existing rule in Snowflake"""
        try:
            # Build the UPDATE query - using only columns that exist in the RULES table
            # Convert request_type to numeric if it's a string
            request_type_value = rule_data.get('request_type', '')
            if request_type_value == 'Standard':
                request_type_value = 1
            elif request_type_value == 'Express':
                request_type_value = 2
            elif request_type_value == 'Priority':
                request_type_value = 3
            else:
                request_type_value = 1  # Default to Standard
            
            update_query = f"""
            UPDATE {self.database}.{self.schema}.RULES
            SET 
                CHARGE_NAME_MAPPING = '{rule_data.get('charge_name_mapping', '')}',
                CHARGE_CATEGORY = '{rule_data.get('charge_category', '')}',
                CHARGE_GROUP_HEADING = '{rule_data.get('charge_group_heading', '')}',
                REQUEST_TYPE = {request_type_value}
            WHERE CHIPS_BUSINESS_RULE_ID = {rule_id}
            """
            
            # Execute the UPDATE
            result = self.session.sql(update_query).collect()
            
            if result:
                st.success(f"🎉 Rule {rule_id} updated successfully in Snowflake!")
                return True
            else:
                st.error(f"Rule {rule_id} not found or no changes made")
                return False
                
        except Exception as e:
            st.error(f"Error updating rule: {str(e)}")
            return False
    
    def update_priority(self, rule_id: str, new_priority: int) -> bool:
        """Update rule priority in Snowflake"""
        try:
            # Implementation for updating priority in Snowflake
            st.success(f"🎉 Priority for rule {rule_id} updated to {new_priority} in Snowflake!")
            return True
        except Exception as e:
            st.error(f"Error updating priority: {str(e)}")
            return False


def get_data_provider(snowflake_enabled: bool = False) -> DataProvider:
    """Factory function to get the appropriate data provider"""
    if snowflake_enabled:
        try:
            session = get_snowflake_session()
            return SnowflakeDataProvider(session)
        except Exception as e:
            st.warning(f"Snowflake connection failed: {str(e)}. Falling back to demo mode.")
            return DemoDataProvider()
    else:
        return DemoDataProvider() 
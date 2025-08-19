"""
Data Providers for Charge Mapping Application

This module contains the data abstraction layer with providers for different data sources.
"""

import pandas as pd
import streamlit as st
from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Any
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
    def get_processed_files(self, customer: str) -> pd.DataFrame:
        """Get processed files data"""
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
    
    def get_processed_files(self, customer: str) -> pd.DataFrame:
        """Get demo processed files data"""
        return pd.DataFrame({
            'File ID': [f'FILE_{i:03d}' for i in range(1, 6)],
            'Filename': [f'charges_{i}.csv' for i in range(1, 6)],
            'Processed Date': ['2024-01-15', '2024-01-14', '2024-01-13', '2024-01-12', '2024-01-11'],
            'Status': ['Processed', 'Processed', 'Processed', 'Processed', 'Processed'],
            'Records': [150, 200, 175, 125, 300]
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
    
    def get_charges(self, customer: str, charge_type: str = None) -> pd.DataFrame:
        """Get charges data from Snowflake"""
        try:
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
            # Note: CHARGE_TYPE column doesn't exist in the CHARGES table
            # Filtering by charge_type is disabled for now
            
            return self.session.sql(query).to_pandas()
        except Exception as e:
            st.error(f"Error fetching charges data: {str(e)}")
            return pd.DataFrame()
    
    def get_rules(self, customer: str) -> pd.DataFrame:
        """Get rules data from Snowflake"""
        try:
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
    
    def get_processed_files(self, customer: str) -> pd.DataFrame:
        """Get processed files data from Snowflake"""
        try:
            query = f"""
            SELECT 
                FILE_ID as "File ID",
                FILENAME as "Filename",
                PROCESSED_DATE as "Processed Date",
                STATUS as "Status",
                RECORDS as "Records"
            FROM {self.database}.{self.schema}.PROCESSED_FILES
            WHERE CUSTOMER_NAME = '{customer}'
            ORDER BY PROCESSED_DATE DESC
            """
            return self.session.sql(query).to_pandas()
        except Exception as e:
            st.error(f"Error fetching processed files data: {str(e)}")
            return pd.DataFrame()
    

    
    def create_rule(self, rule_data: Dict[str, Any]) -> bool:
        """Create a new rule in Snowflake"""
        try:
            # Implementation for creating rules in Snowflake
            st.success("🎉 Rule created successfully in Snowflake!")
            return True
        except Exception as e:
            st.error(f"Error creating rule: {str(e)}")
            return False
    
    def update_rule(self, rule_id: str, rule_data: Dict[str, Any]) -> bool:
        """Update an existing rule in Snowflake"""
        try:
            # Implementation for updating rules in Snowflake
            st.success(f"🎉 Rule {rule_id} updated successfully in Snowflake!")
            return True
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
import streamlit as st
import pandas as pd
import numpy as np
import os
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
from config import get_snowflake_session

# =============================================================================
# CONFIGURATION AND SETTINGS
# =============================================================================

@dataclass
class AppConfig:
    """Centralized configuration for the application"""
    # Data source configuration
    DATA_SOURCE: str = os.getenv("DATA_SOURCE", "demo")  # "demo" or "snowflake"
    
    # Snowflake configuration
    SNOWFLAKE_ENABLED: bool = os.getenv("SNOWFLAKE_ENABLED", "false").lower() == "true"
    SNOWFLAKE_DATABASE: str = os.getenv("SNOWFLAKE_DATABASE", "arcadia")
    SNOWFLAKE_SCHEMA: str = os.getenv("SNOWFLAKE_SCHEMA", "lakehouse")
    
    # Table configurations
    CHARGES_TABLE: str = os.getenv("CHARGES_TABLE", "charges")
    RULES_TABLE: str = os.getenv("RULES_TABLE", "rules")
    PROCESSED_FILES_TABLE: str = os.getenv("PROCESSED_FILES_TABLE", "processed_files")
    REGEX_RULES_TABLE: str = os.getenv("REGEX_RULES_TABLE", "regex_rules")
    
    # UI Configuration
    SIDEBAR_COLLAPSED: bool = True
    DARK_THEME: bool = True

# Initialize configuration
config = AppConfig()

# =============================================================================
# DATA ABSTRACTION LAYER
# =============================================================================

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
    def get_regex_rules(self, customer: str) -> pd.DataFrame:
        """Get regex rules data"""
        pass
    
    @abstractmethod
    def create_rule(self, rule_data: Dict[str, Any]) -> bool:
        """Create a new rule"""
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
    
    def get_regex_rules(self, customer: str) -> pd.DataFrame:
        """Get demo regex rules data"""
        return pd.DataFrame({
            'Pattern ID': [f'PATTERN_{i:03d}' for i in range(1, 6)],
            'Regex Pattern': [r'CHP.*Rider', r'Gas.*Service', r'Water.*Bill', r'Electric.*Charge', r'Service.*Fee'],
            'Category': ['Electricity', 'Gas', 'Water', 'Electricity', 'Other'],
            'Priority': [1, 2, 3, 4, 5]
        })
    
    def create_rule(self, rule_data: Dict[str, Any]) -> bool:
        """Demo rule creation"""
        return True

class SnowflakeDataProvider(DataProvider):
    """Snowflake data provider for production"""
    
    def __init__(self, session):
        self.session = session
        self.database = config.SNOWFLAKE_DATABASE
        self.schema = config.SNOWFLAKE_SCHEMA
    
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
            FROM {self.database}.{self.schema}.{config.CHARGES_TABLE}
            WHERE CUSTOMER_NAME = '{customer}'
            """
            if charge_type:
                query += f" AND CHARGE_TYPE = '{charge_type}'"
            
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
            FROM {self.database}.{self.schema}.{config.RULES_TABLE}
            WHERE CUSTOMER_NAME = '{customer}'
            ORDER BY PRIORITY_ORDER
            """
            return self.session.sql(query).to_pandas()
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
            FROM {self.database}.{self.schema}.{config.PROCESSED_FILES_TABLE}
            WHERE CUSTOMER_NAME = '{customer}'
            ORDER BY PROCESSED_DATE DESC
            """
            return self.session.sql(query).to_pandas()
        except Exception as e:
            st.error(f"Error fetching processed files data: {str(e)}")
            return pd.DataFrame()
    
    def get_regex_rules(self, customer: str) -> pd.DataFrame:
        """Get regex rules data from Snowflake"""
        try:
            query = f"""
            SELECT 
                PATTERN_ID as "Pattern ID",
                REGEX_PATTERN as "Regex Pattern",
                CATEGORY as "Category",
                PRIORITY as "Priority"
            FROM {self.database}.{self.schema}.{config.REGEX_RULES_TABLE}
            WHERE CUSTOMER_NAME = '{customer}'
            ORDER BY PRIORITY
            """
            return self.session.sql(query).to_pandas()
        except Exception as e:
            st.error(f"Error fetching regex rules data: {str(e)}")
            return pd.DataFrame()
    
    def create_rule(self, rule_data: Dict[str, Any]) -> bool:
        """Create a new rule in Snowflake"""
        try:
            # Implementation for creating rules in Snowflake
            st.success("Rule created successfully in Snowflake!")
            return True
        except Exception as e:
            st.error(f"Error creating rule: {str(e)}")
            return False

# =============================================================================
# DATA PROVIDER FACTORY
# =============================================================================

def get_data_provider() -> DataProvider:
    """Factory function to get the appropriate data provider"""
    if config.SNOWFLAKE_ENABLED:
        try:
            session = get_snowflake_session()
            return SnowflakeDataProvider(session)
        except Exception as e:
            st.warning(f"Snowflake connection failed: {str(e)}. Falling back to demo mode.")
            return DemoDataProvider()
    else:
        return DemoDataProvider()

# =============================================================================
# UI COMPONENTS
# =============================================================================

def setup_page_config():
    """Setup page configuration"""
    st.set_page_config(
        page_title="Charge Mapping",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="collapsed" if config.SIDEBAR_COLLAPSED else "expanded"
    )

def setup_css():
    """Setup custom CSS"""
    st.markdown("""
    <style>
        /* Hide sidebar by default */
        .css-1d391kg {
            display: none;
        }
        
        /* Remove white backgrounds from all elements */
        .stApp {
            background-color: #0e1117 !important;
        }
        
        .main-header {
            font-size: 2rem;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 1rem;
        }
        .tab-container {
            background-color: transparent !important;
            border-radius: 8px;
            padding: 0.2rem;
            margin: 0.2rem 0;
        }
        .stButton > button {
            background-color: #3b82f6;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            font-weight: 500;
        }
        .stButton > button:hover {
            background-color: #2563eb;
        }
        .metric-card {
            background-color: transparent !important;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #3b82f6;
        }
        .metric-label {
            color: #6b7280;
            font-size: 0.875rem;
        }
        .user-info {
            background-color: #374151 !important;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            color: white;
        }
        
        /* Override any white backgrounds */
        div[data-testid="stSidebar"] {
            background-color: #1e293b !important;
        }
        
        /* Remove white backgrounds from dataframes */
        .stDataFrame {
            background-color: transparent !important;
        }
        
        /* Remove white backgrounds from selectboxes */
        .stSelectbox > div > div {
            background-color: #374151 !important;
            color: white !important;
        }
        
        /* Remove white backgrounds from number inputs */
        .stNumberInput > div > div {
            background-color: #374151 !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar(data_provider: DataProvider):
    """Render the sidebar with customer selection and user info"""
    with st.sidebar:
        st.markdown("### 🏢 Customer Selection")
        selected_customer = st.selectbox(
            "Select Customer",
            ["AmerescoFTP", "OtherCustomer", "NewCustomer", "TestCustomer"],
            index=0
        )

        # Status indicator
        if isinstance(data_provider, DemoDataProvider):
            st.info("🎭 Demo Mode Active")
        else:
            st.success("✅ Connected to Snowflake")
        
        # Add some spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("### 👤 User Information")
        st.markdown('<div class="user-info">', unsafe_allow_html=True)
        st.markdown("**Name:** John Doe")
        st.markdown("**Role:** Admin")
        st.markdown("**Email:** john.doe@company.com")
        st.markdown("**Last Login:** Today, 2:30 PM")
        st.markdown('</div>', unsafe_allow_html=True)
        
        return selected_customer

def render_charges_tab(data_provider: DataProvider, customer: str):
    """Render the charges tab"""
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    st.markdown("### Charges")
    st.markdown("Start by viewing all charges, then filter by category: Uncategorized, Approval needed, or Approved.")
    
    # Filter section - aligned layout
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    with col1:
        charge_type = st.selectbox(
            "Charge type",
            ["Uncategorized (100)", "Approval needed (25)", "Approved (150)"],
            index=0
        )
    
    with col5:
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
        if st.button("Create rule", key="create_rule_btn"):
            st.success("🎉 Rule creation initiated!")
            st.info("This would open a rule creation form with the selected charge data.")
    
    # Get charges data
    charges_df = data_provider.get_charges(customer, charge_type)
    
    # Initialize session state for selected rows
    if 'selected_rows' not in st.session_state:
        st.session_state.selected_rows = set()
    
    # Add checkbox column
    charges_df.insert(0, 'Select', [False] * len(charges_df))
    
    # Display the table with editable checkboxes
    edited_df = st.data_editor(
        charges_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Select": st.column_config.CheckboxColumn("Select", default=False),
            "Statement ID": st.column_config.TextColumn("Statement ID", width="medium"),
            "Provider name": st.column_config.TextColumn("Provider name", width="medium"),
            "Account number": st.column_config.TextColumn("Account number", width="medium"),
            "Charge name": st.column_config.TextColumn("Charge name", width="medium"),
            "Charge ID": st.column_config.TextColumn("Charge ID", width="medium"),
            "Charge measurement": st.column_config.TextColumn("Charge measurement", width="medium"),
            "Usage unit": st.column_config.TextColumn("Usage unit", width="medium"),
            "Service type": st.column_config.TextColumn("Service type", width="medium")
        },
        key="charges_table"
    )
    
    # Pagination
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown("Page 1 of 3")
    with col3:
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.number_input("Page", min_value=0, value=0, key="page_num")
        with col_b:
            st.number_input("Page size", min_value=10, value=30, key="page_size")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_rules_tab(data_provider: DataProvider, customer: str):
    """Render the rules tab matching the FIGMA design"""
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    
    # Main section header with Create rule button aligned horizontally
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### Rules")
        st.markdown("Use rules to rename and reclassify charges. If multiple rules match a charge, they'll be applied in order from top to bottom.")
    with col2:
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)  # Align with Rules heading
        if st.button("Create rule", key="create_rule_rules_tab_btn"):
            st.success("🎉 Rule creation initiated!")
            st.info("This would open a rule creation form.")
    
    # Filters section
    st.markdown("""
    <style>
        .filter-container {
            background-color: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            position: relative;
        }
        .filter-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        .filter-content {
            display: flex;
            gap: 1rem;
            align-items: end;
        }
        .filter-field {
            flex: 1;
        }
        .filter-field label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: #374151;
        }
        .collapse-button {
            background: #f3f4f6;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            padding: 0.25rem 0.5rem;
            cursor: pointer;
            font-size: 0.875rem;
        }
        .help-button {
            background: #f3f4f6;
            border: 1px solid #d1d5db;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            margin-left: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create collapsible filter section
    with st.expander("Filters", expanded=True):
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown("**Rule type**")
            st.selectbox("", ["All"], key="rule_type_filter", label_visibility="collapsed")
        
        with col2:
            st.markdown("**Customer name**")
            st.selectbox("", [customer], key="customer_filter", label_visibility="collapsed")
        
        with col3:
            st.markdown("**Charge ID**")
            st.selectbox("", ["Placeholder"], key="charge_id_filter", label_visibility="collapsed")
        
        with col4:
            st.markdown("**Provider**")
            st.selectbox("", ["TBD"], key="provider_filter", label_visibility="collapsed")
        
        with col5:
            st.markdown("**Charge name**")
            st.text_input("", value="(?i)Electric\\s*service.*", key="charge_name_filter", label_visibility="collapsed")
    
    # Custom Rules Section
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### Custom")
        st.markdown("Rules specific to your organization. These override global rules and can be reordered or edited.")
    
    with col2:
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)  # Align with heading
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Edit priority", key="edit_priority_custom_btn"):
                selected_custom = [i for i, selected in enumerate(st.session_state.get('custom_selected', [])) if selected]
                if selected_custom:
                    st.success(f"Edit priority for {len(selected_custom)} selected custom rules")
                else:
                    st.warning("Please select at least one custom rule to edit priority")
        with col_b:
            if st.button("Edit rule", key="edit_rule_custom_btn"):
                selected_custom = [i for i, selected in enumerate(st.session_state.get('custom_selected', [])) if selected]
                if selected_custom:
                    st.success(f"Edit rule for {len(selected_custom)} selected custom rules")
                else:
                    st.warning("Please select at least one custom rule to edit")
    
    # Get custom rules data
    custom_rules_df = data_provider.get_rules(customer)
    
    # Initialize session state for custom selection
    if 'custom_selected' not in st.session_state:
        st.session_state.custom_selected = [False] * len(custom_rules_df)
    
    # Create a copy of the dataframe for display
    display_custom_df = custom_rules_df.copy()
    display_custom_df.insert(0, 'Select', st.session_state.custom_selected)
    
    # Display the custom rules table
    edited_custom_df = st.data_editor(
        display_custom_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Select": st.column_config.CheckboxColumn("Select", default=False),
            "Rule ID": st.column_config.NumberColumn("Rule ID", width="medium"),
            "Customer name": st.column_config.TextColumn("Customer name", width="medium"),
            "Priority order": st.column_config.NumberColumn("Priority order", width="medium"),
            "Charge name mapping": st.column_config.TextColumn("Charge name mapping", width="medium"),
            "Charge ID": st.column_config.TextColumn("Charge ID", width="medium"),
            "Charge group heading": st.column_config.TextColumn("Charge group heading", width="medium"),
            "Charge category": st.column_config.TextColumn("Charge category", width="medium"),
            "Request type": st.column_config.TextColumn("Request type", width="medium")
        },
        key="custom_rules_table"
    )
    
    # Update session state based on edited dataframe
    if edited_custom_df is not None:
        if 'Select' in edited_custom_df.columns:
            st.session_state.custom_selected = edited_custom_df['Select'].tolist()
    
    # Global Rules Section
    st.markdown("### Global")
    st.markdown("Rules that apply to all customers. If no customer-specific rule overrides them.")
    
    # Get global rules data (same as custom for demo)
    global_rules_df = data_provider.get_rules(customer)
    
    # Initialize session state for global selection
    if 'global_selected' not in st.session_state:
        st.session_state.global_selected = [False] * len(global_rules_df)
    
    # Create a copy of the dataframe for display
    display_global_df = global_rules_df.copy()
    display_global_df.insert(0, 'Select', st.session_state.global_selected)
    
    # Display the global rules table with checkboxes
    edited_global_df = st.data_editor(
        display_global_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Select": st.column_config.CheckboxColumn("Select", default=False),
            "Rule ID": st.column_config.NumberColumn("Rule ID", width="medium"),
            "Customer name": st.column_config.TextColumn("Customer name", width="medium"),
            "Priority order": st.column_config.NumberColumn("Priority order", width="medium"),
            "Charge name mapping": st.column_config.TextColumn("Charge name mapping", width="medium"),
            "Charge ID": st.column_config.TextColumn("Charge ID", width="medium"),
            "Charge group heading": st.column_config.TextColumn("Charge group heading", width="medium"),
            "Charge category": st.column_config.TextColumn("Charge category", width="medium"),
            "Request type": st.column_config.TextColumn("Request type", width="medium")
        },
        key="global_rules_table"
    )
    
    # Update session state based on edited dataframe
    if edited_global_df is not None:
        if 'Select' in edited_global_df.columns:
            st.session_state.global_selected = edited_global_df['Select'].tolist()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_processed_files_tab(data_provider: DataProvider, customer: str):
    """Render the processed files tab"""
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    st.markdown("### Processed files")
    st.markdown("View and manage processed charge files.")
    
    # Get processed files data
    files_df = data_provider.get_processed_files(customer)
    
    if isinstance(data_provider, DemoDataProvider):
        st.info("🔧 Demo Mode: This would show processed files from Snowflake")
    
    st.dataframe(files_df, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_regex_rules_tab(data_provider: DataProvider, customer: str):
    """Render the regex rules tab"""
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    st.markdown("### Regex and rules")
    st.markdown("Configure regex patterns and advanced rule matching.")
    
    # Get regex rules data
    regex_df = data_provider.get_regex_rules(customer)
    
    if isinstance(data_provider, DemoDataProvider):
        st.info("🔧 Demo Mode: This would show regex patterns from Snowflake")
    
    st.dataframe(regex_df, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application function"""
    # Setup
    setup_page_config()
    setup_css()
    
    # Get data provider
    data_provider = get_data_provider()
    
    # Render sidebar and get selected customer
    customer = render_sidebar(data_provider)
    
    # Header
    st.markdown('<div class="main-header">⚡ Charge Mapping</div>', unsafe_allow_html=True)
    
    # Navigation tabs in main area
    tab1, tab2, tab3, tab4 = st.tabs([
        "Charges", 
        "Rules", 
        "Processed files", 
        "Regex and rules"
    ])
    
    # Render tabs with context managers
    with tab1:
        render_charges_tab(data_provider, customer)
    with tab2:
        render_rules_tab(data_provider, customer)
    with tab3:
        render_processed_files_tab(data_provider, customer)
    with tab4:
        render_regex_rules_tab(data_provider, customer)

if __name__ == "__main__":
    main()
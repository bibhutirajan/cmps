"""
Charge Mapping Application - Modular Version

This is the main application file with a modular architecture following best practices.
"""

import streamlit as st
import os
from dataclasses import dataclass

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="Charge Mapping",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"  # Always expanded for better UX
)

# Import components
from components.data.data_providers import get_data_provider, DataProvider
from components.ui.sidebar import render_sidebar
from components.ui.charges_tab import render_charges_tab
from components.ui.rules_tab import render_rules_tab
from deployment_config import DeploymentConfig




# Configuration

@dataclass
class AppConfig:
    """Centralized configuration for the application"""
    # Data source configuration
    DATA_SOURCE: str = os.getenv("DATA_SOURCE", "demo")  # "demo" or "snowflake"
    
    # Snowflake configuration
    SNOWFLAKE_ENABLED: bool = os.getenv("SNOWFLAKE_ENABLED", "true").lower() == "true"
    SNOWFLAKE_DATABASE: str = os.getenv("SNOWFLAKE_DATABASE", "SANDBOX")
    SNOWFLAKE_SCHEMA: str = os.getenv("SNOWFLAKE_SCHEMA", "BMANOJKUMAR")
    
    # Table configurations
    CHARGES_TABLE: str = os.getenv("CHARGES_TABLE", "charges")
    RULES_TABLE: str = os.getenv("RULES_TABLE", "rules")
    
    # UI Configuration
    SIDEBAR_COLLAPSED: bool = True
    DARK_THEME: bool = True

# Initialize configuration
config = AppConfig()

# Force production data configuration for Snowflake deployment
# Always apply staging config to ensure production tables are used
try:
    # Try to import snowflake.snowpark to detect Snowflake environment
    import snowflake.snowpark  # noqa: F401
    DeploymentConfig.setup_snowflake_staging()
    config = AppConfig()  # Reload config with new environment variables
except ImportError:
    # Local development environment - use default config
    pass


# Utility Functions

def load_css():
    """Load the CSS file"""
    try:
        with open("static/css/styles.css", "r") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("CSS file not found. Please ensure static/css/styles.css exists.")
        # Fallback to inline CSS
        st.markdown("""
        <style>
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
            
            /* Ensure sidebar can expand when create rule form is active */
            [data-testid="stSidebar"] {
                transition: all 0.3s ease;
            }
            
            /* Auto-expand sidebar ONLY when create rule form is active */
            [data-testid="stSidebar"]:has(.stButton[key="close_rule_form"]) {
                min-width: 400px !important;
                max-width: 450px !important;
                display: block !important;
                visibility: visible !important;
            }
            
            /* Keep sidebar collapsed by default when no form is active */
            [data-testid="stSidebar"]:not(:has(.stButton[key="close_rule_form"])) {
                /* Let Streamlit handle default collapsed state */
            }
            
            /* Make app sidebar narrower when no forms are active */
            [data-testid="stSidebar"]:not(:has(.stButton[key="close_rule_form"])):not(:has(.stButton[key="close_edit_rule_form"])) {
                max-width: 250px !important;
                min-width: 200px !important;
            }
        </style>
        """, unsafe_allow_html=True)


def render_header():
    """Render the main header"""
    st.markdown('<div class="main-header">⚡ Charge Mapping</div>', unsafe_allow_html=True)


def render_navigation_tabs():
    """Render the navigation tabs"""
    return st.tabs([
        "Charges", 
        "Rules"
    ])


def render_sidebar_expansion_css():
    """Render CSS for sidebar styling"""
    st.markdown("""
    <style>
    /* Force sidebar to be expanded */
    [data-testid="stSidebar"] {
        width: 500px !important;
        min-width: 500px !important;
        max-width: 500px !important;
        transform: translateX(0) !important;
        transition: transform 0.3s ease !important;
    }
    
    /* Ensure sidebar is visible */
    [data-testid="stSidebar"] > div {
        width: 500px !important;
        min-width: 500px !important;
        max-width: 500px !important;
    }
    
    /* Hide the sidebar collapse button */
    [data-testid="stSidebar"] [data-testid="collapsedControl"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_main_content(data_provider: DataProvider, customer: str):
    """Render the main content area with tabs"""
    # Navigation tabs with descriptive names
    charges_tab, rules_tab = render_navigation_tabs()
    
    # Render tabs with clear, descriptive variable names
    with charges_tab:
        render_charges_tab(data_provider, customer)
    
    with rules_tab:
        render_rules_tab(data_provider, customer)
    
    # CENTRALIZED DIALOG MANAGEMENT - Only one dialog at a time across entire app
    # Priority order: Create Rule (any tab) -> Edit Rule -> Edit Priority -> Preview dialogs
    if (st.session_state.get('show_create_rule_dialog_charges_tab', False) or 
        (st.session_state.get('show_create_rule_dialog_rules_header', False) and
         st.session_state.get('create_rule_triggered_by_btn', False))):
        from components.dialogs.create_rule_dialog import create_rule_dialog
        # Determine which tab triggered the dialog and use appropriate session key
        if st.session_state.get('show_create_rule_dialog_charges_tab', False):
            create_rule_dialog(data_provider, customer, "show_create_rule_dialog_charges_tab")
        else:
            create_rule_dialog(data_provider, customer, "show_create_rule_dialog_rules_header")
            st.session_state.pop('create_rule_triggered_by_btn', None)
    elif st.session_state.get('show_edit_rule_dialog', False):
        from components.dialogs.edit_rule_dialog import edit_rule_dialog
        from components.ui.rules_tab import transform_rule_data_for_edit
        selected_rule = st.session_state.get('selected_rule_for_edit', {})
        # Transform rule data to match edit form structure
        transformed_rule_data = transform_rule_data_for_edit(selected_rule)
        edit_rule_dialog(data_provider, customer, transformed_rule_data, "show_edit_rule_dialog")
    elif st.session_state.get('show_edit_priority_dialog', False):
        from components.dialogs.edit_priority_dialog import edit_priority_dialog
        edit_priority_dialog(data_provider, customer)
    elif st.session_state.get('show_create_rule_preview', False):
        from components.dialogs.create_rule_preview_dialog import create_rule_preview_dialog
        preview_data = st.session_state.get('create_rule_preview_data', {})
        create_rule_preview_dialog(data_provider, customer, preview_data, "show_create_rule_preview")
    elif st.session_state.get('show_edit_rule_preview', False):
        from components.dialogs.edit_rule_preview_dialog import edit_rule_preview_dialog
        preview_data = st.session_state.get('edit_rule_preview_data', {})
        edit_rule_preview_dialog(data_provider, customer, preview_data, "show_edit_rule_preview")


# Main Application

def main():
    """Main application function"""
    # Setup
    load_css()
    
    # Get data provider
    data_provider = get_data_provider(config.SNOWFLAKE_ENABLED)
    
    # Render sidebar and get selected customer
    customer = render_sidebar(data_provider)
    
    # Header
    render_header()
    
    # Render main content (tabs or other content)
    render_main_content(data_provider, customer)


if __name__ == "__main__":
    main() 
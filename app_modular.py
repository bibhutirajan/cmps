"""
Charge Mapping Application - Modular Version

This is the main application file with a modular architecture following best practices.
"""

import streamlit as st
import os
import pandas as pd
from typing import Optional
from dataclasses import dataclass

# Import components
from components.data.providers import get_data_provider, DataProvider
from components.ui.sidebar.main_sidebar import render_main_sidebar
from components.ui.charges_tab import render_charges_tab
from components.ui.rules_tab import render_rules_tab
from components.ui.processed_files_tab import render_processed_files_tab
from components.ui.regex_rules_tab import render_regex_rules_tab



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
# UTILITY FUNCTIONS
# =============================================================================

def setup_page_config():
    """Setup page configuration"""
    st.set_page_config(
        page_title="Charge Mapping",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="collapsed" if config.SIDEBAR_COLLAPSED else "expanded"
    )


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
                max-width: 500px !important;
                display: block !important;
                visibility: visible !important;
            }
            
            /* Keep sidebar collapsed by default when no form is active */
            [data-testid="stSidebar"]:not(:has(.stButton[key="close_rule_form"])) {
                /* Let Streamlit handle default collapsed state */
            }
        </style>
        """, unsafe_allow_html=True)


def load_js():
    """Load the JavaScript file"""
    try:
        with open("static/js/modal.js", "r") as f:
            js = f.read()
        st.markdown(f"<script>{js}</script>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("JavaScript file not found. Modal functionality may not work properly.")


def render_header():
    """Render the main header"""
    st.markdown('<div class="main-header">⚡ Charge Mapping</div>', unsafe_allow_html=True)


def render_navigation_tabs():
    """Render the navigation tabs"""
    return st.tabs([
        "Charges", 
        "Rules", 
        "Processed files", 
        "Regex and rules"
    ])


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application function"""
    # Setup
    setup_page_config()
    load_css()
    load_js()
    
    # Get data provider
    data_provider = get_data_provider(config.SNOWFLAKE_ENABLED)
    
    # Check if modal should be shown and handle sidebar expansion
    if st.session_state.get('show_create_rule_modal', False) or st.session_state.get('show_edit_rule_modal', False):
        # Force sidebar to be expanded when modal is shown
        st.markdown("""
        <style>
        /* Force sidebar to be expanded when modal is active */
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
        
        /* Hide the sidebar collapse button when modal is active */
        [data-testid="stSidebar"] [data-testid="collapsedControl"] {
            display: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Render sidebar and get selected customer
    customer = render_main_sidebar(data_provider)
    
    # Render edit priority modal as floating overlay if active
    if st.session_state.get('show_edit_priority_modal', False):
        from components.modals.edit_priority_modal import edit_priority_modal
        edit_priority_modal(data_provider, customer)
    
    # Note: Modal rendering is handled by the sidebar components now
    
    # Header
    render_header()
    
    # Render preview on main page if in preview mode - BEFORE tabs
    if st.session_state.get('show_preview', False) and st.session_state.get('show_create_rule_modal', False):
        # Create rule preview
        with st.container():
            st.markdown("### 🔍 Rule Preview")
            st.markdown("This rule will update the Charge ID for the charges listed below. Review the changes before saving.")
            
            # Rule summary section for new rule
            rule_form_data = st.session_state.get('rule_form_data', {})
            
            # Create rule summary data for new rule
            rule_summary_data = {
                "Rule ID": ["New"],
                "Customer name": [rule_form_data.get('customer', 'AmerescoFTP')],
                "Priority order": ["Auto-assigned"],
                "Charge name mappi...": [rule_form_data.get('charge_name', 'CHP Rider')],
                "Charge ID": [rule_form_data.get('charge_id', 'NewBatch')],
                "Charge grou...": [""],
                "Charge category": ["ch.usage_charge"]
            }
            
            # Display rule summary table
            st.markdown("#### Rule summary")
            rule_summary_df = pd.DataFrame(rule_summary_data)
            st.dataframe(
                rule_summary_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Rule ID": st.column_config.TextColumn("Rule ID", width="small"),
                    "Customer name": st.column_config.TextColumn("Customer name", width="medium"),
                    "Priority order": st.column_config.TextColumn("Priority order", width="small"),
                    "Charge name mappi...": st.column_config.TextColumn("Charge name mappi...", width="medium"),
                    "Charge ID": st.column_config.TextColumn("Charge ID", width="medium"),
                    "Charge grou...": st.column_config.TextColumn("Charge grou...", width="medium"),
                    "Charge category": st.column_config.TextColumn("Charge category", width="medium")
                }
            )
            
            st.markdown("---")
            
            # Generate preview data based on the rule
            from components.modals.create_rule_modal import generate_preview_data
            preview_data = generate_preview_data(st.session_state.rule_form_data)
            
            # Display the preview table with native Streamlit dataframe
            st.dataframe(
                preview_data,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Charge name": st.column_config.TextColumn("Charge name", width="medium"),
                    "Provider name": st.column_config.TextColumn("Provider name", width="medium"),
                    "Account number": st.column_config.TextColumn("Account number", width="medium"),
                    "Statement ID": st.column_config.TextColumn("Statement ID", width="medium"),
                    "Current Charge ID": st.column_config.TextColumn("Current Charge ID", width="medium"),
                    "New Charge ID": st.column_config.TextColumn("New Charge ID", width="medium"),
                    "Usage unit": st.column_config.TextColumn("Usage unit", width="small"),
                    "Service": st.column_config.TextColumn("Service", width="small")
                }
            )
            
            # Add CSS for strikethrough effect on Current Charge ID column
            st.markdown("""
            <style>
            /* Target the 5th column (Current Charge ID) in Streamlit dataframes */
            [data-testid="stDataFrame"] td:nth-child(5) {
                text-decoration: line-through !important;
                color: #888888 !important;
                font-style: italic !important;
            }
            
            /* Alternative selectors for better compatibility */
            .stDataFrame td:nth-child(5) {
                text-decoration: line-through !important;
                color: #888888 !important;
                font-style: italic !important;
            }
            
            /* Target by content for specific values */
            [data-testid="stDataFrame"] td:has-text("Uncategorized"),
            [data-testid="stDataFrame"] td:has-text("eh.special_regulatory_charges") {
                text-decoration: line-through !important;
                color: #888888 !important;
                font-style: italic !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Add JavaScript to apply strikethrough effect
            st.markdown("""
            <script>
            // Apply strikethrough to Current Charge ID column
            function applyStrikethrough() {
                const tables = document.querySelectorAll('[data-testid="stDataFrame"]');
                tables.forEach(function(table) {
                    const rows = table.querySelectorAll('tr');
                    rows.forEach(function(row) {
                        const cells = row.querySelectorAll('td');
                        if (cells.length >= 5) { // Current Charge ID is 5th column (0-indexed)
                            const currentChargeCell = cells[4]; // 5th column (0-indexed)
                            if (currentChargeCell) {
                                currentChargeCell.style.textDecoration = 'line-through';
                                currentChargeCell.style.color = '#888888';
                                currentChargeCell.style.fontStyle = 'italic';
                            }
                        }
                    });
                });
            }
            
            // Apply immediately and with delays to ensure it works
            applyStrikethrough();
            setTimeout(applyStrikethrough, 100);
            setTimeout(applyStrikethrough, 500);
            setTimeout(applyStrikethrough, 1000);
            </script>
            """, unsafe_allow_html=True)
            
            # Clean preview - no buttons or checkboxes in main area
            # Navigation will be handled in the sidebar
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Add some spacing after the preview
        st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Render edit rule preview on main page if in edit preview mode
    elif st.session_state.get('show_edit_preview', False) and st.session_state.get('show_edit_rule_modal', False):
        # Edit rule preview
        with st.container():
            st.markdown("### 🔍 Edit Rule Preview")
            st.markdown("These changes will affect all the charges listed below. Review the changes before saving.")
            
            # Rule summary section
            original_rule = st.session_state.get('selected_rule_for_edit', {})
            updated_rule_data = st.session_state.get('edit_rule_form_data', {})
            
            # Create rule summary data
            rule_summary_data = {
                "Rule ID": [original_rule.get('Rule ID', '8912000')],
                "Customer name": [original_rule.get('Customer name', 'AmerescoFTP')],
                "Priority order": [original_rule.get('Priority order', '3101')],
                "Charge name mappi...": [original_rule.get('Charge name mapping', '(?i)Electric\\s*servic...')],
                "Charge ID": [updated_rule_data.get('charge_id', 'NewBatch')],
                "Charge grou...": [original_rule.get('Charge group heading', '')],
                "Charge category": [original_rule.get('Charge category', 'ch.usage_charge')]
            }
            
            # Display rule summary table
            st.markdown("#### Rule summary")
            rule_summary_df = pd.DataFrame(rule_summary_data)
            st.dataframe(
                rule_summary_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Rule ID": st.column_config.NumberColumn("Rule ID", width="small"),
                    "Customer name": st.column_config.TextColumn("Customer name", width="medium"),
                    "Priority order": st.column_config.NumberColumn("Priority order", width="small"),
                    "Charge name mappi...": st.column_config.TextColumn("Charge name mappi...", width="medium"),
                    "Charge ID": st.column_config.TextColumn("Charge ID", width="medium"),
                    "Charge grou...": st.column_config.TextColumn("Charge grou...", width="medium"),
                    "Charge category": st.column_config.TextColumn("Charge category", width="medium")
                }
            )
            
            st.markdown("---")
            
            # Generate preview data based on the rule changes
            from components.modals.edit_rule_modal import generate_edit_preview_data
            preview_data = generate_edit_preview_data(st.session_state.edit_rule_form_data, original_rule)
            
            # Display the preview table with native Streamlit dataframe
            st.dataframe(
                preview_data,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Charge name": st.column_config.TextColumn("Charge name", width="medium"),
                    "Provider name": st.column_config.TextColumn("Provider name", width="medium"),
                    "Account number": st.column_config.TextColumn("Account number", width="medium"),
                    "Statement ID": st.column_config.TextColumn("Statement ID", width="medium"),
                    "Current Charge ID": st.column_config.TextColumn("Current Charge ID", width="medium"),
                    "New Charge ID": st.column_config.TextColumn("New Charge ID", width="medium"),
                    "Usage unit": st.column_config.TextColumn("Usage unit", width="small"),
                    "Service": st.column_config.TextColumn("Service", width="small")
                }
            )
            
            # Add CSS for strikethrough effect on Current Charge ID column
            st.markdown("""
            <style>
            /* Target the 5th column (Current Charge ID) in Streamlit dataframes */
            [data-testid="stDataFrame"] td:nth-child(5) {
                text-decoration: line-through !important;
                color: #888888 !important;
                font-style: italic !important;
            }
            
            /* Alternative selectors for better compatibility */
            .stDataFrame td:nth-child(5) {
                text-decoration: line-through !important;
                color: #888888 !important;
                font-style: italic !important;
            }
            
            /* Target by content for specific values */
            [data-testid="stDataFrame"] td:has-text("Uncategorized"),
            [data-testid="stDataFrame"] td:has-text("eh.special_regulatory_charges") {
                text-decoration: line-through !important;
                color: #888888 !important;
                font-style: italic !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Add JavaScript to apply strikethrough effect
            st.markdown("""
            <script>
            // Apply strikethrough to Current Charge ID column
            function applyStrikethrough() {
                const tables = document.querySelectorAll('[data-testid="stDataFrame"]');
                tables.forEach(function(table) {
                    const rows = table.querySelectorAll('tr');
                    rows.forEach(function(row) {
                        const cells = row.querySelectorAll('td');
                        if (cells.length >= 5) { // Current Charge ID is 5th column (0-indexed)
                            const currentChargeCell = cells[4]; // 5th column (0-indexed)
                            if (currentChargeCell) {
                                currentChargeCell.style.textDecoration = 'line-through';
                                currentChargeCell.style.color = '#888888';
                                currentChargeCell.style.fontStyle = 'italic';
                            }
                        }
                    });
                });
            }
            
            // Apply immediately and with delays to ensure it works
            applyStrikethrough();
            setTimeout(applyStrikethrough, 100);
            setTimeout(applyStrikethrough, 500);
            setTimeout(applyStrikethrough, 1000);
            </script>
            """, unsafe_allow_html=True)
            
            # Clean preview - no buttons or checkboxes in main area
            # Navigation will be handled in the sidebar
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Add some spacing after the preview
        st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = render_navigation_tabs()
    
    # Render tabs
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
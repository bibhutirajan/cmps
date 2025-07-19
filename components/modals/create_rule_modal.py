"""
Create Rule Modal Component

This module provides the modal interface for creating new charge mapping rules.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional, List
from components.data.providers import DataProvider


def create_rule_modal(data_provider: DataProvider, customer: str, selected_charges: list = None) -> Optional[Dict[str, Any]]:
    """
    Render the create rule modal in the sidebar
    
    Args:
        data_provider: The data provider instance
        customer: The customer name
        selected_charges: List of selected charges (optional)
    
    Returns:
        None (modal is rendered in sidebar)
    """
    
    # Initialize form data in session state if not exists
    if 'rule_form_data' not in st.session_state:
        st.session_state.rule_form_data = {
            'provider': 'Atmos',
            'charge_name_match': 'Exactly matches',
            'charge_name_value': '',
            'account_number_match': 'Exactly matches',
            'account_number_value': '',
            'usage_unit': '',
            'service_type': '',
            'tariff': '',
            'raw_charge_name_match': 'Exactly matches',
            'raw_charge_name_value': '',
            'charge_id': 'NewBatch',
            'active': True
        }
    
    # Initialize preview state
    if 'show_preview' not in st.session_state:
        st.session_state.show_preview = False
    
    # Modal header with close button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("### Create Rule")
    with col2:
        if st.button("✕", key="close_modal_x", help="Close modal"):
            st.session_state.show_create_rule_modal = False
            st.session_state.show_preview = False
            st.rerun()
    
    st.divider()
    
    # Check if we're in preview mode
    if not st.session_state.get('show_preview', False):
        # Form mode - show the rule creation form
        with st.form("create_rule_form", clear_on_submit=False):
            # Left section: "If charge matches criteria..."
            st.markdown("**If charge matches criteria...**")
            
            # Provider
            provider_options = ["Atmos", "Other"]
            provider_index = 0
            if st.session_state.rule_form_data['provider'] in provider_options:
                provider_index = provider_options.index(st.session_state.rule_form_data['provider'])
            
            st.session_state.rule_form_data['provider'] = st.selectbox(
                "Provider",
                options=provider_options,
                index=provider_index,
                key="modal_provider"
            )
            
            # Charge name
            col1, col2 = st.columns([1, 2])
            with col1:
                match_options = ["Exactly matches", "Contains", "Starts with", "Ends with"]
                match_index = 0
                if st.session_state.rule_form_data['charge_name_match'] in match_options:
                    match_index = match_options.index(st.session_state.rule_form_data['charge_name_match'])
                
                st.session_state.rule_form_data['charge_name_match'] = st.selectbox(
                    "Charge name",
                    options=match_options,
                    index=match_index,
                    key="modal_charge_name_match"
                )
            with col2:
                st.session_state.rule_form_data['charge_name_value'] = st.text_input(
                    "Value",
                    value=st.session_state.rule_form_data['charge_name_value'],
                    key="modal_charge_name_value"
                )
            
            # Advanced conditions toggle
            show_advanced = st.checkbox("Show advanced conditions", key="modal_show_advanced")
            
            if show_advanced:
                # Account number
                col1, col2 = st.columns([1, 2])
                with col1:
                    account_match_index = 0
                    if st.session_state.rule_form_data['account_number_match'] in match_options:
                        account_match_index = match_options.index(st.session_state.rule_form_data['account_number_match'])
                    
                    st.session_state.rule_form_data['account_number_match'] = st.selectbox(
                        "Account number",
                        options=match_options,
                        index=account_match_index,
                        key="modal_account_number_match"
                    )
                with col2:
                    st.session_state.rule_form_data['account_number_value'] = st.text_input(
                        "Value",
                        value=st.session_state.rule_form_data['account_number_value'],
                        key="modal_account_number_value"
                    )
                
                # Usage unit
                st.session_state.rule_form_data['usage_unit'] = st.text_input(
                    "Usage unit",
                    value=st.session_state.rule_form_data['usage_unit'],
                    key="modal_usage_unit"
                )
                
                # Service type
                st.session_state.rule_form_data['service_type'] = st.text_input(
                    "Service type",
                    value=st.session_state.rule_form_data['service_type'],
                    key="modal_service_type"
                )
                
                # Tariff
                st.session_state.rule_form_data['tariff'] = st.text_input(
                    "Tariff",
                    value=st.session_state.rule_form_data['tariff'],
                    key="modal_tariff"
                )
                
                # Raw charge name
                col1, col2 = st.columns([1, 2])
                with col1:
                    raw_match_index = 0
                    if st.session_state.rule_form_data['raw_charge_name_match'] in match_options:
                        raw_match_index = match_options.index(st.session_state.rule_form_data['raw_charge_name_match'])
                    
                    st.session_state.rule_form_data['raw_charge_name_match'] = st.selectbox(
                        "Raw charge name",
                        options=match_options,
                        index=raw_match_index,
                        key="modal_raw_charge_name_match"
                    )
                with col2:
                    st.session_state.rule_form_data['raw_charge_name_value'] = st.text_input(
                        "Value",
                        value=st.session_state.rule_form_data['raw_charge_name_value'],
                        key="modal_raw_charge_name_value"
                    )
            
            st.divider()
            
            # Right section: "Then categorize the charge as..."
            st.markdown("**Then categorize the charge as...**")
            
            # Charge ID
            charge_id_options = ["NewBatch", "Existing Batch", "Other"]
            charge_id_index = 0
            if st.session_state.rule_form_data['charge_id'] in charge_id_options:
                charge_id_index = charge_id_options.index(st.session_state.rule_form_data['charge_id'])
            
            st.session_state.rule_form_data['charge_id'] = st.selectbox(
                "Charge ID",
                options=charge_id_options,
                index=charge_id_index,
                key="modal_charge_id"
            )
            
            # Active toggle
            st.session_state.rule_form_data['active'] = st.checkbox(
                "Active",
                value=st.session_state.rule_form_data['active'],
                key="modal_active"
            )
            
            # Form actions
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Cancel", type="secondary"):
                    st.session_state.show_create_rule_modal = False
                    st.session_state.show_preview = False
                    st.rerun()
            with col2:
                if st.form_submit_button("Preview changes", type="primary"):
                    st.session_state.show_preview = True
                    st.rerun()
    
    else:
        # Preview mode - show controls in sidebar
        st.markdown("**Preview Mode**")
        st.markdown("Review the changes in the main area below.")
        
        # Action buttons for preview mode
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back to form", key="preview_back_btn_rules"):
                st.session_state.show_preview = False
                st.rerun()
        with col2:
            if st.button("Save rule", type="primary", key="save_rule_btn_rules"):
                # Generate preview data for saving
                preview_data = generate_preview_data(st.session_state.rule_form_data)
                # Save the rule to Snowflake
                success = save_rule_to_snowflake(st.session_state.rule_form_data, preview_data)
                if success:
                    st.success("Rule saved successfully!")
                    st.session_state.show_create_rule_modal = False
                    st.session_state.show_preview = False
                    st.rerun()
                else:
                    st.error("Failed to save rule. Please try again.")
    
    return None


def generate_preview_data(rule_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Generate preview data showing how the rule will affect existing charges
    
    Args:
        rule_data: The rule configuration data
    
    Returns:
        DataFrame with preview data
    """
    # This is sample data - in a real implementation, you would query your database
    # to find charges that match the rule criteria
    sample_data = [
        {
            "Charge name": rule_data.get('charge_name_value', 'CHP Rider'),
            "Provider name": rule_data.get('provider', 'Atmos'),
            "Account number": rule_data.get('account_number_value', '3018639036'),
            "Statement ID": "1efe9dd1-6cad-d3c...",
            "Current Charge ID": "Uncategorized",
            "New Charge ID": rule_data.get('charge_id', 'NewBatch'),
            "Usage unit": "kW",
            "Service": "None"
        }
    ]
    
    # Generate multiple rows for demonstration
    preview_data = []
    for i in range(12):  # 12 rows as shown in the Figma
        row = sample_data[0].copy()
        if i >= 9:  # Last 3 rows have different current charge ID
            row["Current Charge ID"] = "eh.special_regulatory_charges"
        if i > 0:  # All rows except first have different usage unit
            row["Usage unit"] = "None"
        preview_data.append(row)
    
    return pd.DataFrame(preview_data)


def save_rule_to_snowflake(rule_data: Dict[str, Any], affected_charges: pd.DataFrame) -> bool:
    """
    Save the rule to Snowflake database
    
    Args:
        rule_data: The rule configuration data
        affected_charges: DataFrame of charges that will be affected
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Here you would implement the actual Snowflake database write
        # For now, we'll simulate a successful save
        
        # Example SQL (you would need to adapt this to your actual schema):
        # INSERT INTO charge_mapping_rules (
        #     customer, provider, charge_name_match, charge_name_value,
        #     account_number_match, account_number_value, usage_unit,
        #     service_type, tariff, raw_charge_name_match, raw_charge_name_value,
        #     charge_id, active, created_at
        # ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
        
        # For demonstration, we'll just return True
        # In a real implementation, you would:
        # 1. Connect to Snowflake
        # 2. Execute the INSERT statement
        # 3. Update the affected charges with the new charge_id
        # 4. Handle any errors and return appropriate status
        
        st.info(f"Rule would be saved to Snowflake with {len(affected_charges)} affected charges")
        return True
        
    except Exception as e:
        st.error(f"Error saving rule: {str(e)}")
        return False


def render_create_rule_button(data_provider: DataProvider, context: Dict[str, Any] = None, unique_key: str = ""):
    """
    Render the Create Rule button that opens the modal
    
    Args:
        data_provider: The data provider instance
        context: Context dictionary containing customer and selected data
        unique_key: Unique identifier for this button instance
    """
    
    # Get customer from context or session state
    if isinstance(context, dict):
        customer = context.get('customer', st.session_state.get('selected_customer', 'Default Customer'))
        selected_charges = context.get('selected_charges', [])
    else:
        customer = st.session_state.get('selected_customer', 'Default Customer')
        selected_charges = []
    
    # Create unique button key
    button_key = f"create_rule_btn_{unique_key}" if unique_key else "create_rule_btn"
    
    # Check if button is clicked
    if st.button("Create rule", key=button_key, type="primary"):
        # Store customer in session state for modal use
        st.session_state.selected_customer = customer
        # Show modal and force sidebar expansion
        st.session_state.show_create_rule_modal = True
        # Add CSS to immediately expand sidebar
        st.markdown("""
        <style>
        /* Immediately expand sidebar when modal is triggered */
        [data-testid="stSidebar"] {
            width: 500px !important;
            min-width: 500px !important;
            max-width: 500px !important;
            transform: translateX(0) !important;
            transition: transform 0.3s ease !important;
        }
        </style>
        """, unsafe_allow_html=True)
        st.rerun() 
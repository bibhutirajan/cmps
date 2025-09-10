"""
Create Rule Popup Component

This module contains the create rule popup using Streamlit's native st.dialog.
"""

import streamlit as st
from components.data.data_providers import DataProvider


@st.dialog("➕ Create Rule", width="medium")
def create_rule_dialog(data_provider: DataProvider, customer: str, dialog_state_key: str = "show_create_rule_dialog"):
    """
    Render the create rule dialog using st.dialog
    
    Args:
        data_provider: The data provider instance
        customer: The selected customer name
    """
    # Hide the default close button and add custom close button
    st.html(
        '''
            <style>
                div[aria-label="dialog"]>button[aria-label="Close"] {
                    display: none;
                }
            </style>
        '''
    )
    
    # Custom close button positioned in top-right corner
    col1, col2 = st.columns([1, 0.1])
    with col2:
        if st.button("", type="secondary", icon=":material/close:", key="create_rule_close"):
            # Clear the dialog state and force rerun
            st.session_state.pop(dialog_state_key, None)
            st.session_state.pop('create_rule_triggered_by_btn', None)
            st.rerun()
    
    # Dialog content
    st.markdown(f"**Customer:** {customer}")
    st.markdown("---")
    
    # If charge matches criteria section
    st.markdown("### If charge matches criteria...")
    
    # Provider
    form_data = st.session_state.get('create_rule_form_data', {})
    provider_options = ["Atmos", "Other Provider", "Test Provider"]
    provider_index = provider_options.index(form_data.get('provider', 'Atmos')) if form_data.get('provider') in provider_options else 0
    
    provider = st.selectbox(
        "Provider",
        provider_options,
        index=provider_index,
        key="dialog_rule_provider"
    )
    
    # Charge name with condition dropdown - exactly like sidebar
    col1, col2 = st.columns([1, 2])
    with col1:
        condition_options = ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"]
        condition_index = condition_options.index(form_data.get('charge_name_condition', 'Exactly matches')) if form_data.get('charge_name_condition') in condition_options else 0
        
        charge_name_condition = st.selectbox(
            "Condition",
            condition_options,
            index=condition_index,
            key="dialog_charge_name_condition"
        )
    with col2:
        charge_name = st.text_input(
            "Charge name",
            value=form_data.get('charge_name', 'CHP rider'),
            key="dialog_rule_charge_name"
        )
    
    # Advanced conditions toggle
    advanced_enabled = st.toggle("Advanced conditions", value=form_data.get('advanced_enabled', True), key="dialog_advanced_conditions")
    
    if advanced_enabled:
        # Account number - exactly like sidebar
        col1, col2 = st.columns([1, 2])
        with col1:
            account_condition_options = ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"]
            account_condition_index = account_condition_options.index(form_data.get('account_condition', 'Exactly matches')) if form_data.get('account_condition') in account_condition_options else 0
            
            account_condition = st.selectbox(
                "Condition",
                account_condition_options,
                index=account_condition_index,
                key="dialog_account_condition"
            )
        with col2:
            account_number = st.text_input(
                "Account number",
                value=form_data.get('account_number', '00000000'),
                key="dialog_rule_account_number"
            )
        
        # Meter number - exactly like sidebar
        col1, col2 = st.columns([1, 2])
        with col1:
            meter_condition_options = ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"]
            meter_condition_index = meter_condition_options.index(form_data.get('meter_condition', 'Exactly matches')) if form_data.get('meter_condition') in meter_condition_options else 0
            
            meter_condition = st.selectbox(
                "Condition",
                meter_condition_options,
                index=meter_condition_index,
                key="dialog_meter_condition"
            )
        with col2:
            meter_number = st.text_input(
                "Meter number",
                value=form_data.get('meter_number', '00000000'),
                key="dialog_rule_meter_number"
            )
    
    st.markdown("---")
    
    # Then map to section
    st.markdown("### Then map to...")
    
    # Charge group heading
    charge_group_heading = st.text_input(
        "Charge group heading",
        value=form_data.get('charge_group_heading', 'New Charge Group'),
        key="dialog_rule_charge_group_heading"
    )
    
    # Charge category
    category_options = ["Energy", "Delivery", "Taxes", "Other"]
    category_index = category_options.index(form_data.get('charge_category', 'Energy')) if form_data.get('charge_category') in category_options else 0
    
    charge_category = st.selectbox(
        "Charge category",
        category_options,
        index=category_index,
        key="dialog_rule_charge_category"
    )
    
    # Priority order
    priority_order = st.number_input(
        "Priority order",
        min_value=1,
        max_value=1000,
        value=form_data.get('priority_order', 100),
        key="dialog_rule_priority_order"
    )
    
    st.markdown("---")
    
    # Action buttons
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("❌ Cancel", key="dialog_cancel_rule"):
            # Clear the dialog state and form data
            st.session_state.pop(dialog_state_key, None)
            st.session_state.pop('create_rule_form_data', None)
            st.session_state.pop('create_rule_original_key', None)
            st.session_state.pop('create_rule_triggered_by_btn', None)
            st.rerun()
    
    with col2:
        if st.button("🔍 Preview", key="dialog_preview_rule", type="primary"):
            # Create rule data for preview
            rule_data = {
                "customer": customer,
                "provider": provider,
                "charge_name_condition": charge_name_condition,
                "charge_name": charge_name,
                "advanced_enabled": advanced_enabled,
                "account_condition": account_condition if advanced_enabled else None,
                "account_number": account_number if advanced_enabled else None,
                "meter_condition": meter_condition if advanced_enabled else None,
                "meter_number": meter_number if advanced_enabled else None,
                "charge_group_heading": charge_group_heading,
                "charge_category": charge_category,
                "priority_order": priority_order
            }
            
            # Store rule data and form data for restoration
            st.session_state.create_rule_preview_data = rule_data
            st.session_state.create_rule_form_data = {
                "provider": provider,
                "charge_name_condition": charge_name_condition,
                "charge_name": charge_name,
                "advanced_enabled": advanced_enabled,
                "account_condition": account_condition if advanced_enabled else None,
                "account_number": account_number if advanced_enabled else None,
                "meter_condition": meter_condition if advanced_enabled else None,
                "meter_number": meter_number if advanced_enabled else None,
                "charge_group_heading": charge_group_heading,
                "charge_category": charge_category,
                "priority_order": priority_order
            }
            # Store the original dialog state key for restoration
            st.session_state.create_rule_original_key = dialog_state_key
            st.session_state.show_create_rule_preview = True
            st.session_state.pop(dialog_state_key, None)  # Close current dialog
            st.rerun()
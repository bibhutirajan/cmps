"""
Edit Rule Popup Component

This module contains the edit rule popup using Streamlit's native st.dialog.
"""

import streamlit as st
from components.data.data_providers import DataProvider


def safe_get_index(rule_data: dict, key: str, options: list, default: str = None) -> int:
    """
    Safely get the index of a value from rule_data in the given options list
    
    Args:
        rule_data: The rule data dictionary
        key: The key to look up in rule_data
        options: List of valid options
        default: Default value if key not found or invalid
    
    Returns:
        Index of the value in options list
    """
    if default is None:
        default = options[0]
    
    value = rule_data.get(key, default) if rule_data else default
    if value not in options:
        value = default
    return options.index(value)


@st.dialog("✏️ Edit Rule", width="medium")
def edit_rule_dialog(data_provider: DataProvider, customer: str, rule_data: dict = None, dialog_state_key: str = "show_edit_rule_dialog"):
    """
    Render the edit rule dialog using st.dialog
    
    Args:
        data_provider: The data provider instance
        customer: The selected customer name
        rule_data: The rule data to pre-populate the form
        dialog_state_key: The session state key to control dialog visibility
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
        if st.button("", type="secondary", icon=":material/close:", key="edit_rule_close"):
            st.session_state.pop(dialog_state_key, None)
            st.rerun()
    
    # Dialog content
    st.markdown(f"**Customer:** {customer}")
    st.markdown("---")
    
    # If charge matches criteria section
    st.markdown("### If charge matches criteria...")
    
    # Provider
    provider_options = ["Atmos", "Other Provider", "Test Provider"]
    provider = st.selectbox(
        "Provider",
        provider_options,
        index=safe_get_index(rule_data, "provider", provider_options, "Atmos"),
        key="edit_dialog_rule_provider"
    )
    
    # Charge name with condition dropdown
    col1, col2 = st.columns([1, 2])
    with col1:
        condition_options = ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"]
        charge_name_condition = st.selectbox(
            "Condition",
            condition_options,
            index=safe_get_index(rule_data, "charge_name_condition", condition_options, "Exactly matches"),
            key="edit_dialog_charge_name_condition"
        )
    with col2:
        charge_name = st.text_input(
            "Charge name",
            value=rule_data.get("charge_name", "CHP rider") if rule_data else "CHP rider",
            key="edit_dialog_rule_charge_name"
        )
    
    # Advanced conditions toggle
    advanced_enabled = st.toggle("Advanced conditions", value=rule_data.get("advanced_enabled", True) if rule_data else True, key="edit_dialog_advanced_conditions")
    
    if advanced_enabled:
        # Account number
        col1, col2 = st.columns([1, 2])
        with col1:
            account_condition = st.selectbox(
                "Condition",
                condition_options,
                index=safe_get_index(rule_data, "account_condition", condition_options, "Exactly matches"),
                key="edit_dialog_account_condition"
            )
        with col2:
            account_number = st.text_input(
                "Account number",
                value=rule_data.get("account_number", "00000000") if rule_data else "00000000",
                key="edit_dialog_rule_account_number"
            )
        
        # Usage unit
        col1, col2 = st.columns([1, 2])
        with col1:
            usage_unit_condition = st.selectbox(
                "Condition",
                condition_options,
                index=safe_get_index(rule_data, "usage_unit_condition", condition_options, "Exactly matches"),
                key="edit_dialog_usage_unit_condition"
            )
        with col2:
            usage_unit_options = ["kWh", "therms", "gallons", "cubic feet"]
            usage_unit = st.selectbox(
                "Usage unit",
                usage_unit_options,
                index=safe_get_index(rule_data, "usage_unit", usage_unit_options, "kWh"),
                key="edit_dialog_rule_usage_unit"
            )
        
        # Service type
        col1, col2 = st.columns([1, 2])
        with col1:
            service_type_condition = st.selectbox(
                "Condition",
                condition_options,
                index=safe_get_index(rule_data, "service_type_condition", condition_options, "Exactly matches"),
                key="edit_dialog_service_type_condition"
            )
        with col2:
            service_type_options = ["Electric", "Gas", "Water", "Other"]
            service_type = st.selectbox(
                "Service type",
                service_type_options,
                index=safe_get_index(rule_data, "service_type", service_type_options, "Electric"),
                key="edit_dialog_rule_service_type"
            )
        
        # Tariff
        tariff = st.text_input(
            "Tariff",
            value=rule_data.get("tariff", "Lorem ipsum") if rule_data else "Lorem ipsum",
            key="edit_dialog_rule_tariff"
        )
        
        # Raw charge name
        col1, col2 = st.columns([1, 2])
        with col1:
            raw_charge_condition = st.selectbox(
                "Condition",
                condition_options,
                index=safe_get_index(rule_data, "raw_charge_condition", condition_options, "Exactly matches"),
                key="edit_dialog_raw_charge_condition"
            )
        with col2:
            raw_charge_name = st.text_input(
                "Raw charge name",
                value=rule_data.get("raw_charge_name", "Lorem ipsum") if rule_data else "Lorem ipsum",
                key="edit_dialog_rule_raw_charge_name"
            )
        
        # Legacy rule values
        st.markdown("**Legacy rule values**")
        legacy_description = st.text_area(
            "Description",
            value=rule_data.get("legacy_description", "Add a description that explain why they are seeing this") if rule_data else "Add a description that explain why they are seeing this",
            key="edit_dialog_rule_legacy_description",
            height=100
        )
        
        # Meter number
        meter_number = st.text_input(
            "Meter number:",
            value=rule_data.get("meter_number", "") if rule_data else "",
            key="edit_dialog_rule_meter_number"
        )
        
        # Measurement type
        measurement_type = st.text_input(
            "Measurement type:",
            value=rule_data.get("measurement_type", "") if rule_data else "",
            key="edit_dialog_rule_measurement_type"
        )
    
    st.markdown("---")
    
    # Then apply these actions section
    st.markdown("### Then categorize the charge as...")
    
    # Charge ID
    charge_id_options = ["NewBatch", "Energy", "Delivery", "Taxes", "Fees", "Other"]
    charge_id = st.selectbox(
        "Charge ID",
        charge_id_options,
        index=safe_get_index(rule_data, "charge_id", charge_id_options, "NewBatch"),
        key="edit_dialog_rule_charge_id"
    )
    
    st.markdown("---")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ Cancel", key="edit_rule_cancel"):
            st.session_state.pop(dialog_state_key, None)
            st.rerun()
    
    with col2:
        if st.button("🔍 Preview Changes", key="edit_rule_preview", type="primary"):
            # Create rule data for preview
            updated_rule_data = {
                "customer": customer,
                "provider": provider,
                "charge_name_condition": charge_name_condition,
                "charge_name": charge_name,
                "advanced_enabled": advanced_enabled,
                "account_condition": account_condition if advanced_enabled else None,
                "account_number": account_number if advanced_enabled else None,
                "usage_unit_condition": usage_unit_condition if advanced_enabled else None,
                "usage_unit": usage_unit if advanced_enabled else None,
                "service_type_condition": service_type_condition if advanced_enabled else None,
                "service_type": service_type if advanced_enabled else None,
                "tariff": tariff if advanced_enabled else None,
                "raw_charge_condition": raw_charge_condition if advanced_enabled else None,
                "raw_charge_name": raw_charge_name if advanced_enabled else None,
                "legacy_description": legacy_description if advanced_enabled else None,
                "meter_number": meter_number if advanced_enabled else None,
                "measurement_type": measurement_type if advanced_enabled else None,
                "charge_id": charge_id,
                "original_rule": rule_data  # Store original for comparison
            }
            
            # Store rule data and close current dialog to show preview dialog
            st.session_state.edit_rule_preview_data = updated_rule_data
            st.session_state.show_edit_rule_preview = True
            st.session_state.pop(dialog_state_key, None)  # Close current dialog
            st.rerun()
    

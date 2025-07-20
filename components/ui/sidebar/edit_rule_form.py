"""
Edit Rule Form Component

This module contains the edit rule form that appears in the sidebar.
"""

import streamlit as st
from components.data.providers import DataProvider


def render_edit_rule_form(data_provider: DataProvider, customer: str, rule_data: dict = None):
    """
    Render the edit rule form with pre-populated data
    
    Args:
        data_provider: The data provider instance
        customer: The selected customer name
        rule_data: The rule data to pre-populate the form
    """
    # Add CSS to ensure sidebar is visible and expanded ONLY when form is active
    st.markdown("""
    <style>
    /* Force sidebar to expand ONLY when edit rule form is active */
    [data-testid="stSidebar"]:has(.stButton[key="close_edit_rule_form"]) {
        padding-top: 0.5rem !important;
        min-width: 400px !important;
        max-width: 500px !important;
        display: block !important;
        visibility: visible !important;
        transform: translateX(0) !important;
        opacity: 1 !important;
    }
    [data-testid="stSidebar"]:has(.stButton[key="close_edit_rule_form"]) > div:first-child {
        padding-top: 0.5rem !important;
    }
    /* Ensure sidebar content is visible when form is active */
    [data-testid="stSidebar"]:has(.stButton[key="close_edit_rule_form"]) > div {
        display: block !important;
        visibility: visible !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with cross icon and Edit rule text aligned horizontally
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("## Edit rule")
    with col2:
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        if st.button("✖️", key="close_edit_rule_form", help="Close form"):
            st.session_state.show_edit_rule_modal = False
            st.rerun()
    
    st.markdown("---")
    
    # If charge matches criteria section
    st.markdown("### If charge matches criteria...")
    
    # Provider
    provider = st.selectbox(
        "Provider",
        ["Atmos", "Other Provider", "Test Provider"],
        index=0 if not rule_data else ["Atmos", "Other Provider", "Test Provider"].index(rule_data.get("provider", "Atmos")),
        key="edit_rule_provider"
    )
    
    # Charge name with condition dropdown
    col1, col2 = st.columns([1, 2])
    with col1:
        charge_name_condition = st.selectbox(
            "Condition",
            ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
            index=0 if not rule_data else ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"].index(rule_data.get("charge_name_condition", "Exactly matches")),
            key="edit_charge_name_condition"
        )
    with col2:
        charge_name = st.text_input(
            "Charge name",
            value=rule_data.get("charge_name", "CHP rider") if rule_data else "CHP rider",
            key="edit_rule_charge_name"
        )
    
    # Advanced conditions toggle
    advanced_enabled = st.toggle("Advanced conditions", value=rule_data.get("advanced_enabled", True) if rule_data else True, key="edit_advanced_conditions")
    
    if advanced_enabled:
        # Account number
        col1, col2 = st.columns([1, 2])
        with col1:
            account_condition = st.selectbox(
                "Condition",
                ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                index=0 if not rule_data else ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"].index(rule_data.get("account_condition", "Exactly matches")),
                key="edit_account_condition"
            )
        with col2:
            account_number = st.text_input(
                "Account number",
                value=rule_data.get("account_number", "00000000") if rule_data else "00000000",
                key="edit_rule_account_number"
            )
        
        # Usage unit
        col1, col2 = st.columns([1, 2])
        with col1:
            usage_unit_condition = st.selectbox(
                "Condition",
                ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                index=0 if not rule_data else ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"].index(rule_data.get("usage_unit_condition", "Exactly matches")),
                key="edit_usage_unit_condition"
            )
        with col2:
            usage_unit = st.selectbox(
                "Usage unit",
                ["kWh", "therms", "gallons", "cubic feet"],
                index=0 if not rule_data else ["kWh", "therms", "gallons", "cubic feet"].index(rule_data.get("usage_unit", "kWh")),
                key="edit_rule_usage_unit"
            )
        
        # Service type
        col1, col2 = st.columns([1, 2])
        with col1:
            service_type_condition = st.selectbox(
                "Condition",
                ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                index=0 if not rule_data else ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"].index(rule_data.get("service_type_condition", "Exactly matches")),
                key="edit_service_type_condition"
            )
        with col2:
            service_type = st.selectbox(
                "Service type",
                ["Electric", "Gas", "Water", "Other"],
                index=0 if not rule_data else ["Electric", "Gas", "Water", "Other"].index(rule_data.get("service_type", "Electric")),
                key="edit_rule_service_type"
            )
        
        # Tariff
        tariff = st.text_input(
            "Tariff",
            value=rule_data.get("tariff", "Lorem ipsum") if rule_data else "Lorem ipsum",
            key="edit_rule_tariff"
        )
        
        # Raw charge name
        col1, col2 = st.columns([1, 2])
        with col1:
            raw_charge_condition = st.selectbox(
                "Condition",
                ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                index=0 if not rule_data else ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"].index(rule_data.get("raw_charge_condition", "Exactly matches")),
                key="edit_raw_charge_condition"
            )
        with col2:
            raw_charge_name = st.text_input(
                "Raw charge name",
                value=rule_data.get("raw_charge_name", "Lorem ipsum") if rule_data else "Lorem ipsum",
                key="edit_rule_raw_charge_name"
            )
        
        # Legacy rule values
        st.markdown("**Legacy rule values**")
        legacy_description = st.text_area(
            "Description",
            value=rule_data.get("legacy_description", "Add a description that explain why they are seeing this") if rule_data else "Add a description that explain why they are seeing this",
            key="edit_rule_legacy_description",
            height=100
        )
        
        # Meter number
        meter_number = st.text_input(
            "Meter number:",
            value=rule_data.get("meter_number", "") if rule_data else "",
            key="edit_rule_meter_number"
        )
        
        # Measurement type
        measurement_type = st.text_input(
            "Measurement type:",
            value=rule_data.get("measurement_type", "") if rule_data else "",
            key="edit_rule_measurement_type"
        )
    
    st.markdown("---")
    
    # Then apply these actions section
    st.markdown("### Then categorize the charge as...")
    
    # Charge ID
    charge_id = st.selectbox(
        "Charge ID",
        ["NewBatch", "Energy", "Delivery", "Taxes", "Fees", "Other"],
        index=0 if not rule_data else ["NewBatch", "Energy", "Delivery", "Taxes", "Fees", "Other"].index(rule_data.get("charge_id", "NewBatch")),
        key="edit_rule_charge_id"
    )
    
    st.markdown("---")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", key="cancel_edit_rule_btn"):
            st.session_state.show_edit_rule_modal = False
            st.rerun()
    
    with col2:
        if st.button("Preview Changes", key="preview_changes_edit_btn", type="primary"):
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
            
            # Store rule data for preview and show preview
            st.session_state.edit_rule_form_data = updated_rule_data
            st.session_state.show_edit_preview = True
            st.rerun() 
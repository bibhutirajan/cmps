"""
Edit Rule Popup Component

This module contains the edit rule popup using Streamlit's native st.popover.
"""

import streamlit as st
from components.data.providers import DataProvider


def render_edit_rule_popup(data_provider: DataProvider, customer: str, rule_data: dict = None):
    """
    Render the edit rule popup using st.popover
    
    Args:
        data_provider: The data provider instance
        customer: The selected customer name
        rule_data: The rule data to pre-populate the form
    """
    # Only render if popup is triggered
    if not st.session_state.get('show_edit_rule_popup', False):
        return
    
    # Create a centered container for the popup
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Use st.popover for native Streamlit popup
        with st.popover("✏️ Edit Rule", help="Edit existing rule", use_container_width=True):
            
            # If charge matches criteria section
            st.markdown("### If charge matches criteria...")
            
            # Provider
            provider = st.selectbox(
                "Provider",
                ["Atmos", "Other Provider", "Test Provider"],
                index=0 if not rule_data else ["Atmos", "Other Provider", "Test Provider"].index(rule_data.get("provider", "Atmos")),
                key="popup_edit_rule_provider"
            )
            
            # Charge name with condition dropdown - exactly like sidebar
            col1, col2 = st.columns([1, 2])
            with col1:
                charge_name_condition = st.selectbox(
                    "Condition",
                    ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                    index=0 if not rule_data else ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"].index(rule_data.get("charge_name_condition", "Exactly matches")),
                    key="popup_edit_charge_name_condition"
                )
            with col2:
                charge_name = st.text_input(
                    "Charge name",
                    value=rule_data.get("charge_name", "CHP rider") if rule_data else "CHP rider",
                    key="popup_edit_rule_charge_name"
                )
            
            # Advanced conditions toggle
            advanced_enabled = st.toggle("Advanced conditions", value=rule_data.get("advanced_enabled", True) if rule_data else True, key="popup_edit_advanced_conditions")
            
            if advanced_enabled:
                # Account number - exactly like sidebar
                col1, col2 = st.columns([1, 2])
                with col1:
                    account_condition = st.selectbox(
                        "Condition",
                        ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                        index=0 if not rule_data else ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"].index(rule_data.get("account_condition", "Exactly matches")),
                        key="popup_edit_account_condition"
                    )
                with col2:
                    account_number = st.text_input(
                        "Account number",
                        value=rule_data.get("account_number", "00000000") if rule_data else "00000000",
                        key="popup_edit_rule_account_number"
                    )
                
                # Usage unit - exactly like sidebar
                col1, col2 = st.columns([1, 2])
                with col1:
                    usage_unit_condition = st.selectbox(
                        "Condition",
                        ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                        index=0 if not rule_data else ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"].index(rule_data.get("usage_unit_condition", "Exactly matches")),
                        key="popup_edit_usage_unit_condition"
                    )
                with col2:
                    usage_unit = st.selectbox(
                        "Usage unit",
                        ["kWh", "therms", "gallons", "cubic feet"],
                        index=0 if not rule_data else ["kWh", "therms", "gallons", "cubic feet"].index(rule_data.get("usage_unit", "kWh")),
                        key="popup_edit_rule_usage_unit"
                    )
                
                # Service type - exactly like sidebar
                col1, col2 = st.columns([1, 2])
                with col1:
                    service_type_condition = st.selectbox(
                        "Condition",
                        ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                        index=0 if not rule_data else ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"].index(rule_data.get("service_type_condition", "Exactly matches")),
                        key="popup_edit_service_type_condition"
                    )
                with col2:
                    service_type = st.selectbox(
                        "Service type",
                        ["Electric", "Gas", "Water", "Other"],
                        index=0 if not rule_data else ["Electric", "Gas", "Water", "Other"].index(rule_data.get("service_type", "Electric")),
                        key="popup_edit_rule_service_type"
                    )
            
            st.markdown("---")
            
            # Then apply these actions section
            st.markdown("**Then apply these actions...**")
            
            # Charge name mapping - exactly like sidebar
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Charge name mapping**")
            with col2:
                charge_name_mapping = st.text_input(
                    "New charge name",
                    value=rule_data.get("charge_name_mapping", "CHP Rider Charge") if rule_data else "CHP Rider Charge",
                    key="popup_edit_rule_charge_name_mapping"
                )
            
            # Charge category - exactly like sidebar
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Charge category**")
            with col2:
                charge_category = st.selectbox(
                    "Category",
                    ["Energy", "Delivery", "Taxes", "Fees", "Other"],
                    index=0 if not rule_data else ["Energy", "Delivery", "Taxes", "Fees", "Other"].index(rule_data.get("charge_category", "Energy")),
                    key="popup_edit_rule_charge_category"
                )
            
            # Charge group heading - exactly like sidebar
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Charge group heading**")
            with col2:
                charge_group_heading = st.text_input(
                    "Group heading",
                    value=rule_data.get("charge_group_heading", "Energy Charges") if rule_data else "Energy Charges",
                    key="popup_edit_rule_charge_group_heading"
                )
            
            # Request type - exactly like sidebar
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Request type**")
            with col2:
                request_type = st.selectbox(
                    "Request type",
                    ["Standard", "Priority", "Emergency"],
                    index=0 if not rule_data else ["Standard", "Priority", "Emergency"].index(rule_data.get("request_type", "Standard")),
                    key="popup_edit_rule_request_type"
                )
            
            st.markdown("---")
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("Cancel", key="popup_cancel_edit"):
                    st.session_state.show_edit_rule_popup = False
                    st.rerun()
            with col2:
                if st.button("Preview", key="popup_preview_edit"):
                    # Store form data in session state for preview
                    st.session_state.preview_rule_data = {
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
                        "charge_name_mapping": charge_name_mapping,
                        "charge_category": charge_category,
                        "charge_group_heading": charge_group_heading,
                        "request_type": request_type,
                        "customer": customer
                    }
                    st.session_state.show_edit_preview_popup = True
                    st.rerun()
            with col3:
                if st.button("Update", type="primary", key="popup_update_rule"):
                    # Get the rule ID from session state
                    rule_id = st.session_state.get('selected_rule_for_edit', {}).get('Rule ID', '')
                    
                    # Store form data in session state for preview (same as Preview button)
                    st.session_state.preview_rule_data = {
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
                        "charge_name_mapping": charge_name_mapping,
                        "charge_category": charge_category,
                        "charge_group_heading": charge_group_heading,
                        "request_type": request_type,
                        "customer": customer
                    }
                    # Store the rule ID for the edit preview
                    st.session_state.edit_rule_id = rule_id
                    st.session_state.show_edit_preview_popup = True
                    st.rerun()

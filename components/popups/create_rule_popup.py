"""
Create Rule Popup Component

This module contains the create rule popup that appears as a centrally located modal.
"""

import streamlit as st
from components.data.providers import DataProvider


def create_rule_popup(data_provider: DataProvider, customer: str):
    """
    Render the create rule popup as a centrally located modal
    
    Args:
        data_provider: The data provider instance
        customer: The selected customer name
    """
    # Create a very compact, centered popup container
    with st.container():
        # Create a centered column layout with wider width
        col1, col2, col3 = st.columns([3, 1, 3])
        
        with col2:
            # Very compact popup container with styling
            st.markdown("""
            <style>
            .popup-container {
                background-color: #0e1117;
                border: 2px solid #262730;
                border-radius: 8px;
                padding: 40px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
                max-width: 700px;
                margin: 20px auto;
                width: 100%;
            }
            .popup-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 1px solid #262730;
            }
            </style>
            """, unsafe_allow_html=True)
            
            with st.container():
                st.markdown('<div class="popup-container">', unsafe_allow_html=True)
                
                # Compact header with close button
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown("**New Rule**")
                with col2:
                    if st.button("✖️", key="close_rule_popup", help="Close popup"):
                        st.session_state.show_create_rule_modal = False
                        st.rerun()
                
                st.markdown("---")
                
                # Very compact form layout
                st.markdown("**If charge matches criteria...**")
                
                # Provider
                provider = st.selectbox(
                    "Provider",
                    ["Atmos", "Other Provider", "Test Provider"],
                    index=0,
                    key="popup_rule_provider"
                )
                
                # Charge name with condition dropdown - exactly like sidebar
                col1, col2 = st.columns([1, 2])
                with col1:
                    charge_name_condition = st.selectbox(
                        "Condition",
                        ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                        key="popup_charge_name_condition"
                    )
                with col2:
                    charge_name = st.text_input(
                        "Charge name",
                        value="CHP rider",
                        key="popup_rule_charge_name"
                    )
                
                # Advanced conditions toggle
                advanced_enabled = st.toggle("Advanced conditions", value=True, key="popup_advanced_conditions")
                
                if advanced_enabled:
                    # Account number - exactly like sidebar
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        account_condition = st.selectbox(
                            "Condition",
                            ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                            key="popup_account_condition"
                        )
                    with col2:
                        account_number = st.text_input(
                            "Account number",
                            value="00000000",
                            key="popup_rule_account_number"
                        )
                    
                    # Usage unit - exactly like sidebar
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        usage_unit_condition = st.selectbox(
                            "Condition",
                            ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                            key="popup_usage_unit_condition"
                        )
                    with col2:
                        usage_unit = st.selectbox(
                            "Usage unit",
                            ["kWh", "therms", "gallons", "cubic feet"],
                            index=0,
                            key="popup_rule_usage_unit"
                        )
                    
                    # Service type - exactly like sidebar
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        service_type_condition = st.selectbox(
                            "Condition",
                            ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                            key="popup_service_type_condition"
                        )
                    with col2:
                        service_type = st.selectbox(
                            "Service type",
                            ["Electric", "Gas", "Water", "Other"],
                            index=0,
                            key="popup_rule_service_type"
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
                        value="CHP Rider Charge",
                        key="popup_rule_charge_name_mapping"
                    )
                
                # Charge category - exactly like sidebar
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown("**Charge category**")
                with col2:
                    charge_category = st.selectbox(
                        "Category",
                        ["Energy", "Delivery", "Taxes", "Fees", "Other"],
                        index=0,
                        key="popup_rule_charge_category"
                    )
                
                # Charge group heading - exactly like sidebar
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown("**Charge group heading**")
                with col2:
                    charge_group_heading = st.text_input(
                        "Group heading",
                        value="Energy Charges",
                        key="popup_rule_charge_group_heading"
                    )
                
                # Request type - exactly like sidebar
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown("**Request type**")
                with col2:
                    request_type = st.selectbox(
                        "Request type",
                        ["Standard", "Priority", "Emergency"],
                        key="popup_rule_request_type"
                    )
                
                st.markdown("---")
                
                # Action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Cancel", key="popup_cancel_rule_btn"):
                        st.session_state.show_create_rule_modal = False
                        st.rerun()
                
                with col2:
                    if st.button("Preview Changes", key="popup_preview_changes_btn", type="primary"):
                        # Create rule data for preview
                        rule_data = {
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
                            "charge_name_mapping": charge_name_mapping,
                            "charge_category": charge_category,
                            "charge_group_heading": charge_group_heading,
                            "request_type": request_type
                        }
                        
                        # Store rule data for preview and show preview
                        st.session_state.rule_form_data = rule_data
                        st.session_state.show_preview = True
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)

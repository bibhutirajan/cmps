"""
Edit Preview Popup Component

This module contains the edit preview popup using Streamlit's native st.popover.
"""

import streamlit as st
from components.data.providers import DataProvider


def render_edit_preview_popup(data_provider: DataProvider, customer: str):
    """
    Render the edit preview popup using st.popover
    
    Args:
        data_provider: The data provider instance
        customer: The selected customer name
    """
    # Check if preview data exists
    if not hasattr(st.session_state, 'preview_rule_data') or not st.session_state.preview_rule_data:
        return
    
    rule_data = st.session_state.preview_rule_data
    
    # Create a centered container for the popup
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Use st.popover for native Streamlit popup
        with st.popover("👁️ Preview Changes", help="Preview rule changes", use_container_width=True):
            st.markdown("## Rule Changes Preview")
            st.markdown("---")
            
            # If charge matches criteria section
            st.markdown("### If charge matches criteria...")
            
            # Provider
            st.markdown(f"**Provider:** {rule_data.get('provider', 'N/A')}")
            
            # Charge name with condition
            st.markdown(f"**Charge name:** {rule_data.get('charge_name_condition', 'N/A')} '{rule_data.get('charge_name', 'N/A')}'")
            
            # Advanced conditions
            if rule_data.get('advanced_enabled', False):
                st.markdown("**Advanced conditions enabled:**")
                if rule_data.get('account_number'):
                    st.markdown(f"  - Account number: {rule_data.get('account_condition', 'N/A')} '{rule_data.get('account_number', 'N/A')}'")
                if rule_data.get('usage_unit'):
                    st.markdown(f"  - Usage unit: {rule_data.get('usage_unit_condition', 'N/A')} '{rule_data.get('usage_unit', 'N/A')}'")
                if rule_data.get('service_type'):
                    st.markdown(f"  - Service type: {rule_data.get('service_type_condition', 'N/A')} '{rule_data.get('service_type', 'N/A')}'")
            else:
                st.markdown("**Advanced conditions:** Disabled")
            
            st.markdown("---")
            
            # Then apply these actions section
            st.markdown("**Then apply these actions...**")
            
            st.markdown(f"**Charge name mapping:** {rule_data.get('charge_name_mapping', 'N/A')}")
            st.markdown(f"**Charge category:** {rule_data.get('charge_category', 'N/A')}")
            st.markdown(f"**Charge group heading:** {rule_data.get('charge_group_heading', 'N/A')}")
            st.markdown(f"**Request type:** {rule_data.get('request_type', 'N/A')}")
            
            st.markdown("---")
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Back to Edit", key="edit_preview_back_to_edit"):
                    st.session_state.show_edit_preview_popup = False
                    st.rerun()
            with col2:
                if st.button("Update Rule", type="primary", key="edit_preview_update_rule"):
                    # Here you would typically update the rule in the database
                    st.success("Rule updated successfully!")
                    st.session_state.show_edit_preview_popup = False
                    st.rerun()

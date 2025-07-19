"""
Sidebar UI Component

This module contains the sidebar with customer selection and user information.
"""

import streamlit as st
from components.data.providers import DataProvider
from components.modals.create_rule_modal import create_rule_modal
from components.modals.edit_rule_modal import edit_rule_modal


def render_sidebar(data_provider: DataProvider) -> str:
    """
    Render the sidebar with customer selection and user info
    
    Args:
        data_provider: The data provider instance
    
    Returns:
        The selected customer name
    """
    
    with st.sidebar:
        # Check if create rule modal should be shown
        if st.session_state.get('show_create_rule_modal', False):
            # Render the create rule modal in sidebar
            customer = st.session_state.get('selected_customer', 'Default Customer')
            create_rule_modal(data_provider, customer, [])
            return customer
        # Check if edit rule modal should be shown
        elif st.session_state.get('show_edit_rule_modal', False):
            # Render the edit rule modal in sidebar
            customer = st.session_state.get('selected_customer', 'Default Customer')
            selected_rules = st.session_state.get('selected_rules_for_edit', [])
            edit_rule_modal(data_provider, customer, selected_rules)
            return customer
        else:
            # Render normal sidebar content
            st.markdown("### 🏢 Customer Selection")
            selected_customer = st.selectbox(
                "Select Customer",
                ["AmerescoFTP", "OtherCustomer", "NewCustomer", "TestCustomer"],
                index=0
            )
            
            # Status indicator
            if isinstance(data_provider, data_provider.__class__):  # Check if demo provider
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
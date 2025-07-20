"""
Main Sidebar Orchestrator

This module contains the main sidebar function that orchestrates all sidebar components.
"""

import streamlit as st
from components.data.providers import DataProvider
from .customer_sidebar import render_customer_sidebar
from .create_rule_form import render_create_rule_form
from .edit_rule_form import render_edit_rule_form


def render_main_sidebar(data_provider: DataProvider) -> str:
    """
    Main sidebar function that orchestrates all sidebar components
    
    Args:
        data_provider: The data provider instance
    
    Returns:
        The selected customer name
    """
    # Initialize session state for modal visibility
    if 'show_create_rule_modal' not in st.session_state:
        st.session_state.show_create_rule_modal = False
    
    with st.sidebar:
        # If create rule modal is active, show only the modal
        if st.session_state.show_create_rule_modal:
            render_create_rule_form(data_provider, "AmerescoFTP")  # Default customer when modal is active
            return "AmerescoFTP"
        else:
            # Show customer sidebar (default collapsed)
            customer = render_customer_sidebar(data_provider)
            return customer 
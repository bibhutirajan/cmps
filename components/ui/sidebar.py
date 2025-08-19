"""
Sidebar UI Components (Legacy)

This module has been modularized. Please use the new modular structure:
- components/ui/sidebar/customer_sidebar.py
- components/ui/sidebar/create_rule_form.py
- components/ui/sidebar/edit_rule_form.py
- components/ui/sidebar/main_sidebar.py

This file is kept for backward compatibility.
"""

import streamlit as st
from components.data.providers import DataProvider
from .sidebar.customer_sidebar import render_customer_sidebar
from .sidebar.main_sidebar import render_main_sidebar


# Legacy function for backward compatibility
def render_customer_sidebar(data_provider: DataProvider) -> str:
    """Legacy function - use components.ui.sidebar.customer_sidebar.render_customer_sidebar instead"""
    return render_customer_sidebar(data_provider)


# Legacy wrapper functions for backward compatibility
def render_create_rule_form(data_provider: DataProvider, customer: str):
    """Legacy function - use components.popups.create_rule_popup.create_rule_popup instead"""
    from components.popups.create_rule_popup import create_rule_popup
    return create_rule_popup(data_provider, customer)

def render_edit_rule_form(data_provider: DataProvider, customer: str):
    """Legacy function - use components.popups.edit_rule_popup.edit_rule_popup instead"""
    from components.popups.edit_rule_popup import edit_rule_popup
    rule_data = st.session_state.get('selected_rule_for_edit', {})
    return edit_rule_popup(data_provider, customer, rule_data)

def render_main_sidebar(data_provider: DataProvider) -> str:
    """Legacy function - use components.ui.sidebar.main_sidebar.render_main_sidebar instead"""
    return render_main_sidebar(data_provider) 
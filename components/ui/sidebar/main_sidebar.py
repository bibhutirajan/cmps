"""
Main Sidebar Orchestrator

This module contains the main sidebar function that orchestrates all sidebar components.
"""

import streamlit as st
from components.data.providers import DataProvider
from .app_sidebar import render_app_sidebar
from components.popups.create_rule_popup import create_rule_popup
from components.popups.edit_rule_popup import edit_rule_popup
from components.popups.preview_popup import preview_popup
from components.popups.edit_preview_popup import edit_preview_popup


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
        # If in edit preview mode, show edit preview popup
        if st.session_state.get('show_edit_preview', False):
            # Return default customer when in edit preview
            return "AmerescoFTP"
        # If in preview mode, show preview popup
        elif st.session_state.get('show_preview', False):
            # Return default customer when in preview
            return "AmerescoFTP"
        # If create rule modal is active, show create popup
        elif st.session_state.show_create_rule_modal:
            # Return default customer when modal is active
            return "AmerescoFTP"
        # If edit rule modal is active, show edit popup
        elif st.session_state.get('show_edit_rule_modal', False):
            # Return default customer when modal is active
            return "AmerescoFTP"
        else:
            # Show app sidebar (default collapsed)
            customer = render_app_sidebar(data_provider)
            return customer


def render_preview_navigation(data_provider: DataProvider):
    """
    Render preview navigation in sidebar (DEPRECATED - now using popup)
    
    Args:
        data_provider: The data provider instance
    """
    # This function is deprecated - preview is now handled by popup
    pass


def render_edit_preview_navigation(data_provider: DataProvider):
    """
    Render edit preview navigation in sidebar (DEPRECATED - now using popup)
    
    Args:
        data_provider: The data provider instance
    """
    # This function is deprecated - edit preview is now handled by popup
    pass 
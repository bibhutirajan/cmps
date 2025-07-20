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
        # If in edit preview mode, show edit preview navigation
        if st.session_state.get('show_edit_preview', False):
            render_edit_preview_navigation(data_provider)
            return "AmerescoFTP"  # Default customer when in edit preview
        # If in preview mode, show preview navigation
        elif st.session_state.get('show_preview', False):
            render_preview_navigation(data_provider)
            return "AmerescoFTP"  # Default customer when in preview
        # If create rule modal is active, show create form (override edit if active)
        elif st.session_state.show_create_rule_modal:
            # Check if we just switched from edit to create and show warning
            if st.session_state.get('_switched_from_edit_to_create', False):
                st.warning("⚠️ Edit rule form was closed to open create rule form.")
                # Clear the flag
                st.session_state._switched_from_edit_to_create = False
            render_create_rule_form(data_provider, "AmerescoFTP")  # Default customer when modal is active
            return "AmerescoFTP"
        # If edit rule modal is active, show only the edit form
        elif st.session_state.get('show_edit_rule_modal', False):
            # Check if we just switched from create to edit and show warning
            if st.session_state.get('_switched_from_create_to_edit', False):
                st.warning("⚠️ Create rule form was closed to open edit rule form.")
                # Clear the flag
                st.session_state._switched_from_create_to_edit = False
            rule_data = st.session_state.get('selected_rule_for_edit', {})
            render_edit_rule_form(data_provider, "AmerescoFTP", rule_data)
            return "AmerescoFTP"
        else:
            # Show customer sidebar (default collapsed)
            customer = render_customer_sidebar(data_provider)
            return customer


def render_preview_navigation(data_provider: DataProvider):
    """
    Render preview navigation in sidebar
    
    Args:
        data_provider: The data provider instance
    """
    st.markdown("## 🔍 Rule Preview")
    st.markdown("Review the changes before saving.")
    
    # Rule application settings
    st.markdown("### 📋 Application Settings")
    apply_to_existing = st.checkbox(
        "Apply rule to existing charges",
        value=True,
        key="apply_to_existing_preview",
        help="Apply this rule to existing charges that match the criteria"
    )
    
    st.markdown("---")
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back to Form", key="back_to_form_sidebar_btn", help="Return to edit the rule"):
            st.session_state.show_preview = False
            st.rerun()
    
    with col2:
        if st.button("💾 Save Rule", key="save_rule_sidebar_btn", type="primary", help="Save the rule and close form"):
            # Save the rule using the stored form data
            if data_provider.create_rule(st.session_state.rule_form_data):
                st.session_state.show_preview = False
                st.session_state.show_create_rule_modal = False
                st.success("✅ Rule saved successfully!")
                st.rerun()


def render_edit_preview_navigation(data_provider: DataProvider):
    """
    Render edit preview navigation in sidebar
    
    Args:
        data_provider: The data provider instance
    """
    st.markdown("## 🔍 Edit Rule Preview")
    st.markdown("Review the changes before saving.")
    
    # Rule application settings
    st.markdown("### 📋 Application Settings")
    apply_to_existing = st.checkbox(
        "Apply rule changes to existing charges",
        value=True,
        key="apply_edit_to_existing_preview",
        help="Apply these rule changes to existing charges that match the criteria"
    )
    
    st.markdown("---")
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back to Form", key="back_to_edit_form_sidebar_btn", help="Return to edit the rule"):
            st.session_state.show_edit_preview = False
            st.rerun()
    
    with col2:
        if st.button("💾 Save Changes", key="save_edit_rule_sidebar_btn", type="primary", help="Save the rule changes and close form"):
            # Save the rule changes using the stored form data
            original_rule = st.session_state.get('selected_rule_for_edit', {})
            rule_id = original_rule.get('Rule ID', 'unknown')
            if data_provider.update_rule(rule_id, st.session_state.edit_rule_form_data):
                st.session_state.show_edit_preview = False
                st.session_state.show_edit_rule_modal = False
                st.success("✅ Rule updated successfully!")
                st.rerun() 
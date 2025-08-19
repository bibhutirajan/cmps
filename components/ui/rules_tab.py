"""
Rules Tab UI Component

This module contains the UI for the Rules tab with filter bar and data table.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any
from components.data.providers import DataProvider
from components.modals.create_rule_modal import render_create_rule_button
from components.modals.edit_rule_modal import render_edit_rule_button
from components.modals.edit_priority_modal import render_edit_priority_button


def render_rules_tab(data_provider: DataProvider, customer: str):
    """
    Render the Rules tab
    
    Args:
        data_provider: The data provider instance
        customer: The selected customer
    """
    
    # Rules Header Section with inline Create rule button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("## Rules")
        st.markdown("Use rules to rename and reclassify charges. If multiple rules match a charge, they'll be applied in order from top to bottom.")
    with col2:
        st.markdown("")  # Add some spacing
        st.markdown("")  # Add more spacing to align with heading
        render_create_rule_button(data_provider, {"customer": customer}, "rules_header")
    
    # Get rules data
    rules_df = data_provider.get_rules(customer)
    
    # Initialize session state for selected rules
    if 'selected_rules' not in st.session_state:
        st.session_state.selected_rules = []
    
    # Filters Section - minimal approach
    with st.expander("### Filters", expanded=True):
        # Filter dropdowns - compact layout
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown("**Rule type**")
            st.selectbox(
                "Rule type",
                ["All", "Custom", "Global"],
                key="filter_rule_type",
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown("**Customer name**")
            st.selectbox(
                "Customer name",
                [customer],
                key="filter_customer_name",
                label_visibility="collapsed"
            )
        
        with col3:
            st.markdown("**Charge ID**")
            st.selectbox(
                "Charge ID",
                ["Placeholder", "NewBatch", "Other"],
                key="filter_charge_id",
                label_visibility="collapsed"
            )
        
        with col4:
            st.markdown("**Provider**")
            st.selectbox(
                "Provider",
                ["TBD", "Atmos", "Other"],
                key="filter_provider",
                label_visibility="collapsed"
            )
        
        with col5:
            st.markdown("**Charge name**")
            st.selectbox(
                "Charge name",
                ["(?i)Electric\\s*service.*", "CHP Rider", "Other"],
                key="filter_charge_name",
                label_visibility="collapsed"
            )
    
    # Custom Rules Section
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    with col1:
        st.markdown("### Custom")
        st.markdown("Rules specific to your organization. These override global rules and can be reordered or edited.")
    with col2:
        st.markdown("")  # Add spacing to align with heading
        render_edit_priority_button(data_provider, {"customer": customer}, "custom_rules")
    with col3:
        st.markdown("")  # Add spacing to align with heading
        render_edit_rule_button(data_provider, {"customer": customer}, "custom_rules")
    with col4:
        st.markdown("")  # Empty column to push buttons more to the right
    
    # Filter for custom rules (customer-specific)
    custom_rules_df = rules_df[rules_df['Customer name'] == customer].copy()
    
    # Convert Request type column to string and handle NULL values
    if 'Request type' in custom_rules_df.columns:
        custom_rules_df['Request type'] = custom_rules_df['Request type'].astype(str).fillna('')
    
    if not custom_rules_df.empty:
        # Initialize custom selection state
        if 'custom_selected_rules' not in st.session_state:
            st.session_state.custom_selected_rules = []
        
        # Display custom rules table
        edited_custom_df = st.data_editor(
            custom_rules_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rule ID": st.column_config.NumberColumn("Rule ID", width="small"),
                "Customer name": st.column_config.TextColumn("Customer name", width="medium", max_chars=15),
                "Priority order": st.column_config.NumberColumn("Priority order", width="small"),
                "Charge name mapping": st.column_config.TextColumn("Charge name mapping", width="medium", max_chars=25),
                "Charge ID": st.column_config.TextColumn("Charge ID", width="medium", max_chars=15),
                "Charge group heading": st.column_config.TextColumn("Charge group heading", width="medium", max_chars=20),
                "Charge category": st.column_config.TextColumn("Charge category", width="medium", max_chars=20),
                "Request type": st.column_config.TextColumn("Request type", width="medium", max_chars=15)
            },
            key="custom_rules_table"
        )
        
        # For now, no selection tracking without checkboxes
        st.session_state.custom_selected_rules = []
    else:
        st.info("No custom rules found for this customer.")
        st.session_state.custom_selected_rules = []
    
    # Global Rules Section
    st.markdown("### Global")
    st.markdown("Rules that apply to all customers. If no customer-specific rule overrides them.")
    
    # Filter for global rules (all customers)
    global_rules_df = rules_df.copy()
    
    # Convert Request type column to string and handle NULL values
    if 'Request type' in global_rules_df.columns:
        global_rules_df['Request type'] = global_rules_df['Request type'].astype(str).fillna('')
    
    if not global_rules_df.empty:
        # Initialize global selection state
        if 'global_selected_rules' not in st.session_state:
            st.session_state.global_selected_rules = []
        
        # Display global rules table
        edited_global_df = st.data_editor(
            global_rules_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rule ID": st.column_config.NumberColumn("Rule ID", width="small"),
                "Customer name": st.column_config.TextColumn("Customer name", width="medium", max_chars=15),
                "Priority order": st.column_config.NumberColumn("Priority order", width="small"),
                "Charge name mapping": st.column_config.TextColumn("Charge name mapping", width="medium", max_chars=25),
                "Charge ID": st.column_config.TextColumn("Charge ID", width="medium", max_chars=15),
                "Charge group heading": st.column_config.TextColumn("Charge group heading", width="medium", max_chars=20),
                "Charge category": st.column_config.TextColumn("Charge category", width="medium", max_chars=20),
                "Request type": st.column_config.TextColumn("Request type", width="medium", max_chars=15)
            },
            key="global_rules_table"
        )
        
        # For now, no selection tracking without checkboxes
        st.session_state.global_selected_rules = []
    else:
        st.info("No global rules found.")
        st.session_state.global_selected_rules = []
    
    # Combine custom and global selected rules
    custom_selected = st.session_state.get('custom_selected_rules', [])
    global_selected = st.session_state.get('global_selected_rules', [])
    all_selected_rules = custom_selected + global_selected
    st.session_state.selected_rules = all_selected_rules
    
    # Display selected count
    selected_count = len(all_selected_rules)
    if selected_count > 0:
        st.info(f"📋 {selected_count} rule(s) selected")


def get_selected_rules() -> list:
    """
    Get the currently selected rules from the data table
    
    Returns:
        List of selected rule dictionaries
    """
    return st.session_state.get('selected_rules', [])


def get_selected_rule_ids() -> list:
    """
    Get the IDs of currently selected rules
    
    Returns:
        List of selected rule IDs
    """
    selected_rules = get_selected_rules()
    return [rule.get('Rule ID') for rule in selected_rules if rule.get('Rule ID') is not None] 
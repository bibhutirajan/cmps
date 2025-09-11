"""
Rules Tab UI Component

This module contains the UI for the Rules tab with filter bar and data table.
"""

import streamlit as st
import pandas as pd
from components.data.data_providers import DataProvider


def render_rules_tab(data_provider: DataProvider, customer: str):
    """
    Render the Rules tab
    
    Args:
        data_provider: The data provider instance
        customer: The selected customer
    """
    
    # Clear dialog states that shouldn't persist when just viewing/selecting rows
    # Only keep create rule dialog state if it was explicitly triggered by button
    if not st.session_state.get('create_rule_triggered_by_btn', False):
        st.session_state.pop('show_create_rule_dialog_rules_header', None)
    
    # Clear edit priority dialog state if it wasn't explicitly triggered
    # This prevents accidental dialog opening from other interactions
    if not st.session_state.get('edit_priority_triggered_by_btn', False):
        st.session_state.pop('show_edit_priority_dialog', None)
    
    # Ensure we're not in a row selection state that could trigger dialogs
    # Reset any lingering dialog states that might have been set incorrectly
    if 'custom_rules_table' in st.session_state or 'global_rules_table' in st.session_state:
        # If we're just selecting rows, don't show create rule dialog
        if not st.session_state.get('create_rule_triggered_by_btn', False):
            st.session_state.pop('show_create_rule_dialog_rules_header', None)
        # Don't show edit priority dialog unless explicitly triggered
        if not st.session_state.get('edit_priority_triggered_by_btn', False):
            st.session_state.pop('show_edit_priority_dialog', None)
    
    # Map column names for the specific columns we want to display
    column_mappings = {
        "RULE_ID": ("RULE_ID", "Rule ID"),
        "CUSTOMER_NAME": ("CUSTOMER_NAME", "Customer Name"),
        "PRIORITY_ORDER": ("PRIORITY_ORDER", "Priority Order"),
        "CHARGE_NAME": ("CHARGE_NAME", "Charge Name"),
        "CHARGE_ID": ("CHARGE_ID", "Charge ID/Category"),
        "SERVICE_TYPE": ("SERVICE_TYPE", "Service Type"),
        "ACCOUNT_NUMBER": ("ACCOUNT_NUMBER", "Account Number"),
        "PROVIDER_NAME": ("PROVIDER_NAME", "Provider Name"),
        "CREATED_DATE": ("CREATED_DATE", "Created Date"),
        "MODIFIED_DATE": ("MODIFIED_DATE", "Modified Date"),
        "CREATED_BY": ("CREATED_BY", "Created By"),
        "MODIFIED_BY": ("MODIFIED_BY", "Modified By"),
        "CHARGE_MEASUREMENT": ("CHARGE_MEASUREMENT", "Charge Measurement"),
        "RULE_TYPE": ("RULE_TYPE", "Rule Type")
    }
    
    # Rules Header Section with inline Create rule button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("## Rules")
        st.markdown("Use rules to rename and reclassify charges. If multiple rules match a charge, they'll be applied in order from top to bottom.")
    with col2:
        st.markdown("")
        st.markdown("")
        # Direct Create Rule button
        if st.button("Create rule", key="create_rule_rules_header", type="primary"):
            st.session_state.show_create_rule_dialog_rules_header = True
            st.session_state.create_rule_triggered_by_btn = True
            st.rerun()
        
    
    # Get filter options for dynamic dropdowns
    filter_options = data_provider.get_filter_options(customer)
    
    # Get current filter values from session state
    current_filters = {
        'rule_type': st.session_state.get('filter_rule_type', 'All'),
        'charge_id': st.session_state.get('filter_charge_id', 'All Charge IDs'),
        'provider': st.session_state.get('filter_provider', 'All Providers'),
        'charge_name': st.session_state.get('filter_charge_name', 'All Charge Names')
    }
    
    # Get rules data with filters
    rules_df = data_provider.get_rules(customer, current_filters)
    
    # Handle data type issues for Streamlit compatibility
    if not rules_df.empty:
        for col in rules_df.columns:
            # Convert all columns to string to avoid type compatibility issues
            if col in ["RULE_ID", "PRIORITY_ORDER"]:
                # Convert numeric columns to string
                rules_df[col] = rules_df[col].astype(str)
            elif col in ["CREATED_DATE", "MODIFIED_DATE"]:
                # Convert datetime columns to string
                rules_df[col] = rules_df[col].astype(str)
            elif rules_df[col].dtype == 'object':
                # Fill NaN values for object columns
                rules_df[col] = rules_df[col].fillna('')
            else:
                # Convert all other columns to string
                rules_df[col] = rules_df[col].astype(str)
    
    # Initialize session state for selected rules
    if 'selected_rules' not in st.session_state:
        st.session_state.selected_rules = []
    
    # Filters Section - minimal approach
    with st.expander("### Filters", expanded=True):
        # Filter dropdowns - compact layout (removed Customer name dropdown)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("**Rule type**")
            st.selectbox(
                "Rule type",
                ["All", "Custom", "Global"],
                key="filter_rule_type",
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown("**Charge ID**")
            st.selectbox(
                "Charge ID",
                filter_options.get('charge_ids', ['All Charge IDs', 'NewBatch', 'Other']),
                key="filter_charge_id",
                label_visibility="collapsed"
            )
        
        with col3:
            st.markdown("**Provider**")
            st.selectbox(
                "Provider",
                filter_options.get('providers', ['All Providers', 'Atmos', 'Other']),
                key="filter_provider",
                label_visibility="collapsed"
            )
        
        with col4:
            st.markdown("**Charge name**")
            st.selectbox(
                "Charge name",
                filter_options.get('charge_names', ['All Charge Names', 'CHP Rider', 'Other']),
                key="filter_charge_name",
                label_visibility="collapsed"
            )
    
    # Filter for custom rules (customer-specific) - moved before UI elements
    if 'CUSTOMER_NAME' in rules_df.columns:
        # Filter for custom rules (RULE_TYPE = 'Custom')
        custom_rules_df = rules_df[rules_df['RULE_TYPE'] == 'Custom'].copy()
    else:
        # No customer column available
        custom_rules_df = pd.DataFrame()
    
    # Custom Rules Section
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    with col1:
        st.markdown("### Custom")
        st.markdown("Rules specific to your organization. These override global rules and can be reordered or edited.")
        with col2:
            st.markdown("")  # Add spacing to align with heading
            # Direct Edit Priority button - only show if there are custom rules
            if not custom_rules_df.empty:
                if st.button("Edit priority", key="edit_priority_custom_rules"):
                    st.session_state.show_edit_priority_dialog = True
                    st.session_state.edit_priority_triggered_by_btn = True
                    st.rerun()

    with col3:
        st.markdown("")  # Add spacing to align with heading
        # Edit Rule button - use existing button but with new dialog functionality
        if st.button("✏️ Edit rule", key="edit_rule_custom", type="secondary"):
            # Check if any rules are selected
            selected_rules = st.session_state.get('selected_rules', [])
            if selected_rules:
                # Use the first selected rule for editing
                st.session_state.selected_rule_for_edit = selected_rules[0]
                st.session_state.show_edit_rule_dialog = True
                st.rerun()
            else:
                st.warning("Please select a rule to edit")
        
    with col4:
        st.markdown("")  # Empty column to push buttons more to the right
    
    # No need to convert Request type column as it's not in our selected columns
    
    if not custom_rules_df.empty:
        # Initialize custom selection state
        if 'custom_selected_rules' not in st.session_state:
            st.session_state.custom_selected_rules = []
        
        # Create dynamic column configuration based on available columns
        column_config = {}
        
        # Build column configuration for available columns
        for col in custom_rules_df.columns:
            if col in column_mappings:
                remote_col, display_name = column_mappings[col]
                if col in ["RULE_ID", "PRIORITY_ORDER"]:
                    column_config[col] = st.column_config.NumberColumn(display_name, width="small")
                elif col in ["CREATED_DATE", "MODIFIED_DATE"]:
                    column_config[col] = st.column_config.TextColumn(display_name, width="medium")
                else:
                    column_config[col] = st.column_config.TextColumn(display_name, width="medium", max_chars=20)
            else:
                # Default configuration for unmapped columns
                column_config[col] = st.column_config.TextColumn(col, width="medium", max_chars=20)
        
        # Display custom rules table with selection capability
        selected_custom_rows = st.dataframe(
            custom_rules_df,
            use_container_width=True,
            hide_index=True,
            column_config=column_config,
            key="custom_rules_table",
            selection_mode="multi-row",
            on_select="rerun"
        )
        
        # Handle custom rules selection
        if selected_custom_rows.selection.rows:
            # Get selected custom rules
            selected_indices = selected_custom_rows.selection.rows
            selected_custom_rules = custom_rules_df.iloc[selected_indices].to_dict('records')
            
            # Store selected custom rules in session state
            st.session_state.custom_selected_rules = selected_custom_rules
            
            # Display selection info
            st.info(f"📋 {len(selected_custom_rules)} custom rule(s) selected for editing")
        else:
            # Clear selection if no rows selected
            st.session_state.custom_selected_rules = []
            st.info("💡 Select custom rules using the checkboxes to edit them")
        
    else:
        st.info("No custom rules found for this customer.")
        st.session_state.custom_selected_rules = []
    
    # Global Rules Section
    st.markdown("### Global")
    st.markdown("Rules that apply to all customers. If no customer-specific rule overrides them.")
    
    # Filter for global rules (RULE_TYPE = 'Global')
    if 'RULE_TYPE' in rules_df.columns:
        global_rules_df = rules_df[rules_df['RULE_TYPE'] == 'Global'].copy()
    else:
        # No RULE_TYPE column available
        global_rules_df = pd.DataFrame()
    
    if not global_rules_df.empty:
        # Initialize global selection state
        if 'global_selected_rules' not in st.session_state:
            st.session_state.global_selected_rules = []
        
        # Create dynamic column configuration for global rules
        global_column_config = {}
        
        # Build column configuration for available columns
        for col in global_rules_df.columns:
            if col in column_mappings:
                remote_col, display_name = column_mappings[col]
                if col in ["RULE_ID", "PRIORITY_ORDER"]:
                    global_column_config[col] = st.column_config.NumberColumn(display_name, width="small")
                elif col in ["CREATED_DATE", "MODIFIED_DATE"]:
                    global_column_config[col] = st.column_config.TextColumn(display_name, width="medium")
                else:
                    global_column_config[col] = st.column_config.TextColumn(display_name, width="medium", max_chars=20)
            else:
                # Default configuration for unmapped columns
                global_column_config[col] = st.column_config.TextColumn(col, width="medium", max_chars=20)
        
        # Display global rules table with selection capability
        selected_global_rows = st.dataframe(
            global_rules_df,
            use_container_width=True,
            hide_index=True,
            column_config=global_column_config,
            key="global_rules_table",
            selection_mode="multi-row",
            on_select="rerun"
        )
        
        # Handle global rules selection
        if selected_global_rows.selection.rows:
            # Get selected global rules
            selected_indices = selected_global_rows.selection.rows
            selected_global_rules = global_rules_df.iloc[selected_indices].to_dict('records')
            
            # Store selected global rules in session state
            st.session_state.global_selected_rules = selected_global_rules
            
            # Display selection info
            st.info(f"📋 {len(selected_global_rules)} global rule(s) selected for editing")
        else:
            # Clear selection if no rows selected
            st.session_state.global_selected_rules = []
            st.info("💡 Select global rules using the checkboxes to edit them")
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
    
    # All dialogs are now handled by centralized dialog manager in main.py


def transform_rule_data_for_edit(rule_data: dict) -> dict:
    """
    Transform rule data from database format to edit form format
    
    Args:
        rule_data: Rule data from database
        
    Returns:
        Transformed rule data for edit form
    """
    if not rule_data:
        return {}
    
    # Map database columns to form fields
    transformed = {
        "provider": rule_data.get("PROVIDER_ALIAS", "Atmos"),
        "charge_name": rule_data.get("CHARGE_NAME", "CHP rider"),
        "charge_name_condition": "Exactly matches",  # Default
        "advanced_enabled": True,  # Default
        "account_number": rule_data.get("ACCOUNT_NUMBER", "00000000"),
        "account_condition": "Exactly matches",  # Default
        "usage_unit": rule_data.get("USAGE_UNIT", "kWh"),
        "usage_unit_condition": "Exactly matches",  # Default
        "service_type": rule_data.get("SERVICE_TYPE", "Electric"),
        "service_type_condition": "Exactly matches",  # Default
        "tariff": rule_data.get("TARIFF", "Lorem ipsum"),
        "raw_charge_name": rule_data.get("RAW_CHARGE_NAME", "Lorem ipsum"),
        "raw_charge_condition": "Exactly matches",  # Default
        "legacy_description": rule_data.get("LEGACY_DESCRIPTION", "Add a description that explain why they are seeing this"),
        "meter_number": rule_data.get("METER_NUMBER", ""),
        "measurement_type": rule_data.get("MEASUREMENT_TYPE", ""),
        "charge_id": rule_data.get("CHARGE_ID", "NewBatch")
    }
    
    return transformed


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
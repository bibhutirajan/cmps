"""
Edit Rule Modal Component

This module provides the modal interface for editing existing charge mapping rules.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional, List
from components.data.providers import DataProvider


def edit_rule_modal(data_provider: DataProvider, customer: str, selected_rules: list) -> Optional[Dict[str, Any]]:
    """
    Render the edit rule modal in the sidebar
    
    Args:
        data_provider: The data provider instance
        customer: The customer name
        selected_rules: List of selected rules to edit
    
    Returns:
        None (modal is rendered in sidebar)
    """
    
    if not selected_rules:
        st.warning("No rules selected for editing")
        return None
    
    # Use the first selected rule for editing
    rule_data = selected_rules[0] if selected_rules else {}
    
    # Initialize form data in session state if not exists
    if 'edit_rule_form_data' not in st.session_state:
        st.session_state.edit_rule_form_data = {
            'provider': rule_data.get('provider', 'Atmos'),
            'charge_name_match': rule_data.get('charge_name_match', 'Exactly matches'),
            'charge_name_value': rule_data.get('charge_name_value', 'CHP rider'),
            'account_number_match': rule_data.get('account_number_match', 'Exactly matches'),
            'account_number_value': rule_data.get('account_number_value', '00000000'),
            'usage_unit': rule_data.get('usage_unit', 'kWh'),
            'service_type': rule_data.get('service_type', 'Electric'),
            'tariff': rule_data.get('tariff', 'Lorem ipsum'),
            'raw_charge_name_match': rule_data.get('raw_charge_name_match', 'Exactly matches'),
            'raw_charge_name_value': rule_data.get('raw_charge_name_value', 'Lorem ipsum'),
            'charge_id': rule_data.get('charge_id', 'NewBatch'),
            'active': rule_data.get('active', True),
            'meter_number': rule_data.get('meter_number', ''),
            'measurement_type': rule_data.get('measurement_type', ''),
            'description': rule_data.get('description', ''),
            'advanced_conditions': rule_data.get('advanced_conditions', True)
        }
    
    # Apply custom CSS for modal styling
    st.markdown("""
    <style>
    /* Modal styling */
    .edit-modal-container {
        background: white;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
    }
    
    /* User avatar styling */
    .user-avatar {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #e0e0e0;
        display: inline-block;
        margin-left: 8px;
        vertical-align: middle;
    }
    
    /* Section headers */
    .section-header {
        font-weight: bold;
        color: #333;
        margin-bottom: 15px;
    }
    
    /* Field labels */
    .field-label {
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
    }
    
    /* Button styling */
    .modal-button {
        border-radius: 4px;
        padding: 8px 16px;
        font-size: 14px;
        border: none;
        cursor: pointer;
    }
    
    .modal-button-secondary {
        background: white;
        color: #666;
        border: 1px solid #ddd;
    }
    
    .modal-button-primary {
        background: #0068c9;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Modal header
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Edit rule")
    with col2:
        if st.button("✕", key="edit_close_modal_x_unique", help="Close modal"):
            st.session_state.show_edit_rule_modal = False
            st.rerun()
    
    st.divider()
    
    # Check if preview mode is active
    if st.session_state.get('show_edit_preview', False):
        # Preview mode - show controls in sidebar
        st.markdown("**Preview Mode**")
        st.markdown("Review the changes in the main area below.")
        
        # Action buttons for preview mode
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back to form", key="edit_preview_back_btn_unique"):
                st.session_state.show_edit_preview = False
                st.rerun()
        with col2:
            if st.button("Save changes", type="primary", key="save_edit_rule_btn_unique"):
                # Save the rule to Snowflake
                success = save_edited_rule_to_snowflake(st.session_state.edit_rule_form_data, rule_data)
                if success:
                    st.success("Rule updated successfully!")
                    st.session_state.show_edit_rule_modal = False
                    st.session_state.show_edit_preview = False
                    st.rerun()
                else:
                    st.error("Failed to update rule. Please try again.")
    else:
        # Form mode - Two column layout matching Figma design
        col1, col2 = st.columns([3, 1])  # 3:1 ratio for left:right sections
        
        with col1:
            # Left section: "If charge matches criteria..."
            st.markdown("**If charge matches criteria...**")
            
            # Provider
            provider_options = ["Atmos", "Other"]
            provider_index = 0
            if st.session_state.edit_rule_form_data['provider'] in provider_options:
                provider_index = provider_options.index(st.session_state.edit_rule_form_data['provider'])
            
            st.session_state.edit_rule_form_data['provider'] = st.selectbox(
                "Provider",
                options=provider_options,
                index=provider_index,
                key="edit_modal_provider_unique"
            )
            
            # Charge name
            col1, col2 = st.columns([1, 2])
            with col1:
                match_options = ["Exactly matches", "Contains", "Starts with", "Ends with"]
                match_index = 0
                if st.session_state.edit_rule_form_data['charge_name_match'] in match_options:
                    match_index = match_options.index(st.session_state.edit_rule_form_data['charge_name_match'])
                
                st.session_state.edit_rule_form_data['charge_name_match'] = st.selectbox(
                    "Charge name",
                    options=match_options,
                    index=match_index,
                    key="edit_modal_charge_name_match_unique"
                )
            with col2:
                st.session_state.edit_rule_form_data['charge_name_value'] = st.text_input(
                    "Value",
                    value=st.session_state.edit_rule_form_data['charge_name_value'],
                    key="edit_modal_charge_name_value_unique"
                )
            
            # Advanced conditions toggle
            st.session_state.edit_rule_form_data['advanced_conditions'] = st.toggle(
                "Advanced conditions",
                value=st.session_state.edit_rule_form_data.get('advanced_conditions', True),
                key="edit_modal_advanced_conditions_unique"
            )
            
            # Account number
            col1, col2 = st.columns([1, 2])
            with col1:
                account_match_index = 0
                if st.session_state.edit_rule_form_data['account_number_match'] in match_options:
                    account_match_index = match_options.index(st.session_state.edit_rule_form_data['account_number_match'])
                
                st.session_state.edit_rule_form_data['account_number_match'] = st.selectbox(
                    "Account number",
                    options=match_options,
                    index=account_match_index,
                    key="edit_modal_account_number_match_unique"
                )
            with col2:
                st.session_state.edit_rule_form_data['account_number_value'] = st.text_input(
                    "Value",
                    value=st.session_state.edit_rule_form_data['account_number_value'],
                    key="edit_modal_account_number_value_unique"
                )
            
            # Usage unit
            usage_options = ["kWh", "kW", "None"]
            usage_index = 0
            if st.session_state.edit_rule_form_data['usage_unit'] in usage_options:
                usage_index = usage_options.index(st.session_state.edit_rule_form_data['usage_unit'])
            
            st.session_state.edit_rule_form_data['usage_unit'] = st.selectbox(
                "Usage unit",
                options=usage_options,
                index=usage_index,
                key="edit_modal_usage_unit_unique"
            )
            
            # Service type
            service_options = ["Electric", "Gas", "Water", "None"]
            service_index = 0
            if st.session_state.edit_rule_form_data['service_type'] in service_options:
                service_index = service_options.index(st.session_state.edit_rule_form_data['service_type'])
            
            st.session_state.edit_rule_form_data['service_type'] = st.selectbox(
                "Service type",
                options=service_options,
                index=service_index,
                key="edit_modal_service_type_unique"
            )
            
            # Tariff
            st.session_state.edit_rule_form_data['tariff'] = st.text_input(
                "Tariff",
                value=st.session_state.edit_rule_form_data['tariff'],
                key="edit_modal_tariff_unique"
            )
            
            # Raw charge name
            col1, col2 = st.columns([1, 2])
            with col1:
                raw_match_index = 0
                if st.session_state.edit_rule_form_data['raw_charge_name_match'] in match_options:
                    raw_match_index = match_options.index(st.session_state.edit_rule_form_data['raw_charge_name_match'])
                
                st.session_state.edit_rule_form_data['raw_charge_name_match'] = st.selectbox(
                    "Raw charge name",
                    options=match_options,
                    index=raw_match_index,
                    key="edit_modal_raw_charge_name_match_unique"
                )
            with col2:
                st.session_state.edit_rule_form_data['raw_charge_name_value'] = st.text_input(
                    "Value",
                    value=st.session_state.edit_rule_form_data['raw_charge_name_value'],
                    key="edit_modal_raw_charge_name_value_unique"
                )
            
            # Legacy rule values section
            st.markdown("**Legacy rule values**")
            st.markdown("Add a description that explains why they are seeing this")
            
            # Description text area with user avatar
            col1, col2 = st.columns([1, 0.1])
            with col1:
                st.session_state.edit_rule_form_data['description'] = st.text_area(
                    "Description",
                    value=st.session_state.edit_rule_form_data['description'],
                    key="edit_modal_description_unique"
                )
            with col2:
                st.markdown('<div class="user-avatar"></div>', unsafe_allow_html=True)
            
            # Meter number and measurement type
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.edit_rule_form_data['meter_number'] = st.text_input(
                    "Meter number:",
                    value=st.session_state.edit_rule_form_data['meter_number'],
                    key="edit_modal_meter_number_unique"
                )
            with col2:
                st.session_state.edit_rule_form_data['measurement_type'] = st.text_input(
                    "Measurement type:",
                    value=st.session_state.edit_rule_form_data['measurement_type'],
                    key="edit_modal_measurement_type_unique"
                )
        
        with col2:
            # Right section: "Then categorize the charge as..."
            st.markdown("**Then categorize the charge as...**")
            
            # Charge ID with user avatar
            charge_id_options = ["NewBatch", "Existing Batch", "Other"]
            charge_id_index = 0
            if st.session_state.edit_rule_form_data['charge_id'] in charge_id_options:
                charge_id_index = charge_id_options.index(st.session_state.edit_rule_form_data['charge_id'])
            
            st.session_state.edit_rule_form_data['charge_id'] = st.selectbox(
                "Charge ID",
                options=charge_id_options,
                index=charge_id_index,
                key="edit_modal_charge_id_unique"
            )
            
            # User avatar below Charge ID
            st.markdown('<div class="user-avatar"></div>', unsafe_allow_html=True)
        
        # Footer buttons
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Cancel", key="edit_cancel_btn_unique", type="secondary"):
                st.session_state.show_edit_rule_modal = False
                st.session_state.show_edit_preview = False
                st.rerun()
        with col2:
            if st.button("Preview changes", key="edit_preview_btn_unique", type="primary"):
                st.session_state.show_edit_preview = True
                st.rerun()
    
    return None


def generate_edit_preview_data(rule_data: Dict[str, Any], original_rule: Dict[str, Any]) -> pd.DataFrame:
    """
    Generate preview data showing how the rule changes will affect existing charges
    
    Args:
        rule_data: The updated rule configuration data
        original_rule: The original rule data
    
    Returns:
        DataFrame with preview data
    """
    # This is sample data - in a real implementation, you would query your database
    # to find charges that match the rule criteria
    sample_data = [
        {
            "Charge name": rule_data.get('charge_name_value', original_rule.get('Charge name mapping', 'CHP Rider')),
            "Provider name": rule_data.get('provider', original_rule.get('Provider name', 'Atmos')),
            "Account number": rule_data.get('account_number_value', original_rule.get('Account number', '3018639036')),
            "Statement ID": "1efe9dd1-6cad-d3c...",
            "Current Charge ID": original_rule.get('Charge ID', 'Uncategorized'),
            "New Charge ID": rule_data.get('charge_id', 'NewBatch'),
            "Usage unit": rule_data.get('usage_unit', original_rule.get('Usage unit', 'kW')),
            "Service": rule_data.get('service_type', original_rule.get('Service', 'None'))
        }
    ]
    
    # Generate multiple rows for demonstration
    preview_data = []
    for i in range(8):  # 8 rows for edit preview
        row = sample_data[0].copy()
        if i >= 6:  # Last 2 rows have different current charge ID
            row["Current Charge ID"] = "eh.special_regulatory_charges"
        if i > 0:  # All rows except first have different usage unit
            row["Usage unit"] = "None"
        preview_data.append(row)
    
    return pd.DataFrame(preview_data)


def save_edited_rule_to_snowflake(rule_data: Dict[str, Any], original_rule: Dict[str, Any]) -> bool:
    """
    Save the edited rule to Snowflake database
    
    Args:
        rule_data: The updated rule configuration data
        original_rule: The original rule data
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Here you would implement the actual Snowflake database update
        # For now, we'll simulate a successful update
        
        # Example SQL (you would need to adapt this to your actual schema):
        # UPDATE charge_mapping_rules SET
        #     provider = ?, charge_name_match = ?, charge_name_value = ?,
        #     account_number_match = ?, account_number_value = ?, usage_unit = ?,
        #     service_type = ?, tariff = ?, raw_charge_name_match = ?, 
        #     raw_charge_name_value = ?, charge_id = ?, active = ?, 
        #     meter_number = ?, measurement_type = ?, description = ?,
        #     updated_at = NOW()
        # WHERE rule_id = ?
        
        # For demonstration, we'll just return True
        # In a real implementation, you would:
        # 1. Connect to Snowflake
        # 2. Execute the UPDATE statement
        # 3. Update the affected charges with the new charge_id
        # 4. Handle any errors and return appropriate status
        
        st.info(f"Rule would be updated in Snowflake with changes to {original_rule.get('Rule ID', 'unknown')} rule")
        return True
        
    except Exception as e:
        st.error(f"Error updating rule: {str(e)}")
        return False


def render_edit_rule_button(data_provider: DataProvider, context: Dict[str, Any] = None, unique_key: str = ""):
    """
    Render the Edit Rule button that opens the modal
    
    Args:
        data_provider: The data provider instance
        context: Context dictionary containing customer and selected data
        unique_key: Unique identifier for this button instance
    """
    
    # Get customer from context or session state
    if isinstance(context, dict):
        customer = context.get('customer', st.session_state.get('selected_customer', 'Default Customer'))
        selected_rules = context.get('selected_rules', [])
    else:
        customer = st.session_state.get('selected_customer', 'Default Customer')
        selected_rules = []
    
    # Get selected rules from session state if not provided
    if not selected_rules:
        selected_rules = st.session_state.get('selected_rules', [])
    
    # Get immediate selection state from both custom and global tables
    custom_selected = st.session_state.get('custom_selected_rules', [])
    global_selected = st.session_state.get('global_selected_rules', [])
    immediate_selected = custom_selected + global_selected
    
    # Use immediate selection if available, otherwise fall back to session state
    if immediate_selected:
        selected_rules = immediate_selected
    
    # Determine button state
    is_disabled = len(selected_rules) == 0
    button_text = "Edit rule"
    
    if len(selected_rules) == 1:
        button_text = f"Edit rule (1 rule)"
    elif len(selected_rules) > 1:
        button_text = f"Edit rule ({len(selected_rules)} rules)"
    
    # Create unique button key
    button_key = f"edit_rule_btn_{unique_key}" if unique_key else "edit_rule_btn"
    
    # Check if button is clicked
    if st.button(button_text, key=button_key, type="secondary", use_container_width=False):
        if len(selected_rules) == 0:
            st.warning("Please select at least one rule to edit")
            return
        
        # Check if create rule modal was active and set flag for warning
        if st.session_state.get('show_create_rule_modal', False):
            # Clear create rule session state
            st.session_state.show_create_rule_modal = False
            st.session_state.show_preview = False
            st.session_state.rule_form_data = None
            # Set flag to show warning in sidebar
            st.session_state._switched_from_create_to_edit = True
        
        # Store customer and selected rule data in session state for sidebar form
        st.session_state.selected_customer = customer
        st.session_state.selected_rule_for_edit = selected_rules[0]  # Use first selected rule
        # Show sidebar form
        st.session_state.show_edit_rule_modal = True
        st.rerun() 
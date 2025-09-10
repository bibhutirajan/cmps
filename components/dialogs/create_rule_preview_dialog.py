"""
Create Rule Preview Dialog Component

This module contains the create rule preview dialog using Streamlit's native st.dialog.
"""

import streamlit as st
from components.data.data_providers import DataProvider


@st.dialog("🔍 Preview Rule", width="medium")
def create_rule_preview_dialog(data_provider: DataProvider, customer: str, rule_data: dict, dialog_state_key: str = "show_create_rule_preview"):
    """
    Render the create rule preview dialog using st.dialog
    
    Args:
        data_provider: The data provider instance
        customer: The selected customer name
        rule_data: The rule data to preview
        dialog_state_key: The session state key to control dialog visibility
    """
    # Hide the default close button and add custom close button
    st.html(
        '''
            <style>
                div[aria-label="dialog"]>button[aria-label="Close"] {
                    display: none;
                }
            </style>
        '''
    )
    
    # Custom close button positioned in top-right corner
    col1, col2 = st.columns([1, 0.1])
    with col2:
        if st.button("", type="secondary", icon=":material/close:", key="preview_dialog_close_btn"):
            st.session_state.pop(dialog_state_key, None)
            st.rerun()
    
    st.markdown("## Rule Summary")
    
    # Create rule summary table
    import pandas as pd
    
    summary_data = {
        "Rule ID": ["New Rule"],
        "Customer name": [rule_data.get('customer', 'N/A')],
        "Priority order": [rule_data.get('priority_order', 'N/A')],
        "Charge name mapping": [f"{rule_data.get('charge_name_condition', 'N/A')} '{rule_data.get('charge_name', 'N/A')}'"],
        "Charge ID": ["NewCharge"],
        "Charge group heading": [rule_data.get('charge_group_heading', 'N/A')],
        "Charge category": [rule_data.get('charge_category', 'N/A')]
    }
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Affected charges section
    st.markdown("These changes will affect all charges matching the criteria below. Review the changes before saving.")
    
    # Sample affected charges table
    import pandas as pd
    
    sample_charges = pd.DataFrame({
        "Charge name": ["Sample Charge 1", "Sample Charge 2", "Sample Charge 3"],
        "Provider name": [rule_data.get('provider', 'N/A')] * 3,
        "Account number": [rule_data.get('account_number', 'N/A')] * 3,
        "Statement ID": ["sample-1", "sample-2", "sample-3"],
        "Current Charge ID": ["Uncategorized →"] * 3,
        "New Charge ID": ["NewCharge"] * 3,
        "Usage unit": ["kW", "kWh", "kW"],
        "Service": ["Electric", "Electric", "Electric"]
    })
    
    st.dataframe(sample_charges, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Apply to existing charges checkbox
    apply_to_existing = st.checkbox("Apply rule to 3 existing charge(s)", value=True, key="preview_apply_to_existing")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Cancel", key="create_preview_cancel"):
            st.session_state.pop(dialog_state_key, None)
            st.session_state.pop('create_rule_form_data', None)
            st.session_state.pop('create_rule_original_key', None)
            st.session_state.pop('create_rule_triggered_by_btn', None)
            st.rerun()
    
    with col2:
        if st.button("✏️ Back to Edit", key="create_preview_back"):
            # Close preview dialog and return to create rule dialog
            st.session_state.pop(dialog_state_key, None)
            # Restore the create rule dialog using the original dialog key
            original_dialog_key = st.session_state.get('create_rule_original_key', 'show_create_rule_dialog')
            st.session_state[original_dialog_key] = True
            # Set the trigger flag to allow the dialog to open
            st.session_state.create_rule_triggered_by_btn = True
            st.rerun()
    
    with col3:
        if st.button("Save", key="create_preview_save", type="primary"):
            # Save the rule to the database
            if data_provider.create_rule(rule_data):
                st.session_state.pop(dialog_state_key, None)
                # Clear the original dialog key and form data
                original_dialog_key = st.session_state.get('create_rule_original_key', 'show_create_rule_dialog')
                st.session_state.pop(original_dialog_key, None)
                st.session_state.pop('create_rule_form_data', None)
                st.session_state.pop('create_rule_original_key', None)
                st.session_state.pop('create_rule_triggered_by_btn', None)
                st.rerun()
            else:
                st.error("Failed to create rule. Please try again.")

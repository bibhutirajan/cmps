"""
Edit Rule Preview Dialog Component

This module contains the edit rule preview dialog using Streamlit's native st.dialog.
"""

import streamlit as st
from components.data.data_providers import DataProvider


@st.dialog("🔍 Preview Changes", width="medium")
def edit_rule_preview_dialog(data_provider: DataProvider, customer: str, rule_data: dict, dialog_state_key: str = "show_edit_rule_preview"):
    """
    Render the edit rule preview dialog using st.dialog
    
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
        if st.button("", type="secondary", icon=":material/close:", key="edit_preview_close"):
            st.session_state.pop(dialog_state_key, None)
            st.rerun()
    
    st.markdown("## Rule Summary")
    
    # Create rule summary table
    import pandas as pd
    
    original_rule = rule_data.get('original_rule', {})
    summary_data = {
        "Rule ID": [original_rule.get('CHIPS_BUSINESS_RULE_ID', 'N/A')],
        "Customer name": [rule_data.get('customer', 'N/A')],
        "Priority order": [rule_data.get('priority_order', original_rule.get('Priority order', 'N/A'))],
        "Charge name mapping": [f"{rule_data.get('charge_name_condition', 'N/A')} '{rule_data.get('charge_name', 'N/A')}'"],
        "Charge ID": [rule_data.get('charge_id', 'N/A')],
        "Charge group heading": [rule_data.get('charge_group_heading', original_rule.get('Charge group heading', 'N/A'))],
        "Charge category": [rule_data.get('charge_category', original_rule.get('Charge category', 'N/A'))]
    }
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Affected charges section
    st.markdown("These changes will affect all the charges listed below. Review the changes before saving.")
    
    # Sample affected charges table
    import pandas as pd
    
    sample_charges = pd.DataFrame({
        "Charge name": ["CHP Rider"] * 12,
        "Provider name": ["Atmos"] * 12,
        "Account number": ["3018639036"] * 12,
        "Statement ID": [f"1efe9dd1-6cad-d3c-{i:03d}" for i in range(1, 13)],
        "Current Charge ID": ["Uncategorized →"] * 9 + ["eh.special_regulatory_charges →"] * 3,
        "New Charge ID": ["NewBatch"] * 12,
        "Usage unit": ["kW"] + ["None"] * 11,
        "Service": ["None"] * 12
    })
    
    st.dataframe(sample_charges, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Apply to existing charges checkbox
    apply_to_existing = st.checkbox("Apply rule to 12 existing charge(s)", value=True, key="edit_preview_apply_to_existing")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Cancel", key="edit_preview_cancel"):
            st.session_state.pop(dialog_state_key, None)
            st.rerun()
    
    with col2:
        if st.button("✏️ Back to Edit", key="edit_preview_back"):
            # Close preview dialog and return to edit rule dialog
            st.session_state.pop(dialog_state_key, None)
            # Restore the edit rule dialog
            st.session_state.show_edit_rule_dialog = True
            st.rerun()
    
    with col3:
        if st.button("Save", key="edit_preview_save", type="primary"):
            # Get the rule ID from session state
            rule_id = st.session_state.get('selected_rule_for_edit', {}).get('CHIPS_BUSINESS_RULE_ID', '')
            
            # Update the rule in the database
            if data_provider.update_rule(rule_id, rule_data):
                st.session_state.pop(dialog_state_key, None)
                st.session_state.pop("show_edit_rule_dialog", None)
                st.rerun()
            else:
                st.error("Failed to update rule. Please try again.")

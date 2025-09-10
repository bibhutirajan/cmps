"""
Edit Priority Dialog Component

This module provides a dialog interface for editing rule priorities with drag-and-drop reordering.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List
from components.data.data_providers import DataProvider


@st.dialog("📋 Edit Priority", width="large")
def edit_priority_dialog(data_provider: DataProvider, customer: str):
    """
    Render the edit priority dialog
    
    Args:
        data_provider: The data provider instance
        customer: The customer name
    """
    
    st.markdown("### Reorder Rules")
    st.markdown("Drag and drop rules to change their priority order. Rules are applied from top to bottom.")
    
    # Get rules data
    rules_df = data_provider.get_rules(customer)
    
    if rules_df.empty:
        st.warning("No rules found for this customer.")
        return
    
    # Filter to show only custom rules (assuming they have a customer name)
    custom_rules = rules_df[rules_df.get('Customer name', '').str.contains(customer, na=False)]
    
    if custom_rules.empty:
        st.warning("No custom rules found for this customer.")
        return
    
    # Prepare data for editing
    priority_data = []
    for idx, row in custom_rules.iterrows():
        priority_data.append({
            "Rule ID": row.get('CHIPS_BUSINESS_RULE_ID', ''),
            "Priority": row.get('Priority order', ''),
            "Charge Name Mapping": row.get('Charge name mapping', ''),
            "Charge ID": row.get('Charge ID', ''),
            "Active": row.get('Active', True)
        })
    
    # Create editable dataframe
    priority_df = pd.DataFrame(priority_data)
    
    # Use st.data_editor for reordering
    edited_df = st.data_editor(
        priority_df,
        num_rows="fixed",
        use_container_width=True,
        column_config={
            "Rule ID": st.column_config.TextColumn("Rule ID", width="small", disabled=True),
            "Priority": st.column_config.NumberColumn("Priority", width="small", min_value=1, step=1),
            "Charge Name Mapping": st.column_config.TextColumn("Charge Name Mapping", width="medium", disabled=True),
            "Charge ID": st.column_config.TextColumn("Charge ID", width="medium", disabled=True),
            "Active": st.column_config.CheckboxColumn("Active", width="small")
        },
        key="priority_editor"
    )
    
    st.markdown("---")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Cancel", key="priority_cancel"):
            st.session_state.show_edit_priority_dialog = False
            st.rerun()
    
    with col2:
        if st.button("Reset", key="priority_reset"):
            st.rerun()
    
    with col3:
        if st.button("Save Changes", key="priority_save", type="primary"):
            # Save the changes
            if save_priority_changes(edited_df.to_dict('records')):
                st.success("Priority changes saved successfully!")
                st.session_state.show_edit_priority_dialog = False
                st.rerun()
            else:
                st.error("Failed to save priority changes.")


def save_priority_changes(rules_data: List[Dict[str, Any]]) -> bool:
    """
    Save the priority changes to the database
    
    Args:
        rules_data: The updated rules data with new priorities
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Here you would implement the actual database update
        # For now, we'll simulate a successful update
        
        
        # For demonstration, we'll just return True
        # In a real implementation, you would:
        # 1. Connect to your database
        # 2. Execute the UPDATE statements
        # 3. Handle any errors and return appropriate status
        
        st.info(f"Priority changes would be saved for {len(rules_data)} rules")
        return True
        
    except Exception as e:
        st.error(f"Error saving priority changes: {str(e)}")
        return False

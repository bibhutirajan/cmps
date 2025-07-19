"""
Edit Priority Modal Component

This module provides the modal interface for editing rule priorities with drag-and-drop reordering.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional, List
from components.data.providers import DataProvider


def edit_priority_modal(data_provider: DataProvider, customer: str) -> Optional[Dict[str, Any]]:
    """
    Render the edit priority modal as a floating overlay
    
    Args:
        data_provider: The data provider instance
        customer: The customer name
    
    Returns:
        None (modal is rendered as overlay)
    """
    
    # Apply custom CSS for floating modal
    st.markdown("""
    <style>
    /* Floating modal overlay */
    .edit-priority-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 1000;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .edit-priority-modal {
        background: white;
        border-radius: 8px;
        padding: 24px;
        max-width: 90%;
        max-height: 90%;
        overflow-y: auto;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Drag handle styling */
    .drag-handle {
        cursor: grab;
        color: #666;
        font-size: 16px;
        text-align: center;
        user-select: none;
    }
    
    .drag-handle:hover {
        color: #333;
    }
    
    /* Table styling */
    .priority-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 16px;
    }
    
    .priority-table th {
        background: #f5f5f5;
        padding: 12px 8px;
        text-align: left;
        font-weight: bold;
        border-bottom: 1px solid #ddd;
    }
    
    .priority-table td {
        padding: 12px 8px;
        border-bottom: 1px solid #eee;
    }
    
    .priority-table tr:hover {
        background: #f9f9f9;
    }
    
    /* Button styling */
    .modal-button {
        border-radius: 4px;
        padding: 8px 16px;
        font-size: 14px;
        border: none;
        cursor: pointer;
        margin-left: 8px;
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
    
    /* Reorder buttons styling */
    .reorder-btn {
        padding: 2px 6px;
        margin: 0 2px;
        font-size: 12px;
        border-radius: 3px;
        border: 1px solid #ddd;
        background: #f8f9fa;
        cursor: pointer;
    }
    
    .reorder-btn:hover {
        background: #e9ecef;
    }
    
    .reorder-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if modal should be shown
    if not st.session_state.get('show_edit_priority_modal', False):
        return None
    
    # Initialize priority data if not exists
    if 'priority_rules_data' not in st.session_state:
        st.session_state.priority_rules_data = generate_priority_rules_data(customer)
    
    # Modal header
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Edit priority")
    with col2:
        if st.button("✕", key="priority_close_modal_x_unique", help="Close modal"):
            st.session_state.show_edit_priority_modal = False
            st.rerun()
    
    # Instructional text
    st.markdown("Reorder the rules and click Check for conflicts to ensure priority changes won't override existing rules.")
    
    # Rules table with reorder functionality
    display_priority_table_with_reorder(st.session_state.priority_rules_data)
    
    # Footer buttons
    st.divider()
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Cancel", key="priority_cancel_btn_unique", type="secondary"):
            st.session_state.show_edit_priority_modal = False
            st.rerun()
    with col2:
        if st.button("Preview changes", key="priority_preview_btn_unique", type="primary"):
            st.session_state.show_priority_preview = True
            st.rerun()
    
    return None


def generate_priority_rules_data(customer: str) -> List[Dict[str, Any]]:
    """
    Generate sample priority rules data
    
    Args:
        customer: The customer name
    
    Returns:
        List of rule data dictionaries
    """
    return [
        {
            "rule_id": "8912000",
            "customer_name": customer,
            "priority_order": "3101",
            "charge_name_mapping": "(?i)Electric\\s*servic...",
            "charge_id": "Placeholder",
            "charge_group_heading": "Usage Charges",
            "charge_category": "ch.usage_cha"
        },
        {
            "rule_id": "8912003",
            "customer_name": customer,
            "priority_order": "3100",
            "charge_name_mapping": "(?i)Electric\\s*servic...",
            "charge_id": "Placeholder",
            "charge_group_heading": "Usage Charges",
            "charge_category": "ch.usage_cha"
        },
        {
            "rule_id": "8912004",
            "customer_name": customer,
            "priority_order": "3099",
            "charge_name_mapping": "(?i)Electric\\s*servic...",
            "charge_id": "Placeholder",
            "charge_group_heading": "Usage Charges",
            "charge_category": "ch.usage_cha"
        },
        {
            "rule_id": "8912005",
            "customer_name": customer,
            "priority_order": "3098",
            "charge_name_mapping": "(?i)Electric\\s*servic...",
            "charge_id": "Placeholder",
            "charge_group_heading": "Usage Charges",
            "charge_category": "ch.usage_cha"
        },
        {
            "rule_id": "8912006",
            "customer_name": customer,
            "priority_order": "3097",
            "charge_name_mapping": "(?i)Electric\\s*servic...",
            "charge_id": "Placeholder",
            "charge_group_heading": "Usage Charges",
            "charge_category": "ch.usage_cha"
        },
        {
            "rule_id": "8912007",
            "customer_name": customer,
            "priority_order": "3096",
            "charge_name_mapping": "(?i)Electric\\s*servic...",
            "charge_id": "Placeholder",
            "charge_group_heading": "Usage Charges",
            "charge_category": "ch.usage_cha"
        },
        {
            "rule_id": "8912008",
            "customer_name": customer,
            "priority_order": "3095",
            "charge_name_mapping": "(?i)Electric\\s*servic...",
            "charge_id": "Placeholder",
            "charge_group_heading": "Usage Charges",
            "charge_category": "ch.usage_cha"
        },
        {
            "rule_id": "8912009",
            "customer_name": customer,
            "priority_order": "3094",
            "charge_name_mapping": "(?i)Electric\\s*servic...",
            "charge_id": "Placeholder",
            "charge_group_heading": "Usage Charges",
            "charge_category": "ch.usage_cha"
        }
    ]


def display_priority_table_with_reorder(rules_data: List[Dict[str, Any]]):
    """
    Display the priority rules table with reorder functionality
    
    Args:
        rules_data: List of rule data dictionaries
    """
    st.markdown("### Rules Priority Order")
    
    # Display each rule with reorder buttons
    for i, rule in enumerate(rules_data):
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1, 2, 2, 2, 3, 2, 2, 2])
            
            with col1:
                st.markdown("**=", help="Drag handle")
            
            with col2:
                st.markdown(f"**{rule['rule_id']}**")
            
            with col3:
                st.markdown(f"**{rule['customer_name']}**")
            
            with col4:
                st.markdown(f"**{rule['priority_order']}**")
            
            with col5:
                st.markdown(f"**{rule['charge_name_mapping']}**")
            
            with col6:
                st.markdown(f"**{rule['charge_id']}**")
            
            with col7:
                st.markdown(f"**{rule['charge_group_heading']}**")
            
            with col8:
                # Reorder buttons
                col_up, col_down = st.columns(2)
                with col_up:
                    if st.button("↑", key=f"move_up_{i}_unique", disabled=i==0, help="Move up"):
                        if i > 0:
                            # Swap with previous item
                            rules_data[i], rules_data[i-1] = rules_data[i-1], rules_data[i]
                            st.rerun()
                
                with col_down:
                    if st.button("↓", key=f"move_down_{i}_unique", disabled=i==len(rules_data)-1, help="Move down"):
                        if i < len(rules_data) - 1:
                            # Swap with next item
                            rules_data[i], rules_data[i+1] = rules_data[i+1], rules_data[i]
                            st.rerun()
        
        # Add separator between rows
        if i < len(rules_data) - 1:
            st.divider()
    
    # Add drag-and-drop instructions
    st.markdown("""
    <div style="margin-top: 16px; padding: 12px; background: #f8f9fa; border-radius: 4px; border-left: 4px solid #0068c9;">
        <strong>💡 Tip:</strong> Use the ↑ and ↓ buttons to reorder rules. Higher priority rules should be at the top.
    </div>
    """, unsafe_allow_html=True)


def display_priority_table(rules_data: List[Dict[str, Any]]):
    """
    Display the priority rules table with drag handles (legacy method)
    
    Args:
        rules_data: List of rule data dictionaries
    """
    # Create DataFrame for display
    df_data = []
    for i, rule in enumerate(rules_data):
        df_data.append({
            "": "=",  # Drag handle column
            "Rule ID": rule["rule_id"],
            "Customer name": rule["customer_name"],
            "Priority order": rule["priority_order"],
            "Charge name mappi...": rule["charge_name_mapping"],
            "Charge ID": rule["charge_id"],
            "Charge group headi...": rule["charge_group_heading"],
            "Charge categ": rule["charge_category"]
        })
    
    df = pd.DataFrame(df_data)
    
    # Display the table with custom styling
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "": st.column_config.TextColumn("", width="small"),
            "Rule ID": st.column_config.TextColumn("Rule ID", width="medium"),
            "Customer name": st.column_config.TextColumn("Customer name", width="medium"),
            "Priority order": st.column_config.TextColumn("Priority order", width="medium"),
            "Charge name mappi...": st.column_config.TextColumn("Charge name mappi...", width="large"),
            "Charge ID": st.column_config.TextColumn("Charge ID", width="medium"),
            "Charge group headi...": st.column_config.TextColumn("Charge group headi...", width="medium"),
            "Charge categ": st.column_config.TextColumn("Charge categ", width="medium")
        }
    )


def render_edit_priority_button(data_provider: DataProvider, context: Dict[str, Any] = None, unique_key: str = ""):
    """
    Render the Edit Priority button that opens the modal
    
    Args:
        data_provider: The data provider instance
        context: Context dictionary containing customer and selected data
        unique_key: Unique identifier for this button instance
    """
    
    # Get customer from context or session state
    if isinstance(context, dict):
        customer = context.get('customer', st.session_state.get('selected_customer', 'Default Customer'))
    else:
        customer = st.session_state.get('selected_customer', 'Default Customer')
    
    # Create unique button key
    button_key = f"edit_priority_btn_{unique_key}" if unique_key else "edit_priority_btn"
    
    # Check if button is clicked
    if st.button("Edit Priority", key=button_key, type="secondary", use_container_width=False):
        # Store customer in session state for modal use
        st.session_state.selected_customer = customer
        # Show modal
        st.session_state.show_edit_priority_modal = True
        st.rerun()


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
        
        # Example SQL (you would need to adapt this to your actual schema):
        # UPDATE charge_mapping_rules SET
        #     priority_order = ?, updated_at = NOW()
        # WHERE rule_id = ?
        
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
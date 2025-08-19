"""
Charges Tab UI Component

This module contains the UI for the Charges tab with data table and filtering functionality.
"""

import streamlit as st
import pandas as pd
from typing import Optional, List, Dict
from components.data.providers import DataProvider
from components.modals.create_rule_modal import render_create_rule_button


def render_charges_tab(data_provider: DataProvider, customer: str):
    """
    Render the Charges tab
    
    Args:
        data_provider: The data provider instance
        customer: The selected customer
    """
    
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    st.markdown("### Charges")
    st.markdown("Start by viewing all charges, then filter by category: Uncategorized, Approval needed, or Approved.")
    
    # Filter section - improved layout
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    with col1:
        charge_type = st.selectbox(
            "Charge type",
            ["Uncategorized (100)", "Approval needed (25)", "Approved (150)"],
            index=0
        )
    
    with col5:
        render_create_rule_button(data_provider, {"customer": customer}, "charges_tab")
    
    # Get charges data
    charges_df = data_provider.get_charges(customer, charge_type)
    
    # Convert numeric columns to string to avoid type compatibility issues
    if not charges_df.empty:
        if 'Account number' in charges_df.columns:
            charges_df['Account number'] = charges_df['Account number'].astype(str)
        if 'Statement ID' in charges_df.columns:
            charges_df['Statement ID'] = charges_df['Statement ID'].astype(str)
        if 'Service type' in charges_df.columns:
            charges_df['Service type'] = charges_df['Service type'].astype(str).fillna('')
        if 'Usage unit' in charges_df.columns:
            charges_df['Usage unit'] = charges_df['Usage unit'].astype(str).fillna('')
        if 'Charge measurement' in charges_df.columns:
            charges_df['Charge measurement'] = charges_df['Charge measurement'].astype(str).fillna('')
    
    # Initialize session state for selected rows
    if 'selected_rows' not in st.session_state:
        st.session_state.selected_rows = set()
    
    # Display the table without checkbox column for now
    edited_df = st.data_editor(
        charges_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Statement ID": st.column_config.TextColumn("Statement ID", width="medium"),
            "Provider name": st.column_config.TextColumn("Provider name", width="medium"),
            "Account number": st.column_config.TextColumn("Account number", width="medium"),
            "Charge name": st.column_config.TextColumn("Charge name", width="medium"),
            "Charge ID": st.column_config.TextColumn("Charge ID", width="medium"),
            "Charge measurement": st.column_config.TextColumn("Charge measurement", width="medium"),
            "Usage unit": st.column_config.TextColumn("Usage unit", width="medium"),
            "Service type": st.column_config.TextColumn("Service type", width="medium")
        },
        key="charges_table"
    )
    
    # Pagination
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown("Page 1 of 3")
    with col3:
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.number_input("Page", min_value=0, value=0, key="page_num")
        with col_b:
            st.number_input("Page size", min_value=10, value=30, key="page_size")
    
    st.markdown('</div>', unsafe_allow_html=True)


def get_selected_charges() -> List[Dict]:
    """
    Get the currently selected charges from the data editor
    
    Returns:
        List of selected charge dictionaries
    """
    # This would need to be implemented based on how you want to track selections
    # For now, return empty list
    return [] 
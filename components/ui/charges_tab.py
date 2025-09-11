"""
Charges Tab UI Component

This module contains the UI for the Charges tab with data table and filtering functionality.
"""

import streamlit as st
from components.data.data_providers import DataProvider


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
            ["Uncategorized"],
            index=0
        )
    
    with col5:
        # Direct Create Rule button
        if st.button("Create rule", key="create_rule_charges_tab", type="primary"):
            st.session_state.show_create_rule_dialog_charges_tab = True
            st.rerun()
        
        # Dialog will be handled by centralized dialog manager in main.py
    
    # Get charges data
    charges_df = data_provider.get_charges(customer, charge_type)
    
    # Handle data type issues for Streamlit compatibility
    if not charges_df.empty:
        for col in charges_df.columns:
            # Convert all columns to string to avoid type compatibility issues
            if col in ["STATEMENT_CREATED_DATE"]:
                # Convert date columns to string
                charges_df[col] = charges_df[col].astype(str)
            elif charges_df[col].dtype == 'object':
                # Fill NaN values for object columns
                charges_df[col] = charges_df[col].fillna('')
            else:
                # Convert all other columns to string
                charges_df[col] = charges_df[col].astype(str)
    
    # Initialize session state for selected rows
    if 'selected_rows' not in st.session_state:
        st.session_state.selected_rows = set()
    
    # Create column configuration for the specific columns we want to display
    column_config = {
        "STATEMENT_ID": st.column_config.TextColumn("Statement ID", width="medium"),
        "STATEMENT_CREATED_DATE": st.column_config.TextColumn("Statement Created Date", width="medium"),
        "PROVIDER_NAME": st.column_config.TextColumn("Provider Name", width="medium"),
        "ACCOUNT_NUMBER": st.column_config.TextColumn("Account Number", width="medium"),
        "CHARGE_NAME": st.column_config.TextColumn("Charge Name", width="medium"),
        "CHARGE_ID_CATEGORY": st.column_config.TextColumn("Charge ID/Category", width="medium"),
        "CHARGE_MEASUREMENT": st.column_config.TextColumn("Charge Measurement", width="medium"),
        "USAGE_UNIT": st.column_config.TextColumn("Usage Unit", width="medium"),
        "SERVICE_TYPE": st.column_config.TextColumn("Service Type", width="medium")
    }
    
    # Display the table with selection capability
    selected_rows = st.dataframe(
        charges_df,
        use_container_width=True,
        hide_index=True,
        column_config=column_config,
        key="charges_table",
        selection_mode="multi-row",
        on_select="rerun"
    )
    
    # Handle row selection
    if selected_rows.selection.rows:
        # Get selected rows data
        selected_indices = selected_rows.selection.rows
        selected_charges = charges_df.iloc[selected_indices].to_dict('records')
        
        # Store selected charges in session state
        st.session_state.selected_charges = selected_charges
        
        # Display selection info
        st.info(f"📋 {len(selected_charges)} row(s) selected for rule creation/editing")
    else:
        # Clear selection if no rows selected
        st.session_state.selected_charges = []
        st.info("💡 Select rows using the checkboxes to create or edit rules")
    
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



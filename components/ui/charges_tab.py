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
    st.markdown("This table shows list of uncategorized charges from the processed statements.")
    
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
    
    # Pagination settings
    if 'charges_page_size' not in st.session_state:
        st.session_state.charges_page_size = 50
    page_size = st.session_state.charges_page_size
    
    if 'charges_page' not in st.session_state:
        st.session_state.charges_page = 1
    
    # Reset to page 1 when charge type changes
    if 'last_charge_type' not in st.session_state:
        st.session_state.last_charge_type = charge_type
    elif st.session_state.last_charge_type != charge_type:
        st.session_state.charges_page = 1
        st.session_state.last_charge_type = charge_type
    
    # Get total count for pagination
    total_count = data_provider.get_charges_count(customer, charge_type)
    
    # Calculate total pages
    total_pages = int((total_count + page_size - 1) // page_size) if total_count > 0 else 1
    
    # Get charges data for current page
    charges_df = data_provider.get_charges(customer, charge_type, st.session_state.charges_page, page_size)
    
    # Show message if no charges found
    if charges_df.empty:
        st.info("No uncategorized charges found.")
    
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
    
    # pagination controls at bottom of table
    if total_count > 0:
        # Create a single row with page info (including total count) on left and controls on right
        col1, col2, col3 = st.columns([4, 0.8, 0.8])
        
        with col1:
            # Page info with total count on the left (unbolded)
            st.markdown(f"Page {st.session_state.charges_page} of {total_pages} ({total_count:,} total)")
        
        with col2:
            # Page input control
            page_input = st.number_input(
                "Page", 
                min_value=1, 
                max_value=total_pages, 
                value=st.session_state.charges_page,
                step=1,
                key="page_input"
            )
            if page_input != st.session_state.charges_page:
                st.session_state.charges_page = int(page_input)
                st.rerun()
        
        with col3:
            # Page size input control
            rows_per_page = st.number_input(
                "Page size", 
                min_value=10, 
                max_value=1000, 
                value=st.session_state.charges_page_size,
                step=10,
                key="rows_per_page"
            )
            if rows_per_page != st.session_state.charges_page_size:
                st.session_state.charges_page_size = int(rows_per_page)
                st.session_state.charges_page = 1  # Reset to page 1 when page size changes
                st.rerun()
    
    # Handle row selection
    if selected_rows.selection.rows:
        # Get selected rows data from the full dataframe
        selected_indices = selected_rows.selection.rows
        selected_charges = charges_df.iloc[selected_indices].to_dict('records')
        
        # Store selected charges in session state
        st.session_state.selected_charges = selected_charges
        
        # Display selection info
        st.info(f"📋 {len(selected_charges)} row(s) selected for rule creation/editing")
    else:
        # Clear selection if no rows selected
        st.session_state.selected_charges = []
    
    st.markdown('</div>', unsafe_allow_html=True)



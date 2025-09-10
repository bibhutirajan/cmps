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
            ["Uncategorized (100)", "Approval needed (25)", "Approved (150)"],
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
            if col in ["STATEMENT_DATE", "INTERVAL_START_DATE", "INTERVAL_END_DATE"]:
                # Convert date columns to string
                charges_df[col] = charges_df[col].astype(str)
            elif col in ["ODIN_ORGANIZATION_ID", "ODIN_ACCOUNT_ID", "ODIN_METER_ID"]:
                # Convert integer columns to string
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
    
    # Create dynamic column configuration based on Snowflake table definition
    column_config = {}
    
    for col in charges_df.columns:
        # Map column names to user-friendly display names based on Snowflake table definition
        if col == "ODIN_STATEMENT_ID":
            column_config[col] = st.column_config.TextColumn("Statement ID", width="medium")
        elif col == "UTILITY_PROVIDER_NAME":
            column_config[col] = st.column_config.TextColumn("Provider", width="medium")
        elif col == "NORMALIZED_ACCOUNT_NUMBER":
            column_config[col] = st.column_config.TextColumn("Account", width="medium")
        elif col == "TARIFF_NAME":
            column_config[col] = st.column_config.TextColumn("Charge Name", width="medium")
        elif col == "CHARGE_ID":
            column_config[col] = st.column_config.TextColumn("Charge ID", width="medium")
        elif col == "MEASUREMENT_TYPE":
            column_config[col] = st.column_config.TextColumn("Measurement", width="medium")
        elif col == "SERVICE_TYPE":
            column_config[col] = st.column_config.TextColumn("Service Type", width="medium")
        elif col == "CONTRIBUTION_STATUS":
            column_config[col] = st.column_config.TextColumn("Status", width="small")
        elif col == "DEREGULATION_STATUS":
            column_config[col] = st.column_config.TextColumn("Deregulation", width="small")
        elif col == "CHARGE_AMOUNT":
            column_config[col] = st.column_config.TextColumn("Amount", width="small")
        elif col == "CHARGE_AMOUNT_CURRENCY":
            column_config[col] = st.column_config.TextColumn("Currency", width="small")
        elif col == "STATEMENT_DATE":
            column_config[col] = st.column_config.TextColumn("Statement Date", width="small")
        elif col == "INTERVAL_START_DATE":
            column_config[col] = st.column_config.TextColumn("Interval Start", width="small")
        elif col == "INTERVAL_END_DATE":
            column_config[col] = st.column_config.TextColumn("Interval End", width="small")
        elif col == "ODIN_ORGANIZATION_ID":
            column_config[col] = st.column_config.TextColumn("Org ID", width="small")
        elif col == "ODIN_ACCOUNT_ID":
            column_config[col] = st.column_config.TextColumn("Account ID", width="small")
        elif col == "ODIN_METER_ID":
            column_config[col] = st.column_config.TextColumn("Meter ID", width="small")
        elif col == "ODIN_SITE_ID":
            column_config[col] = st.column_config.TextColumn("Site ID", width="small")
        elif col == "NORMALIZED_METER_NUMBER":
            column_config[col] = st.column_config.TextColumn("Meter Number", width="medium")
        elif col == "NORMALIZED_POD_NUMBER":
            column_config[col] = st.column_config.TextColumn("POD Number", width="medium")
        elif col == "CHARGE_RULE_ID":
            column_config[col] = st.column_config.TextColumn("Rule ID", width="medium")
        elif col == "CHARGE_RULE_SOURCE":
            column_config[col] = st.column_config.TextColumn("Rule Source", width="small")
        elif col == "STATEMENT_TYPE":
            column_config[col] = st.column_config.TextColumn("Statement Type", width="small")
        elif col == "SOURCE_IDS":
            column_config[col] = st.column_config.TextColumn("Source IDs", width="medium")
        elif col == "ODIN_CHARGE_ITEM_ID":
            column_config[col] = st.column_config.TextColumn("Charge Item ID", width="medium")
        elif col == "ODIN_DEFAULT_STATEMENT_VERSION_ID":
            column_config[col] = st.column_config.TextColumn("Statement Version", width="medium")
        elif col == "ODIN_METER_DATA_ID":
            column_config[col] = st.column_config.TextColumn("Meter Data ID", width="medium")
        else:
            # Default configuration for other columns
            column_config[col] = st.column_config.TextColumn(col, width="medium")
    
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



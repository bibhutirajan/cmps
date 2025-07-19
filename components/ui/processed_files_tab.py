"""
Processed Files Tab UI Component

This module contains the UI for the Processed Files tab.
"""

import streamlit as st
from components.data.providers import DataProvider


def render_processed_files_tab(data_provider: DataProvider, customer: str):
    """
    Render the Processed Files tab
    
    Args:
        data_provider: The data provider instance
        customer: The selected customer
    """
    
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    st.markdown("### Processed files")
    st.markdown("View and manage processed charge files.")
    
    # Get processed files data
    files_df = data_provider.get_processed_files(customer)
    
    if isinstance(data_provider, data_provider.__class__):  # Check if demo provider
        st.info("🔧 Demo Mode: This would show processed files from Snowflake")
    
    st.dataframe(files_df, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True) 
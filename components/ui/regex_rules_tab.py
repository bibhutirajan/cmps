"""
Regex Rules Tab UI Component

This module contains the UI for the Regex Rules tab.
"""

import streamlit as st
from components.data.providers import DataProvider


def render_regex_rules_tab(data_provider: DataProvider, customer: str):
    """
    Render the Regex Rules tab
    
    Args:
        data_provider: The data provider instance
        customer: The selected customer
    """
    
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    st.markdown("### Regex and rules")
    st.markdown("Configure regex patterns and advanced rule matching.")
    
    # Get regex rules data
    regex_df = data_provider.get_regex_rules(customer)
    
    if isinstance(data_provider, data_provider.__class__):  # Check if demo provider
        st.info("🔧 Demo Mode: This would show regex patterns from Snowflake")
    
    st.dataframe(regex_df, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True) 
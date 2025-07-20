"""
Customer Sidebar Component

This module contains the customer selection and user information sidebar.
"""

import streamlit as st
from components.data.providers import DataProvider


def render_customer_sidebar(data_provider: DataProvider) -> str:
    """
    Render the customer selection and user info sidebar (default collapsed)
    
    Args:
        data_provider: The data provider instance
    
    Returns:
        The selected customer name
    """
    with st.sidebar:
        st.markdown("### 🏢 Customer Selection")
        selected_customer = st.selectbox(
            "Select Customer",
            ["AmerescoFTP", "OtherCustomer", "NewCustomer", "TestCustomer"],
            index=0
        )
        
        # Status indicator
        if hasattr(data_provider, '__class__') and 'Demo' in data_provider.__class__.__name__:
            st.info("🎭 Demo Mode Active")
        else:
            st.success("✅ Connected to Snowflake")
        
        # Add some spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("### 👤 User Information")
        st.markdown('<div class="user-info">', unsafe_allow_html=True)
        st.markdown("**Name:** John Doe")
        st.markdown("**Role:** Admin")
        st.markdown("**Email:** john.doe@company.com")
        st.markdown("**Last Login:** Today, 2:30 PM")
        st.markdown('</div>', unsafe_allow_html=True)
        
        return selected_customer 
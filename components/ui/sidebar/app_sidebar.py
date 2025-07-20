"""
App Sidebar Component

This module contains the main application sidebar with customer selection, 
mode indicator, theme toggle, and user information.
"""

import streamlit as st
from components.data.providers import DataProvider


def render_app_sidebar(data_provider: DataProvider) -> str:
    """
    Render the main application sidebar with all controls and info
    
    Args:
        data_provider: The data provider instance
    
    Returns:
        The selected customer name
    """
    with st.sidebar:
        # Customer Selection Section
        st.markdown("### 🏢 Customer Selection")
        selected_customer = st.selectbox(
            "Select Customer",
            ["AmerescoFTP", "OtherCustomer", "NewCustomer", "TestCustomer"],
            index=0,
            help="Choose the customer account to work with"
        )
        
        # Mode Indicator Section
        st.markdown("### 🔧 System Mode")
        if hasattr(data_provider, '__class__') and 'Demo' in data_provider.__class__.__name__:
            st.info("🎭 Demo Mode Active", icon="🎭")
        else:
            st.success("✅ Connected to Snowflake", icon="✅")
        
        # Theme Toggle Section
        st.markdown("### 🌓 Theme")
        col1, col2 = st.columns([3, 1])
        with col1:
            theme_label = "🌙 Dark Mode" if st.session_state.get('dark_theme', False) else "☀️ Light Mode"
            st.markdown(f"**{theme_label}**")
        with col2:
            if st.button("🔄", key="theme_toggle", help="Toggle between light and dark theme"):
                st.session_state.dark_theme = not st.session_state.get('dark_theme', False)
                st.rerun()
        
        # User Information Section
        st.markdown("### 👤 User Information")
        st.markdown('<div class="user-info">', unsafe_allow_html=True)
        st.markdown("**Name:** John Doe")
        st.markdown("**Role:** Admin")
        st.markdown("**Email:** john.doe@company.com")
        st.markdown("**Last Login:** Today, 2:30 PM")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Actions Section
        st.markdown("### ⚡ Quick Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Refresh Data", key="refresh_data", help="Refresh all data from source"):
                st.rerun()
        with col2:
            if st.button("⚙️ Settings", key="settings", help="Open application settings"):
                st.info("Settings panel coming soon!")
        
        return selected_customer 
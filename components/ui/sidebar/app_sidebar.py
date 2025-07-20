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
        st.markdown("### 🏢 Customer")
        selected_customer = st.selectbox(
            "Customer",
            ["AmerescoFTP", "OtherCustomer", "NewCustomer", "TestCustomer"],
            index=0,
            label_visibility="collapsed"
        )
        
        # Mode Toggle Section
        st.markdown("### ⚙️ Mode")
        # Initialize mode in session state if not exists
        if 'demo_mode' not in st.session_state:
            st.session_state.demo_mode = hasattr(data_provider, '__class__') and 'Demo' in data_provider.__class__.__name__
        
        col1, col2 = st.columns([3, 1])
        with col1:
            mode_label = "Demo" if st.session_state.demo_mode else "Prod"
            st.markdown(f"**{mode_label}**")
        with col2:
            if st.button("↻", key="mode_toggle", help="Toggle between Demo and Prod modes"):
                st.session_state.demo_mode = not st.session_state.demo_mode
                st.rerun()
        
        # Theme Toggle Section
        st.markdown("### 🌓 Theme")
        col1, col2 = st.columns([3, 1])
        with col1:
            theme_label = "Dark" if st.session_state.get('dark_theme', False) else "Light"
            st.markdown(f"**{theme_label}**")
        with col2:
            if st.button("↻", key="theme_toggle", help="Toggle theme"):
                st.session_state.dark_theme = not st.session_state.get('dark_theme', False)
                st.rerun()
        
        # User Information Section
        st.markdown("### 👤 User")
        st.markdown("**Bibhuti Rajan**<br>Admin<br>bibhuti.rajan@company.com<br>Today, 2:30 PM", unsafe_allow_html=True)
        
        return selected_customer 
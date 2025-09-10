"""
Sidebar Component

This module contains the main application sidebar with customer selection 
and user information.
"""

import streamlit as st
from components.data.data_providers import DataProvider


def render_sidebar(data_provider: DataProvider) -> str:
    """
    Render the main application sidebar with customer selection and user info
    
    Args:
        data_provider: The data provider instance
    
    Returns:
        The selected customer name
    """
    with st.sidebar:
        # Customer Selection Section
        st.markdown("### 🏢 Customer")
        
        # Get available customers based on the data provider type
        if hasattr(data_provider, '__class__') and 'Demo' in data_provider.__class__.__name__:
            # Demo mode - use hardcoded customers
            customer_options = ["AmerescoFTP", "OtherCustomer", "NewCustomer", "TestCustomer"]
        else:
            # Production mode - use customer names that map to organization IDs
            customer_options = ["AmerescoFTP", "OtherCustomer", "NewCustomer", "TestCustomer"]
        
        selected_customer = st.selectbox(
            "Customer",
            customer_options,
            index=0,
            label_visibility="collapsed"
        )
        
        # User Information Section
        st.markdown("### 👤 User")
        
        # Get current user from data provider
        try:
            if hasattr(data_provider, 'session') and data_provider.session:
                # Fetch current user from Snowflake
                current_user_result = data_provider.session.sql("SELECT CURRENT_USER()").collect()
                current_user = current_user_result[0][0] if current_user_result and current_user_result[0] else "Unknown User"
                
                # Get current timestamp
                timestamp_result = data_provider.session.sql("SELECT CURRENT_TIMESTAMP()").collect()
                current_time = timestamp_result[0][0] if timestamp_result and timestamp_result[0] else "Unknown Time"
                
                # Format the time nicely
                try:
                    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S") if hasattr(current_time, 'strftime') else str(current_time)
                except:
                    formatted_time = str(current_time)
                
                # Display user info
                st.markdown(f"""
                **{current_user}**<br>
                Snowflake User<br>
                {formatted_time}
                """, unsafe_allow_html=True)
            else:
                # Fallback for demo mode
                st.markdown("**Demo User**<br>Local Development<br>Demo Mode", unsafe_allow_html=True)
        except Exception as e:
            # Fallback in case of any errors
            st.markdown("**Current User**<br>Charge Mapping App<br>Active Session", unsafe_allow_html=True)
        
        return selected_customer

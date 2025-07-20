"""
Sidebar UI Components

This module contains modular sidebar components for different functionalities:
- Customer selection and user info (default collapsed)
- Create rule form (expands when triggered)
- Edit rule form (for future use)
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


def render_create_rule_form(data_provider: DataProvider, customer: str):
    """
    Render the create rule form (only when triggered)
    
    Args:
        data_provider: The data provider instance
        customer: The selected customer name
    """
    # Rule creation form - only render when triggered
    # Add CSS to ensure sidebar is visible and expanded ONLY when form is active
    st.markdown("""
    <style>
    /* Force sidebar to expand ONLY when create rule form is active */
    [data-testid="stSidebar"]:has(.stButton[key="close_rule_form"]) {
        padding-top: 0.5rem !important;
        min-width: 400px !important;
        max-width: 500px !important;
        display: block !important;
        visibility: visible !important;
        transform: translateX(0) !important;
        opacity: 1 !important;
    }
    [data-testid="stSidebar"]:has(.stButton[key="close_rule_form"]) > div:first-child {
        padding-top: 0.5rem !important;
    }
    /* Ensure sidebar content is visible when form is active */
    [data-testid="stSidebar"]:has(.stButton[key="close_rule_form"]) > div {
        display: block !important;
        visibility: visible !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with cross icon and New rule text aligned horizontally - optimized spacing
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("## New rule")
    with col2:
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)  # Reduced spacing
        if st.button("✖️", key="close_rule_form", help="Close form"):
            st.session_state.show_rule_form = False
            st.rerun()
    
    st.markdown("---")
    
    # If charge matches criteria section
    st.markdown("### If charge matches criteria...")
    
    # Provider
    provider = st.selectbox(
        "Provider",
        ["Atmos", "Other Provider", "Test Provider"],
        index=0,
        key="rule_provider"
    )
    
    # Charge name with condition dropdown
    col1, col2 = st.columns([1, 2])
    with col1:
        charge_name_condition = st.selectbox(
            "Condition",
            ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
            key="charge_name_condition"
        )
    with col2:
        charge_name = st.text_input(
            "Charge name",
            value="CHP rider",
            key="rule_charge_name"
        )
    
    # Advanced conditions toggle
    advanced_enabled = st.toggle("Advanced conditions", value=True, key="advanced_conditions")
    
    if advanced_enabled:
        # Account number
        col1, col2 = st.columns([1, 2])
        with col1:
            account_condition = st.selectbox(
                "Condition",
                ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                key="account_condition"
            )
        with col2:
            account_number = st.text_input(
                "Account number",
                value="00000000",
                key="rule_account_number"
            )
        
        # Usage unit
        col1, col2 = st.columns([1, 2])
        with col1:
            usage_unit_condition = st.selectbox(
                "Condition",
                ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                key="usage_unit_condition"
            )
        with col2:
            usage_unit = st.selectbox(
                "Usage unit",
                ["kWh", "therms", "gallons", "cubic feet"],
                index=0,
                key="rule_usage_unit"
            )
        
        # Service type
        col1, col2 = st.columns([1, 2])
        with col1:
            service_type_condition = st.selectbox(
                "Condition",
                ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                key="service_type_condition"
            )
        with col2:
            service_type = st.selectbox(
                "Service type",
                ["Electric", "Gas", "Water", "Other"],
                index=0,
                key="rule_service_type"
            )
    
    st.markdown("---")
    
    # Then apply these actions section
    st.markdown("### Then apply these actions...")
    
    # Charge name mapping
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("**Charge name mapping**")
    with col2:
        charge_name_mapping = st.text_input(
            "New charge name",
            value="CHP Rider Charge",
            key="rule_charge_name_mapping"
        )
    
    # Charge category
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("**Charge category**")
    with col2:
        charge_category = st.selectbox(
            "Category",
            ["Energy", "Delivery", "Taxes", "Fees", "Other"],
            index=0,
            key="rule_charge_category"
        )
    
    # Charge group heading
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("**Charge group heading**")
    with col2:
        charge_group_heading = st.text_input(
            "Group heading",
            value="Energy Charges",
            key="rule_charge_group_heading"
        )
    
    # Request type
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("**Request type**")
    with col2:
        request_type = st.selectbox(
            "Request type",
            ["Standard", "Priority", "Emergency"],
            index=0,
            key="rule_request_type"
        )
    
    st.markdown("---")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save rule", key="save_rule_btn", type="primary"):
            # Create rule data
            rule_data = {
                "customer": customer,
                "provider": provider,
                "charge_name_condition": charge_name_condition,
                "charge_name": charge_name,
                "advanced_enabled": advanced_enabled,
                "account_condition": account_condition if advanced_enabled else None,
                "account_number": account_number if advanced_enabled else None,
                "usage_unit_condition": usage_unit_condition if advanced_enabled else None,
                "usage_unit": usage_unit if advanced_enabled else None,
                "service_type_condition": service_type_condition if advanced_enabled else None,
                "service_type": service_type if advanced_enabled else None,
                "charge_name_mapping": charge_name_mapping,
                "charge_category": charge_category,
                "charge_group_heading": charge_group_heading,
                "request_type": request_type
            }
            
            # Save the rule
            if data_provider.create_rule(rule_data):
                st.session_state.show_rule_form = False
                st.rerun()
    
    with col2:
        if st.button("Cancel", key="cancel_rule_btn"):
            st.session_state.show_rule_form = False
            st.rerun()


def render_edit_rule_form(data_provider: DataProvider, customer: str):
    """
    Render the edit rule form (for future use)
    
    Args:
        data_provider: The data provider instance
        customer: The selected customer name
    """
    # Initialize session state for edit rule form
    if 'show_edit_rule_form' not in st.session_state:
        st.session_state.show_edit_rule_form = False
    
    # Edit rule form (placeholder for future implementation)
    if st.session_state.show_edit_rule_form:
        st.markdown("## Edit Rule")
        st.info("Edit rule functionality will be implemented here")
        
        if st.button("Close", key="close_edit_rule_form"):
            st.session_state.show_edit_rule_form = False
            st.rerun()


def render_main_sidebar(data_provider: DataProvider) -> str:
    """
    Main sidebar function that orchestrates all sidebar components
    
    Args:
        data_provider: The data provider instance
    
    Returns:
        The selected customer name
    """
    # Initialize session state for rule creation form
    if 'show_rule_form' not in st.session_state:
        st.session_state.show_rule_form = False
    
    with st.sidebar:
        # If create rule form is active, show only the form
        if st.session_state.show_rule_form:
            render_create_rule_form(data_provider, "AmerescoFTP")  # Default customer when form is active
            return "AmerescoFTP"
        else:
            # Show customer sidebar (default collapsed)
            customer = render_customer_sidebar(data_provider)
            return customer 
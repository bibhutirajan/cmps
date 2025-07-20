import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Charge Mapping",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Hide sidebar by default */
    .css-1d391kg {
        display: none;
    }
    
    /* Remove white backgrounds from all elements */
    .stApp {
        background-color: #0e1117 !important;
    }
    
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    .tab-container {
        background-color: transparent !important;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .stButton > button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton > button:hover {
        background-color: #2563eb;
    }
    .metric-card {
        background-color: transparent !important;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #3b82f6;
    }
    .metric-label {
        color: #6b7280;
        font-size: 0.875rem;
    }
    .user-info {
        background-color: #374151 !important;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: white;
    }
    
    /* Override any white backgrounds */
    div[data-testid="stSidebar"] {
        background-color: #1e293b !important;
    }
    
    /* Remove white backgrounds from dataframes */
    .stDataFrame {
        background-color: transparent !important;
    }
    
    /* Remove white backgrounds from selectboxes */
    .stSelectbox > div > div {
        background-color: #374151 !important;
        color: white !important;
    }
    
    /* Remove white backgrounds from number inputs */
    .stNumberInput > div > div {
        background-color: #374151 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar: Customer Selector and User Details
with st.sidebar:
    st.markdown("### 🏢 Customer Selection")
    selected_customer = st.selectbox(
        "Select Customer",
        ["AmerescoFTP", "OtherCustomer", "NewCustomer", "TestCustomer"],
        index=0
    )
    
    # Status indicator
    st.info("🎭 Demo Mode Active")
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### 👤 User Information")
    st.markdown('<div class="user-info">', unsafe_allow_html=True)
    st.markdown("**Name:** John Doe")
    st.markdown("**Role:** Admin")
    st.markdown("**Email:** john.doe@company.com")
    st.markdown("**Last Login:** Today, 2:30 PM")
    st.markdown('</div>', unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown('<div class="main-header">⚡ Charge Mapping</div>', unsafe_allow_html=True)

# Navigation tabs in main area with descriptive names
charges_tab, rules_tab, processed_files_tab, regex_rules_tab = st.tabs([
    "Charges", 
    "Rules", 
    "Processed files", 
    "Regex and rules"
])

# Demo data for charges
def create_demo_charges():
    return pd.DataFrame({
        'Statement ID': ['1efe9dd1-6cad-d3c...', '1efe9dd1-6cad-d3c...', '1efe9dd1-6cad-d3c...', '1efe9dd1-6cad-d3c...'],
        'Provider name': ['Atmos', 'Atmos', 'Atmos', 'Atmos'],
        'Account number': ['3018639036', '3018639036', '3018639036', '3018639036'],
        'Charge name': ['CHP Rider', 'CHP Rider', 'CHP Rider', 'CHP Rider'],
        'Charge ID': ['NewBatch', 'NewBatch', 'NewBatch', 'NewBatch'],
        'Charge measurement': ['general_consumption', 'general_consumption', 'general_consumption', 'general_consumption'],
        'Usage unit': ['None', 'None', 'None', 'None'],
        'Service type': ['None', 'None', 'None', 'None']
    })

# Demo data for rules
def create_demo_rules():
    return pd.DataFrame({
        'Rule ID': [f'RULE_{i:03d}' for i in range(1, 11)],
        'Provider': [f'Provider_{i}' for i in range(1, 11)],
        'Category': ['Electricity', 'Gas', 'Water', 'Electricity', 'Gas', 
                    'Water', 'Electricity', 'Gas', 'Water', 'Electricity'],
        'Status': ['Active', 'Active', 'Active', 'Pending', 'Active', 
                  'Active', 'Active', 'Active', 'Pending', 'Active'],
        'Priority': list(range(1, 11))
    })

# Charges Tab
with charges_tab:
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    
    st.markdown("### Charges")
    st.markdown("Start by viewing all charges, then filter by category: Uncategorized, Approval needed, or Approved.")
    
    # Filter section - removed container, direct layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        charge_type = st.selectbox(
            "Charge type",
            ["Uncategorized (100)", "Approval needed (25)", "Approved (150)"],
            index=0
        )
    
    with col2:
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
        if st.button("Create rule", key="create_rule_btn"):
            st.success("Create rule functionality would be implemented here")
    
    # Data table
    demo_charges = create_demo_charges()
    
    # Add checkbox column
    demo_charges.insert(0, 'Select', [True] + [False] * (len(demo_charges) - 1))
    
    # Display the table
    st.dataframe(
        demo_charges,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Select": st.column_config.CheckboxColumn("Select", default=False),
            "Statement ID": st.column_config.TextColumn("Statement ID", width="medium"),
            "Provider name": st.column_config.TextColumn("Provider name", width="medium"),
            "Account number": st.column_config.TextColumn("Account number", width="medium"),
            "Charge name": st.column_config.TextColumn("Charge name", width="medium"),
            "Charge ID": st.column_config.TextColumn("Charge ID", width="medium"),
            "Charge measurement": st.column_config.TextColumn("Charge measurement", width="medium"),
            "Usage unit": st.column_config.TextColumn("Usage unit", width="medium"),
            "Service type": st.column_config.TextColumn("Service type", width="medium")
        }
    )
    
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

# Rules Tab
with rules_tab:
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    st.markdown("### Rules")
    st.markdown("Manage charge mapping rules and business logic.")
    
    # Filter section (dark grey bar)
    st.markdown("""
    <style>
        .filter-bar {
            background-color: #374151;
            border-radius: 6px;
            padding: 1rem;
            margin: 1rem 0;
        }
        .filter-dropdown {
            background-color: white;
            border-radius: 4px;
            padding: 0.5rem;
            margin: 0 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 1, 1, 2])
    
    with col1:
        st.selectbox("Filter 1", ["All"], key="filter1_demo")
    with col2:
        st.selectbox("Filter 2", ["AmerescoFTP"], key="filter2_demo")
    with col3:
        st.selectbox("Filter 3", ["Placeholder"], key="filter3_demo")
    with col4:
        st.selectbox("Filter 4", ["TBD"], key="filter4_demo")
    with col5:
        st.selectbox("Filter 5", ["(?i)Electric\\s*service.*"], key="filter5_demo")
    with col6:
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
        if st.button("Edit priority", key="edit_priority_btn_demo"):
            st.success("Edit priority functionality would be implemented here")
    with col7:
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
        if st.button("Edit rule", key="edit_rule_btn_demo"):
            st.success("Edit rule functionality would be implemented here")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Rules data table
    demo_rules = pd.DataFrame({
        'Rule ID': [8912000, 8912003, 8912005, 8912008, 8912010, 8912011, 8912017, 8912020],
        'Customer name': ['AmerescoFTP'] * 8,
        'Priority order': [3101, 3100, 3299, 3112, 3113, 3120, 3102.0, 3102.0],
        'Charge name mapping': ['(?i)Electric\\s*servic...'] * 8,
        'Charge ID': ['Placeholder'] * 8,
        'Charge group heading': [''] * 8,
        'Charge category': ['ch.usage_charge'] * 8,
        'Request type': [''] * 8
    })
    
    # Add checkbox column for selection
    demo_rules.insert(0, 'Select', [True] + [False] * (len(demo_rules) - 1))
    
    # Display the rules table
    st.dataframe(
        demo_rules,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Select": st.column_config.CheckboxColumn("Select", default=False),
            "Rule ID": st.column_config.NumberColumn("Rule ID", width="medium"),
            "Customer name": st.column_config.TextColumn("Customer name", width="medium"),
            "Priority order": st.column_config.NumberColumn("Priority order", width="medium"),
            "Charge name mapping": st.column_config.TextColumn("Charge name mapping", width="medium"),
            "Charge ID": st.column_config.TextColumn("Charge ID", width="medium"),
            "Charge group heading": st.column_config.TextColumn("Charge group heading", width="medium"),
            "Charge category": st.column_config.TextColumn("Charge category", width="medium"),
            "Request type": st.column_config.TextColumn("Request type", width="medium")
        }
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Processed files Tab
with processed_files_tab:
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    st.markdown("### Processed files")
    st.markdown("View and manage processed charge files.")
    
    demo_files = pd.DataFrame({
        'File ID': [f'FILE_{i:03d}' for i in range(1, 6)],
        'Filename': [f'charges_{i}.csv' for i in range(1, 6)],
        'Processed Date': ['2024-01-15', '2024-01-14', '2024-01-13', '2024-01-12', '2024-01-11'],
        'Status': ['Processed', 'Processed', 'Processed', 'Processed', 'Processed'],
        'Records': [150, 200, 175, 125, 300]
    })
    st.dataframe(demo_files, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Regex and rules Tab
with regex_rules_tab:
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    st.markdown("### Regex and rules")
    st.markdown("Configure regex patterns and advanced rule matching.")
    
    demo_regex = pd.DataFrame({
        'Pattern ID': [f'PATTERN_{i:03d}' for i in range(1, 6)],
        'Regex Pattern': [r'CHP.*Rider', r'Gas.*Service', r'Water.*Bill', r'Electric.*Charge', r'Service.*Fee'],
        'Category': ['Electricity', 'Gas', 'Water', 'Electricity', 'Other'],
        'Priority': [1, 2, 3, 4, 5]
    })
    st.dataframe(demo_regex, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True) 
"""
Create Rule Popup Component

This module contains the create rule form that appears as a popup using st.popover with enhanced styling.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any
from components.data.providers import DataProvider


def generate_preview_data(rule_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Generate preview data showing how the rule will affect existing charges
    
    Args:
        rule_data: The rule configuration data
    
    Returns:
        DataFrame with preview data
    """
    # This is sample data - in a real implementation, you would query your database
    # to find charges that match the rule criteria
    sample_data = [
        {
            "Charge name": rule_data.get('charge_name', 'CHP Rider'),
            "Provider name": rule_data.get('provider', 'Atmos'),
            "Account number": rule_data.get('account_number', '3018639036'),
            "Statement ID": "1efe9dd1-6cad-d3c...",
            "Current Charge ID": "Uncategorized",
            "New Charge ID": rule_data.get('charge_name_mapping', 'NewBatch'),
            "Usage unit": "kW",
            "Service": "None"
        }
    ]
    
    # Generate multiple rows for demonstration
    preview_data = []
    for i in range(12):  # 12 rows as shown in the Figma
        row = sample_data[0].copy()
        if i >= 9:  # Last 3 rows have different current charge ID
            row["Current Charge ID"] = "eh.special_regulatory_charges"
        if i > 0:  # All rows except first have different usage unit
            row["Usage unit"] = "None"
        preview_data.append(row)
    
    return pd.DataFrame(preview_data)


def render_create_rule_popup(data_provider: DataProvider, customer: str, key_prefix: str = "popup"):
    """
    Render the create rule form as a popup using st.popover with enhanced styling
    
    Args:
        data_provider: The data provider instance
        customer: The selected customer name
        key_prefix: Unique prefix for form keys to avoid duplicates
    """
    # Create the popover with enhanced styling
    with st.popover("➕ Create Rule", help="Click to create a new rule", use_container_width=True):
        # Add some spacing and better visual separation
        st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)
        
        # Header with cross icon and New rule text aligned horizontally - optimized spacing
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown("## 📝 New Rule")
        with col2:
            st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)  # Reduced spacing
        
        st.markdown("---")
        
        # If charge matches criteria section
        st.markdown("### 🎯 If charge matches criteria...")
        
        # Provider
        provider = st.selectbox(
            "Provider",
            ["Atmos", "Other Provider", "Test Provider"],
            index=0,
            key=f"rule_provider_{key_prefix}"
        )
        
        # Charge name with condition dropdown
        col1, col2 = st.columns([1, 2])
        with col1:
            charge_name_condition = st.selectbox(
                "Condition",
                ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                key=f"charge_name_condition_{key_prefix}"
            )
        with col2:
            charge_name = st.text_input(
                "Charge name",
                value="CHP rider",
                key=f"rule_charge_name_{key_prefix}"
            )
        
        # Advanced conditions toggle
        advanced_enabled = st.toggle("Advanced conditions", value=True, key=f"advanced_conditions_{key_prefix}")
        
        if advanced_enabled:
            # Account number
            col1, col2 = st.columns([1, 2])
            with col1:
                account_condition = st.selectbox(
                    "Condition",
                    ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                    key=f"account_condition_{key_prefix}"
                )
            with col2:
                account_number = st.text_input(
                    "Account number",
                    value="00000000",
                    key=f"rule_account_number_{key_prefix}"
                )
            
            # Usage unit
            col1, col2 = st.columns([1, 2])
            with col1:
                usage_unit_condition = st.selectbox(
                    "Condition",
                    ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                    key=f"usage_unit_condition_{key_prefix}"
                )
            with col2:
                usage_unit = st.selectbox(
                    "Usage unit",
                    ["kWh", "therms", "gallons", "cubic feet"],
                    index=0,
                    key=f"rule_usage_unit_{key_prefix}"
                )
            
            # Service type
            col1, col2 = st.columns([1, 2])
            with col1:
                service_type_condition = st.selectbox(
                    "Condition",
                    ["Exactly matches", "Contains", "Starts with", "Ends with", "Regex"],
                    key=f"service_type_condition_{key_prefix}"
                )
            with col2:
                service_type = st.selectbox(
                    "Service type",
                    ["Electric", "Gas", "Water", "Other"],
                    index=0,
                    key=f"rule_service_type_{key_prefix}"
                )
        
        st.markdown("---")
        
        # Then apply these actions section
        st.markdown("### ⚡ Then apply these actions...")
        
        # Charge name mapping
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("**Charge name mapping**")
        with col2:
            charge_name_mapping = st.text_input(
                "New charge name",
                value="CHP Rider Charge",
                key=f"rule_charge_name_mapping_{key_prefix}"
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
                key=f"rule_charge_category_{key_prefix}"
            )
        
        # Charge group heading
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("**Charge group heading**")
        with col2:
            charge_group_heading = st.text_input(
                "Group heading",
                value="Energy Charges",
                key=f"rule_charge_group_heading_{key_prefix}"
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
                key=f"rule_request_type_{key_prefix}"
            )
        
        st.markdown("---")
        
        # Action buttons with better spacing
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Cancel", key=f"cancel_rule_{key_prefix}", use_container_width=True):
                st.rerun()
        
        with col2:
            if st.button("🔍 Preview Changes", key=f"preview_changes_{key_prefix}", type="primary", use_container_width=True):
                # Create rule data for preview
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
                
                # Store rule data for preview and show preview
                st.session_state.rule_form_data = rule_data
                st.session_state.show_preview = True
                st.rerun()
        
        # Add some bottom spacing
        st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)


def render_preview_popup(data_provider: DataProvider, customer: str, key_prefix: str = "preview"):
    """
    Render the preview popup that shows rule summary and changes preview
    
    Args:
        data_provider: The data provider instance
        customer: The selected customer name
        key_prefix: Unique prefix for form keys to avoid duplicates
    """
    # Create the preview popover with enhanced styling
    with st.popover("🔍 Preview Changes", help="Review rule changes before saving", use_container_width=True):
        # Add some spacing and better visual separation
        st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)
        
        # Header with better styling
        st.markdown("## 🔍 Rule Preview")
        st.markdown("---")
        
        # Rule summary section
        st.markdown("### 📋 Rule Summary")
        rule_form_data = st.session_state.get('rule_form_data', {})
        
        # Create rule summary data
        rule_summary_data = {
            "Rule ID": ["New"],
            "Customer name": [rule_form_data.get('customer', 'AmerescoFTP')],
            "Priority order": ["Auto-assigned"],
            "Charge name mappi...": [rule_form_data.get('charge_name', 'CHP Rider')],
            "Charge ID": [rule_form_data.get('charge_name_mapping', 'NewBatch')],
            "Charge grou...": [rule_form_data.get('charge_group_heading', '')],
            "Charge category": [rule_form_data.get('charge_category', 'ch.usage_charge')]
        }
        
        # Display rule summary table with better styling
        rule_summary_df = pd.DataFrame(rule_summary_data)
        st.dataframe(
            rule_summary_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rule ID": st.column_config.TextColumn("Rule ID", width="small"),
                "Customer name": st.column_config.TextColumn("Customer name", width="medium"),
                "Priority order": st.column_config.TextColumn("Priority order", width="small"),
                "Charge name mappi...": st.column_config.TextColumn("Charge name mappi...", width="medium"),
                "Charge ID": st.column_config.TextColumn("Charge ID", width="medium"),
                "Charge grou...": st.column_config.TextColumn("Charge grou...", width="medium"),
                "Charge category": st.column_config.TextColumn("Charge category", width="medium")
            }
        )
        
        st.markdown("---")
        
        # Changes Preview section
        st.markdown("### 📊 Changes Preview")
        st.markdown("These changes will affect all the charges listed below. Review the changes before saving.")
        
        # Generate preview data based on the rule
        try:
            preview_data = generate_preview_data(st.session_state.rule_form_data)
        except Exception as e:
            st.error(f"Error generating preview data: {str(e)}")
            # Fallback to empty dataframe
            preview_data = pd.DataFrame()
        
        # Display the preview table with visual indicators for Current Charge ID
        if not preview_data.empty and 'Current Charge ID' in preview_data.columns:
            preview_data = preview_data.copy()
            preview_data['Current Charge ID'] = preview_data['Current Charge ID'].apply(
                lambda x: f"❌ {x}" if pd.notna(x) and str(x).strip() != '' else x
            )
        
        if not preview_data.empty:
            st.dataframe(
                preview_data,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Charge name": st.column_config.TextColumn("Charge name", width="medium"),
                    "Provider name": st.column_config.TextColumn("Provider name", width="medium"),
                    "Account number": st.column_config.TextColumn("Account number", width="medium"),
                    "Statement ID": st.column_config.TextColumn("Statement ID", width="medium"),
                    "Current Charge ID": st.column_config.TextColumn("Current Charge ID", width="medium", help="❌ indicates values that will be replaced"),
                    "New Charge ID": st.column_config.TextColumn("New Charge ID", width="medium"),
                    "Usage unit": st.column_config.TextColumn("Usage unit", width="small"),
                    "Service": st.column_config.TextColumn("Service", width="small")
                }
            )
        else:
            st.warning("No preview data available")
        
        st.markdown("---")
        
        # Bottom action bar with better styling
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            # Apply to existing charges checkbox
            apply_to_existing = st.checkbox(
                f"Apply rule to {len(preview_data) if not preview_data.empty else 0} existing charge(s)",
                value=True,
                key=f"apply_to_existing_{key_prefix}"
            )
        
        with col2:
            if st.button("❌ Cancel", key=f"cancel_preview_{key_prefix}", use_container_width=True):
                st.session_state.show_preview = False
                st.rerun()
        
        with col3:
            if st.button("💾 Save", key=f"save_rule_{key_prefix}", type="primary", use_container_width=True):
                # Save the rule using the stored form data
                if data_provider.create_rule(st.session_state.rule_form_data):
                    st.session_state.show_preview = False
                    st.success("✅ Rule saved successfully!")
                    st.rerun()
        
        # Add some bottom spacing
        st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True) 
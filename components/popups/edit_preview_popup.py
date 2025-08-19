"""
Edit Preview Popup Component

This module contains the edit preview popup that appears as a centrally located modal.
"""

import streamlit as st
from components.data.providers import DataProvider


def edit_preview_popup(data_provider: DataProvider, customer: str):
    """
    Render the edit preview popup as a centrally located modal
    
    Args:
        data_provider: The data provider instance
        customer: The selected customer name
    """
    # Create a very compact, centered popup container
    with st.container():
        # Create a centered column layout with wider width
        col1, col2, col3 = st.columns([3, 1, 3])
        
        with col2:
            # Very compact popup container with styling
            st.markdown("""
            <style>
            .popup-container {
                background-color: #0e1117;
                border: 2px solid #262730;
                border-radius: 8px;
                padding: 30px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
                max-width: 600px;
                margin: 20px auto;
                width: 100%;
            }
            .popup-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 1px solid #262730;
            }
            </style>
            """, unsafe_allow_html=True)
            
            with st.container():
                st.markdown('<div class="popup-container">', unsafe_allow_html=True)
                
                # Compact header with close button
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown("**Edit Rule Preview**")
                with col2:
                    if st.button("✖️", key="close_edit_preview_popup", help="Close popup"):
                        st.session_state.show_edit_preview = False
                        st.rerun()
                
                st.markdown("## 🔍 Edit Rule Preview")
                st.markdown("Review the changes before saving.")
                
                # Rule application settings
                st.markdown("### 📋 Application Settings")
                apply_to_existing = st.checkbox(
                    "Apply rule changes to existing charges",
                    value=True,
                    key="popup_apply_edit_to_existing_preview",
                    help="Apply these rule changes to existing charges that match the criteria"
                )
                
                st.markdown("---")
                
                # Navigation buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("← Back to Form", key="popup_back_to_edit_form_btn", help="Return to edit the rule"):
                        st.session_state.show_edit_preview = False
                        st.rerun()
                
                with col2:
                    if st.button("💾 Save Changes", key="popup_save_edit_rule_btn", type="primary", help="Save the rule changes and close form"):
                        # Save the rule changes using the stored form data
                        original_rule = st.session_state.get('selected_rule_for_edit', {})
                        rule_id = original_rule.get('Rule ID', 'unknown')
                        if data_provider.update_rule(rule_id, st.session_state.edit_rule_form_data):
                            st.session_state.show_edit_preview = False
                            st.session_state.show_edit_rule_modal = False
                            st.success("✅ Rule updated successfully!")
                            st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)

import pandas as pd
import streamlit as st

# Example: Load rules for a customer
@st.cache_data(ttl=60)
def load_rules(session, customer):
    query = f"""
        SELECT * EXCLUDE(is_approved, validated_at, validated_by, value),
               value AS CHARGE_CATEGORY
        FROM arcadia.lakehouse.f_uds_charge_mapping_rules
        WHERE customer_name = '{customer}'
          AND REQUEST_TYPE = 'RecategorizeCharge'
        QUALIFY ROW_NUMBER() OVER (PARTITION BY chips_business_rule_id ORDER BY PRIORITY_ORDER ASC) = 1
        ORDER BY PRIORITY_ORDER ASC;
    """
    df = session.sql(query).to_pandas()
    return df.reset_index(drop=True)

# Example: Writeback updated rules
def writeback_rules(session, updated_df):
    """Update priority order for existing rules"""
    try:
        # Convert DataFrame to Snowpark DataFrame
        snow_df = session.create_dataframe(updated_df)
        
        # Update the priority order in Snowflake
        update_query = f"""
        UPDATE arcadia.lakehouse.f_uds_charge_mapping_rules t
        SET priority_order = s.ORDER_INDEX
        FROM ({snow_df.to_pandas().to_sql('temp_updates', index=False)}) s
        WHERE t.chips_business_rule_id = s.CHIPS_BUSINESS_RULE_ID
        """
        session.sql(update_query).collect()
        return True
    except Exception as e:
        st.error(f"Error updating rules: {str(e)}")
        return False

# Example: Add new rules
def add_new_rules(session, new_rules_df):
    """Insert new charge mapping rules"""
    try:
        # Add required columns for new rules
        new_rules_df['is_approved'] = False
        new_rules_df['validated_at'] = None
        new_rules_df['validated_by'] = None
        new_rules_df['request_type'] = 'RecategorizeCharge'
        
        # Convert to Snowpark DataFrame and insert
        snow_df = session.create_dataframe(new_rules_df)
        snow_df.write.mode("append").save_as_table("arcadia.lakehouse.f_uds_charge_mapping_rules")
        return True
    except Exception as e:
        st.error(f"Error adding new rules: {str(e)}")
        return False

# Example: Approve rules
def approve_rules(session, rule_ids):
    """Approve selected rules"""
    try:
        rule_ids_str = "', '".join(rule_ids)
        approve_query = f"""
        UPDATE arcadia.lakehouse.f_uds_charge_mapping_rules
        SET is_approved = TRUE,
            validated_at = CURRENT_TIMESTAMP(),
            validated_by = CURRENT_USER()
        WHERE chips_business_rule_id IN ('{rule_ids_str}')
        """
        session.sql(approve_query).collect()
        return True
    except Exception as e:
        st.error(f"Error approving rules: {str(e)}")
        return False 
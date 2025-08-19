#!/usr/bin/env python3
"""
Test script to verify Snowflake connection and check updated data
"""

import os
import pandas as pd
from snowflake.snowpark.session import Session

def get_snowflake_session():
    """Create Snowflake session"""
    connection_parameters = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "authenticator": os.getenv("SNOWFLAKE_AUTHENTICATOR", "externalbrowser"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "RD_ORG_WH"),
        "database": os.getenv("SNOWFLAKE_DATABASE", "SANDBOX"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA", "BMANOJKUMAR"),
        "role": os.getenv("SNOWFLAKE_ROLE", "RD_ORG_READ")
    }
    
    return Session.builder.configs(connection_parameters).create()

def test_connection():
    """Test Snowflake connection and check data"""
    print("🔍 Testing Snowflake connection...")
    
    try:
        # Create session
        session = get_snowflake_session()
        print("✅ Connected to Snowflake successfully!")
        
        # Test query to check the updated rule
        print("\n📊 Checking the updated rule (ID: 8912000)...")
        result = session.sql("""
            SELECT CHIPS_BUSINESS_RULE_ID, charge_category, charge_name_mapping
            FROM RULES 
            WHERE CHIPS_BUSINESS_RULE_ID = 8912000
        """).collect()
        
        if result:
            rule = result[0]
            print(f"✅ Found rule 8912000:")
            print(f"   - Charge Category: {rule['CHARGE_CATEGORY']}")
            print(f"   - Charge Name Mapping: {rule['CHARGE_NAME_MAPPING']}")
        else:
            print("❌ Rule 8912000 not found")
        
        # Check total rules count
        print("\n📊 Checking total rules count...")
        count_result = session.sql("SELECT COUNT(*) as count FROM RULES").collect()
        print(f"✅ Total rules in database: {count_result[0]['COUNT']}")
        
        # Check a few sample rules
        print("\n📊 Sample rules from database:")
        sample_rules = session.sql("""
            SELECT CHIPS_BUSINESS_RULE_ID, charge_category, charge_name_mapping
            FROM RULES 
            ORDER BY CHIPS_BUSINESS_RULE_ID
            LIMIT 5
        """).collect()
        
        for rule in sample_rules:
            print(f"   - Rule {rule['CHIPS_BUSINESS_RULE_ID']}: {rule['CHARGE_CATEGORY']}")
        
        print("\n✅ Snowflake connection test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_connection()


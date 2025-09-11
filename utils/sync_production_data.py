#!/usr/bin/env python3
"""
Replicate Production Tables to Sandbox Schema

This script copies production data to SANDBOX.BMANOJKUMAR.* tables with:
- 100 records maximum
- Organization ID = 75 (AmerescoFTP-Test) if applicable
- Same table structure as production
"""

import os
import sys
import pandas as pd
from config import get_snowflake_session
import streamlit as st

def replicate_charges_table(session):
    """Replicate charges table from production"""
    print("🔄 Replicating charges table...")
    
    # Source: Production charges table
    source_query = """
    SELECT *
    FROM arcadia.export.hex_uc_charge_mapping_delivery
    WHERE ODIN_ORGANIZATION_ID = '75'
    LIMIT 100
    """
    
    try:
        # Get data from production
        print("📥 Fetching data from production table...")
        source_df = session.sql(source_query).to_pandas()
        print(f"✅ Found {len(source_df)} records in production")
        
        if source_df.empty:
            print("⚠️  No records found for ODIN_ORGANIZATION_ID = '75'")
            return False
        
        # Create target table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS SANDBOX.BMANOJKUMAR.hex_uc_charge_mapping_delivery AS
        SELECT * FROM arcadia.export.hex_uc_charge_mapping_delivery
        WHERE 1=0  -- Create empty table with same structure
        """
        
        print("🏗️  Creating target table structure...")
        session.sql(create_table_query).collect()
        
        # Clear existing data
        print("🧹 Clearing existing data...")
        session.sql("DELETE FROM SANDBOX.BMANOJKUMAR.hex_uc_charge_mapping_delivery").collect()
        
        # Insert new data
        print("📤 Inserting new data...")
        # Convert DataFrame to Snowpark DataFrame and write to table
        snowpark_df = session.create_dataframe(source_df)
        snowpark_df.write.mode("append").save_as_table("SANDBOX.BMANOJKUMAR.hex_uc_charge_mapping_delivery")
        
        print(f"✅ Successfully replicated {len(source_df)} charge records")
        return True
        
    except Exception as e:
        print(f"❌ Error replicating charges table: {str(e)}")
        return False

def replicate_customer_rules_table(session):
    """Replicate customer rules table from production"""
    print("🔄 Replicating customer rules table...")
    
    # Source: Production customer rules table (use CUSTOMER_NAME instead of ODIN_ORGANIZATION_ID)
    source_query = """
    SELECT *
    FROM arcadia.lakehouse.f_combined_customer_charge_rules
    WHERE CUSTOMER_NAME LIKE '%AmerescoFTP%'
    LIMIT 100
    """
    
    try:
        # Get data from production
        print("📥 Fetching customer rules from production...")
        source_df = session.sql(source_query).to_pandas()
        print(f"✅ Found {len(source_df)} customer rules in production")
        
        # Create target table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS SANDBOX.BMANOJKUMAR.f_combined_customer_charge_rules AS
        SELECT * FROM arcadia.lakehouse.f_combined_customer_charge_rules
        WHERE 1=0  -- Create empty table with same structure
        """
        
        print("🏗️  Creating customer rules table structure...")
        session.sql(create_table_query).collect()
        
        # Clear existing data
        print("🧹 Clearing existing customer rules...")
        session.sql("DELETE FROM SANDBOX.BMANOJKUMAR.f_combined_customer_charge_rules").collect()
        
        # Insert new data if any
        if not source_df.empty:
            print("📤 Inserting customer rules...")
            snowpark_df = session.create_dataframe(source_df)
            snowpark_df.write.mode("append").save_as_table("SANDBOX.BMANOJKUMAR.f_combined_customer_charge_rules")
            print(f"✅ Successfully replicated {len(source_df)} customer rules")
        else:
            print("ℹ️  No customer rules found for ODIN_ORGANIZATION_ID = '75'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error replicating customer rules table: {str(e)}")
        return False

def replicate_global_rules_table(session):
    """Replicate global rules table from production"""
    print("🔄 Replicating global rules table...")
    
    # Source: Production global rules table (no organization filtering for global rules)
    source_query = """
    SELECT *
    FROM arcadia.lakehouse.f_combined_provider_template_charge_rules
    WHERE IS_ENABLED = TRUE
    LIMIT 100
    """
    
    try:
        # Get data from production
        print("📥 Fetching global rules from production...")
        source_df = session.sql(source_query).to_pandas()
        print(f"✅ Found {len(source_df)} global rules in production")
        
        # Create target table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS SANDBOX.BMANOJKUMAR.f_combined_provider_template_charge_rules AS
        SELECT * FROM arcadia.lakehouse.f_combined_provider_template_charge_rules
        WHERE 1=0  -- Create empty table with same structure
        """
        
        print("🏗️  Creating global rules table structure...")
        session.sql(create_table_query).collect()
        
        # Clear existing data
        print("🧹 Clearing existing global rules...")
        session.sql("DELETE FROM SANDBOX.BMANOJKUMAR.f_combined_provider_template_charge_rules").collect()
        
        # Insert new data
        if not source_df.empty:
            print("📤 Inserting global rules...")
            snowpark_df = session.create_dataframe(source_df)
            snowpark_df.write.mode("append").save_as_table("SANDBOX.BMANOJKUMAR.f_combined_provider_template_charge_rules")
            print(f"✅ Successfully replicated {len(source_df)} global rules")
        else:
            print("⚠️  No global rules found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error replicating global rules table: {str(e)}")
        return False

def verify_tables(session):
    """Verify the replicated tables"""
    print("🔍 Verifying replicated tables...")
    
    tables_to_check = [
        "SANDBOX.BMANOJKUMAR.hex_uc_charge_mapping_delivery",
        "SANDBOX.BMANOJKUMAR.f_combined_customer_charge_rules", 
        "SANDBOX.BMANOJKUMAR.f_combined_provider_template_charge_rules"
    ]
    
    for table in tables_to_check:
        try:
            count_query = f"SELECT COUNT(*) as count FROM {table}"
            result = session.sql(count_query).collect()
            count = result[0][0] if result else 0
            print(f"✅ {table}: {count} records")
        except Exception as e:
            print(f"❌ {table}: Error - {str(e)}")

def main():
    """Main replication function"""
    print("🚀 Starting production table replication...")
    print("=" * 60)
    
    try:
        # Get Snowflake session
        session = get_snowflake_session()
        print("✅ Connected to Snowflake")
        
        # Verify we're connected to SANDBOX
        current_db = session.sql("SELECT CURRENT_DATABASE()").collect()[0][0]
        if current_db != "SANDBOX":
            print(f"❌ Error: Connected to {current_db}, but expected SANDBOX")
            print("Please ensure your Snowflake connection is configured for SANDBOX database")
            return False
        
        print(f"✅ Confirmed connection to {current_db} database")
        
        # Replicate all tables
        success = True
        
        success &= replicate_charges_table(session)
        success &= replicate_customer_rules_table(session)
        success &= replicate_global_rules_table(session)
        
        if success:
            print("\n🔍 Verification:")
            verify_tables(session)
            
            print("\n" + "=" * 60)
            print("✅ Table replication completed successfully!")
            print("\n📋 Next steps:")
            print("   1. Update data provider configuration to use local tables")
            print("   2. Test the application with replicated data")
            print("   3. Verify all functionality works with local tables")
            return True
        else:
            print("\n❌ Some tables failed to replicate")
            return False
            
    except Exception as e:
        print(f"❌ Error during replication: {str(e)}")
        return False

if __name__ == "__main__":
    main()

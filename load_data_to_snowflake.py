#!/usr/bin/env python3
"""
Load CSV data into Snowflake tables
"""

import pandas as pd
import os
from snowflake.snowpark.session import Session
from snowflake.snowpark.types import StructType, StructField, StringType, IntegerType, FloatType, DateType

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

def load_charges_data(session):
    """Load charges data"""
    print("📊 Loading charges data...")
    
    # Read CSV file
    df = pd.read_csv('database/charges.csv')
    
    # Convert to Snowpark DataFrame
    snow_df = session.create_dataframe(df)
    
    # Write to Snowflake
    snow_df.write.mode("overwrite").save_as_table("CHARGES")
    
    print(f"✅ Loaded {len(df)} charges records")

def load_rules_data(session):
    """Load rules data"""
    print("📊 Loading rules data...")
    
    # Read CSV file
    df = pd.read_csv('database/rules.csv')
    
    # Convert to Snowpark DataFrame
    snow_df = session.create_dataframe(df)
    
    # Write to Snowflake
    snow_df.write.mode("overwrite").save_as_table("RULES")
    
    print(f"✅ Loaded {len(df)} rules records")

def load_processed_files_data(session):
    """Load processed files data"""
    print("📊 Loading processed files data...")
    
    # Read CSV file
    df = pd.read_csv('database/processed_files.csv')
    
    # Convert to Snowpark DataFrame
    snow_df = session.create_dataframe(df)
    
    # Write to Snowflake
    snow_df.write.mode("overwrite").save_as_table("PROCESSED_FILES")
    
    print(f"✅ Loaded {len(df)} processed files records")

def verify_data(session):
    """Verify data was loaded correctly"""
    print("\n🔍 Verifying data...")
    
    # Check charges
    charges_count = session.sql("SELECT COUNT(*) as count FROM CHARGES").collect()[0]['COUNT']
    print(f"📊 CHARGES table: {charges_count} records")
    
    # Check rules
    rules_count = session.sql("SELECT COUNT(*) as count FROM RULES").collect()[0]['COUNT']
    print(f"📊 RULES table: {rules_count} records")
    
    # Check processed files
    files_count = session.sql("SELECT COUNT(*) as count FROM PROCESSED_FILES").collect()[0]['COUNT']
    print(f"📊 PROCESSED_FILES table: {files_count} records")
    
    print("\n✅ Data verification complete!")

def main():
    """Main function"""
    print("🚀 Starting data load to Snowflake...")
    
    # Check if environment variables are set
    required_vars = ["SNOWFLAKE_ACCOUNT", "SNOWFLAKE_USER"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Please run: source setup_snowflake_env.sh")
        return
    
    try:
        # Create session
        session = get_snowflake_session()
        print("✅ Connected to Snowflake successfully!")
        
        # Load data
        load_charges_data(session)
        load_rules_data(session)
        load_processed_files_data(session)
        
        # Verify data
        verify_data(session)
        
        print("\n🎉 All data loaded successfully!")
        print("💡 You can now run: streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("💡 Please check your Snowflake credentials and connection")

if __name__ == "__main__":
    main()

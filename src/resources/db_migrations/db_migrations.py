import snowflake.connector
import sys

def get_snowflake_connection():
    """Establishes and returns a Snowflake connection."""
    try:
        # config.toml is expected to be in ~/.snowflake/config.toml
        conn = snowflake.connector.connect()
        print("Successfully connected to Snowflake.")
        return conn
    except Exception as e:
        print(f"ERROR: Failed to connect to Snowflake: {e}")
        sys.exit(1) # Exit with error code

def run_ddl_statement(cursor, ddl_statement: str) -> bool:
    """
    Executes a DDL statement and returns True if successful, False otherwise.
    
    Args:
        cursor: Snowflake cursor
        ddl_statement: The DDL statement to execute
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor.execute(ddl_statement)
        print(f"Successfully executed: {ddl_statement[:50]}...")
        return True
    except Exception as e:
        print(f"ERROR executing DDL: {e}")
        print(f"DDL Statement: {ddl_statement}")
        return False

def create_schemas(connection):
    """Create necessary schemas for the CMPS application."""
    cursor = connection.cursor()
    
    # Create schemas if they don't exist
    schemas = [
        "SANDBOX.BMANOJKUMAR",
        "APPLICATIONS.CMPS"
    ]
    
    for schema in schemas:
        database, schema_name = schema.split('.')
        create_schema_sql = f"""
        CREATE SCHEMA IF NOT EXISTS {database}.{schema_name}
        """
        if not run_ddl_statement(cursor, create_schema_sql):
            cursor.close()
            sys.exit(1)
    
    cursor.close()

def run_migrations(connection):
    """Run all database migrations for CMPS application."""
    cursor = connection.cursor()
    
    # Create tables for CMPS application
    tables = [
        # Charges table
        """
        CREATE TABLE IF NOT EXISTS SANDBOX.BMANOJKUMAR.CHARGES (
            CHIPS_BUSINESS_RULE_ID NUMBER,
            CUSTOMER_NAME VARCHAR(255),
            PRIORITY_ORDER NUMBER,
            CHARGE_NAME_MAPPING VARCHAR(255),
            CHARGE_ID VARCHAR(50),
            CHARGE_GROUP_HEADING VARCHAR(255),
            CHARGE_CATEGORY VARCHAR(100),
            REQUEST_TYPE NUMBER,
            CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
            UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
        """,
        
        # Rules table
        """
        CREATE TABLE IF NOT EXISTS SANDBOX.BMANOJKUMAR.RULES (
            CHIPS_BUSINESS_RULE_ID NUMBER,
            CUSTOMER_NAME VARCHAR(255),
            PRIORITY_ORDER NUMBER,
            CHARGE_NAME_MAPPING VARCHAR(255),
            CHARGE_ID VARCHAR(50),
            CHARGE_GROUP_HEADING VARCHAR(255),
            CHARGE_CATEGORY VARCHAR(100),
            REQUEST_TYPE NUMBER,
            CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
            UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
        """,
        
        # Processed Files table
        """
        CREATE TABLE IF NOT EXISTS SANDBOX.BMANOJKUMAR.PROCESSED_FILES (
            FILE_ID NUMBER,
            FILE_NAME VARCHAR(255),
            PROCESSED_DATE TIMESTAMP_NTZ,
            STATUS VARCHAR(50),
            CUSTOMER_NAME VARCHAR(255),
            CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
        """,
        
        # Production tables in APPLICATIONS.CMPS schema
        """
        CREATE TABLE IF NOT EXISTS APPLICATIONS.CMPS.CHARGES (
            CHIPS_BUSINESS_RULE_ID NUMBER,
            CUSTOMER_NAME VARCHAR(255),
            PRIORITY_ORDER NUMBER,
            CHARGE_NAME_MAPPING VARCHAR(255),
            CHARGE_ID VARCHAR(50),
            CHARGE_GROUP_HEADING VARCHAR(255),
            CHARGE_CATEGORY VARCHAR(100),
            REQUEST_TYPE NUMBER,
            CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
            UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
        """,
        
        """
        CREATE TABLE IF NOT EXISTS APPLICATIONS.CMPS.RULES (
            CHIPS_BUSINESS_RULE_ID NUMBER,
            CUSTOMER_NAME VARCHAR(255),
            PRIORITY_ORDER NUMBER,
            CHARGE_NAME_MAPPING VARCHAR(255),
            CHARGE_ID VARCHAR(50),
            CHARGE_GROUP_HEADING VARCHAR(255),
            CHARGE_CATEGORY VARCHAR(100),
            REQUEST_TYPE NUMBER,
            CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
            UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
        """,
        
        """
        CREATE TABLE IF NOT EXISTS APPLICATIONS.CMPS.PROCESSED_FILES (
            FILE_ID NUMBER,
            FILE_NAME VARCHAR(255),
            PROCESSED_DATE TIMESTAMP_NTZ,
            STATUS VARCHAR(50),
            CUSTOMER_NAME VARCHAR(255),
            CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
        """
    ]
    
    for table_sql in tables:
        if not run_ddl_statement(cursor, table_sql):
            cursor.close()
            sys.exit(1)
    
    cursor.close()

if __name__ == "__main__":
    conn = get_snowflake_connection()
    try:
        create_schemas(conn)
        run_migrations(conn)
        print("All database operations completed successfully.")
    finally:
        if conn:
            conn.close()
            print("Snowflake connection closed.")


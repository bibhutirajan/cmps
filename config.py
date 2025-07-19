import os
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.session import Session

def get_snowflake_session():
    """Get Snowflake session - works for both local and Snowflake Native Streamlit"""
    try:
        # Try to get active session (works in Snowflake Native Streamlit)
        return get_active_session()
    except:
        # Fall back to local connection (for local development)
        return get_local_snowflake_session()

def get_local_snowflake_session():
    """Create a local Snowflake session for development"""
    # Base connection parameters
    connection_parameters = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT", "your_account"),
        "user": os.getenv("SNOWFLAKE_USER", "your_username"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        "database": os.getenv("SNOWFLAKE_DATABASE", "arcadia"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA", "lakehouse"),
        "role": os.getenv("SNOWFLAKE_ROLE", "your_role")
    }
    
    # Check if private key authentication is configured
    private_key_path = os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH")
    private_key_passphrase = os.getenv("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE")
    
    if private_key_path and os.path.exists(private_key_path):
        # Use private key authentication
        try:
            with open(private_key_path, 'rb') as key_file:
                private_key = key_file.read()
            
            connection_parameters.update({
                "private_key": private_key,
                "private_key_passphrase": private_key_passphrase
            })
        except Exception as e:
            print(f"Warning: Could not read private key from {private_key_path}: {e}")
            # Fall back to password authentication
            connection_parameters["password"] = os.getenv("SNOWFLAKE_PASSWORD", "your_password")
    else:
        # Use password authentication
        connection_parameters["password"] = os.getenv("SNOWFLAKE_PASSWORD", "your_password")
    
    return Session.builder.configs(connection_parameters).create() 
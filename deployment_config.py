"""
Deployment Configuration for Charge Mapping Application

This file provides easy configuration for different deployment scenarios:
1. Local Development (Demo Mode)
2. Snowflake Native App
3. External Hosting with Snowflake
"""

import os
from typing import Dict, Any

class DeploymentConfig:
    """Configuration class for different deployment scenarios"""
    
    @staticmethod
    def get_local_dev_config() -> Dict[str, Any]:
        """Configuration for local development with demo data"""
        return {
            "DATA_SOURCE": "demo",
            "SNOWFLAKE_ENABLED": "false",
            "SIDEBAR_COLLAPSED": "true",
            "DARK_THEME": "true"
        }
    
    @staticmethod
    def get_snowflake_native_config() -> Dict[str, Any]:
        """Configuration for Snowflake Native App deployment"""
        return {
            "DATA_SOURCE": "snowflake",
            "SNOWFLAKE_ENABLED": "true",
            "SNOWFLAKE_DATABASE": "arcadia",
            "SNOWFLAKE_SCHEMA": "lakehouse", 
            "CHARGES_TABLE": "arcadia.export.hex_uc_charge_mapping_delivery",
            "RULES_CUSTOMER_TABLE": "arcadia.lakehouse.f_combined_customer_charge_rules",
            "RULES_PROVIDER_TABLE": "arcadia.lakehouse.f_combined_provider_template_charge_rules",
            "SIDEBAR_COLLAPSED": "true",
            "DARK_THEME": "false"
        }
    
    @staticmethod
    def get_snowflake_staging_config() -> Dict[str, Any]:
        """Configuration for Snowflake Staging deployment (BMANOJKUMAR.Sandbox.staging)"""
        return {
            "DATA_SOURCE": "snowflake",
            "SNOWFLAKE_ENABLED": "true",
            "SNOWFLAKE_DATABASE": "BMANOJKUMAR",
            "SNOWFLAKE_SCHEMA": "SANDBOX",
            "CHARGES_TABLE": "arcadia.export.hex_uc_charge_mapping_delivery",
            "RULES_CUSTOMER_TABLE": "arcadia.lakehouse.f_combined_customer_charge_rules", 
            "RULES_PROVIDER_TABLE": "arcadia.lakehouse.f_combined_provider_template_charge_rules",
            "SIDEBAR_COLLAPSED": "true",
            "DARK_THEME": "false"
        }
    
    @staticmethod
    def get_external_hosting_config() -> Dict[str, Any]:
        """Configuration for external hosting (Heroku, AWS, etc.)"""
        return {
            "DATA_SOURCE": "snowflake",
            "SNOWFLAKE_ENABLED": "true",
            "SNOWFLAKE_DATABASE": "arcadia",
            "SNOWFLAKE_SCHEMA": "lakehouse",
            "CHARGES_TABLE": "charges",
            "RULES_TABLE": "rules",
            "PROCESSED_FILES_TABLE": "processed_files",
            "SIDEBAR_COLLAPSED": "true",
            "DARK_THEME": "true"
        }
    
    @staticmethod
    def apply_config(config: Dict[str, Any]):
        """Apply configuration to environment variables"""
        for key, value in config.items():
            os.environ[key] = str(value)
    
    @staticmethod
    def setup_local_dev():
        """Setup for local development"""
        config = DeploymentConfig.get_local_dev_config()
        DeploymentConfig.apply_config(config)
        print("✅ Local development configuration applied (Demo Mode)")
    
    @staticmethod
    def setup_snowflake_native():
        """Setup for Snowflake Native App"""
        config = DeploymentConfig.get_snowflake_native_config()
        DeploymentConfig.apply_config(config)
        print("✅ Snowflake Native App configuration applied")
        print("⚠️  Make sure to set SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, etc.")
    
    @staticmethod
    def setup_snowflake_staging():
        """Setup for Snowflake Staging deployment"""
        config = DeploymentConfig.get_snowflake_staging_config()
        DeploymentConfig.apply_config(config)
        print("✅ Snowflake Staging configuration applied (BMANOJKUMAR.Sandbox.staging)")
        print("⚠️  Make sure Snowflake connection is configured for staging environment")
    
    @staticmethod
    def setup_external_hosting():
        """Setup for external hosting"""
        config = DeploymentConfig.get_external_hosting_config()
        DeploymentConfig.apply_config(config)
        print("✅ External hosting configuration applied")
        print("⚠️  Make sure to set SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, etc.")

def create_env_file(config_type: str = "local"):
    """Create a .env file for the specified configuration"""
    if config_type == "local":
        config = DeploymentConfig.get_local_dev_config()
    elif config_type == "snowflake":
        config = DeploymentConfig.get_snowflake_native_config()
    elif config_type == "external":
        config = DeploymentConfig.get_external_hosting_config()
    else:
        raise ValueError("config_type must be 'local', 'snowflake', or 'external'")
    
    with open(".env", "w") as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")
    
    print(f"✅ .env file created for {config_type} configuration")
    print("⚠️  Remember to add your Snowflake credentials manually for snowflake/external configs")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        config_type = sys.argv[1]
        if config_type in ["local", "snowflake", "external"]:
            create_env_file(config_type)
        else:
            print("Usage: python deployment_config.py [local|snowflake|external]")
    else:
        print("Available configurations:")
        print("1. local - Local development with demo data")
        print("2. snowflake - Snowflake Native App")
        print("3. external - External hosting with Snowflake")
        print("\nUsage: python deployment_config.py [local|snowflake|external]") 
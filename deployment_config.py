"""
Deployment Configuration for Charge Mapping Application

This file provides easy configuration for different deployment scenarios:
1. LOCAL - Local development with SANDBOX tables
2. SANDBOX - Sandbox environment with SANDBOX tables  
3. PRODUCTION - Production environment with ARCADIA tables

NOTE: Currently bypassing environment logic to always use PRODUCTION tables.
See data_providers.py _get_table_config() method for details.
"""

import os
from typing import Dict, Any

class DeploymentConfig:
    """Configuration class for different deployment scenarios"""
    
    @staticmethod
    def get_local_config() -> Dict[str, Any]:
        """Configuration for local development with SANDBOX tables"""
        return {
            "ENVIRONMENT": "LOCAL",
            "DATA_SOURCE": "snowflake",
            "SNOWFLAKE_ENABLED": "true",
            "SNOWFLAKE_DATABASE": "SANDBOX",
            "SNOWFLAKE_SCHEMA": "BMANOJKUMAR",
            "CHARGES_TABLE": "SANDBOX.BMANOJKUMAR.hex_uc_charge_mapping_delivery",
            "RULES_CUSTOMER_TABLE": "SANDBOX.BMANOJKUMAR.f_combined_customer_charge_rules",
            "RULES_GLOBAL_TABLE": "SANDBOX.BMANOJKUMAR.f_combined_provider_template_charge_rules",
            "SIDEBAR_COLLAPSED": "true",
            "DARK_THEME": "true"
        }
    
    @staticmethod
    def get_sandbox_config() -> Dict[str, Any]:
        """Configuration for SANDBOX environment"""
        return {
            "ENVIRONMENT": "SANDBOX",
            "DATA_SOURCE": "snowflake",
            "SNOWFLAKE_ENABLED": "true",
            "SNOWFLAKE_DATABASE": "SANDBOX",
            "SNOWFLAKE_SCHEMA": "BMANOJKUMAR",
            "CHARGES_TABLE": "SANDBOX.BMANOJKUMAR.hex_uc_charge_mapping_delivery",
            "RULES_CUSTOMER_TABLE": "SANDBOX.BMANOJKUMAR.f_combined_customer_charge_rules",
            "RULES_GLOBAL_TABLE": "SANDBOX.BMANOJKUMAR.f_combined_provider_template_charge_rules",
            "SIDEBAR_COLLAPSED": "true",
            "DARK_THEME": "true"
        }
    
    @staticmethod
    def get_production_config() -> Dict[str, Any]:
        """Configuration for PRODUCTION environment"""
        return {
            "ENVIRONMENT": "PRODUCTION",
            "DATA_SOURCE": "snowflake",
            "SNOWFLAKE_ENABLED": "true",
            "SNOWFLAKE_DATABASE": "arcadia",
            "SNOWFLAKE_SCHEMA": "lakehouse",
            "CHARGES_TABLE": "arcadia.export.hex_uc_charge_mapping_delivery",
            "RULES_CUSTOMER_TABLE": "arcadia.lakehouse.f_combined_customer_charge_rules",
            "RULES_GLOBAL_TABLE": "arcadia.lakehouse.f_combined_provider_template_charge_rules",
            "SIDEBAR_COLLAPSED": "true",
            "DARK_THEME": "true"
        }
    
    @staticmethod
    def apply_config(config: Dict[str, Any]):
        """Apply configuration to environment variables"""
        for key, value in config.items():
            os.environ[key] = str(value)
    
    @staticmethod
    def setup_local():
        """Setup for LOCAL environment (uses SANDBOX tables)"""
        config = DeploymentConfig.get_local_config()
        DeploymentConfig.apply_config(config)
        print("✅ LOCAL environment configuration applied (SANDBOX tables)")
        print("⚠️  Make sure Snowflake connection is configured for SANDBOX database")
    
    @staticmethod
    def setup_sandbox():
        """Setup for SANDBOX environment"""
        config = DeploymentConfig.get_sandbox_config()
        DeploymentConfig.apply_config(config)
        print("✅ SANDBOX environment configuration applied")
        print("⚠️  Make sure Snowflake connection is configured for SANDBOX database")
    
    @staticmethod
    def setup_production():
        """Setup for PRODUCTION environment"""
        config = DeploymentConfig.get_production_config()
        DeploymentConfig.apply_config(config)
        print("✅ PRODUCTION environment configuration applied (ARCADIA tables)")
        print("⚠️  Make sure Snowflake connection is configured for ARCADIA database")
    
    @staticmethod
    def setup_snowflake_staging():
        """Setup for Snowflake staging/sandbox environment (legacy method)"""
        config = DeploymentConfig.get_sandbox_config()
        DeploymentConfig.apply_config(config)
        print("✅ Snowflake Staging configuration applied (SANDBOX.BMANOJKUMAR)")
        print("⚠️  Make sure Snowflake connection is configured for staging environment")

def create_env_file(config_type: str = "local"):
    """Create a .env file for the specified configuration"""
    if config_type == "local":
        config = DeploymentConfig.get_local_config()
    elif config_type == "sandbox":
        config = DeploymentConfig.get_sandbox_config()
    elif config_type == "production":
        config = DeploymentConfig.get_production_config()
    else:
        raise ValueError("config_type must be 'local', 'sandbox', or 'production'")
    
    with open(".env", "w") as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")
    
    print(f"✅ .env file created for {config_type.upper()} environment")
    print("⚠️  Remember to add your Snowflake credentials manually")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        config_type = sys.argv[1]
        if config_type in ["local", "sandbox", "production"]:
            create_env_file(config_type)
        else:
            print("Usage: python deployment_config.py [local|sandbox|production]")
    else:
        print("Available configurations:")
        print("1. local - Local development with SANDBOX tables")
        print("2. sandbox - SANDBOX environment with SANDBOX tables")
        print("3. production - PRODUCTION environment with ARCADIA tables")
        print("\nUsage: python deployment_config.py [local|sandbox|production]") 
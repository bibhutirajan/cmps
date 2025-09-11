#!/usr/bin/env python3
"""
Configure Application to Use Local Sandbox Tables

This script updates the data provider configuration to use replicated tables
in SANDBOX.BMANOJKUMAR.* instead of production tables.
"""

import os

def configure_for_local():
    """Configure environment for LOCAL (uses SANDBOX tables)"""
    print("⚙️  Configuring application for LOCAL environment...")
    
    from deployment_config import DeploymentConfig
    DeploymentConfig.setup_local()
    
    print("\n✅ Configuration updated for LOCAL environment")
    print("📋 Using SANDBOX tables:")
    print("   • Charges: SANDBOX.BMANOJKUMAR.hex_uc_charge_mapping_delivery")
    print("   • Customer Rules: SANDBOX.BMANOJKUMAR.f_combined_customer_charge_rules")
    print("   • Global Rules: SANDBOX.BMANOJKUMAR.f_combined_provider_template_charge_rules")

def configure_for_sandbox():
    """Configure environment for SANDBOX"""
    print("⚙️  Configuring application for SANDBOX environment...")
    
    from deployment_config import DeploymentConfig
    DeploymentConfig.setup_sandbox()
    
    print("\n✅ Configuration updated for SANDBOX environment")
    print("📋 Using SANDBOX tables:")
    print("   • Charges: SANDBOX.BMANOJKUMAR.hex_uc_charge_mapping_delivery")
    print("   • Customer Rules: SANDBOX.BMANOJKUMAR.f_combined_customer_charge_rules")
    print("   • Global Rules: SANDBOX.BMANOJKUMAR.f_combined_provider_template_charge_rules")

def configure_for_production():
    """Configure environment for PRODUCTION"""
    print("⚙️  Configuring application for PRODUCTION environment...")
    
    from deployment_config import DeploymentConfig
    DeploymentConfig.setup_production()
    
    print("\n✅ Configuration updated for PRODUCTION environment")
    print("📋 Using ARCADIA tables:")
    print("   • Charges: arcadia.export.hex_uc_charge_mapping_delivery")
    print("   • Customer Rules: arcadia.lakehouse.f_combined_customer_charge_rules")
    print("   • Global Rules: arcadia.lakehouse.f_combined_provider_template_charge_rules")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "local":
            configure_for_local()
        elif mode == "sandbox":
            configure_for_sandbox()
        elif mode == "production":
            configure_for_production()
        else:
            print("Usage: python configure_local_tables.py [local|sandbox|production]")
            print("  local      - LOCAL environment (uses SANDBOX tables)")
            print("  sandbox    - SANDBOX environment (uses SANDBOX tables)")
            print("  production - PRODUCTION environment (uses ARCADIA tables)")
    else:
        print("Available configurations:")
        print("1. local      - LOCAL environment (uses SANDBOX tables)")
        print("2. sandbox    - SANDBOX environment (uses SANDBOX tables)")
        print("3. production - PRODUCTION environment (uses ARCADIA tables)")
        print("\nUsage: python configure_local_tables.py [local|sandbox|production]")

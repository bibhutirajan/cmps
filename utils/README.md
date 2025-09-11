# Utils Package

This package contains utility scripts for the Charge Mapping Application.

## Available Utilities

### 1. `setup_environment.py`
**Purpose**: Configure environment variables for different deployment scenarios

**Usage**:
```bash
# Configure for local development
python utils/setup_environment.py local

# Configure for sandbox environment  
python utils/setup_environment.py sandbox

# Configure for production environment
python utils/setup_environment.py production
```

**What it does**:
- Sets environment variables for database connections
- Configures table names based on environment
- Applies UI settings (sidebar, theme)

### 2. `sync_production_data.py`
**Purpose**: Synchronize production data to local sandbox schema

**Usage**:
```bash
# Sync production data to SANDBOX.BMANOJKUMAR schema
python utils/sync_production_data.py
```

**What it does**:
- Replicates production tables to local sandbox
- Fetches 100 records for testing
- Creates tables: `hex_uc_charge_mapping_delivery`, `f_combined_customer_charge_rules`, `f_combined_provider_template_charge_rules`

## Best Practices

- All utilities follow Python best practices
- Environment-based configuration
- Error handling and logging
- Clear documentation and usage examples
- Native Streamlit compatibility

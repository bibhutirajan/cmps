# Deployment Guide

## 🏗️ Environment Overview

| Environment | Authentication | Database | Deployment Method |
|-------------|----------------|----------|-------------------|
| **LOCAL** | External Browser | SANDBOX | `./bin/start_streamlit.sh` |
| **SANDBOX** | External Browser | SANDBOX | `./bin/deploy_to_sandbox.sh` |
| **PRODUCTION** | Private Key | APPLICATIONS | GitHub Actions CI/CD |

## 🚀 Quick Start

### Local Development
```bash
# 1. Setup Snowflake configuration
./setup_snowflake_config.sh

# 2. Start the application
./bin/start_streamlit.sh

# 3. Access at http://localhost:8501
```

### Sandbox Deployment

**Option 1: Shell Script (Recommended)**
```bash
# Simple deployment with database verification
./bin/deploy_to_sandbox.sh
```

**Option 2: Python Script (Detailed logging)**
```bash
# Deployment with verbose output and URL retrieval
python deploy_to_snowflake_sandbox.py
```

**Verify deployment:**
```bash
snow streamlit list
snow streamlit get-url charge-mapping
```

### Production Deployment
Production deployment is automated via **GitHub Actions CI/CD** when code is pushed to main branch.

**Manual deployment (if needed):**
```bash
./setup_private_key_auth.sh
snow streamlit deploy charge-mapping_prod --replace
```

## 🔐 Authentication

### External Browser (Local/Sandbox)
```toml
# ~/.snowflake/config.toml
[connections.default]
account = "your-account"
user = "your-username"
authenticator = "externalbrowser"
database = "SANDBOX"
schema = "BMANOJKUMAR"
```

### Private Key (Production)
```bash
# Setup private key authentication
./setup_private_key_auth.sh

# Verify connection
snow connection test --connection production
```

For detailed private key setup, see [PRIVATE_KEY_AUTH_IMPLEMENTATION.md](./PRIVATE_KEY_AUTH_IMPLEMENTATION.md)

## 📊 Data Sources

- **Production**: `arcadia.export.hex_uc_charge_mapping_delivery`
- **Sandbox**: `SANDBOX.BMANOJKUMAR.charges`
- **Demo**: In-memory sample data for offline development

## 🛠️ Utility Scripts

The `utils/` folder contains helpful scripts for development and deployment:

### Environment Configuration
```bash
# Configure for different environments
python utils/setup_environment.py local     # Local development
python utils/setup_environment.py sandbox   # Sandbox environment  
python utils/setup_environment.py production # Production environment
```

### Data Synchronization
```bash
# Sync production data to local sandbox
python utils/sync_production_data.py
```

For more details, see [utils/README.md](./utils/README.md)

## 🐛 Troubleshooting

### Common Issues
- **Port 8501 in use**: `pkill -f streamlit`
- **Authentication failed**: Check `~/.snowflake/config.toml` credentials  
- **Deployment errors**: Verify Snowflake CLI with `snow --version`

### Logs
```bash
# Local logs
tail -f streamlit.log

# Snowflake app logs  
snow streamlit logs charge-mapping
```

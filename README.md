# Charge Mapping Application

A modern **Streamlit application** for managing charge mapping rules with seamless **Snowflake integration**.

## ✨ Features

- **📊 Interactive Data Management** - View and manage charge mapping rules
- **🎯 Smart Rule Creation** - Create custom mapping rules with preview  
- **🔍 Advanced Filtering** - Filter charges by multiple criteria
- **☁️ Snowflake Integration** - Production and sandbox data sources
- **🎨 Modern UI** - Clean interface with dark theme sidebar

## 🚀 Quick Start

```bash
# 1. Setup Snowflake configuration
./setup_snowflake_config.sh

# 2. Start the application
./bin/start_streamlit.sh

# 3. Open browser to http://localhost:8501
```

**Deploy to Sandbox:**
```bash
# Recommended: Simple deployment
./bin/deploy_to_sandbox.sh

# Alternative: Detailed logging
python deploy_to_snowflake_sandbox.py
```

For detailed deployment instructions, see **[DEPLOYMENT.md](./DEPLOYMENT.md)**

## 🏗️ Architecture

**Modular Streamlit Application** following clean architecture principles:

- **`main.py`** - Main Streamlit application entry point
- **`components/`** - Modular UI components (dialogs, tabs, data providers)  
- **`config.py`** - Snowflake connection and environment management
- **`utils/`** - Utility scripts for environment setup and data sync
- **`static/css/`** - Custom styling and theme
- **`bin/`** - Deployment and setup scripts

## 🌍 Environments

| Environment | Authentication | Deployment |
|-------------|----------------|------------|
| **LOCAL** | External Browser | `./bin/start_streamlit.sh` |
| **SANDBOX** | External Browser | `./bin/deploy_to_sandbox.sh` |
| **PRODUCTION** | Private Key | GitHub Actions CI/CD |

## 📋 Requirements

- **Python 3.9+** with Streamlit 1.44.1+
- **Snowflake account** with appropriate permissions
- **Snowflake CLI** configured (`snow --version`)

## 📊 Data Sources

- **Production**: `arcadia.export.hex_uc_charge_mapping_delivery`
- **Sandbox**: `SANDBOX.BMANOJKUMAR.charges`
- **Demo**: In-memory sample data for offline development

## 🛠️ Development

### Best Practices
- **Modular architecture** with clear separation of concerns
- **`@st.cache_data`** for expensive operations  
- **`@st.dialog`** decorator for modal dialogs
- **Clean component boundaries** and proper error handling

### Contributing
1. Follow **Python PEP 8** style guidelines
2. Test changes in **sandbox** environment first
3. Update documentation for new features

## 🐛 Troubleshooting

**Common Issues:**
- **Port conflicts**: `pkill -f streamlit`
- **Authentication**: Check `~/.snowflake/config.toml`  
- **Dependencies**: `pip install -r requirements.txt`

For detailed troubleshooting, see **[DEPLOYMENT.md](./DEPLOYMENT.md)**
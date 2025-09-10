#!/bin/bash

# Snowflake Environment Setup Script
# Replace the values below with your actual Snowflake credentials

echo "Setting up Snowflake environment variables..."

# Export Snowflake configuration
export SNOWFLAKE_ENABLED=true
export SNOWFLAKE_ACCOUNT="KDA03952-FGA72401"        # Your Snowflake account
export SNOWFLAKE_USER="BIBHUTIRAJANMANOJKUMAR"      # Your username
export SNOWFLAKE_AUTHENTICATOR="externalbrowser"    # Browser-based authentication
export SNOWFLAKE_WAREHOUSE="RD_ORG_WH"              # Your warehouse
export SNOWFLAKE_DATABASE="SANDBOX"
export SNOWFLAKE_SCHEMA="BMANOJKUMAR"
export SNOWFLAKE_ROLE="RD_ORG_READ"                 # Your role

# Application configuration
export DATA_SOURCE=snowflake
export SIDEBAR_COLLAPSED=true
export DARK_THEME=true

echo "✅ Snowflake environment variables set!"
echo ""
echo "📋 Next steps:"
echo "1. Edit this script and replace the placeholder values with your actual Snowflake credentials"
echo "2. Run: source setup_snowflake_env.sh"
echo "3. Run: streamlit run main.py"
echo ""
echo "✅ Configuration set for external browser authentication!"
echo "🌐 When you run the application, it will open your browser for authentication."

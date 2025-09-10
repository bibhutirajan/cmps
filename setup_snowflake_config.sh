#!/bin/bash

# Setup script for Snowflake configuration file
# This script helps set up the ~/.snowflake/config.toml file

echo "🔧 Setting up Snowflake configuration file..."

# Create .snowflake directory if it doesn't exist
SNOWFLAKE_DIR="$HOME/.snowflake"
if [ ! -d "$SNOWFLAKE_DIR" ]; then
    mkdir -p "$SNOWFLAKE_DIR"
    echo "✅ Created directory: $SNOWFLAKE_DIR"
fi

# Copy the configuration file
CONFIG_FILE="$SNOWFLAKE_DIR/config.toml"
cp snowflake_config.toml "$CONFIG_FILE"

echo "✅ Copied configuration file to: $CONFIG_FILE"

# Set proper permissions
chmod 600 "$CONFIG_FILE"
echo "✅ Set proper permissions (600) on config file"

echo ""
echo "📝 Configuration options:"
echo ""
echo "1. **Browser Authentication (Default)**:"
echo "   - Uses the [connections.default] section"
echo "   - Authenticates via browser/SSO"
echo "   - Ready to use immediately"
echo ""
echo "2. **Private Key Authentication**:"
echo "   - Edit $CONFIG_FILE"
echo "   - Uncomment the [connections.private_key] section"
echo "   - Update the private_key_file path if needed"
echo "   - Set the correct passphrase"
echo "   - Comment out the [connections.default] section"
echo ""
echo "3. **Switch between methods**:"
echo "   - Edit $CONFIG_FILE to enable/disable sections"
echo "   - Restart the application"
echo ""
echo "🔐 Current configuration:"
echo "   - Account: KDA03952-FGA72401"
echo "   - User: BIBHUTIRAJANMANOJKUMAR"
echo "   - Database: SANDBOX"
echo "   - Schema: BMANOJKUMAR"
echo "   - Role: RD_ORG_READ"
echo "   - Warehouse: RD_ORG_WH"
echo ""
echo "✅ Setup complete! The application will now use the config.toml file for authentication."


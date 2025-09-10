#!/bin/bash

# Setup script for private key authentication with Snowflake
# This script helps configure environment variables for private key authentication

echo "🔧 Setting up private key authentication for Snowflake..."

# Check if private key files exist
if [ ! -f "charge_mapping_encrypted_private_key.p8" ]; then
    echo "❌ Private key file 'charge_mapping_encrypted_private_key.p8' not found!"
    echo "Please ensure the private key file is in the current directory."
    exit 1
fi

if [ ! -f "charge_mapping_encrypted_public_key.pub" ]; then
    echo "❌ Public key file 'charge_mapping_encrypted_public_key.pub' not found!"
    echo "Please ensure the public key file is in the current directory."
    exit 1
fi

echo "✅ Private key files found"

# Create or update .env file for private key authentication
ENV_FILE=".env.private_key"

cat > "$ENV_FILE" << EOF
# Snowflake Private Key Authentication Configuration
# Copy these to your environment or source this file: source $ENV_FILE

# Authentication method
export SNOWFLAKE_AUTHENTICATOR="snowflake_jwt"

# Private key configuration
export SNOWFLAKE_PRIVATE_KEY_PATH="charge_mapping_encrypted_private_key.p8"
export SNOWFLAKE_PRIVATE_KEY_PASSPHRASE="your_passphrase_here"

# Snowflake connection details (update these with your values)
export SNOWFLAKE_ACCOUNT="KDA03952-FGA72401"
export SNOWFLAKE_USER="BIBHUTIRAJANMANOJKUMAR"
export SNOWFLAKE_WAREHOUSE="RD_ORG_WH"
export SNOWFLAKE_DATABASE="SANDBOX"
export SNOWFLAKE_SCHEMA="BMANOJKUMAR"
export SNOWFLAKE_ROLE="RD_ORG_READ"
EOF

echo "✅ Created environment configuration file: $ENV_FILE"
echo ""
echo "📝 Next steps:"
echo "1. Edit $ENV_FILE and update the values:"
echo "   - Set SNOWFLAKE_PRIVATE_KEY_PASSPHRASE to your actual passphrase"
echo "   - Update other connection parameters if needed"
echo ""
echo "2. Source the environment file:"
echo "   source $ENV_FILE"
echo ""
echo "3. Test the connection:"
echo "   python test_private_key_connection.py"
echo ""
echo "4. Or test with the main connection script:"
echo "   SNOWFLAKE_AUTHENTICATOR=snowflake_jwt python test_snowflake_connection.py"
echo ""
echo "🔐 To switch back to browser authentication:"
echo "   export SNOWFLAKE_AUTHENTICATOR=externalbrowser"


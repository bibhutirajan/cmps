#!/bin/bash

# Setup script for local development
echo "🔧 Setting up local environment for Arcadia Charge Mapping Tool"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file for local development..."
    cat > .env << EOF
# Snowflake Connection Parameters
# Replace these with your actual Snowflake credentials
export SNOWFLAKE_ACCOUNT=your_account
export SNOWFLAKE_USER=your_username
export SNOWFLAKE_PASSWORD=your_password
export SNOWFLAKE_WAREHOUSE=COMPUTE_WH
export SNOWFLAKE_DATABASE=arcadia
export SNOWFLAKE_SCHEMA=lakehouse
export SNOWFLAKE_ROLE=your_role
EOF
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env file with your actual Snowflake credentials"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🚀 To run the app locally:"
echo "1. Edit .env file with your Snowflake credentials"
echo "2. Source the environment: source .env"
echo "3. Activate virtual environment: source venv/bin/activate"
echo "4. Run the app: streamlit run app_modular.py"
echo ""
echo "🌐 The app will be available at: http://localhost:8501" 
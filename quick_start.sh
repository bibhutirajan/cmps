#!/bin/bash

# Quick Start Script for Snowflake Native Streamlit Deployment
# Make sure you have snowsql configured with your connection

echo "🚀 Deploying Arcadia Charge Mapping Tool to Snowflake Native Streamlit..."

# Step 1: Create stage (run this in Snowflake SQL Editor first)
echo "📝 Step 1: Create stage in Snowflake SQL Editor:"
echo "CREATE OR REPLACE STAGE my_streamlit_stage DIRECTORY = (ENABLE = TRUE);"
echo ""

# Step 2: Upload files
echo "📤 Step 2: Uploading files to Snowflake stage..."
snowsql -c your_connection -q "
PUT file://app.py @my_streamlit_stage/;
PUT file://config.py @my_streamlit_stage/;
PUT file://db.py @my_streamlit_stage/;
PUT file://requirements.txt @my_streamlit_stage/;
"

# Step 3: Create Streamlit app
echo "🎯 Step 3: Creating Streamlit app..."
snowsql -c your_connection -q "
CREATE OR REPLACE STREAMLIT charge_mapping_app
FROM @my_streamlit_stage
MAIN_FILE = 'app.py'
QUERY_WAREHOUSE = COMPUTE_WH;
"

echo "✅ Deployment complete!"
echo "🌐 Access your app at: Snowsight → Streamlit Apps → charge_mapping_app" 
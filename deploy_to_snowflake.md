# Deploy to Snowflake Native Streamlit

## Step 1: Create a Snowflake Stage
```sql
-- Create a stage for your Streamlit app
CREATE OR REPLACE STAGE my_streamlit_stage
  DIRECTORY = (ENABLE = TRUE);
```

## Step 2: Upload Files to Stage
```bash
# From your local /opt/cmps directory
snowsql -c your_connection -q "
PUT file://app_modular.py @my_streamlit_stage/;
PUT file://config.py @my_streamlit_stage/;
PUT file://db.py @my_streamlit_stage/;
PUT file://requirements.txt @my_streamlit_stage/;
PUT file://pages/__init__.py @my_streamlit_stage/pages/;
PUT file://pages/existing_rules.py @my_streamlit_stage/pages/;
PUT file://pages/add_new_rule.py @my_streamlit_stage/pages/;
PUT file://pages/approve_rules.py @my_streamlit_stage/pages/;
PUT file://pages/uncategorized.py @my_streamlit_stage/pages/;
"
```

## Step 3: Create the Streamlit App
```sql
CREATE OR REPLACE STREAMLIT charge_mapping_app
FROM @my_streamlit_stage
MAIN_FILE = 'app_modular.py'
QUERY_WAREHOUSE = COMPUTE_WH;  -- Replace with your warehouse
```

## Step 4: Grant Permissions
```sql
-- Grant access to users/roles who need to use the app
GRANT USAGE ON STREAMLIT charge_mapping_app TO ROLE your_role;
```

## Step 5: Access Your App
- Go to Snowsight → Streamlit Apps
- Click on your `charge_mapping_app`
- Your app will run with the Snowflake session automatically available 
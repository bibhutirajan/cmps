# Snowflake Setup for Charge Mapping Application

This document provides instructions for setting up the Snowflake database tables and loading the mock data for the Charge Mapping application.

## Files Included

1. **create_snowflake_tables.sql** - SQL script to create all tables
2. **charges.csv** - Sample charges data
3. **rules.csv** - Sample business rules data
4. **processed_files.csv** - Sample processed files data

## Setup Instructions

### Step 1: Create Tables in Snowflake

1. Connect to your Snowflake instance
2. Execute the `create_snowflake_tables.sql` script
3. This will create the following tables in the `arcadia.lakehouse` schema:
   - `charges` - Contains charge data
   - `rules` - Contains business rules
   - `processed_files` - Contains file processing history

### Step 2: Load CSV Data

You can load the CSV files using one of these methods:

#### Method 1: Using Snowflake Web Interface
1. Go to your Snowflake web interface
2. Navigate to the `arcadia.lakehouse` schema
3. For each table, use the "Load Data" feature
4. Upload the corresponding CSV file
5. Map the columns correctly

#### Method 2: Using SnowSQL CLI
```bash
# Load charges data
snowsql -c your_connection -q "
COPY INTO arcadia.lakehouse.charges 
FROM @your_stage/charges.csv 
FILE_FORMAT = (TYPE = 'CSV' FIELD_DELIMITER = ',' SKIP_HEADER = 1)
"

# Load rules data
snowsql -c your_connection -q "
COPY INTO arcadia.lakehouse.rules 
FROM @your_stage/rules.csv 
FILE_FORMAT = (TYPE = 'CSV' FIELD_DELIMITER = ',' SKIP_HEADER = 1)
"

# Load processed_files data
snowsql -c your_connection -q "
COPY INTO arcadia.lakehouse.processed_files 
FROM @your_stage/processed_files.csv 
FILE_FORMAT = (TYPE = 'CSV' FIELD_DELIMITER = ',' SKIP_HEADER = 1)
"


```

#### Method 3: Using Python with Snowflake Connector
```python
import pandas as pd
from snowflake.connector import connect

# Connect to Snowflake
conn = connect(
    user='your_username',
    password='your_password',
    account='your_account',
    warehouse='your_warehouse',
    database='arcadia',
    schema='lakehouse'
)

# Load data
charges_df = pd.read_csv('charges.csv')
rules_df = pd.read_csv('rules.csv')
processed_files_df = pd.read_csv('processed_files.csv')

# Write to Snowflake
charges_df.to_sql('charges', conn, if_exists='append', index=False)
rules_df.to_sql('rules', conn, if_exists='append', index=False)
processed_files_df.to_sql('processed_files', conn, if_exists='append', index=False)
```

### Step 3: Verify Data Loading

Run these queries to verify the data was loaded correctly:

```sql
-- Check charges data
SELECT COUNT(*) as charge_count FROM arcadia.lakehouse.charges;
SELECT * FROM arcadia.lakehouse.charges LIMIT 5;

-- Check rules data
SELECT COUNT(*) as rule_count FROM arcadia.lakehouse.rules;
SELECT * FROM arcadia.lakehouse.rules LIMIT 5;

-- Check processed files data
SELECT COUNT(*) as file_count FROM arcadia.lakehouse.processed_files;
SELECT * FROM arcadia.lakehouse.processed_files LIMIT 5;


```

## Table Schemas

### CHARGES Table
- `STATEMENT_ID` - Unique statement identifier
- `PROVIDER_NAME` - Name of the utility provider
- `ACCOUNT_NUMBER` - Customer account number
- `CHARGE_NAME` - Name of the charge
- `CHARGE_ID` - Charge category identifier
- `CHARGE_MEASUREMENT` - Type of measurement
- `USAGE_UNIT` - Unit of usage measurement
- `SERVICE_TYPE` - Type of service
- `CUSTOMER_NAME` - Customer identifier

### RULES Table
- `CHIPS_BUSINESS_RULE_ID` - Unique rule identifier
- `CUSTOMER_NAME` - Customer identifier
- `PRIORITY_ORDER` - Rule priority (numeric)
- `CHARGE_NAME_MAPPING` - Regex pattern for charge name matching
- `CHARGE_ID` - Target charge category
- `CHARGE_GROUP_HEADING` - Group heading for charges
- `CHARGE_CATEGORY` - Category of the charge
- `REQUEST_TYPE` - Type of request
- `PROVIDER_NAME` - Provider name
- `ACCOUNT_NUMBER` - Account number
- `USAGE_UNIT` - Usage unit
- `SERVICE_TYPE` - Service type
- `TARIFF` - Tariff information
- `RAW_CHARGE_NAME` - Original charge name
- `LEGACY_DESCRIPTION` - Description text
- `METER_NUMBER` - Meter number
- `MEASUREMENT_TYPE` - Type of measurement

### PROCESSED_FILES Table
- `FILE_ID` - Unique file identifier
- `FILENAME` - Name of the processed file
- `PROCESSED_DATE` - Date when file was processed
- `STATUS` - Processing status
- `RECORDS` - Number of records in file
- `CUSTOMER_NAME` - Customer identifier



## Application Configuration

After setting up the tables, update your application configuration to use Snowflake:

1. Set `snowflake_enabled = True` in your configuration
2. Ensure your Snowflake connection parameters are correct
3. The application will automatically switch from demo mode to Snowflake mode

## Notes

- All tables include `CREATED_AT` and `UPDATED_AT` timestamp columns
- Indexes are created for better query performance
- The sample data includes the customer "AmerescoFTP" - adjust as needed for your use case
- Make sure to grant appropriate permissions to your application's Snowflake role

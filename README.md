# Charge Mapping Application

A modern Streamlit application for managing charge mapping rules and business logic with seamless integration between demo data and Snowflake.

## 🏗️ Architecture Overview

The application follows a **modular clean architecture pattern** with clear separation of concerns:

### 📁 Project Structure
```
cmps/
├── app.py                         # Main application
├── config.py                      # Snowflake configuration
├── deployment_config.py           # Deployment configuration helper
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── components/                    # Modular components
│   ├── __init__.py
│   ├── data/                      # Data layer
│   │   ├── __init__.py
│   │   └── providers.py           # Data providers (Demo/Snowflake)
│   ├── ui/                        # UI components
│   │   ├── __init__.py
│   │   ├── sidebar.py             # Sidebar component
│   │   ├── charges_tab.py         # Charges tab
│   │   ├── rules_tab.py           # Rules tab
│   │   ├── processed_files_tab.py # Processed files tab
│   │   └── regex_rules_tab.py     # Regex rules tab
│   └── modals/                    # Modal components
│       ├── __init__.py
│       ├── create_rule_modal.py   # Create rule modal
│       ├── edit_rule_modal.py     # Edit rule modal
│       └── edit_priority_modal.py # Edit priority modal
├── static/                        # Static assets
│   ├── css/
│   │   └── styles.css             # Main stylesheet
│   └── js/
│       └── modal.js               # Modal JavaScript
└── templates/                     # HTML templates (future use)
```

### Core Components

1. **Configuration Layer** (`AppConfig`)
   - Centralized configuration management
   - Environment-based settings
   - Easy deployment configuration

2. **Data Abstraction Layer** (`DataProvider`)
   - Abstract base class for data providers
   - Consistent interface across data sources
   - Easy migration between demo and production data

3. **UI Components** (`components/ui/`)
   - Modular UI components for each tab
   - Reusable across different data sources
   - Consistent user experience

4. **Modal Components** (`components/modals/`)
   - Separate modal components for different actions
   - Create Rule, Edit Rule, Edit Priority modals
   - Proper form validation and error handling

5. **Static Assets** (`static/`)
   - CSS styles in separate file
   - JavaScript for modal functionality
   - Clean separation of styling and behavior

## 🚀 Deployment Options

### Option 1: Local Development (Demo Mode)
```bash
# Run with demo data (default)
streamlit run app.py --server.port 8501
```

### Option 2: Snowflake Native App

**Using Password Authentication:**
```bash
# Set environment variables for Snowflake
export SNOWFLAKE_ENABLED=true
export SNOWFLAKE_ACCOUNT=your_account
export SNOWFLAKE_USER=your_username
export SNOWFLAKE_PASSWORD=your_password
export SNOWFLAKE_WAREHOUSE=COMPUTE_WH
export SNOWFLAKE_DATABASE=arcadia
export SNOWFLAKE_SCHEMA=lakehouse
export SNOWFLAKE_ROLE=your_role

# Run the application
streamlit run app.py --server.port 8501
```

**Using Private Key Authentication (Recommended):**
```bash
# Set environment variables for Snowflake with private key
export SNOWFLAKE_ENABLED=true
export SNOWFLAKE_ACCOUNT=your_account
export SNOWFLAKE_USER=your_username
export SNOWFLAKE_PRIVATE_KEY_PATH=/path/to/your/private_key.p8
export SNOWFLAKE_PRIVATE_KEY_PASSPHRASE=your_passphrase  # Optional
export SNOWFLAKE_WAREHOUSE=COMPUTE_WH
export SNOWFLAKE_DATABASE=arcadia
export SNOWFLAKE_SCHEMA=lakehouse
export SNOWFLAKE_ROLE=your_role

# Run the application
streamlit run app.py --server.port 8501
```

### Option 3: External Hosting with Snowflake
```bash
# Configure for external hosting
export SNOWFLAKE_ENABLED=true
export DATA_SOURCE=snowflake
# ... other Snowflake environment variables

# Deploy to your preferred hosting platform
# (Heroku, AWS, GCP, Azure, etc.)
```

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATA_SOURCE` | `demo` | Data source: `demo` or `snowflake` |
| `SNOWFLAKE_ENABLED` | `false` | Enable Snowflake integration |
| `SNOWFLAKE_ACCOUNT` | `your_account` | Snowflake account identifier |
| `SNOWFLAKE_USER` | `your_username` | Snowflake username |
| `SNOWFLAKE_PASSWORD` | `your_password` | Snowflake password (if not using private key) |
| `SNOWFLAKE_PRIVATE_KEY_PATH` | `None` | Path to private key file (for key-based auth) |
| `SNOWFLAKE_PRIVATE_KEY_PASSPHRASE` | `None` | Passphrase for private key (if encrypted) |
| `SNOWFLAKE_WAREHOUSE` | `COMPUTE_WH` | Snowflake warehouse name |
| `SNOWFLAKE_DATABASE` | `arcadia` | Snowflake database name |
| `SNOWFLAKE_SCHEMA` | `lakehouse` | Snowflake schema name |
| `SNOWFLAKE_ROLE` | `your_role` | Snowflake role name |
| `CHARGES_TABLE` | `charges` | Charges table name |
| `RULES_TABLE` | `rules` | Rules table name |
| `PROCESSED_FILES_TABLE` | `processed_files` | Processed files table name |
| `REGEX_RULES_TABLE` | `regex_rules` | Regex rules table name |

### Snowflake Configuration

#### Authentication Methods

The application supports two authentication methods for Snowflake:

**1. Password Authentication (Default)**
```bash
export SNOWFLAKE_ACCOUNT=your_account
export SNOWFLAKE_USER=your_username
export SNOWFLAKE_PASSWORD=your_password
export SNOWFLAKE_WAREHOUSE=COMPUTE_WH
export SNOWFLAKE_DATABASE=arcadia
export SNOWFLAKE_SCHEMA=lakehouse
export SNOWFLAKE_ROLE=your_role
```

**2. Private Key Authentication (Recommended for Production)**
```bash
export SNOWFLAKE_ACCOUNT=your_account
export SNOWFLAKE_USER=your_username
export SNOWFLAKE_PRIVATE_KEY_PATH=/path/to/your/private_key.p8
export SNOWFLAKE_PRIVATE_KEY_PASSPHRASE=your_passphrase  # Optional
export SNOWFLAKE_WAREHOUSE=COMPUTE_WH
export SNOWFLAKE_DATABASE=arcadia
export SNOWFLAKE_SCHEMA=lakehouse
export SNOWFLAKE_ROLE=your_role
```

**Setting up Private Key Authentication:**

1. **Generate Private Key Pair:**
   ```bash
   # Generate private key (RSA 2048-bit)
   openssl genrsa -aes256 -out rsa_key.pem 2048
   
   # Extract public key
   openssl rsa -in rsa_key.pem -pubout -out rsa_key.pub
   ```

2. **Convert to Snowflake Format:**
   ```bash
   # Convert to PKCS8 format (required by Snowflake)
   openssl pkcs8 -topk8 -inform PEM -outform PEM -in rsa_key.pem -out rsa_key.p8 -nocrypt
   ```

3. **Upload Public Key to Snowflake:**
   ```sql
   -- Execute in Snowflake
   ALTER USER your_username SET RSA_PUBLIC_KEY='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...';
   ```

4. **Set Environment Variables:**
   ```bash
   export SNOWFLAKE_PRIVATE_KEY_PATH=/path/to/rsa_key.p8
   export SNOWFLAKE_PRIVATE_KEY_PASSPHRASE=your_passphrase  # If key is encrypted
   ```

**Security Best Practices:**
- Store private keys securely (not in version control)
- Use environment variables or secure secret management
- Rotate keys regularly
- Use different keys for different environments

The application expects the following Snowflake tables:

#### Charges Table
```sql
CREATE TABLE charges (
    STATEMENT_ID VARCHAR,
    PROVIDER_NAME VARCHAR,
    ACCOUNT_NUMBER VARCHAR,
    CHARGE_NAME VARCHAR,
    CHARGE_ID VARCHAR,
    CHARGE_MEASUREMENT VARCHAR,
    USAGE_UNIT VARCHAR,
    SERVICE_TYPE VARCHAR,
    CUSTOMER_NAME VARCHAR,
    CHARGE_TYPE VARCHAR
);
```

#### Rules Table
```sql
CREATE TABLE rules (
    CHIPS_BUSINESS_RULE_ID NUMBER,
    CUSTOMER_NAME VARCHAR,
    PRIORITY_ORDER NUMBER,
    CHARGE_NAME_MAPPING VARCHAR,
    CHARGE_ID VARCHAR,
    CHARGE_GROUP_HEADING VARCHAR,
    CHARGE_CATEGORY VARCHAR,
    REQUEST_TYPE VARCHAR
);
```

#### Processed Files Table
```sql
CREATE TABLE processed_files (
    FILE_ID VARCHAR,
    FILENAME VARCHAR,
    PROCESSED_DATE DATE,
    STATUS VARCHAR,
    RECORDS NUMBER,
    CUSTOMER_NAME VARCHAR
);
```

#### Regex Rules Table
```sql
CREATE TABLE regex_rules (
    PATTERN_ID VARCHAR,
    REGEX_PATTERN VARCHAR,
    CATEGORY VARCHAR,
    PRIORITY NUMBER,
    CUSTOMER_NAME VARCHAR
);
```

## 🔄 Migration Strategy

### From Demo to Snowflake

1. **Setup Snowflake Environment**
   ```bash
   export SNOWFLAKE_ENABLED=true
   # Configure other Snowflake environment variables
   ```

2. **Create Snowflake Tables**
   - Use the SQL schemas provided above
   - Ensure proper permissions are set

3. **Update Configuration**
   - Set table names in environment variables
   - Configure database and schema names

4. **Test Migration**
   - Run the application
   - Verify data is loading from Snowflake
   - Check error handling and fallback mechanisms

### From External Hosting to Snowflake Native

1. **Update Environment Variables**
   ```bash
   # Remove external hosting specific variables
   # Add Snowflake Native App variables
   ```

2. **Deploy to Snowflake Native Apps**
   - Package the application
   - Deploy using Snowflake Native Apps framework

## 🛠️ Development Best Practices

### Code Structure
```
app.py
├── Configuration Layer (AppConfig)
├── Data Abstraction Layer (DataProvider)
├── UI Components (components/ui/)
├── Modal Components (components/modals/)
├── Static Assets (static/)
└── Main Application (main)
```

### Adding New Features

1. **Add to DataProvider Interface**
   ```python
   @abstractmethod
   def new_feature(self, customer: str) -> pd.DataFrame:
       pass
   ```

2. **Implement in Both Providers**
   ```python
   # DemoDataProvider
   def new_feature(self, customer: str) -> pd.DataFrame:
       return pd.DataFrame(...)
   
   # SnowflakeDataProvider
   def new_feature(self, customer: str) -> pd.DataFrame:
       query = "SELECT ... FROM ..."
       return self.session.sql(query).to_pandas()
   ```

3. **Add UI Component**
   ```python
   # components/ui/new_feature_tab.py
   def render_new_feature_tab(data_provider: DataProvider, customer: str):
       # UI implementation
   ```

4. **Add Modal Component** (if needed)
   ```python
   # components/modals/new_feature_modal.py
   def new_feature_modal(data_provider: DataProvider, data: Dict):
       # Modal implementation
   ```

### Error Handling

- **Graceful Fallbacks**: Application falls back to demo mode if Snowflake connection fails
- **User Feedback**: Clear status indicators show current data source
- **Error Logging**: Comprehensive error handling with user-friendly messages

## 🔧 Customization

### Adding New Data Sources

1. **Create New DataProvider**
   ```python
   class CustomDataProvider(DataProvider):
       def get_charges(self, customer: str, charge_type: str = None) -> pd.DataFrame:
           # Custom implementation
   ```

2. **Update Factory Function**
   ```python
   def get_data_provider() -> DataProvider:
       if config.CUSTOM_DATA_SOURCE_ENABLED:
           return CustomDataProvider()
       # ... existing logic
   ```

### UI Customization

- **CSS Styling**: Modify `static/css/styles.css`
- **Layout Changes**: Update individual UI components in `components/ui/`
- **New Components**: Add new UI components following the existing pattern

### Modal Customization

- **New Modals**: Create new modal components in `components/modals/`
- **JavaScript**: Add custom JavaScript in `static/js/`
- **Styling**: Update CSS for modal styles

## 📊 Performance Considerations

### Demo Mode
- Fast startup with static data
- No external dependencies
- Ideal for development and testing

### Snowflake Mode
- Optimized queries with proper indexing
- Connection pooling for better performance
- Caching strategies for frequently accessed data

## 🔒 Security

### Environment Variables
- Never commit sensitive credentials to version control
- Use environment variables for all configuration
- Implement proper secret management in production

### Snowflake Security
- Use role-based access control (RBAC)
- Implement proper user permissions
- Secure connection parameters
- **Use private key authentication for production environments**
- Store private keys securely (not in version control)
- Rotate keys regularly
- Use different keys for different environments

## 🚀 Deployment Checklist

### Local Development
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Set environment variables (optional)
- [ ] Run: `streamlit run app.py`

### Snowflake Native App
- [ ] Configure Snowflake environment variables
- [ ] Create required tables in Snowflake
- [ ] Test connection and data access
- [ ] Deploy using Snowflake Native Apps framework

### External Hosting
- [ ] Set up hosting platform (Heroku, AWS, etc.)
- [ ] Configure environment variables
- [ ] Set up Snowflake connection
- [ ] Deploy application
- [ ] Test functionality

## 🐛 Troubleshooting

### Common Issues

1. **Snowflake Connection Failed**
   - Check environment variables
   - Verify Snowflake credentials
   - Ensure network connectivity
   - **For private key auth**: Verify key file path and permissions
   - **For private key auth**: Check if key is in correct PKCS8 format
   - **For private key auth**: Verify public key is uploaded to Snowflake

2. **Data Not Loading**
   - Verify table names and schemas
   - Check SQL query syntax
   - Review Snowflake permissions

3. **UI Issues**
   - Clear browser cache
   - Check CSS conflicts
   - Verify Streamlit version compatibility

4. **Modal Issues**
   - Check JavaScript console for errors
   - Verify modal CSS is loaded
   - Ensure modal IDs are unique

### Debug Mode

Enable debug mode by setting:
```bash
export STREAMLIT_DEBUG=true
```

## 📈 Monitoring and Logging

### Application Logs
- Streamlit provides built-in logging
- Monitor for connection errors
- Track user interactions

### Snowflake Monitoring
- Monitor query performance
- Track connection usage
- Review error logs

## 🤝 Contributing

1. Follow the established architecture patterns
2. Add proper error handling
3. Include documentation for new features
4. Test with both demo and Snowflake data sources
5. Update this README for significant changes

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 
# CMPS Deployment Guide

This guide provides step-by-step instructions for deploying the CMPS (Charge Mapping) application to different environments.

## 🏗️ Architecture Overview

The CMPS application supports multiple deployment scenarios:

1. **Local Development** - External Browser Authentication
2. **Sandbox Testing** - SANDBOX.BMANOJKUMAR.* schema
3. **Production** - APPLICATIONS.CMPS.* schema with automated CI/CD

## 📋 Prerequisites

### Required Tools
- Python 3.11+
- Snowflake CLI (`snow`)
- Git
- AWS CLI (for production deployments)

### Snowflake Setup
- Access to Snowflake account
- Appropriate roles and permissions
- RSA key pair for production authentication

## 🚀 Deployment Scenarios

### 1. Local Development Setup

#### Step 1: Clone and Setup
```bash
git clone <repository-url>
cd cmps
```

#### Step 2: Configure Snowflake Connection
```bash
# Create Snowflake config directory
mkdir -p ~/.snowflake

# Copy example configuration
cp example_config.toml ~/.snowflake/config.toml

# Edit the configuration with your credentials
nano ~/.snowflake/config.toml
```

#### Step 3: Update Configuration
Edit `~/.snowflake/config.toml`:
```toml
[connections.default]
account = "eda55635.us-east-1"
user = "your_username"
authenticator = "externalbrowser"
database = "SANDBOX"
schema = "BMANOJKUMAR"
role = "your_role"
warehouse = "your_warehouse"
```

#### Step 4: Start Application
```bash
# Option 1: Use start script
./bin/start_streamlit.sh

# Option 2: Manual start
source venv/bin/activate
streamlit run app.py --server.port 8501
```

### 2. Sandbox Deployment

#### Step 1: Verify SANDBOX Connection
```bash
# Ensure you're connected to SANDBOX database
snow sql --query "select current_database();"
```

#### Step 2: Deploy to Sandbox
```bash
# Run the deployment script
./bin/local_deploy.sh
```

This script will:
- Run database migrations
- Create necessary tables in `SANDBOX.BMANOJKUMAR.*`
- Deploy the Streamlit app to your sandbox

#### Step 3: Access Application
- Navigate to your Snowflake account
- Go to Streamlit Apps section
- Find and open the `cmps` application

### 3. Production Deployment

#### Step 1: Prepare RSA Key Pair
```bash
# Generate private key (if not already done)
openssl genrsa -aes256 -out rsa_key.pem 2048

# Convert to PKCS8 format
openssl pkcs8 -topk8 -inform PEM -outform PEM -in rsa_key.pem -out rsa_key.p8

# Extract public key
openssl rsa -in rsa_key.pem -pubout -out rsa_key.pub
```

#### Step 2: Upload Public Key to Snowflake
```sql
-- Execute in Snowflake
ALTER USER svc_cmps_user SET RSA_PUBLIC_KEY='<your_public_key_content>';
```

#### Step 3: Store Private Key in AWS Parameter Store
```bash
# Store the private key securely
aws ssm put-parameter \
    --name "/prd/cmps/snowflake-private-key" \
    --value "$(cat rsa_key.p8)" \
    --type "SecureString" \
    --description "Private key for CMPS Snowflake service user"
```

#### Step 4: Trigger Production Deployment
```bash
# Push to main branch (triggers automatic deployment)
git push origin main

# Or manually trigger deployment
# Go to GitHub Actions and run "Deploy CMPS Streamlit App to Snowflake"
```

#### Step 5: Access Production Application
- **URL**: `https://eda55635.us-east-1.snowflakeapp.com/applications/cmps/cmps`
- **Database**: `APPLICATIONS.CMPS.*`
- **Authentication**: RSA Private Key (automated)

## 🔧 Configuration Files

### snowflake.yml
Defines the Streamlit application configuration for both dev and production environments.

### environment.yml
Specifies Python dependencies for Snowflake deployment.

### .streamlit/config.toml
Streamlit application configuration.

### .github/config/config_prd.toml
Production Snowflake connection configuration for GitHub Actions.

## 🗄️ Database Schema

### Tables Created
- `CHARGES` - Charge mapping data
- `RULES` - Business rules configuration  
- `PROCESSED_FILES` - File processing tracking

### Schema Locations
- **Sandbox**: `SANDBOX.BMANOJKUMAR.*`
- **Production**: `APPLICATIONS.CMPS.*`

## 🔐 Security Considerations

### Authentication Methods
1. **Local Development**: External Browser Authentication
2. **Production**: RSA Private Key Authentication

### Secrets Management
- Private keys stored in AWS Parameter Store
- No secrets committed to version control
- Environment-specific configurations

### Access Control
- Role-based access in Snowflake
- Different roles for different environments
- Proper permissions for service users

## 🚨 Troubleshooting

### Common Issues

#### 1. Connection Errors
```bash
# Verify Snowflake connection
snow sql --query "select current_user();"

# Check configuration
cat ~/.snowflake/config.toml
```

#### 2. Permission Errors
```sql
-- Check user permissions
SHOW GRANTS TO USER your_username;
SHOW GRANTS TO ROLE your_role;
```

#### 3. Deployment Failures
```bash
# Check GitHub Actions logs
# Verify AWS Parameter Store access
aws ssm get-parameter --name "/prd/cmps/snowflake-private-key" --with-decryption
```

#### 4. Application Not Loading
- Verify Streamlit app is deployed
- Check Snowflake warehouse is running
- Review application logs in Snowflake

### Debug Commands
```bash
# Test Snowflake connection
python -c "import snowflake.connector; print('Connection successful')"

# Check deployment status
snow streamlit list

# View application logs
snow streamlit logs cmps_prd
```

## 📞 Support

For deployment issues:
1. Check the troubleshooting section above
2. Review GitHub Actions logs
3. Verify Snowflake permissions and configuration
4. Contact the development team

## 🔄 CI/CD Pipeline

### Automated Workflows
1. **Main Branch Push** → Triggers production deployment
2. **Manual Branch Deployment** → Deploy specific branches for testing
3. **Database Migrations** → Automatic schema updates

### Deployment Steps
1. Checkout code
2. Setup Snowflake configuration
3. Install dependencies
4. Run database migrations
5. Deploy Streamlit application
6. Grant necessary permissions
7. Provide application URL

### Monitoring
- GitHub Actions provide deployment status
- Snowflake logs track application performance
- AWS CloudWatch monitors infrastructure


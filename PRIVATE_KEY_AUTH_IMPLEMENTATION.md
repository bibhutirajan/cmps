# Private Key Authentication Implementation

## Overview

This document describes the implementation of private key (JWT) authentication for Snowflake connections in the charge-mapping application. The implementation supports both browser-based authentication and private key authentication, allowing users to choose the most appropriate method for their environment.

## Files Modified/Created

### Modified Files

1. **`config.py`**
   - Updated `get_local_snowflake_session()` function to support JWT authentication
   - Added support for `snowflake_jwt` authenticator
   - Maintains backward compatibility with browser authentication
   - Includes fallback mechanisms for error handling

2. **`test_snowflake_connection.py`**
   - Enhanced to support multiple authentication methods
   - Added private key loading and processing logic
   - Improved error handling and user feedback

3. **`example_config.toml`**
   - Added example configuration for private key authentication
   - Documented both browser and JWT authentication options

4. **`README.md`**
   - Updated authentication methods documentation
   - Added JWT authentication as option 2
   - Updated environment variables table
   - Added quick setup instructions

### New Files Created

1. **`test_private_key_connection.py`**
   - Dedicated test script for private key authentication
   - Standalone testing without dependencies on main application
   - Comprehensive error handling and user feedback

2. **`setup_private_key_auth.sh`**
   - Automated setup script for private key authentication
   - Creates environment configuration file
   - Provides step-by-step instructions

3. **`demo_auth_methods.py`**
   - Demonstration script showing both authentication methods
   - Useful for testing and validation
   - Shows how to switch between authentication methods

4. **`PRIVATE_KEY_AUTH_IMPLEMENTATION.md`** (this file)
   - Documentation of the implementation

## Authentication Methods Supported

### 1. External Browser Authentication (Default)
- Uses SSO/browser-based authentication
- Set `SNOWFLAKE_AUTHENTICATOR=externalbrowser`
- No additional files required

### 2. Private Key Authentication (JWT)
- Uses encrypted private key for authentication
- Set `SNOWFLAKE_AUTHENTICATOR=snowflake_jwt`
- Requires private key file and optionally a passphrase
- More secure for production environments

### 3. Password Authentication
- Traditional username/password authentication
- Set `SNOWFLAKE_AUTHENTICATOR=password`
- Requires password in environment variables

## Environment Variables

| Variable | Description | Required for JWT |
|----------|-------------|------------------|
| `SNOWFLAKE_AUTHENTICATOR` | Authentication method | Yes |
| `SNOWFLAKE_PRIVATE_KEY_PATH` | Path to private key file | Yes |
| `SNOWFLAKE_PRIVATE_KEY_PASSPHRASE` | Passphrase for encrypted key | Optional |
| `SNOWFLAKE_ACCOUNT` | Snowflake account | Yes |
| `SNOWFLAKE_USER` | Snowflake username | Yes |
| `SNOWFLAKE_WAREHOUSE` | Warehouse name | Yes |
| `SNOWFLAKE_DATABASE` | Database name | Yes |
| `SNOWFLAKE_SCHEMA` | Schema name | Yes |
| `SNOWFLAKE_ROLE` | Role name | Yes |

## Usage Examples

### Quick Setup with Private Key
```bash
# Run setup script
./setup_private_key_auth.sh

# Edit the generated .env.private_key file
# Set your passphrase and other values

# Source the environment
source .env.private_key

# Test the connection
python test_private_key_connection.py
```

### Manual Configuration
```bash
# Set environment variables
export SNOWFLAKE_AUTHENTICATOR="snowflake_jwt"
export SNOWFLAKE_PRIVATE_KEY_PATH="charge_mapping_encrypted_private_key.p8"
export SNOWFLAKE_PRIVATE_KEY_PASSPHRASE="your_passphrase"

# Test connection
python test_snowflake_connection.py
```

### Switch to Browser Authentication
```bash
export SNOWFLAKE_AUTHENTICATOR="externalbrowser"
python test_snowflake_connection.py
```

## Security Considerations

1. **Private Key Storage**
   - Private keys should never be committed to version control
   - Use secure secret management systems in production
   - Consider using AWS Parameter Store or similar services

2. **Passphrase Management**
   - Store passphrases securely
   - Use environment variables or secure vaults
   - Rotate passphrases regularly

3. **Key Rotation**
   - Implement regular key rotation policies
   - Update public keys in Snowflake when rotating
   - Test new keys before removing old ones

## Testing

### Test Scripts Available

1. **`test_private_key_connection.py`**
   - Tests only private key authentication
   - Standalone script with minimal dependencies

2. **`test_snowflake_connection.py`**
   - Tests all authentication methods
   - Uses the main application's connection logic

3. **`demo_auth_methods.py`**
   - Demonstrates switching between authentication methods
   - Useful for validation and testing

### Running Tests

```bash
# Test private key authentication
python test_private_key_connection.py

# Test with specific authenticator
SNOWFLAKE_AUTHENTICATOR=snowflake_jwt python test_snowflake_connection.py

# Demo all methods
python demo_auth_methods.py
```

## Troubleshooting

### Common Issues

1. **Private Key File Not Found**
   - Ensure the file exists in the specified path
   - Check file permissions
   - Verify the path is correct

2. **Invalid Passphrase**
   - Verify the passphrase is correct
   - Check for extra spaces or special characters
   - Ensure the key is actually encrypted

3. **Public Key Not Registered**
   - Verify the public key is registered in Snowflake
   - Check the user has the correct permissions
   - Ensure the key format is correct

4. **Connection Timeout**
   - Check network connectivity
   - Verify account identifier is correct
   - Check firewall settings

### Debug Mode

Enable debug logging by setting:
```bash
export SNOWFLAKE_DEBUG=true
```

## Future Enhancements

1. **AWS Parameter Store Integration**
   - Store private keys in AWS Parameter Store
   - Automatic key retrieval and decryption
   - Enhanced security for production environments

2. **Key Rotation Automation**
   - Automated key generation and rotation
   - Integration with Snowflake user management
   - Monitoring and alerting for key expiration

3. **Multi-Environment Support**
   - Environment-specific key management
   - Support for multiple Snowflake accounts
   - Configuration templates for different environments

## Conclusion

The private key authentication implementation provides a secure, production-ready alternative to browser-based authentication while maintaining full backward compatibility. The modular design allows for easy switching between authentication methods and provides comprehensive testing and setup tools.


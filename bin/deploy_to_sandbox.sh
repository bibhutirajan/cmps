#!/bin/bash

# Exit if current database is not SANDBOX
if snow sql --query "select current_database();" | grep -q "SANDBOX"; then
  echo "Verified connection to the SANDBOX database"
else
  echo "You are not connected to the SANDBOX database. Please verify your default connection in ~/.snowflake/config.toml. Exiting."
  exit 1
fi

deploy_charge_mapping() {
  # Uses your sandbox schema configured in ~/.snowflake/config.toml
      snow sql --query "drop stage if exists charge_mapping"

  # Deploy the app to the sandbox
  # Note: --replace only adds or updates existing files. It does not delete files. That's why we need the command above.
      snow streamlit deploy charge-mapping --replace
}

dispatch_deploy() {
  deploy_charge_mapping
}

dispatch_deploy


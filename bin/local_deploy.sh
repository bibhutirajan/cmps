#!/bin/bash

# Exit if current database is not SANDBOX
if snow sql --query "select current_database();" | grep -q "SANDBOX"; then
  echo "Verified connection to the SANDBOX database"
else
  echo "You are not connected to the SANDBOX database. Please verify your default connection in ~/.snowflake/config.toml. Exiting."
  exit 1
fi

deploy_cmps() {
  # Uses your sandbox schema configured in ~/.snowflake/config.toml
  snow sql --query "drop stage if exists cmps"

  # Deploy the app to the sandbox
  # Note: --replace only adds or updates existing files. It does not delete files. That's why we need the command above.
  snow streamlit deploy cmps_dev --replace
}

deploy_application_dbs() {
  python "$(dirname "$0")"/../src/resources/db_migrations/db_migrations.py
  if [ $? -ne 0 ]; then
    echo "Database migrations failed. Exiting."
    exit 1
  fi
}

dispatch_deploy() {
  deploy_application_dbs
  deploy_cmps
}

dispatch_deploy


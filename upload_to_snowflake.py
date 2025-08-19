#!/usr/bin/env python3
"""
Script to upload all files from cmps project to Snowflake stage
Handles nested directories and preserves structure
"""

import os
import snowflake.connector
from pathlib import Path

def upload_to_snowflake():
    """Upload all files from cmps project to Snowflake stage"""
    
    # Snowflake connection parameters
    conn = snowflake.connector.connect(
        user='your_username',
        password='your_password',
        account='your_account',
        warehouse='COMPUTE_WH',
        database='SANDBOX',
        schema='PUBLIC'
    )
    
    cursor = conn.cursor()
    
    # Project root directory
    project_root = Path('/opt/cmps')
    
    # Files to upload (main files)
    main_files = [
        'app.py',
        'config.py',
        'db.py',
        'requirements.txt',
        'deployment_config.py',
        'README.md'
    ]
    
    # Upload main files
    for file_name in main_files:
        file_path = project_root / file_name
        if file_path.exists():
            print(f"Uploading {file_name}...")
            cursor.execute(f"PUT file://{file_path} @cmps_app_stage")
    
    # Upload components directory
    components_dir = project_root / 'components'
    if components_dir.exists():
        print("Uploading components directory...")
        for file_path in components_dir.rglob('*.py'):
            relative_path = file_path.relative_to(project_root)
            print(f"Uploading {relative_path}...")
            cursor.execute(f"PUT file://{file_path} @cmps_app_stage")
    
    # Upload static directory
    static_dir = project_root / 'static'
    if static_dir.exists():
        print("Uploading static directory...")
        for file_path in static_dir.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(project_root)
                print(f"Uploading {relative_path}...")
                cursor.execute(f"PUT file://{file_path} @cmps_app_stage")
    
    print("Upload completed!")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    upload_to_snowflake() 
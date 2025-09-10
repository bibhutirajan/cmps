#!/usr/bin/env python3
"""
Deploy Charge Mapping App to Snowflake Sandbox
Following onboarding-observability deployment pattern
"""

import os
import sys
import subprocess
from pathlib import Path

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check if snow CLI is installed
    try:
        result = subprocess.run(['snow', '--version'], capture_output=True, text=True)
        print(f"✅ Snow CLI found: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Snow CLI not found. Please install it first:")
        print("   pip install snowflake-cli-labs")
        return False
    
    # Check if snowflake.yml exists
    if not os.path.exists('snowflake.yml'):
        print("❌ snowflake.yml not found")
        return False
    
    # Check environment.yml for conda compatibility and version issues
    if os.path.exists('environment.yml'):
        with open('environment.yml', 'r') as f:
            content = f.read()
            fixed = False
            
            # Fix conda-incompatible syntax
            if '[secure-local-storage]' in content:
                print("⚠️  Fixing environment.yml - removing conda-incompatible syntax")
                content = content.replace('  - snowflake-connector-python[secure-local-storage]\n', '')
                fixed = True
            
            # Check for unsupported channels
            if 'conda-forge' in content:
                print("⚠️  Fixing environment.yml - removing unsupported conda-forge channel")
                content = content.replace('  - conda-forge\n', '')
                fixed = True
            
            if fixed:
                with open('environment.yml', 'w') as f_out:
                    f_out.write(content)
                print("✅ Fixed environment.yml")
    
    # Check main.py for st.set_page_config issues
    if os.path.exists('main.py'):
        with open('main.py', 'r') as f:
            content = f.read()
            # Count occurrences of st.set_page_config
            config_count = content.count('st.set_page_config(')
            if config_count > 1:
                print("⚠️  Warning: Multiple st.set_page_config() calls detected")
                print("   This will cause deployment errors. Only one call is allowed.")
                print("   Please follow onboarding-observability pattern.")
    
    # Check for deprecated width='stretch' usage in app files only
    for root, dirs, files in os.walk('.'):
        # Skip virtual environment and deployment files
        if 'venv' in root or 'output' in root:
            continue
        for file in files:
            if file.endswith('.py') and not file.startswith('deploy_'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    if "width='stretch'" in content or 'width="stretch"' in content:
                        print(f"⚠️  Warning: Deprecated width='stretch' found in {file_path}")
                        print("   Use use_container_width=True instead for Snowflake compatibility.")
                        print("   Snowflake Streamlit only supports integer width values or use_container_width.")
    
    print("✅ All prerequisites met")
    return True

def deploy_to_sandbox():
    """Deploy the Streamlit app to Snowflake sandbox"""
    print("📦 Deploying to sandbox...")
    
    try:
        # Deploy streamlit app command
        deploy_cmd = [
            'snow', 'streamlit', 'deploy',
            'charge-mapping',
            '--replace'
        ]
        
        print(f"Running: {' '.join(deploy_cmd)}")
        result = subprocess.run(deploy_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Successfully deployed to Snowflake sandbox")
            print(result.stdout)
        else:
            print("❌ Deployment failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error during deployment: {e}")
        return False
    
    return True

def get_app_url():
    """Get the Snowflake Streamlit app URL"""
    print("🔗 Getting app URL...")
    
    try:
        url_cmd = ['snow', 'streamlit', 'get-url', 'charge_mapping']
        result = subprocess.run(url_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            url = result.stdout.strip()
            print(f"🎉 App deployed successfully!")
            print(f"📱 Access your app at: {url}")
            return url
        else:
            print("⚠️  Could not retrieve app URL")
            print(result.stderr)
            
    except Exception as e:
        print(f"⚠️  Error getting URL: {e}")
    
    return None

def main():
    """Main deployment function"""
    print("🚀 Starting Charge Mapping deployment to Snowflake sandbox...")
    print("=" * 60)
    
    # Change to the project directory
    os.chdir(Path(__file__).parent)
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Deploy to sandbox
    if not deploy_to_sandbox():
        sys.exit(1)
    
    # Get app URL
    get_app_url()
    
    print("=" * 60)
    print("✅ Deployment completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Access your app using the URL above")
    print("   2. Verify all functionality works correctly")
    print("   3. Check that data loads properly from Snowflake tables")

if __name__ == "__main__":
    main()

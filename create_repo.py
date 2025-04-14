import os
import requests
from dotenv import load_dotenv
import json

def create_github_repo():
    # Load environment variables
    load_dotenv()
    token = os.getenv('GITHUB_TOKEN')
    
    if not token:
        print("Error: GitHub token not found in .env file")
        return
    
    print(f"Token loaded successfully: {token[:10]}...")
    
    # GitHub API endpoint for creating a repository
    url = "https://api.github.com/user/repos"
    
    # Repository details
    repo_data = {
        "name": "naukri_bot",
        "description": "Automated job application bot for Naukri.com",
        "private": False,
        "auto_init": True
    }
    
    # Headers for GitHub API
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        # Create repository
        response = requests.post(url, headers=headers, data=json.dumps(repo_data))
        
        if response.status_code == 201:
            repo_url = response.json()['html_url']
            print(f"Repository created successfully: {repo_url}")
            print("\nNext steps:")
            print("1. git branch -M main")
            print("2. git push -u origin main")
            return repo_url
        else:
            print(f"Error creating repository: {response.status_code}")
            print(response.json())
            return None
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    create_github_repo() 
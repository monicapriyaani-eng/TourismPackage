
from huggingface_hub import HfApi, create_repo
from huggingface_hub.utils import RepositoryNotFoundError
import os

# Retrieve Hugging Face token from environment variables (Colab Secrets, or HF Space Secrets)
access_key = os.getenv("HF_TOKEN") # Changed to use environment variable

repo_id = "Monicapriyaani/TourismPackage"
repo_type = "space" # We are deploying a Streamlit Space

api = HfApi(token=access_key)

# Check if the Space exists, if not, create it
try:
    api.repo_info(repo_id=repo_id, repo_type=repo_type)
    print(f"Hugging Face Space '{repo_id}' already exists. Uploading to it.")
except RepositoryNotFoundError:
    print(f"Hugging Face Space '{repo_id}' not found. Creating a new space...")
    # Specify space_sdk as 'streamlit' for a Streamlit app
    create_repo(repo_id=repo_id, repo_type=repo_type, private=False, space_sdk='streamlit')
    print(f"Hugging Face Space '{repo_id}' created successfully.")
except Exception as e:
    print(f"An unexpected error occurred while checking/creating space: {e}")
    print("Please ensure your HF_TOKEN is valid and has permissions to manage Hugging Face Spaces.")

# List of files to upload from the deployment folder to the root of the space
deployment_files = [
    "model.joblib",
    "features.json",
    "app.py",
    "Dockerfile",
    "requirements.txt"
]
deployment_folder = "Tourism_Package/deployment"

for filename in deployment_files:
    local_path = os.path.join(deployment_folder, filename)
    if os.path.exists(local_path):
        try:
            api.upload_file(
                path_or_fileobj=local_path,
                path_in_repo=filename, # Upload to the root of the space
                repo_id=repo_id,
                repo_type=repo_type,
            )
            print(f"Successfully uploaded {filename} to Hugging Face Space.")
        except Exception as e:
            print(f"Error uploading {filename}: {e}")
    else:
        print(f"Warning: {local_path} not found, skipping upload for this file.")

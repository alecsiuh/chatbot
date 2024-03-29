import os
import json
import pandas as pd
from dotenv import load_dotenv
import requests
import matplotlib.pyplot as plt

# Load variables from .env file into environment
load_dotenv()


class DatasetManager:

    @staticmethod
    def get_all_datasets():
        # print("get_dataset_descriptions was called")
        # print("Current working directory:", os.getcwd())
        dataset_catalogue = pd.DataFrame(columns=['id', 'description'])
        for root, dirs, files in os.walk("./Chatbot/datasets"):
            for file in files:
                if file.endswith('.json'):
                    json_file_path = os.path.join(root, file)
                    with open(json_file_path, 'r') as f:
                        dataset_info = json.load(f)
                        dataset_id = dataset_info.get('dataset')
                        description = dataset_info.get('description')
                        if dataset_id and description:
                            dataset_catalogue.loc[len(dataset_catalogue)] = {'id': dataset_id,
                                                                             'description': description}
        return dataset_catalogue

    @staticmethod
    def search_for_dataset_by_topic(user_query):
        url = os.getenv("WOBBY_URL_ENDPOINT")
        querystring = {"limit": "10", "offset": "0", "sortBy": "relevance"}
        payload = {
            "query": user_query,
            "providers": [os.getenv("WOBBY_DATA_PROVIDER")]
        }
        headers = {
            "auth-token": os.getenv("WOBBY_API_AUTH_TOKEN"),
            "content-type": "application/json"
        }
        response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

        # Parse JSON text into a Python dictionary
        response_dict = json.loads(response.text)
        # Extract datasets from the dictionary
        datasets = response_dict.get('datasets', [])
        if datasets:
            # Convert datasets into a DataFrame
            datasets = pd.json_normalize(datasets, max_level=1)
            return datasets[['dataset.id', 'dataset.name', 'dataset.shortDescription']].rename(
                columns={'dataset.id': 'id', 'dataset.name': 'name', 'dataset.shortDescription': 'description'})
        else:
            return "No dataset about this topic was found."

    @staticmethod
    def get_datasets_by_dataset_id(dataset_id):
        # print("get_datasets_by_dataset_id was called :", dataset_id)
        print("Current working directory:", os.getcwd())
        dataset = pd.DataFrame
        dataset_folder = f"./Chatbot/datasets/{dataset_id}"
        if os.path.exists(dataset_folder):
            for root, dirs, files in os.walk(dataset_folder):
                for file in files:
                    if file.endswith('.parquet'):
                        parquet_file_path = os.path.join(root, file)
                        # Read the parquet file into a pandas DataFrame
                        dataset = pd.read_parquet(parquet_file_path)
                        break
        else:
            print(f"Folder '{dataset_folder}' was not found")
        return dataset

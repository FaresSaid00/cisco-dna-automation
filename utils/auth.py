import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_dnac_token():
    url = f"{os.getenv('DNAC_URL')}/dna/system/api/v1/auth/token"
    response = requests.post(url, auth=(os.getenv("DNAC_USERNAME"), os.getenv("DNAC_PASSWORD")), verify=False)

    if response.status_code == 200:
        return response.json()["Token"]
    else:
        raise Exception(f"Failed to get token: {response.status_code} - {response.text}")

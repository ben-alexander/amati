import requests
import pathlib
import json

if __name__ == "__main__":
    response = requests.get("https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/json/licenses.json")
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    data = json.dumps(response.json())

    
    write_to = pathlib.Path(__file__).parent.parent.resolve() / 'amati/data/spdx-licences.json'  

    with write_to.open("w") as f:
        f.write(data)
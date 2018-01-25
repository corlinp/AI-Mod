from src.utils.ai_utils import root_path
import json

secrets_file_path = root_path + 'secrets.json'

try:
    with open(secrets_file_path, 'r') as f:
        secrets = json.load(f)
except:
    secrets = {}

if __name__ == '__main__':
    print(secrets)

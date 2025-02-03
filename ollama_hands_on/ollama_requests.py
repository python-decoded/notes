# pip install requests

# ollama rest api:  https://www.postman.com/postman-student-programs/ollama-api/documentation/suc47x8/ollama-rest-api

import requests
import json

url = "http://localhost:11434/api/generate"

payload = json.dumps({
  "model": "deepseek-r1:1.5b",
  "prompt": "Ollama is 22 years old and is busy saving the world. Respond using JSON",
  "stream": False,
  "format": {
    "type": "object",
    "properties": {
      "age": {
        "type": "integer"
      },
      "available": {
        "type": "boolean"
      }
    },
    "required": [
      "age",
      "available"
    ]
  }
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
data = json.loads(response.json()["response"])

print(data["age"])
print(data["available"])

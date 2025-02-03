# pip install ollama
# pip install pydantic

# more examples: https://github.com/ollama/ollama-python/tree/main/examples


from pydantic import BaseModel
from ollama import chat


class Data(BaseModel):
    age: int
    available: bool


response = chat(
    model='deepseek-r1:1.5b',
    messages=[{'role': 'user',
               'content': "Ollama is 22 years old and is busy saving the world. Respond using JSON"}],
    format=Data.model_json_schema(),  # Use Pydantic to generate the schema or format=schema
    options={'temperature': 0},  # Make responses more deterministic
)

# Use Pydantic to validate the response
data = Data.model_validate_json(response.message.content)
print(data.age)
print(data.available)

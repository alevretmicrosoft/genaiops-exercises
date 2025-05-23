import requests
from typing_extensions import Self
from typing import TypedDict

class ModelEndpoints:
    def __init__(self: Self, env: dict, model_type: str) -> str:
        self.env = env
        self.model_type = model_type

    class Response(TypedDict):
        query: str
        response: str

    def __call__(self: Self, query: str) -> Response:
        if self.model_type == "gpt-4o":
            output = self.call_gpt4o_endpoint(query)
        elif self.model_type == "gpt-4o-mini":
            output = self.call_gpt4o_mini_endpoint(query)
        else:
            output = self.call_default_endpoint(query)

        return output

    def query(self: Self, endpoint: str, headers: str, payload: str) -> str:
        response = requests.post(url=endpoint, headers=headers, json=payload)
        return response.json()

    def call_gpt4o_endpoint(self: Self, query: str) -> Response:
        endpoint = self.env["gpt-4o"]["endpoint"]
        key = self.env["gpt-4o"]["key"]

        headers = {
            "Content-Type": "application/json", 
            "api-key": key
        }
        payload = {
            "messages": [{"role": "user", "content": query}], 
            "max_tokens": 500,
            "seed": 42,
            "temperature": 0.0
        }

        output = self.query(endpoint=endpoint, headers=headers, payload=payload)
        response = output["choices"][0]["message"]["content"]
        return {"query": query, "response": response}
    
    def call_gpt4o_mini_endpoint(self: Self, query: str) -> Response:
        endpoint = self.env["gpt-4o-mini"]["endpoint"]
        key = self.env["gpt-4o-mini"]["key"]

        headers = {
            "Content-Type": "application/json", 
            "api-key": key
        }
        payload = {
            "messages": [{"role": "user", "content": query}], 
            "max_tokens": 500,
            "seed": 42,
            "temperature": 0.0
        }

        output = self.query(endpoint=endpoint, headers=headers, payload=payload)
        response = output["choices"][0]["message"]["content"]
        return {"query": query, "response": response}

    def call_default_endpoint(self: Self, query: str) -> Response:
        return {"query": query, "response": "Paris"}
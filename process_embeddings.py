#!/usr/bin/env python3
import requests

def get_embedding(filepath: str, embedding_gen_url: str="http://127.0.0.1:5000/model/predict"):
    files = {
        "audio": (filepath, open(filepath, "rb"), "audio/x-wav")
    }
    response = requests.post(embedding_gen_url, files=files)
    return response.json()["embedding"]

if __name__ == "__main__":
    print(get_embedding("dataset_converted/Beast - Vicetone Vs. Nico Vega.wav")) 

#!/usr/bin/env python3
import requests
import os

DATASET_CONVERTED = "dataset_converted"

url = "http://0.0.0.0:5000/model/predict"
files = {
    "audio": (os.path.join(DATASET_CONVERTED, "Beast - Vicetone Vs. Nico Vega.wav"), open(os.path.join(DATASET_CONVERTED, "Beast - Vicetone Vs. Nico Vega.wav"), "rb"), "audio/x-wav")
}
response = requests.post(url, files=files)
print(dir(response))
print(type(response.json()["embedding"][0][0]))

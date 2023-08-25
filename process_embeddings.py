#!/usr/bin/env python3
import requests
import numpy as np
import numpy.typing as npt

def get_embedding(filepath: str, embedding_gen_endp: str="http://127.0.0.1:5000/model/predict") -> npt.NDArray[np.float32]:
    """get embeddings as a numpy ndarray out of floats for a music file
    from a server endpoint specified through embedding_gen_endp
    """
    files = {
        "audio": (filepath, open(filepath, "rb"), "audio/x-wav")
    }
    response = requests.post(embedding_gen_endp, files=files)
    return np.array(response.json()["embedding"])

if __name__ == "__main__":
    embd = get_embedding("dataset_converted/Beast - Vicetone Vs. Nico Vega.wav")
    print(embd.flatten())

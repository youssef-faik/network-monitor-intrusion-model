from datetime import datetime
import hashlib
import json
import pickle
from flask import Flask, request, jsonify
from flask_restful import Api
import os
import tensorflow as tf
from keras.models import load_model
from typing import TypedDict, List
import numpy as np
import pandas as pd
# Initialize Flask app
app = Flask(__name__)



# Load the model
model = load_model(os.path.join(os.path.dirname(__file__), "latest.keras"))
required_fields = [
    "Duration", "Protocol", "SourceIP", "DestinationIP", "SourcePort", "DestinationPort", "PacketCount", "ByteCount"

]


rename_mapping = {
            "flowDuration": "Duration",
            "protocol": "Protocol",
            "sourceIp": "SourceIP",
            "destinationIp": "DestinationIP",
            "sourcePort": "SourcePort",
            "destinationPort": "DestinationPort",
            "packetLength": "PacketCount",
            "totalBytes": "ByteCount",
            
        }


encoders = {}    
categorical_columns = ["Protocol", "SourceIP", "DestinationIP"]
with open(os.path.join(os.path.dirname(__file__), "encoders.pkl"), "rb") as f:
    encoders = pickle.load(f)

def hash_ip(ip: str, hash_size: int = 1000) -> int:
    
    hash_object = hashlib.sha256(ip)
    hash_int = int(hash_object.hexdigest(), 16)
    return hash_int % hash_size

def prepareData(data: list):
    """
    Preprocess incoming data for the model.
    Args:
        data (list): List of JSON-like dictionaries representing incoming data.
    Returns:
        pd.DataFrame: Preprocessed DataFrame ready for prediction.
    """
    # Convert to DataFrame and rename columns
    df = pd.DataFrame(data).rename(columns=rename_mapping)
    
    # Ensure all required fields are present
    for field in required_fields:
        if field not in df:
            df[field] = 0  # Default value for missing fields (adjust as needed)

    # Retain only the required fields
    df = (df[required_fields]).applymap(lambda x: hash_ip(str(x).encode('utf-8')))

    # Transform categorical columns
  

    return df


class PacketData(TypedDict):
    sourceIp: str
    sourcePort: int
    destinationIp: str
    destinationPort: int
    protocol: str
    packetLength: int
    packetType: str
    flags: str
    totalBytes: int
    retransmissionCount: int
    connectionCount: int
    flowDuration: int
    timestamp: str

@app.route('/', methods=['GET'])
def get():
    return 'Hello, World!'

@app.route('/analyze', methods=['POST'])
def analyze_packets():
    try:
        jsondata = request.get_json()
        print(jsondata,"\n\n\n\n")
        x = prepareData(jsondata)
        
        y = model.predict(x)
        y = np.argmax(y, axis=1)
        y_list = y.tolist()
        return jsonify({"success": "Analysis completed" , "data" : y_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)



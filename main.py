import os
import pandas as pd
import numpy as np
from flask import Flask, jsonify, request

app = Flask(__name__)

# 1. Handle startup gracefully if the file is missing
try:
    # 2. Replace Pandas NaNs with None so jsonify outputs valid JSON 'null'
    df = pd.read_csv('hats.csv').replace({np.nan: None})
except FileNotFoundError:
    print("WARNING: 'hats.csv' not found. Starting with an empty DataFrame.")
    df = pd.DataFrame(columns=['category', 'status']) # Fallback structure

@app.route('/hats', methods=['GET'])
def get_hats():
    category = request.args.get('category')
    status = request.args.get('status')
    
    filtered_df = df
    if category:
        filtered_df = filtered_df[filtered_df['category'] == category]
    if status:
        filtered_df = filtered_df[filtered_df['status'] == status]
        
    return jsonify(filtered_df.to_dict(orient='records'))

@app.route('/hats/surprise', methods=['POST'])
def surprise_me():
    # 3. Use get_json(silent=True) to safely parse the payload without crashing
    data = request.get_json(silent=True) or {}
    category = data.get('category')
    status = data.get('status')
    
    filtered_df = df
    if category:
        filtered_df = filtered_df[filtered_df['category'] == category]
    if status:
        filtered_df = filtered_df[filtered_df['status'] == status]
        
    if filtered_df.empty:
        return jsonify({"message": "No hats found matching the criteria."}), 404
        
    # 4. Use Pandas' native .sample() method for cleaner random selection
    random_hat = filtered_df.sample(n=1)
    
    return jsonify(random_hat.to_dict(orient='records')[0])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
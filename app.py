
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS 
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
CORS(app)

# Serve front.html when user opens root "/"
@app.route("/")
def serve_frontend():
    return send_from_directory(os.getcwd(), "front.html")

# API endpoint for fetching and cleaning data
@app.route("/api/fetch")
def fetch_scheme():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL missing"}), 400

    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        eligibility=[]
        documents=[]
        howto=[]

        elig_keywords = ["eligibility", "who can apply", "applicant"]
        doc_keywords = ["document", "certificate", "required papers"]
        apply_keywords = ["how to apply", "apply online", "application process"]
        
    
        for elem in soup.find_all(["p", "li", "div", "span", "td"]):
            text = elem.get_text(strip=True).lower()

            # Eligibility check
            if any(k in text for k in elig_keywords):
                eligibility.append(elem.get_text(strip=True))

            
            if any(k in text for k in doc_keywords):
                documents.append(elem.get_text(strip=True))

            if any(k in text for k in apply_keywords):
                howto.append(elem.get_text(strip=True))

        if not eligibility:
            eligibility = ["Not found"]
        if not documents:
            documents = ["Not found"]
        if not howto:
            howto=["Not found"]

        return jsonify({
            "eligibility": eligibility,
            "documents": documents,
            "howto":howto,
            "links": [url]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)
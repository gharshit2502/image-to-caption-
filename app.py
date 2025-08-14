from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

# === CONFIG ===
API_KEY = "AIzaSyCzkY-nwby9qIUpvZO6z5Rd9_n-tvQSfAw"  
# === FLASK APP ===
app = Flask(__name__)
genai.configure(api_key=API_KEY)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_image():
    try:
        data = request.json
        image_base64 = data.get("image")
        if not image_base64:
            return jsonify({"error": "No image provided"}), 400

        image_part = {
            "inline_data": {
                "mime_type": "image/jpeg",  # Change if PNG
                "data": image_base64
            }
        }

        # Call Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([image_part, "Describe this image as a short caption."])

        caption = response.text.strip()
        return jsonify({"caption": caption})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

import os
import base64
from io import BytesIO
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
PORT = int(os.getenv("PORT", 5000))

app = Flask(__name__)
CORS(app)

def build_prompt(color, fabric, outfit, notes):
    prompt = f"""
    A professional fashion model wearing a {color} {fabric} {outfit},
    {notes},
    full body view, studio photoshoot, clean plain background,
    high quality fashion photography, realistic lighting,
    sharp focus, detailed fabric texture
    """
    return " ".join(prompt.split())

def pil_to_data_url(pil_img):
    buf = BytesIO()
    pil_img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64}"

# HuggingFace client
client = InferenceClient(provider="auto", api_key=HF_TOKEN)

@app.route("/")
def home():
    return "AI Fashion Backend Running!"


# ---------------- HEALTH ----------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "time": datetime.utcnow().isoformat()})

# ---------------- IMAGE GENERATOR ----------------
@app.route("/generate-image", methods=["POST"])
def generate_image():
    try:
        if not HF_TOKEN:
            return jsonify({"error": "HF_TOKEN missing in .env"}), 500

        data = request.get_json(force=True) or {}

        color = data.get("color", "Blue")
        fabric = data.get("fabric", "Cotton")
        outfit = data.get("outfit", "Kurti")
        notes = data.get("notes", "minimal elegant design")

        prompt = build_prompt(color, fabric, outfit, notes)

        pil_image = client.text_to_image(
            prompt,
            model="black-forest-labs/FLUX.1-schnell"
        )

        return jsonify({
            "prompt": prompt,
            "image": pil_to_data_url(pil_image)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- RECOMMENDATIONS ----------------
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json() or {}

    segment = data.get("segment", "")
    season = data.get("season", "")
    goal = data.get("goal", "")

    suggestions = [
        {
            "product": "Lightweight Cotton Kurti",
            "reason": f"Popular among {segment} customers and perfect for {season} season."
        },
        {
            "product": "Pastel Linen Shirt",
            "reason": f"Helps achieve the business goal: {goal} with a modern minimalist look."
        }
    ]

    return jsonify({
        "status": "success",
        "recommendations": suggestions
    })

# ---------------- CONTENT GENERATOR ----------------
@app.route("/content", methods=["POST"])
def content():
    data = request.get_json() or {}

    product = data.get("product", "")
    tone = data.get("tone", "")
    avoid = data.get("avoid", "")
    include = data.get("include", "")

    text = f"""
    Introducing our {product} — designed to bring comfort and style together.
    Crafted with attention to detail, this piece reflects a {tone} brand voice.
    Perfect for everyday elegance. {include}
    """

    if avoid:
        text += f" (Avoiding words like: {avoid})"

    return jsonify({
        "status": "success",
        "generated_text": text.strip()
    })

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=PORT, debug=True)

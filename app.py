from flask import Flask, request, jsonify
from PIL import Image
import base64, io, requests, os

app = Flask(__name__)

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")

@app.route("/screenshot", methods=["POST"])
def screenshot():
    body = request.get_json()
    raw = base64.b64decode(body["data"])
    img = Image.frombytes("RGBA", (body["width"], body["height"]), raw)
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    
    requests.post(DISCORD_WEBHOOK, files={"file": ("screenshot.png", buf, "image/png")})
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

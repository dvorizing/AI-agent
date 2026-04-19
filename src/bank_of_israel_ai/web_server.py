"""Flask web server for the AI Procurement Agent.

Accepts a product name and email address via the web UI prompt
and runs the CrewAI procurement agent.
"""

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from .agents.procurement_agent import run_procurement_agent

app = Flask(__name__, template_folder="templates", static_folder="static")
load_dotenv()


# ----- Routes -----

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/search", methods=["POST"])
def search():
    """Run the procurement agent for the given prompt."""
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()

        if not prompt:
            return jsonify({"error": "הפרומפט ריק – הקלד שם מוצר ומייל"}), 400

        # Send the raw prompt to the CrewAI agent – let the LLM parse it
        result_text = run_procurement_agent(
            prompt=prompt,
            env_path=".env",
        )

        return jsonify(
            {
                "success": True,
                "prompt": prompt,
                "results": result_text,
            }
        )

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


def run_web():
    """Start the Flask development server."""
    print("\n" + "=" * 70)
    print("🌐  AI PROCUREMENT AGENT – Web Interface")
    print("=" * 70)
    print("\n📍  http://127.0.0.1:5000")
    print("Press Ctrl+C to stop\n")
    app.run(debug=False, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    run_web()


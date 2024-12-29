from flask import Flask, render_template, request, send_file
from backend_mul_websites import scrape_multiple_pages_to_csv


import os

app = Flask(__name__)


OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/")
def index():
    """Render the home page."""
    return render_template("index.html")


@app.route("/scrape", methods=["POST"])
def scrape():
    model_filter = request.form.get("model")
    if not model_filter:
        return "Please select a vehicle model.", 400

    output_file = os.path.join(OUTPUT_DIR, "scraped_Hondas.csv")

    try:
        scrape_multiple_pages_to_csv(output_file, model_filter)
        return send_file(output_file, as_attachment=True)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500





if __name__ == "__main__":
    app.run(debug=True)

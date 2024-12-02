from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/hello", methods=["POST"])
def hello():
    # Return the "Hello, World!" message when the button is clicked
    return render_template("index.html", message="Hello, World!")

if __name__ == "__main__":
    app.run(host="::", port=5000, debug=True)  # Bind to IPv6 and enable debug mode

from flask import Flask, request

app = Flask(__name__)

@app.route("/search")
def search():
    # This reflects user input unsafely (for XSS testing only)
    query = request.args.get("q", "")
    return f"""
    <html>
      <body>
        <h1>Search Results</h1>
        <p>You searched for: {query}</p>
      </body>
    </html>
    """

@app.route("/comment", methods=["GET", "POST"])
def comment():
    if request.method == "POST":
        text = request.form.get("text", "")
        # unsafe echo of comment (for stored XSS testing)
        return f"<p>Comment stored: {text}</p>"
    return """
      <form method="post">
        <input type="text" name="text">
        <input type="submit" value="Submit">
      </form>
    """

if __name__ == "__main__":
    app.run(debug=True)

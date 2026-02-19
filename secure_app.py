from flask import Flask, render_template, request, escape

app = Flask(__name__)

@app.route("/search")
def search_secure():
    query = request.args.get("q", "")
    # escape output so it cannot execute as script
    safe_query = escape(query)
    return render_template("search.html", query=safe_query)

@app.route("/comment", methods=["GET", "POST"])
def comment_secure():
    if request.method == "POST":
        text = request.form.get("text", "")
        safe_text = escape(text)  # escape comment
        return render_template("comment.html", comment=safe_text)
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)

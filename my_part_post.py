from textblob import TextBlob
import requests
import json
from flask import Flask, request, render_template, redirect, url_for

## Process data
## ......


app = Flask(__name__, template_folder='templates')

# DASHBOARD
@app.route("/", methods = ["POST", "GET"])
def search():
    if request.method == "POST":
        return redirect(url_for("service"))
    else:
        return render_template("my_part.html")

# SERVICE 1
@app.route("/service", methods = ["POST", "GET"])
def service():
    if request.form['service'] == "translate":
        f = open("test_review.txt",'r')
        l = []
        for l in f.readlines():
            blob = TextBlob(l)    
            chinese_blob = blob.translate(from_lang='en', to='zh-CN')
        f.close()
        return render_template("service.html", name=chinese_blob)
    else:
        return render_template("my_part.html")

# SERVICE 2
# ......


if __name__ == "__main__":
    app.run(port=5000, debug=True)
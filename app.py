import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

openai.api_key = os.environ['openai_api_key']

def training_data(data):
    return """Please predict text as postive or negative.
    text: You are a bad man.
    sentiment: negative
    text: You are a good man.
    sentiment: positive
    text:  {}
    sentiment:""".format(data.capitalize())
 
@app.route('/', methods=("GET", "POST"))
def index():
    if request.method == "POST":
        data = request.form["data"]
        res = openai.Completion.create(model="text-davinci-003", prompt=training_data(data), temperature=0.1)
        return redirect(url_for('index', result=res.choices[0].text))
    result = request.args.get("result")
    return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run()
    

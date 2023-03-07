import os
import uuid 
import openai
from flask import Flask, redirect, render_template, request, url_for
import azure.cosmos.cosmos_client as cosmos_client

app = Flask(__name__)

# Configure variables
openai.api_key = os.environ.get('OPENAI_API_KEY')
db_endpoint = os.environ.get("COSMOS_ENDPOINT")
db_key = os.environ.get("COSMOS_KEY")
database_name = "db1"
container_name = "sentiment"

# Connect to CosmosDB container
client = cosmos_client.CosmosClient(url=db_endpoint, credential=db_key)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

def training_data(data):
    return """Please predict text as POSITIVE, NEGATIVE or NEUTRAL:
    text:  {}
    sentiment:""".format(data)
 
@app.route('/', methods=("GET", "POST"))
def index():
    if request.method == "POST":
        data = request.form["data"]
        res = openai.Completion.create(model="text-davinci-003", prompt=training_data(data), temperature=0.1)
        id = str(uuid.uuid1())
        new_item = {"text": data, "sentiment": res.choices[0].text, "id": id}
        container.upsert_item(new_item)
        return redirect(url_for('index', result=res.choices[0].text))
    result = request.args.get("result")
    return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run()
    

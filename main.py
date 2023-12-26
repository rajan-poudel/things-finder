from flask import Flask , render_template ,request ,redirect ,flash
import os
from werkzeug.utils import secure_filename
import pymongo
import re
from datetime import datetime


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["thingfinder"]
collection = db["thingfinder"] 


app = Flask(__name__)
app.config['Upload_Folder'] = "C:/CodePlayground/Things-Finder/static/Upload_Folder"
app.secret_key="supersecretkeydkdjd"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/thinggot", methods=['GET', 'POST'])
def thinggot():
    if request.method == "POST":
        phone = request.form.get("phone")
        thinggot = request.form.get("thinggot")
        file = request.files['file']
        file.save(os.path.join(app.config['Upload_Folder'],secure_filename(f"{thinggot}.png")))
        user_data = {
    "phone": phone,
    "thinggot":thinggot,
    "date": datetime.now()
}
        result = collection.insert_one(user_data)
        flash("Your data is submitted","success")
        return redirect('/search')
        

@app.route("/thinglost", methods=['GET', 'POST'])
def thinglost():
    if request.method == "POST":
        phone = request.form.get("phone")
        thinglost = request.form.get("thinglost")
        pattern = re.compile(re.escape(thinglost), re.IGNORECASE)
        results = db["thingfinder"].find({"thinggot": pattern})
        return render_template('found.html', results=results)  
    return redirect("/search")

if __name__ == "__main__":
    app.run(debug=True)
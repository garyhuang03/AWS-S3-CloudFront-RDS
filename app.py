from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_bootstrap import Bootstrap
import boto3
from config import S3_BUCKET
import os
from filters import *
from db import Connect
db = Connect()

app = Flask(
    __name__,
    static_folder = "static",
    static_url_path = "/"
)
Bootstrap(app)
app.config.from_object("config")
app.config["DEBUG"]
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = os.urandom(16)

app.jinja_env.filters["datetimeformat"] = datetimeformat
app.jinja_env.filters["file_name"] = file_name

@app.route("/")
def index():
    # get photo_name and url from AWS RDS 
    # s3_resource = boto3.resource("s3")
    # bucket = s3_resource.Bucket(S3_BUCKET)
    # imgs = bucket.objects.all()
    result = db.get_all_photos()
    return render_template("index.html", imgs = result)

@app.route("/upload", methods = ["POST"])
def upload():
    # get file and file name
    file = request.files["file"]
    name = request.form["file-name"] + "." + file.filename.split(".")[1]
    # upload to AWS S3
    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(S3_BUCKET)
    bucket.Object(name).put(Body = file)
    # write to AWS RDS
    result = db.insert(name)
    if result == "insert success":
        flash("File uploaded successfully")
        return redirect(url_for("index"))
    if result == "MySQL connection error":
        flash("File name duplicate or other error")
        return redirect(url_for("index"))

@app.route("/delete", methods = ["POST"])
def delete():
    key = request.form["key"]
    # AWS S3 : delete photo
    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(S3_BUCKET)
    bucket.Object(key).delete()
    # AWS RDS : delete record
    result = db.delete(key)
    if result == "delete success":
        flash("file deleted successfully")
        return redirect(url_for("index"))

@app.route("/download", methods = ["POST"])
def download():
    key = request.form["key"]
    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(S3_BUCKET)
    file_obj = bucket.Object(key).get()
    return Response(
        file_obj["Body"].read(),
        mimetype = "text/plain",
        headers = {
            "Content-Disposition": "attachement;filename={}".format(key.encode("utf-8").decode("latin1"))
        }
    )

if __name__ == "__main__":
    app.run(port = 5000)

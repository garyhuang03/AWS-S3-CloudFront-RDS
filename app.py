from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_bootstrap import Bootstrap
import boto3
from config import S3_BUCKET
import os
import arrow

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

def datetimeformat(date_str):
    dt = arrow.get(date_str)
    return dt.humanize()
app.jinja_env.filters["datetimeformat"] = datetimeformat

@app.route("/")
def index():
    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(S3_BUCKET)
    imgs = bucket.objects.all()
    return render_template("index.html", imgs = imgs)

@app.route("/upload", methods = ["POST"])
def upload():
    file = request.files["file"]
    name = request.form["file-name"] + "." + file.filename.split(".")[1]
    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(S3_BUCKET)
    bucket.Object(name).put(Body = file)
    flash("File uploaded successfully")
    return redirect(url_for("index"))

@app.route("/delete", methods = ["POST"])
def delete():
    key = request.form["key"]
    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(S3_BUCKET)
    bucket.Object(key).delete()
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
            "Content-Disposition": "attachement;filename={}".format(key)
        }
    )

if __name__ == "__main__":
    app.run()

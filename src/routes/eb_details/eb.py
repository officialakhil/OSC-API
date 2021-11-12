from flask import (
    Flask,
    jsonify,
    request,
    Blueprint,
    redirect,
    flash,
    current_app,
)
from pymongo import results
from werkzeug.utils import secure_filename
import os
from src.routes.eb_details.db_connection import *
from src.routes.eb_details.csv_to_json import csv_to_json

UPLOAD_FOLDER = "temp"
ALLOWED_EXTENSIONS = {"csv"}
eb_bp = Blueprint("eb", __name__, url_prefix="/eb")


@eb_bp.route("/", methods=["GET"])
def get_data():
    data = connection()
    return "WORKING ON IT"


@eb_bp.route("/current", methods=["GET"])
def current_eb():
    result = getData()
    return result


@eb_bp.route("/uploadCSV", methods=["GET", "POST"])
def uploadFiles():
    current_app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    if request.method == "POST":
        if "file" not in request.files:
            return "<h2> ERROR: File not found. Please upload a CSV file containing details </h2>"
        file = request.files["file"]
        filename = file.filename
        if filename == "":
            flash("No selected file")
            return "<h2> ERROR: File not found. Please upload a CSV file containing EB details </h2>"
        allowed_file = "." in filename and filename.rsplit(".", 1)[1].lower() in {"csv"}
        if file and allowed_file:
            filename = secure_filename(filename)
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            try:
                result = csv_to_json(f"{UPLOAD_FOLDER}/{filename}")
            except:
                return "<h2> ERROR: Make sure to follow exact structure as provided in examples/ebDetails.csv </h2>"
            return result
        else:
            return (
                "<h2> ERROR: Make sure to upload a CSV file containing EB details </h2>"
            )
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """
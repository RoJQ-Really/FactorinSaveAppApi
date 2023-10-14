from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import zlib
import base64
app = Flask(__name__)
api = Api(app)

@app.route("/upload_save", methods=["POST"])
def upload_save():
    SaveFile = request.files.get("save")
    if SaveFile is None:
        return "Не передано сохраниение", 200
    if SaveFile.filename.split(".")[-1] != "zip":
        return "Тип не соответствует zip", 200
    SaveFile.save("save_directory/save.zip")
    return "true", 200

@app.route("/get_save", methods=["GET"])
def get_save():
    output_file = open("save_directory/save.zip", "rb")
    output_content = base64.a85encode(output_file.read())
    return output_content, 200

if __name__ == '__main__':
    app.run()

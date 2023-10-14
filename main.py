import json

from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import os
import base64
app = Flask(__name__)
api = Api(app)
EXEC_PATH = os.getcwd()
print(EXEC_PATH)
MAX_PASS_LEN = 64  # Длина пароля
with open(f"{EXEC_PATH}/password.json", 'r') as PassFile:
    PassData = json.loads(PassFile.read())  # Пароли
    for index, password_i in enumerate(PassData):
        PassData[index] = password_i.zfill(MAX_PASS_LEN)
with open(f"{EXEC_PATH}/directory_info.json", "r") as DirInfo:
    DirData = json.loads(DirInfo.read())


def check_pass(password: str):
    if len(password) > 64:
        return "Pass is to long", 200
    password_filled = password.zfill(MAX_PASS_LEN)  # Заполняем нулями
    if password_filled not in PassData:
        return 'Неправильный пароль!', 200
    return True

@app.route("/upload_save/password=<password>", methods=["POST"])
def upload_save(password: str):
    check_ = check_pass(password)
    if type(check_) is tuple:
        return check_

    path_to_save = f"{EXEC_PATH}/{DirData.get(password)}/save.zip"
    if os.path.exists(path_to_save):
        os.remove(path_to_save)

    SaveFile = request.files.get("save")
    if SaveFile is None:
        return "Не передано сохраниение", 200
    if SaveFile.filename.split(".")[-1] != "zip":
        return "Тип не соответствует zip", 200
    SaveFile.save(path_to_save)
    return "true", 200


@app.route("/get_save/password=<password>", methods=["GET"])
def get_save(password: str):
    check_ = check_pass(password)
    if type(check_) is tuple:
        return check_
    path_to_file = f"{EXEC_PATH}/{DirData.get(password)}/save.zip"
    with open(path_to_file, 'rb') as ZipBytes:
        output_content = ZipBytes.read()
    return output_content, 200


if __name__ == '__main__':
    app.run()

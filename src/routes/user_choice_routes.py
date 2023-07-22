# to do
from flask import Blueprint, jsonify, request

from dao.CRUD import *
from utils import from_db_to_file
from utils.get_weight import *
from utils.info import *

# Создаем Blueprint, чтобы определить маршруты
user_choice_bp = Blueprint('user_choice_routes', __name__)


@user_choice_bp.route('/user_choice', methods=['POST'])
def user_choice():
    try:
        # Получение данных из тела запроса (тело запроса представляет собой JSON-объект)
        data = request.json

        mes = data['message']
        arr = data["arr_user_choice"]

        # Запись содержимого массива в текстовый файл
        with open('data.txt', 'w') as file:
            file.write(mes + '\n')
            for item in arr:
                file.write(str(item) + '\n')

        # Возвращение ответа клиенту (при необходимости)
        return jsonify(data)

    except Exception as e:
        # Обработка ошибок (например, если данные не были отправлены в правильном формате)
        return jsonify({"error": str(e)}), 400


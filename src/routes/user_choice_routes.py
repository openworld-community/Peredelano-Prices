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
    # Получаем данные из тела запроса
    data = request.json  # Для JSON данных
    # data = request.form['array']  # Для форм-данных, если вы отправляете данные как форму

    if data is None:
        return jsonify({"error": "No data provided"}), 400

    return jsonify({"result": data})

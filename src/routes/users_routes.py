from flask import Blueprint, jsonify, redirect, render_template, url_for, request

from dao.Users_db import *


# Создаем Blueprint, чтобы определить маршруты
users_bp = Blueprint('users_routes', __name__)


@users_bp.route('/add-user/test')
def test_add_user():
    add_user("testname", "testpass", "slave", "1")
    doc = get_user_by_name("testname")
    return str(doc)


@users_bp.route('/update-user/test')
def test_update_user_acc():
    list_to_show = list()
    list_to_show.append(str(get_user_by_name("testname")))
    updated_user = update_acc("testname", "subscription_level", "2")
    list_to_show.append(str(updated_user))
    if updated_user["subscription_level"] == "2":
        list_to_show.append(str(update_acc("testname", "role", "dungeon_master")))
    return jsonify(results=list_to_show)



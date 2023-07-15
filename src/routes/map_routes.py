import folium
from flask import render_template, Blueprint
from folium.plugins import MousePosition

from utils.info import *

# Создаем Blueprint, чтобы определить маршруты
map_bp = Blueprint('map_routes', __name__)


@map_bp.route('/coords-of-markets/<market>')
def get_coords_of_markets(market):
    to_ret = None
    match market:
        case "Aroma":
            to_ret = coords_of_Aroma_markets
        case "Franca":
            to_ret = coords_of_Franca_markets
        case "Voli":
            to_ret = coords_of_Voli_markets

    return to_ret


@map_bp.route('/map')
def open_map():
    map = folium.Map(location=[42.44510285, 19.258387751564968], zoom_start=14)

    for coords in coords_of_Aroma_markets:
        folium.Marker(location=coords, popup="Aroma", icon=folium.Icon(color='orange')).add_to(map)

    for coords in coords_of_Franca_markets:
        folium.Marker(location=coords, popup="Franca", icon=folium.Icon(color='red')).add_to(map)

    for coords in coords_of_Voli_markets:
        folium.Marker(location=coords, popup="Voli", icon=folium.Icon(color='green')).add_to(map)

    map.add_child(folium.ClickForLatLng())
    map.add_child(folium.LatLngPopup())
    map.add_child(folium.ClickForMarker())

    MousePosition().add_to(map)

    map.save("templates/Podgorica_map.html")

    return render_template("Podgorica_map.html")

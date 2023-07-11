import folium


# def on_map_click(event):
#     lat = event.latlng[0]
#     lon = event.latlng[1]
#     print(f"Клик по координатам: ({lat}, {lon})")


def add_handler_for_marker(map):
    click_handler = folium.ClickForMarker()
    map.add_child(click_handler)

def add_handler_for_coords(map):
    click_handler = folium.ClickForLatLng()
    map.add_child(click_handler)
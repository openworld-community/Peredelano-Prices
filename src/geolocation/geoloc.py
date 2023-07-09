
import folium



coords_of_Aroma_markets = [
    [42.44743, 19.25001],
    [42.45004, 19.23621],
    [42.43793, 19.23752],
    [42.42672, 19.24672],
    [42.42758, 19.25225],
    [42.42815, 19.27409],
    [42.43395, 19.28076],
    [42.43547, 19.2778],
    [42.44166, 19.26338],
    [42.44355, 19.25267],
    [42.44159, 19.25163]
]

coords_of_Franca_markets = [
    [42.45401, 19.26063],
    [42.44522, 19.25504],
    [42.45151, 19.23678],
    [42.43805, 19.22601],
    [42.43059, 19.25742],
    [42.43358, 19.26262],
    [42.43556, 19.28016],
    [42.43782, 19.27726],
]

coords_of_Voli_markets = [
    [42.44953, 19.25939],
    [42.44769, 19.24537],
    [42.44712, 19.24267],
    [42.44924, 19.23057],
    [42.43778, 19.2321],
    [42.42913, 19.27182],
    [42.44252, 19.27376],
    [42.4443, 19.25227],
    [42.4421, 19.24817],
    [42.44128, 19.2529],
    [42.44042, 19.26387],
    [42.43491, 19.26032],
]

def open_map_with_markets():

    map = folium.Map(location=[42.44510285, 19.258387751564968], zoom_start=14)

    for coords in coords_of_Aroma_markets:
        folium.Marker(location=coords, popup="Aroma").add_to(map)

    for coords in coords_of_Franca_markets:
        folium.Marker(location=coords, popup="Franca").add_to(map)

    for coords in coords_of_Voli_markets:
        folium.Marker(location=coords, popup="Voli").add_to(map)

    map.save("Podgorica_map.html")

open_map_with_markets()
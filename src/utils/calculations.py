from math import radians, sin, cos, sqrt, atan2


def distance(lat1, lon1, lat2, lon2):

    R = 6371.0

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Разница между широтами и долготами
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    # Формула Haversine
    a = sin(delta_lat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance


def dist_from_user(user_location,
                   coords_of_Aroma_markets,
                   coords_of_Franca_markets,
                   coords_of_Voli_markets):

    min_distance_A = float('inf')
    nearest_shop_A = None

    for shop in coords_of_Aroma_markets:
        shop_lat, shop_lon = shop
        distance_km = distance(user_location[0], user_location[1], shop_lat, shop_lon)

        if distance_km < min_distance_A:
            min_distance_A = distance_km
            nearest_shop_A = shop


    min_distance_F = float('inf')
    nearest_shop_F = None

    for shop in coords_of_Franca_markets:
        shop_lat, shop_lon = shop
        distance_km = distance(user_location[0], user_location[1], shop_lat, shop_lon)

        if distance_km < min_distance_F:
            min_distance_F = distance_km
            nearest_shop_F = shop


    min_distance_V = float('inf')
    nearest_shop_V = None

    for shop in coords_of_Voli_markets:
        shop_lat, shop_lon = shop
        distance_km = distance(user_location[0], user_location[1], shop_lat, shop_lon)

        if distance_km < min_distance_V:
            min_distance_V = distance_km
            nearest_shop_V = shop

    return "min_dist_A = " + str(min_distance_A*1000) +\
        "m;\n min_dist_F = " + str(min_distance_F*1000) +\
        "m;\n min_dist_V = " + str(min_distance_V*1000) + "m;"


def analyze_prices(prices):

    min_price = min(prices)

    max_price = max(prices)

    avg_price = sum(prices) / len(prices)

    sorted_prices = sorted(prices)
    n = len(sorted_prices)
    if n % 2 == 0:
        median_price = (sorted_prices[n//2 - 1] + sorted_prices[n//2]) / 2
    else:
        median_price = sorted_prices[n//2]

    return min_price, max_price, avg_price, median_price


def calculate_price_difference(min_price, avg_price):
    difference_percent = ((avg_price - min_price) / avg_price) * 100
    return difference_percent


def price_per_kg(price, weight):
    if price and weight:
        price = replace_comma_with_dot(price)
        return float(price)/float(weight)*1000
    else:
        return None


def replace_comma_with_dot(number_str):
    return number_str.replace(',', '.')
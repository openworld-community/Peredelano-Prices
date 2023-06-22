from bs4 import BeautifulSoup
import requests
from entities.ProductClass import Product


def get_soup_from_url(url: str):
    with requests.Session() as session:
        result = session.get(url)

    return BeautifulSoup(result.text, "html.parser").find('div', 'store__body__dynamic-content')


def split_weight(describe):
    weight = []
    for word in range(len(describe)):
        if describe[word] == 'l' or describe[word] == 'ml' or describe[word] == 'g':
            weight = [describe[word - 1], describe[word]]
    return weight


def scraping(url_voli, collection_name):
    div_store_body = get_soup_from_url(url=url_voli)
    div_carousels = div_store_body.find_all('div', 'carousel')

    meat_category_url = ""
    milk_category_url = ""
    fruit_category_url = ""
    farinaceous_category_url = ""
    list_voli_category_urls = [
        [meat_category_url, "meatCategory"],
        [milk_category_url, "milkCategory"],
        [fruit_category_url, "fruitCategory"],
        [farinaceous_category_url, "farinaceousCategory"]
    ]

    for temp in div_carousels:

        temp1 = temp.find('div', 'carousel__title-container')
        temp2 = temp1.find('h2', 'carousel__title')

        if "Mesara" in temp2:
            temp1 = temp.find('a', 'carousel__link link')
            temp3 = "https://glovoapp.com" + temp1.get('href')
            list_voli_category_urls[0][0] = temp3

        if "Mliječni proizvodi i jaja" in temp2:
            temp1 = temp.find('a', 'carousel__link link')
            temp3 = "https://glovoapp.com" + temp1.get('href')
            list_voli_category_urls[1][0] = temp3

        if "Voće" in temp2:
            temp1 = temp.find('a', 'carousel__link link')
            temp3 = "https://glovoapp.com" + temp1.get('href')
            list_voli_category_urls[2][0] = temp3

        if "Pekara" in temp2:
            temp1 = temp.find('a', 'carousel__link link')
            temp3 = "https://glovoapp.com" + temp1.get('href')
            list_voli_category_urls[3][0] = temp3

    list_voli_all_urls = []

    for temp_url in list_voli_category_urls:
        if not temp_url[0]:
            print('empty')
            continue

        store_content = get_soup_from_url(url=temp_url[0])

        tiles = store_content.find_all('div', 'tile')

        for tile in tiles:
            for_href = tile.find('a', 'nuxt-link-active')
            href = "https://glovoapp.com" + for_href.get('href')
            forsubcategory = tile.find('div', 'tile__description')
            subcategory = forsubcategory.text

            # to each link chains the name of the category and subcategory
            list_voli_all_urls.append([href, temp_url[1], subcategory])

    counter = 0

    for url in list_voli_all_urls:
        category = url[1]
        currentsubcategory = url[2]
        store_content = get_soup_from_url(url=url[0])

        all_ok = False

        try:
            product_titles = store_content.find_all('div', 'tile')
            all_ok = True
        except:
            all_ok = False

        if all_ok is False:
            product_titles = store_content.find('div', 'tile')

        all_items = []
        for prod_tile in product_titles:
            prod_tile_name = prod_tile.find('span', 'tile__description')
            prod_tile_price = prod_tile.find('span', 'product-price__effective')
            counter += 1
            content_name_tobd = prod_tile_name.text
            content_price_tobd = prod_tile_price.text
            temp_product = Product(content_name_tobd, content_price_tobd)

            temp_item = {
                "_id": counter,
                "product": {'name': temp_product.name.strip(),
                            'price': temp_product.price.strip().split('\xa0'),
                            'weight': split_weight(temp_product.name.strip().lower().split())},
                "category": category.strip(),
                "subcategory": currentsubcategory.strip()
            }
            all_items.append(temp_item)
        collection_name.insert_one(tempItem)
    return counter

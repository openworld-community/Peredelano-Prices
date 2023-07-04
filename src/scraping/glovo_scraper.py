import requests
from bs4 import BeautifulSoup

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


def scraping(markets, urls, collections_names, categories_to_scrap_dict):
    counter = 0
    list_of_problems = list()
    # Aroma, Franca, Voli
    for market in markets:

        url = urls.get(market)
        collection_name = collections_names.get(market)
        categories_to_scrap = categories_to_scrap_dict.get(market)

        div_store_body = get_soup_from_url(url=url)
        div_carousels = div_store_body.find_all('div', 'carousel')

        list_category_urls = list()

        for category in categories_to_scrap:
            is_found = False
            for temp in div_carousels:
                temp1 = temp.find('div', 'carousel__title-container')
                temp2 = temp1.find('h2', 'carousel__title')
                if category in temp2:
                    temp1 = temp.find('a', 'carousel__link link')
                    temp3 = "https://glovoapp.com" + temp1.get('href')
                    list_category_urls.append(temp3)
                    is_found = True
                    break
            if not is_found:
                problem = category + " is not found in " + market + "\n"
                list_of_problems.append(problem)
                #
                # here try another tags
                #

        list_all_urls = list()

        for temp_url in list_category_urls:
            if not temp_url:
                print('empty')
                continue

            store_content = get_soup_from_url(url=temp_url)

            tiles = store_content.find_all('div', 'tile')

            for tile in tiles:
                for_href = tile.find('a', 'nuxt-link-active')
                href = "https://glovoapp.com" + for_href.get('href')
                forsubcategory = tile.find('div', 'tile__description')
                subcategory = forsubcategory.text

                # to each link chains the name of the category and subcategory
                list_all_urls.append([href, subcategory])

        # counter = 0

        for url in list_all_urls:
            currentsubcategory = url[1]
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
                    "product": {
                        'name': temp_product.name.strip(),
                        'price': temp_product.price.strip().split('\xa0'),
                        'weight': split_weight(temp_product.name.strip().lower().split())
                    },
                    "subcategory": currentsubcategory.strip()
                }
                all_items.append(temp_item)
            collection_name.insert_many(all_items)

    with open("file.txt", "w") as file:
        for problem in list_of_problems:
            file.write(problem + "\n        \n")

    return str(counter)

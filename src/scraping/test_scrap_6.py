from dao.CRUD import get_database
from scraping.glovo_scraper import get_soup_from_url
from entities.ProductClass import Product


db = get_database()
collection = db["test6"]


# urls_6_markets = {
#     'Aroma':
#         "https://glovoapp.com/me/en/podgorica/aroma-cetinjska-pdg/",
#     'Franca':
#         "https://glovoapp.com/me/en/podgorica/franca-supermarket/",
#     'Voli':
#         "https://glovoapp.com/me/en/podgorica/voli1/",
#     'IDEA':
#         "https://glovoapp.com/me/en/podgorica/idea-podgorica/",
#     'C_market':
#         "https://glovoapp.com/me/en/podgorica/c-market/",
#     'City_Market':
#         "https://glovoapp.com/me/en/podgorica/city-marketpdg/"
# }


# markets_6 = [
#     'Aroma', 'Franca', 'Voli', 'IDEA', 'C_market', 'City_Market'
# ]


def scraping_6(markets, urls, k):
    counter = k
    for market in markets:

        list_category_urls = list()
        list_all_urls = list()

        url = urls.get(market)
        div_store_body = get_soup_from_url(url)

        div_carousels = div_store_body.find_all('div', 'carousel')
        div_grid = div_store_body.find_all('div', 'grid')


        for temp in div_carousels:
            temp1 = temp.find('a', 'carousel__link link')
            temp2 = "https://glovoapp.com" + temp1.get('href')
            list_category_urls.append(temp2)


        for temp in div_grid:
            list_of_el_with_sub_categories = temp.find('div', 'grid__content')
            elements_sub_categories = list_of_el_with_sub_categories.findAll('div', 'tile')

            for tile in elements_sub_categories:
                for_href = tile.find('a')
                if for_href is not None:
                    href = "https://glovoapp.com" + for_href.get('href')
                    list_all_urls.append(href)


        for temp_url in list_category_urls:
            if not temp_url:
                print('empty')
                continue

            store_content = get_soup_from_url(url=temp_url)

            # тут может быть 1 элемент
            try:
                tiles = store_content.find_all('div', 'tile')
            except:
                tiles = store_content.find('div', 'tile')

            for tile in tiles:
                for_href = tile.find('a')
                if for_href is not None:
                    href = "https://glovoapp.com" + for_href.get('href')
                    list_all_urls.append(href)


        for url in list_all_urls:

            store_content = get_soup_from_url(url)

            if store_content is None:
                continue

            try:
                body_additional = store_content.find_all('div', 'grid')
            except:
                body_additional = store_content.find('div', 'grid')

            for el in body_additional:
                grid_content = el.find('div', 'grid__content')

                products_in_grid_content = grid_content.find_all('div', 'tile')

                for tile in products_in_grid_content:
                    temp_description = tile.find('span', 'tile__description')
                    tile_title_el = temp_description.find('span')
                    name = tile_title_el.get('text')
                    name_to_db = str(name)

                    temp_price = tile.find('div', 'tile__price')
                    price = temp_price.find('span', 'product-price__effective product-price__effective--new-card')
                    price_to_db = price.text

                    product = Product(name_to_db, price_to_db)
                    counter += 1

                    item = {
                        "_id": counter,
                        "product": {
                            'name': product.name.strip(),
                            'price': product.price.strip().split('\xa0')
                        },
                        "market": market
                    }
                    collection.insert_one(item)

    return str(counter)


# print(scraping_6(markets_6, urls_6_markets))

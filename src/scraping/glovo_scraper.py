import requests
from bs4 import BeautifulSoup

from entities.ProductClass import Product


def get_soup_from_url(url: str):
    with requests.Session() as session:
        result = session.get(url)

    return BeautifulSoup(result.text, "html.parser").find('div', 'store__body__dynamic-content')


def split_weight(describe):
    # 'weight': split_weight(temp_product.name.strip().lower().split())
    weight = []
    for word in range(len(describe)):
        if describe[word] == 'l' or describe[word] == 'ml' or describe[word] == 'g':
            weight = [describe[word - 1], describe[word]]
    return weight


def insert_to_db(collection_name, counter, product, sub_category, min_group):
    item = {
            "_id": counter,
            "product": {
                'name': product.name.strip(),
                'price': product.price.strip().split('\xa0')
            },
            "subcategory": sub_category.strip(),
            "group": min_group.strip()
        }
    collection_name.insert_one(item)


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

        list_all_urls = list()

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

                div_grid = div_store_body.find_all('div', 'grid')

                for temp in div_grid:
                    title_of_category = temp.find('h2', 'grid__title')
                    for_search = str(title_of_category)
                    if category in for_search:

                        list_of_el_with_sub_categories = temp.find('div', 'grid__content')
                        elements_sub_categories = list_of_el_with_sub_categories.findAll('div', 'tile')

                        problem = "we found " + category + " in " + market + "\n"
                        list_of_problems.append(problem)

                        for tile in elements_sub_categories:
                            for_href_and_title = tile.find('a')
                            href = "https://glovoapp.com" + for_href_and_title.get('href')
                            forsubcategory = tile.find('div', 'tile__description')
                            subcategory = forsubcategory.text
                            list_all_urls.append([href, subcategory])

                            problem = "href = " + href + " subcategory = " + subcategory + "\n"
                            list_of_problems.append(problem)



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
            all_ok_grid = False

            try:
                body_additional = store_content.find_all('div', 'grid')
                all_ok_grid = True
            except:
                all_ok_grid = False

            if all_ok_grid is False:
                body_additional = store_content.find('div', 'grid')

            for el in body_additional:
                title = el.find('h2', 'grid__title')
                grid_content = el.find('div', 'grid__content')

                with open("file.txt", "w") as file:
                    file.write(str(grid_content))

                title_of_min_group = title.text

                products_in_grid_content = grid_content.find_all('div', 'tile')

                for tile in products_in_grid_content:
                    temp_description = tile.find('span', 'tile__description')
                    tile_title_el = temp_description.find('span')
                    name = tile_title_el.get('text')
                    name_to_db = str(name)

                    temp_price = tile.find('div', 'tile__price')
                    price = temp_price.find('span', 'product-price__effective product-price__effective--new-card')
                    price_to_db = price.text

                    text ="name_to_db = \n" + name_to_db + "\nprice_to_db = \n" + str(price_to_db)
                    list_of_problems.append(text + "\n\n\n")

                    product = Product(name_to_db, price_to_db)
                    counter += 1

                    insert_to_db(collection_name, counter, product, currentsubcategory, title_of_min_group)



    # with open("file.txt", "w") as file:
    #     for problem in list_of_problems:
    #         file.write(problem + "\n        \n")

    return str(counter)

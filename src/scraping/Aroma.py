from bs4 import BeautifulSoup
import requests
from entities.ProductClass import Product


def scraping(urlAroma, collection_name):

    r_Aroma = requests.get(urlAroma)
    soup_Aroma = BeautifulSoup(r_Aroma.text, "html.parser")
    divStoreBody = soup_Aroma.find('div', 'store__body__dynamic-content')
    divCarousels = divStoreBody.find_all('div', 'carousel')

    meatCategoryUrl = ""
    milkCategoryUrl = ""
    fruitCategoryUrl = ""
    list_AromaCategory_urls = [
        [meatCategoryUrl, "meatCategory"],
        [milkCategoryUrl, "milkCategory"],
        [fruitCategoryUrl, "fruitCategory"]
    ]


    for temp in divCarousels:

        temp1 = temp.find('div', 'carousel__title-container')
        temp2 = temp1.find('h2', 'carousel__title')

        if "Mesne prerađevine" in temp2:
            temp1 = temp.find('a', 'carousel__link link')
            temp3 = "https://glovoapp.com" + temp1.get('href')
            list_AromaCategory_urls[0][0] = temp3

        if "Mlijeko, mliječni proizvodi i jaja" in temp2:
            temp1 = temp.find('a', 'carousel__link link')
            temp3 = "https://glovoapp.com" + temp1.get('href')
            list_AromaCategory_urls[1][0] = temp3

        if "Voće i povrće" in temp2:
            temp1 = temp.find('a', 'carousel__link link')
            temp3 = "https://glovoapp.com" + temp1.get('href')
            list_AromaCategory_urls[2][0] = temp3


    list_Aroma_all_urls = list()

    for temp_url in list_AromaCategory_urls:

        if(temp_url[0] == ""): continue

        r_temp = requests.get(temp_url[0])
        soup_temp = BeautifulSoup(r_temp.text, "html.parser")
        storeContent = soup_temp.find('div', 'store__body__dynamic-content')
        tiles = storeContent.find_all('div', 'tile')

        for tile in tiles:
            forHref = tile.find('a', 'nuxt-link-active')
            Href = "https://glovoapp.com" + forHref.get('href')
            forsubcategory = tile.find('div', 'tile__description')
            subcategory = forsubcategory.text

            # to each link chains the name of the category and subcategory
            list_Aroma_all_urls.append([Href, temp_url[1], subcategory])


    counter = 0

    for url in list_Aroma_all_urls:

        r_r = requests.get(url[0])
        category = url[1]
        currentsubcategory = url[2]
        soup_soup = BeautifulSoup(r_r.text, "html.parser")
        store_content = soup_soup.find('div', 'store__body__dynamic-content')

        allOk = False

        try:
            productTiles = store_content.find_all('div', 'tile')
            allOk = True
        except: allOk = False

        if(allOk == False):
            productTiles = store_content.find('div', 'tile')


        for prod_tile in productTiles:
            prod_tile_Name = prod_tile.find('span', 'tile__description')
            prod_tile_Price = prod_tile.find('span', 'product-price__effective')
            counter = counter + 1
            content_nameTOBD = prod_tile_Name.text
            content_priceTOBD = prod_tile_Price.text
            tempProduct = Product(content_nameTOBD, content_priceTOBD)

            tempItem = {
                "_id": counter,
                "product": [tempProduct.name, tempProduct.price],
                "category": category,
                "subcategory": currentsubcategory
            }
            collection_name.insert_one(tempItem)


    return (counter)

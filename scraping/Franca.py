from flask import Flask
from bs4 import BeautifulSoup
import requests

def scraping(urlFranca, collection_name):

    r_Franca = requests.get(urlFranca)
    # print(r_Franca.status_code)
    soup_Franca = BeautifulSoup(r_Franca.text, "html.parser")
    divStoreBody = soup_Franca.find('div', 'store__body__dynamic-content')
    divCarousels = divStoreBody.find_all('div', 'carousel')

    list_Franca_urls = list()

    for temp in divCarousels:
        temp1 = temp.find('div', 'carousel__title-container')
        temp2 = temp1.find('h2', 'carousel__title')
        if "Meso i živina" in temp2:
            temp1 = temp.find('a', 'carousel__link link')
            temp3 = "https://glovoapp.com" + temp1.get('href')
            list_Franca_urls.append(temp3)
            # print(temp3)
            # print("\n\n")
        if "Mliječni proizvodi " in temp2:
            temp1 = temp.find('a', 'carousel__link link')
            temp3 = "https://glovoapp.com" + temp1.get('href')
            list_Franca_urls.append(temp3)
            # print(temp3)
            # print("\n\n")
        if "Voće i povrće " in temp2:
            temp1 = temp.find('a', 'carousel__link link')
            temp3 = "https://glovoapp.com" + temp1.get('href')
            list_Franca_urls.append(temp3)
            # print(temp3)
            # print("\n\n")

    list_Franca_MMF_urls = list()

    for temp_url in list_Franca_urls:
        r_temp = requests.get(temp_url)
        # print(r_temp.status_code)
        soup_temp = BeautifulSoup(r_temp.text, "html.parser")
        storeContent = soup_temp.find('div', 'store__body__dynamic-content')
        tiles = storeContent.find_all('div', 'tile')
        for tile in tiles:
            forHref = tile.find('a', 'nuxt-link-active')
            Href = "https://glovoapp.com" + forHref.get('href')
            list_Franca_MMF_urls.append(Href)
            # print(Href)

    counter = 0
    for url in list_Franca_MMF_urls:
        # print(url)
        # print("\n")
        r_r = requests.get(url)
        # print(r_r.status_code)
        soup_soup = BeautifulSoup(r_r.text, "html.parser")
        store_content = soup_soup.find('div', 'store__body__dynamic-content')
        productTiles = store_content.find_all('div', 'tile')
        for prod_tile in productTiles:
            prod_tile_Name = prod_tile.find('span', 'tile__description')
            prod_tile_Price = prod_tile.find('span', 'product-price__effective')
            counter = counter + 1
            content_nameTOBD = prod_tile_Name.text
            content_priceTOBD = prod_tile_Price.text

            tempItem = {
                "counter": counter,
                "name": content_nameTOBD,
                "price": content_priceTOBD
            }
            collection_name.insert_one(tempItem)

            # print(content_name)
            # print(content_price)
            # print("\n\n")

    # print("!!!!!!!!!!\n\n")
    # print(counter)
    # print("\n\n!!!!!!!!!!")
    return(counter)

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from requests import get
from bs4 import BeautifulSoup


def clean_price(value):
    value = value.replace('$', '')
    value = value.replace('.', '')
    return value.strip()


urls = ['http://www.onceshop.com.ar/antiage_qO22214636XtOcxSM',
        'http://www.onceshop.com.ar/manchas-acne_qO22742522XtOcxSM',
        'http://www.onceshop.com.ar/detox_qO27865225XtOcxSM',
        'http://www.onceshop.com.ar/corporales_qO22740672XtOcxSM',
        'http://www.onceshop.com.ar/antioxidantes_qO22215260XtOcxSM',
        'http://www.onceshop.com.ar/efecto-relleno_qO24759990XtOcxSM',
        'http://www.onceshop.com.ar/efecto-tensor_qO22742105XtOcxSM',
        'http://www.onceshop.com.ar/lineas-reparadoras_qO22741791XtOcxSM',
        'http://www.onceshop.com.ar/lineas-para-tratamiento_qO22742525XtOcxSM',
        'http://www.onceshop.com.ar/limpieza-facial-diaria_qO29695402XtOcxSM',
        'http://www.onceshop.com.ar/maquillaje-inteligente_qO22742539XtOcxSM',
        'http://www.onceshop.com.ar/sets_qO25132627XtOcxSM',
        'http://www.onceshop.com.ar/uso-interno_qO22742102XtOcxSM'
        'http://www.onceshop.com.ar/accesorios_qO30717721XtOcxSM']

products = []
for url in urls:
    response = get(url)
    print url
    html_soup = BeautifulSoup(response.text, 'lxml')
    all_products = html_soup.find_all('div', class_='search-result_container')
    for first_product in all_products:
        prod = {}
        if first_product.find_all('span', class_='money'):
            price = first_product.find_all('span', class_='money')[0].text.strip()
            prod['price'] = clean_price(price)

        if first_product.ins:
            price = first_product.find_all('del')[0].text.strip()
            prod['price'] = clean_price(price)
            price = first_product.find_all('ins')[0].text.strip()
            prod['promo_price'] = clean_price(price)

        prod['name'] = first_product.h2.text.strip()
        products.append(prod)

for prod in products:
    print prod

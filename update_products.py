# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------
#
#    Copyright (C) 2017  jeo Software  (http://www.jeosoft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# -----------------------------------------------------------------------------------
import odoorpc
from secret import odoo_key
from tienda_nube_connector import TiendaNubeCat, TiendaNubeProd, TiendaNube

# conectar con odoo
odoo = odoorpc.ODOO(odoo_key['server'], port=odoo_key['port'])
odoo.login(odoo_key['database'], odoo_key['username'], odoo_key['password'])

CATEG_MILA = [3, 25, 26, 53]


def list_nube_categs():
    tn = TiendaNube()
    for cat in tn.store().categories.list():
        print cat.name


def list_nube_products():
    tn = TiendaNube()
    for prod in tn.store().products.list():
        print prod.id, prod.name.es


def delete_nube_categs():
    tn = TiendaNube()
    for cat in tn.store().categories.list():
        tn.store().categories.delete({'id': cat['id']})


def delete_nube_products():
    tn = TiendaNube()
    for prod in tn.store().products.list():
        tn.store().products.delete({'id': prod.id})


def delete_nube_things():
    delete_nube_categs()
    delete_nube_products()


def update_nube_images():
    tn = TiendaNubeProd()
    # buscamos todos los productos que hay en la tienda
    for prod in tn.store().products.list():
        # por cada producto que hay traemos el correspondiente en odoo
        odoo_prod_obj = odoo.env['product.product']
        ids = odoo_prod_obj.search([('nube_id', '=', prod.id)])
        # y actualizamos el producto, la foto se actualizará con el mismo, en este loop hay siempre uno...
        for pro in odoo_prod_obj.browse(ids):
            tn.update(pro)


def products_odoo2nube(prods_to_update):
    # obtener productos
    tn = TiendaNubeProd()
    odoo_prod_obj = odoo.env['product.product']
    for default_code in prods_to_update:
        ids = odoo_prod_obj.search([('default_code', '=', default_code)])
        for pro in odoo_prod_obj.browse(ids):
            if pro.lst_price > 0:
                tn.update(pro)


def list_nube_images():
    tn = TiendaNube()
    for prod in tn.store().products.list():
        if prod.images:
            print prod.id
            for image in prod.images:
                print image


def update_nube_categs():
    # obtener categorias
    tn = TiendaNubeCat()
    odoo_categ_obj = odoo.env['curso.woo.categ']
    for level in range(1, 4):
        print '=== processing level', level
        ids = odoo_categ_obj.search([('woo_idx', '=', level)])
        for cat in odoo_categ_obj.browse(ids):
            tn.update(cat)


def clean_odoo_prods():
    """ Esto limpia todos los nube_id de odoo """
    odoo_prod_obj = odoo.env['product.product']
    ids = odoo_prod_obj.search([('nube_id', '!=', 0)])
    print ids
    prods = odoo_prod_obj.browse(ids)
    for pro in prods:
        pro.nube_id = 0


def clean_odoo_categs():
    odoo_categ_obj = odoo.env['curso.woo.categ']
    ids = odoo_categ_obj.search([('nube_id', '!=', 0)])
    print ids
    categs = odoo_categ_obj.browse(ids)
    for cat in categs:
        cat.nube_id = 0


def clean_odoo_things():
    clean_odoo_prods()
    clean_odoo_categs()


def calculate_pricelist_price(id_prod, id_pricelist):
    return odoo.env['product.pricelist'].price_get([id_pricelist], id_prod, 1.0)[str(id_pricelist)]


def list_odoo_prods(prods_to_list):
    # obtener productos
    odoo_prod_obj = odoo.env['product.product']
    for default_code in prods_to_list:
        ids = odoo_prod_obj.search([('default_code', '=', default_code)])
        for pro in odoo_prod_obj.browse(ids):
            print pro.default_code


def products_to_update():
    return [
        '583/50',
        '67/100 LIMP/100',
        'MAND GEL LIMP/50',
        '73/50',
        '73/100',
        'PYTOCELL 40',
        '8521/50 E',
        '8521/100 E',
        '586/50',
        '586/100',
        '483/50 SPF 35/50',
        'RFRM CONT 15',
        'S/SEBO50',

        'Set MINI',
        'COMBO OJOS',
        'SET ESENCIAL',

        'P90',
        'BROCHA LUSTRE TRADICIONAL',
        'S11.3',
        'S22.2',
        'TK96',
        'P86',
        'P84',
        'P85 TF',

        'G01',
    ]


products_odoo2nube(products_to_update())
# delete_nube_categs()
# update_nube_categs()
# delete_nube_things()
#delete_nube_products()
# list_nube_products()
# list_nube_images()
# update_nube_images()
#clean_odoo_prods()
# list_odoo_prods(['P84'])

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
        print prod


def list_nube_images():
    tn = TiendaNube()
    for prod in tn.store().products.list():
        print prod.images.list()


def delete_nube_categs():
    tn = TiendaNube()
    for cat in tn.store().categories.list():
        tn.store().categories.delete({'id': cat['id']})


def delete_nube_products():
    print 'deleting products'
    tn = TiendaNube()
    for prod in tn.store().products.list():
        tn.store().products.delete({'id': prod.id})


def update_nube_categs():
    # obtener categorias
    tn = TiendaNubeCat()
    odoo_categ_obj = odoo.env['curso.woo.categ']
    for level in range(1, 4):
        print '=== processing level', level
        ids = odoo_categ_obj.search([('woo_idx', '=', level)])
        for cat in odoo_categ_obj.browse(ids):
            tn.update(cat)


def update_nube_products():
    # obtener productos
    tn = TiendaNubeProd()
    odoo_prod_obj = odoo.env['product.product']
    ids = odoo_prod_obj.search([('categ_id', 'in', CATEG_MILA)], limit=10)
    for pro in odoo_prod_obj.browse(ids):
        tn.update(pro)

    


#update_nube_categs()
#update_nube_products()
#delete_nube_products()
list_nube_products()
#list_nube_images()

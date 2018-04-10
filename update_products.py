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
    """ Pretende listar los productos pero lista solo la primera pagina """
    tn = TiendaNube()
    a = len(tn.store().products.list())
    print 'cantidad de productos', a
    for prod in tn.store().products.list():
        print prod.id, prod.name.es


def delete_nube_things():
    print 'deleting nube things'
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


def delete_nube_products(prods_to_delete='all'):
    """ Elimina un producto de tiendanube, o todos si no le paso parametros
    """
    tn = TiendaNubeProd()
    # borrar todos los productos de la tienda
    if prods_to_delete == 'all':
        cant = 1
        while cant > 0:
            for prod in tn.store().products.list():
                tn.store().products.delete({'id': prod.id})
            cant = len(tn.store().products.list())
        return

    # borrar una lista de productos de la tienda
    odoo_prod_obj = odoo.env['product.product']
    for default_code in prods_to_delete:
        ids = odoo_prod_obj.search([('default_code', '=', default_code)])
        for prod in odoo_prod_obj.browse(ids):
            tn.delete(prod)


def set_weight(prods_to_update, weight):
    odoo_prod_obj = odoo.env['product.product']
    for default_code in prods_to_update:
        ids = odoo_prod_obj.search([('default_code', '=', default_code)])
        for pro in odoo_prod_obj.browse(ids):
            print 'setting weight', pro.default_code, '>', weight
            pro.weight = weight


def products_odoo2nube(prods_to_update):
    # obtener productos
    tn = TiendaNubeProd()
    odoo_prod_obj = odoo.env['product.product']
    for default_code in prods_to_update:
        ids = odoo_prod_obj.search([('default_code', '=', default_code)])
        for pro in odoo_prod_obj.browse(ids):
            tn.update(pro)


def list_nube_images():
    tn = TiendaNube()
    for prod in tn.store().products.list():
        if prod.images:
            print prod.id
            for image in prod.images:
                print image


def list_odoo_categs():
    odoo_categ_obj = odoo.env['curso.woo.categ']
    for level in range(1, 4):
        print '=== processing level', level
        ids = odoo_categ_obj.search([('woo_idx', '=', level)])
        for cat in odoo_categ_obj.browse(ids):
            print cat.name


def update_nube_categs():
    """ Subir las categorias a tienda nube
    """
    # obtener categorias
    tn = TiendaNubeCat()
    odoo_categ_obj = odoo.env['curso.woo.categ']
    for level in range(1, 4):
        print '=== processing level', level
        ids = odoo_categ_obj.search([('woo_idx', '=', level),
                                     ('published', '!=', False)])
        for odoo_cat in odoo_categ_obj.browse(ids):
            print odoo_cat.name
            tn.update(odoo_cat)


def clean_odoo_prods():
    """ Esto limpia todos los nube_id de odoo """
    odoo_prod_obj = odoo.env['product.product']
    ids = odoo_prod_obj.search([('nube_id', '!=', 0)])
    prods = odoo_prod_obj.browse(ids)
    for pro in prods:
        print pro.default_code
        pro.nube_id = 0


def delete_nube_categs():
    """ puede que ande pero da errores
    """
    tn = TiendaNube()
    cant = 1
    while cant > 0:
        for cat in tn.store().categories.list():
            tn.store().categories.delete({'id': cat.id})
        cant = len(tn.store().categories.list())


def clean_odoo_categs():
    """ borrar las referencias de odoo para las categorias """
    odoo_categ_obj = odoo.env['curso.woo.categ']
    ids = odoo_categ_obj.search([('nube_id', '!=', 0)])
    print ids
    categs = odoo_categ_obj.browse(ids)
    for cat in categs:
        print cat.name
        cat.nube_id = 0


def clean_odoo_things():
    """ borrar las referencias de odoo para cargar todo de nuevo """
    print 'clean odoo things'
    clean_odoo_prods()
    clean_odoo_categs()


def calculate_pricelist_price(id_prod, id_pricelist):
    return \
        odoo.env['product.pricelist'].price_get([id_pricelist], id_prod, 1.0)[
            str(id_pricelist)]


def list_odoo_prods(prods_to_list):
    # obtener productos
    odoo_prod_obj = odoo.env['product.product']
    for default_code in prods_to_list:
        ids = odoo_prod_obj.search([('default_code', '=', default_code)])
        for pro in odoo_prod_obj.browse(ids):
            print pro.default_code, pro.name


def odoo_published(from_date=False):
    """ Devuelve los productos que se pueden publicar y que fueron modificaos
        despues de from_date o todos si es False
    """
    # TODO agregar el write_date
    print 'buscando productos en odoo para publicar'
    ret = []
    odoo_prod_obj = odoo.env['product.product']
    domain = [
        ('published', '=', True),
        ('woo_categ', '!=', False),
        ('description', '!=', False),
        ('state', '=', 'sellable')]

    if from_date:
        domain += [('write_date', '>', from_date)]

    ids = odoo_prod_obj.search(domain)

    for pro in odoo_prod_obj.browse(ids):
        print u'> {:35}{}'.format(pro.default_code, pro.write_date)
        ret.append(pro.default_code)
    print 'total productos', len(ids)
    return ret


def delete_empty_categs(selected_prods):
    # obtener las categorias usadas
    used_categ_ids = []
    odoo_prod_obj = odoo.env['product.product']
    nro = len(selected_prods)
    for default_code in selected_prods:
        ids = odoo_prod_obj.search([('default_code', '=', default_code)])
        for pro in odoo_prod_obj.browse(ids):
            print 'producto ', nro, pro.default_code
            nro -= 1
            if pro.woo_categ not in used_categ_ids:
                used_categ_ids += [pro.woo_categ]

    print 'categorias usadas', len(used_categ_ids), used_categ_ids

    # obtener todas las categorias en nube
    odoo_categ_obj = odoo.env['curso.woo.categ']
    all_categ_ids = odoo_categ_obj.search([('nube_id', '!=', 0)])

    # obtener las que hay que borrar
    to_delete = set(used_categ_ids) ^ set(all_categ_ids)

    print 'categs a borrar', len(to_delete)
    tn = TiendaNubeCat()
    for id_cat in to_delete:
        print 'borrando', id_cat
        tn.store().categories.delete({'id': id_cat})


# estos dos borran las cosas en nube y limpian las cosas en odoo, para empezar de cero
# delete_nube_things()
# clean_odoo_things()

# sube todas las categorias a nube va antes de los productos
# update_nube_categs()

# sube / actualiza todos los productos a nube
# products_odoo2nube(odoo_published())

# elimina las categorias que no tienen productos NO ANDA
# delete_empty_categs(odoo_published())
# set_weight(odoo_published(), 0.1)

# products_odoo2nube(odoo_published())

# list_nube_products()
# list_nube_categs()
# list_nube_images()
# update_nube_images()
# clean_odoo_prods()
# list_odoo_prods(['1003-02'])
# print odoo_published()

# products_odoo2nube(['2011P-S02'])


#fotos = ['ESPONJA', 'C23', 'C22']

#list_odoo_prods(fotos1)
#delete_nube_products()

#products_odoo2nube(fotos1)


# ultima publicacion
#products_odoo2nube()

odoo_published('2018-04-10 01:24:13')



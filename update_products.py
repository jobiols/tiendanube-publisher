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


def odoo_published(from_date=False, categs=[], mask=False, noweight=False):
    """ Devuelve los productos que se pueden procesar y que fueron modificaos
        despues de from_date o todos si es False o las categorias o mascara.
    """

    print 'buscando productos en odoo'
    ret = []
    odoo_prod_obj = odoo.env['product.product']
    domain = [
        ('published', '=', True),
        ('woo_categ_ids', '!=', False),
        ('description', '!=', False),
        ('state', '=', 'sellable')
    ]

    if categs:
        domain += ('categ_id', 'in', categs)

    if from_date:
        domain += [('write_date', '>', from_date)]

    if mask:
        domain += [('default_code', 'like', mask)]

    if noweight:
        domain += [('weight', '=', False)]

    ids = odoo_prod_obj.search(domain, order='write_date')

    for pro in odoo_prod_obj.browse(ids):
        print u'> {:7} [{}] {} {}'.format(pro.id, pro.write_date,
                                          pro.default_code, pro.name)
        ret.append(pro.id)
    print 'total productos', len(ids)
    return ret


def list_nube_categs():
    """ Lista las categorias que hay en tienda nube,
        ojo que per page debe ser menor que la cantidad real de items que hay
    """
    tn = TiendaNube()
    page = 1
    total = 0
    ret = []
    while True:
        print 'getting page', page
        categs = tn.store().categories.list(
            filters={'per_page': 200, 'page': page},
            fields='id,parent,name,subcategories')
        page += 1
        for cat in categs:
            ret.append(cat.id)
            print u'[{}] [{:7}] {} {}'.format(cat.id, cat.parent, cat.name.es,
                                              cat.subcategories)
            total += 1
        if len(categs) < 200:
            break

    print 'total', total
    return ret


def list_nube_products():
    """ Lista todos los productos de la tienda, aunque medio trucho porque
        no puedo saber cuantos productos hay en total.
        Seria bueno saber eso, lo explica tienda nube en
        https://github.com/TiendaNube/api-docs#pagination
    """
    tn = TiendaNube()
    page = 1
    ret = []
    while True:
        prods = tn.store().products.list(
            filters={'per_page': 200, 'page': page},
            fields='id,variants,name')
        page += 1

        for prod in prods:
            ret.append({'id': prod.id,
                        'sku': prod.variants[0].sku,
                        'name': prod.name})
            print prod.id, prod.name.es

        if len(prods) < 200:
            break
    return ret


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
    for pro in odoo_prod_obj.browse(prods_to_delete):
        tn.delete(pro)


def set_weight(prods_to_update, weight=0.1):
    """ Revisa todos los productos de odoo y si no tiene peso le pone 100g
    """
    odoo_prod_obj = odoo.env['product.product']
    for pro in odoo_prod_obj.browse(prods_to_update):
        if pro.weight < weight:
            pro.weight = weight
            print 'setting weight', pro.default_code, '>', weight


def products_odoo2nube(prods_to_update):
    """ Esto actualiza los productos de la tienda desde odoo
    """
    tn = TiendaNubeProd()
    odoo_prod_obj = odoo.env['product.product']
    count = len(prods_to_update)
    for pro in odoo_prod_obj.browse(prods_to_update):
        tn.update(pro)
        count -= 1
        print 'quedan ', count


def clean_odoo_prod(prods_to_update, nube_id=0):
    """ Esto limpia los nube_id de los productos listados o el pone un nube_id
    """
    odoo_prod_obj = odoo.env['product.product']
    prods = odoo_prod_obj.browse(prods_to_update)
    for pro in prods:
        print 'limpiando ', pro.default_code, pro.name
        pro.nube_id = nube_id


def list_nube_images():
    """ Esto lista las imagenes que estan en la tienda, solo como muestras
    """
    tn = TiendaNube()
    for prod in tn.store().products.list():
        if prod.images:
            print prod.id
            for image in prod.images:
                print image.position, image.src


def list_odoo_categs():
    """ Lista las categorias nube que hay en odoo
    """
    odoo_categ_obj = odoo.env['curso.woo.categ']
    for level in range(1, 4):
        print '=== processing level', level
        ids = odoo_categ_obj.search([('woo_idx', '=', level)])
        for cat in odoo_categ_obj.browse(ids):
            print cat.name


def update_nube_categs():
    """ Subir las categorias a tienda nube, agrega las nuevas y actualiza
        las viejas
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


def calculate_pricelist_price(id_prod, id_pricelist):
    return \
        odoo.env['product.pricelist'].price_get([id_pricelist], id_prod, 1.0)[
            str(id_pricelist)]


def list_odoo_prods(prods_to_list):
    odoo_prod_obj = odoo.env['product.product']
    for pro in odoo_prod_obj.browse(prods_to_list):
        print pro.id, pro.name


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


def odoo_to_delete():
    """ Devuelve lista de productos que habria que borrar de la tienda porque
        en odoo dice que no hay que publicarlos
    """
    print 'buscando productos en odoo para borrar'
    ret = []
    odoo_prod_obj = odoo.env['product.product']
    domain = [
        ('nube_id', '!=', 0),
        ('published', '=', True),
        ('woo_categ', '!=', False),
        ('state', '=', 'obsolete')
    ]

    ids = odoo_prod_obj.search(domain, order='write_date')

    for pro in odoo_prod_obj.browse(ids):
        print u'> {:10} {} {:8} {}'.format(pro.id, pro.write_date,
                                           pro.default_code, pro.name)
        ret.append(pro.id)
    print 'total productos', len(ids)
    return ret


def cross_check_prods():
    """ Verificar que cada producto que esta en la nube tiene un producto en odoo
    """
    # Bajar los id nube a una lista
    nube_prods = list_nube_products()
    print 'total prods in nube', len(nube_prods)

    odoo_prod_obj = odoo.env['product.product']
    # por cada uno de la lista chequear lo que hay en odoo
    for nube_prod in nube_prods:
        ids = odoo_prod_obj.search([('nube_id', '=', nube_prod['id'])])

        # verificar que el producto este en odoo y que haya uno solo
        # si no lo hay es error catastrofico, termino.
        if len(ids) != 1:
            if not ids:
                print 'el producto no esta en odoo'
                print nube_prod
            if len(ids) >1:
                print 'el producto esta repetido varias veces en odoo'
                print nube_prod
            exit()

        # me traigo el producto
        prod = odoo_prod_obj.browse(ids)

        # verificar que el producto en odoo debe ser publicado si no debe ser
        # publicado es error catastrifico y termino
        if not prod.published:
            print 'no debe estar en tiendanube'
            print nube_prod
            exit()

        # comparar nombres y codigos, ignorar farmacia once
        odc = prod.default_code if prod.default_code else ''
        oname = odc + u' ' + prod.name if prod.name else ''
        nname = nube_prod['name'].es
        ndc = nube_prod['sku']

        if prod.default_code and not (oname.strip() == nname.strip() and (
                odc == ndc)):
            print u'odoo {} {}'.format(odc, oname)
            print u'nube {} {}'.format(ndc, nname)

        # no esta en odoo
        if not prod:
            print u'not in odoo {} {} {}'.format(nube_prod['id'],
                                                 nube_prod['sku'],
                                                 nube_prod['name'].es)


def cross_check_categs():
    """ Verificar que cada categoria que esta en la nube tiene una categoria
        en odoo
    """
    # Bajar los id nube a una lista
    nube_categs = list_nube_categs()
    print 'total categs in nube', len(nube_categs)

    odoo_woo_categ = odoo.env['curso.woo.categ']
    for nube_id in nube_categs:
        print 'checking', nube_id,
        woo_categ = odoo_woo_categ.search([('nube_id', '=', nube_id)])
        if not woo_categ:
            print 'not in odoo'
        else:
            if len(woo_categ) == 1:
                print 'ok'
            else:
                print 'duplicated'


# delete_nube_products(odoo_to_delete())
# sube todas las categorias a nube va antes de los productos
# update_nube_categs()

# sube / actualiza todos los productos a nube
# products_odoo2nube(odoo_published())

# elimina las categorias que no tienen productos NO ANDA
# delete_empty_categs(odoo_published())
# set_weight(odoo_published(), 0.1)

# products_odoo2nube(odoo_published())

# list_nube_products()
# list_nube_images()

# list_odoo_prods(fotos1)
# delete_nube_products()

# esto limpia el id_nube de odoo, o si se le pone un id se lo actualiza, lo
# usamos cuando se desincroniza el id entre ambos
# clean_odoo_prod(odoo_published(mask="FANTASTICO"),nube_id=25025573)

# next upload from this date
#odoo_published('2019-03-31 05:03:15')


#cross_check_prods()

products_odoo2nube(odoo_published('2019-02-22 20:45:03'))


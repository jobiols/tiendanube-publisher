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
from product import NubeProduct, NubeCategory, NubeVariant, NubeImage
import json


class Map(object):
    def get_dict(self):
        return self._p.get_dict()

    def get_formatted_dict(self):
        return json.dumps(self._p.get_dict(), sort_keys=True, indent=4)


class MapProduct(Map):
    """ Mapea un producto de odoo con uno de nube para pasarle los datos
    """
    def __init__(self, odoo_product):
        n = NubeProduct()
        n.name('es', odoo_product.default_code + ' ' + odoo_product.name)
        n.description('es', odoo_product.description)
        n.sku(odoo_product.default_code)
        n.categories([odoo_product.woo_categ.nube_id])

        # si estoy haciendo actualizacion pongo el id
        if odoo_product.nube_id:
            n.id(odoo_product.nube_id)
        else:
            c = MapVariant(odoo_product)
            n.variants([c.get_dict()])
        self._p = n


class MapVariant(Map):
    """ Mapea un producto odoo con una variante de un producto nube
    """

    def __init__(self, odoo_obj, variant_id=False):
        c = NubeVariant()
        if variant_id:
            c.variant_id(variant_id)
        c.price(odoo_obj.lst_price)
        c.sku(odoo_obj.default_code)
        if odoo_obj.promotional_price:
            c.promotional_price(odoo_obj.promotional_price)
        c.stock_management(False)
        c.weight(odoo_obj.weight)
        self._p = c


class MapCategory(Map):
    def __init__(self, category):
        c = NubeCategory()
        c.id(category.nube_id)
        c.name('es', category.name)
        c.description('es', category.name)  # TODO agregar descripcion aca!!!
        c.parent(category.parent.nube_id)
        self._p = c


class MapImage(Map):
    def __init__(self, odoo_obj):
        c = NubeImage()
        c.id(odoo_obj.nube_id)
        c.filename(str(odoo_obj.id) + '.jpg')
        c.attachment(odoo_obj.image)
        self._p = c


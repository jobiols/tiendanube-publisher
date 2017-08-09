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

        - Cuando se quiere pasar un producto sin variantes, no se incluye el
          campo attributes, y los datos del producto van en la unica variante.
        - Si se incluyen variantes, en attributes van las dimensiones y en
          cada variante va en values el valor que esa dimension toma en la
          variante.
        - Sin embargo cuando se hace update no va ninguna variante, ni la unica.
    """

    def __init__(self, odoo_product):
        n = NubeProduct()
        n.name('es', odoo_product.name)
        n.description('es', odoo_product.description)
        n.sku(odoo_product.default_code)
        n.categories([odoo_product.woo_categ.nube_id])

        # los atributos son solo para las variantes
        # n.attributes('es','')

        # si estoy haciendo add pongo la variante y no el id
        if not odoo_product.nube_id:
            v = NubeVariant()
            v.price(odoo_product.public_price)
            v.sku(odoo_product.default_code)
            n.variants([v.get_dict()])
        else:
            n.id(odoo_product.nube_id)

        self._p = n


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

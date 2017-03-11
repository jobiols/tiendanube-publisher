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
from product import NubeProduct, NubeCategory, NubeVariant


class Map(object):
    def get_dict(self):
        return self._p.get_dict()


class MapProduct(Map):
    """ Mapea un objeto de odoo con uno de nube para pasarle los datos

        - Cuando se quiere pasar un producto sin variantes, no se incluye el
          campo attributes, y los datos
          del producto van en la unica variante.
        - Si se incluyen variantes, en attributes van las dimensiones y en
          cada variante va en values el valor que esa dimension toma en la
          variante.
    """

    def __init__(self, product):
        n = NubeProduct()
        n.id(product.nube_id)
        n.name('es', product.name)
        n.description('es', product.description)
        n.sku(product.default_code)
        #       n.attributes('es','')

        # variants
        v = NubeVariant()
        v.price(product.lst_price)
        v.sku(product.default_code)
        n.variants(v.get_dict())

        self._p = n


class MapCategory(Map):
    def __init__(self, category):
        c = NubeCategory()
        c.id(category.nube_id)
        c.name('es', category.name)
        c.description('es', category.name)  # TODO agregar descripcion aca!!!
        c.parent(category.parent.nube_id)
        #        c.subcategories([])
        self._p = c

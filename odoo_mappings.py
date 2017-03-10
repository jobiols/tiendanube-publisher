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
from product import NubeProduct, NubeCategory


class Map(object):
    def get_dict(self):
        return self._p.get_dict()


class MapProduct(Map):
    def __init__(self, product):
        n = NubeProduct()
        n.name('es', product.name)
        n.description('es', product.description)
        n.sku(product.default_code)
        n.seo_description(product.lst_price, 1)
        self._p = n


class MapCategory(Map):
    def __init__(self, category):
        c = NubeCategory()
        #        c.id(category.nube_id)
        c.name('es', category.name)
        c.description('es', category.name)  # TODO agregar descripcion aca!!!
        c.parent(category.parent.nube_id)
        #        c.subcategories([])
        self._p = c


{'sku': u'1000-01',
 'name': {'es': u'Tonalizador Correctivo Beige Amarillento / Beige grisado'},
 'description': {
     'es': u'Corrector cremoso. Petaca d\xfao x 4 grs.\nNeutraliza y corrige todo tipo de imperfecciones como ojeras, manchas y secuelas de acn\xe9. Al mismo tiempo es un corrector compacto cremoso de fina textura con alto poder para cubrir pieles con diferentes tipos de discrom\xedas y es una base. <mas>\nPuede utilizarse directo sobre la piel o realizar aplicaciones por sectores, en los casos donde no se requiera el uso de este tipo de producto en todo el rostro. \nEs apto para todo tipo de piel ideal al\xedpidas (secas).\nContiene filtro solar.\nDos variedades de color alcanzan para cubrir gran variedad de tonalidad de pieles.\n01 - Piel clara\n02 - Piel oscura '}
 }

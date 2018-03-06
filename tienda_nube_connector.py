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
from odoo_mappings import MapCategory, MapProduct, MapImage, MapVariant
from secret import nube_key
from tiendanube.client import NubeClient
from tiendanube.resources.exceptions import APIError
from product import NubeVariant


class TiendaNube(object):
    def __init__(self):
        # conectar con tienda nube
        client = NubeClient(nube_key['api_key'])
        self._store = client.get_store(nube_key['user_id'])

    def update(self, odoo_obj):
        """ Actualiza o crea un objeto en tienda nube basado en un objeto odoo, es un objeto generico
            puede ser producto o categoria
        """
        if odoo_obj.nube_id:
            # tengo el id en odoo, es una modificacion
            self._do_update(odoo_obj)
        else:
            # no tengo el id en odoo, es un alta
            self._do_add(odoo_obj)
        return

        # mapeo el objeto odoo a objeto nube
        c = MapProduct(odoo_obj)

        # si el objeto odoo tiene ide es modificacion
        if odoo_obj.nube_id:
            try:
                print '--- updating ', odoo_obj.name
                # actualizo tienda nube
                res = self._do_update(c)

                # si es una modificacion modifico la variante
                nube_prod = self._store.products.get(res['id'])
                variant = MapVariant(odoo_obj)
                print '---------------'
                print variant.get_formatted_dict()
                print '---------------'
                res = nube_prod.variants.add(variant.get_dict())


            # si no existe es un error, y borro el id de odoo para sincronizar.
            except APIError as error:
                # TODO Mejorar esto y atrapar todos los errores
                print error[0]
                if error.args[0].find('404') > 1:
                    odoo_obj.nube_id = False
                    'print ERROR ----- resetting nube_id'
                    return False
        else:
            print '--- adding', odoo_obj.name
            # no existe el id en odoo entonces agrego en nube
            res = self._do_add(c)

            # agrego la foto solo si lo estoy agregando, en modifi no
            if self.__class__.__name__ == 'TiendaNubeProd' and odoo_obj.image:
                nube_prod = self._store.products.get(res['id'])
                image = MapImage(odoo_obj)
                nube_prod.images.add(image.get_dict())

            # pongo el id en odoo
            odoo_obj.nube_id = res['id']

    def delete(self, odoo_obj):
        self._do_delete(odoo_obj)


class TiendaNubeCat(TiendaNube):
    def __init__(self):
        super(TiendaNubeCat, self).__init__()

    def _do_delete(self, odoo_obj):
        return self._store.categories.delete({'id': odoo_obj.nube_id})

    def _create_map(self, odoo_obj):
        return MapCategory(odoo_obj)

    def _do_update(self, c):
        return self._store.categories.update(c.get_dict())

    def _do_add(self, c):
        return self._store.categories.add(c.get_dict())


class TiendaNubeProd(TiendaNube):
    def __init__(self):
        super(TiendaNubeProd, self).__init__()

    def _do_delete(self, odoo_obj):
        if odoo_obj.nube_id:
            print 'delete product {}, id={}'.format(odoo_obj.default_code,odoo_obj.nube_id)
            dict = {'id': odoo_obj.nube_id}
            odoo_obj.nube_id = False
            print '-------------------'
            print dict
            print '-------------------'
            return self._store.products.delete(dict)
        else:
            print 'objet {} not in nube'.format(odoo_obj.default_code)

    def _do_update(self, odoo_obj):
        """ Actualiza un producto de odoo a tienda nube
        """
        c = MapProduct(odoo_obj)
        print '-------- update product {}'.format(odoo_obj.default_code)
        print c.get_formatted_dict()
        print '--------'
        ret = self._store.products.update(c.get_dict())

        c = MapVariant(odoo_obj, variant_id=ret.variants[0].id)
        print '-------- update product {}'.format(odoo_obj.default_code)
        print c.get_formatted_dict()
        print '--------'
        nube_prod = self._store.products.get(ret.id)
        nube_prod.variants.update(c.get_dict())

    def _do_add(self, odoo_obj):
        """ agrega un producto a tienda nube que no existe dado un producto odoo
        """

        # agregar el producto
        c = MapProduct(odoo_obj)
        print '-------- adding product {}'.format(odoo_obj.default_code)
        print c.get_formatted_dict()
        print '--------'
        nube_prod = self._store.products.add(c.get_dict())
        odoo_obj.nube_id = nube_prod.id

        # agregar la foto, si es que la tiene el objeto
        if odoo_obj.image:
            print '------ adding photo '
            nube_prod = self._store.products.get(nube_prod.id)
            image = MapImage(odoo_obj)
            nube_prod.images.add(image.get_dict())



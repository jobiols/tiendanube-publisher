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
from odoo_mappings import MapCategory, MapProduct, MapImage
from secret import nube_key
from tiendanube.client import NubeClient
from tiendanube.resources.exceptions import APIError


class TiendaNube(object):
    def __init__(self):
        # conectar con tienda nube
        client = NubeClient(nube_key['api_key'])
        self._store = client.get_store(nube_key['user_id'])

    def update(self, odoo_obj):
        # mapeo el objeto odoo a objeto nube
        c = self._create_map(odoo_obj)

        # si el objeto odoo tiene ide es modificacion
        if odoo_obj.nube_id:
            try:
                print  '--- updating ', odoo_obj.name
                # actualizo tienda nube
                return self._do_update(c)

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

            # me devuelve el id y lo pogo en odoo
            odoo_obj.nube_id = res['id']

        # ya esta el producto en nube sea porque lo agregué o porque lo modifiqué. Le agrego las fotos.
        # eso solo si odoo tiene imagen y si esta clase es TiendaNubeProd
        if odoo_obj.image and self.__class__.__name__ == 'TiendaNubeProd':
            nube_prod = self._store.products.get(odoo_obj.nube_id)
            image = MapImage(odoo_obj)
            nube_prod.images.add(image.get_dict())
            # TODO hay que registrar el id en odoo para no poner la foto varias veces.

    def delete(self, odoo_obj):
        print 'deleting', odoo_obj.name
        self._do_delete(odoo_obj)
        odoo_obj.nube_id = False

    def store(self):
        return self._store


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
        return self._store.products.delete({'id': odoo_obj.nube_id})

    def _create_map(self, odoo_obj):
        return MapProduct(odoo_obj)

    def _do_update(self, c):
        print 'update >', c.get_formatted_dict()
        return self._store.products.update(c.get_dict())

    def _do_add(self, c):
        print 'adding start > -------------------'
        print c.get_formatted_dict()
        print 'adding end   > -------------------'
        return self._store.products.add(c.get_dict())




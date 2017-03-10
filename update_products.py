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
from odoo_mappings import MapCategory
from secret import nube_key, odoo_key
from tiendanube.client import NubeClient

# conectar con tienda nube
client = NubeClient(nube_key['api_key'])
store = client.get_store(nube_key['user_id'])

# conectar con odoo
odoo = odoorpc.ODOO(odoo_key['server'], port=odoo_key['port'])
odoo.login(odoo_key['database'], odoo_key['username'], odoo_key['password'])

# obtener categorias
odoo_categ_obj = odoo.env['curso.woo.categ']
ids = odoo_categ_obj.search([('woo_id', '=', 195)])
for cat in odoo_categ_obj.browse(ids):
    m = MapCategory(cat)
    dic = m.get_dict()
    print dic
    print cat.woo_id, cat.woo_ids, cat.name

exit()

# obtener producto
odoo_prod_obj = odoo.env['product.product']
ids = odoo_prod_obj.search([('default_code', '=', '1000-01')])
odoo_prod = odoo_prod_obj.browse(ids)

nube_prod = Odoo2Nube(odoo_prod)
print nube_prod.get_dict()

# agregar un producto
"""
res = store.products.add(
        {
            'name': {'es': 'mi producto'},
            'attributes': [
                {"es": "Size"},
            ],
            'variants': [
                {
                    'sku': 'var1',
                    'values':
                        [
                            {'en': 'Grande'}
                        ]
                },
                {
                    'sku': 'var2',
                    'values':
                        [
                            {'en': 'Chico'}
                        ]
                }
            ]
        })
print res
"""

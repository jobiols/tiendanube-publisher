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
from unittest import TestCase

from product import NubeVariant


class TestNubeVariant(TestCase):
    def test_id(self):
        v = NubeVariant()
        v.variant_id(123456)
        self.assertDictEqual(v.get_dict(), {'id': 123456})

    def test_product_id(self):
        v = NubeVariant()
        v.product_id(123654)
        self.assertDictEqual(v.get_dict(), {'product_id': 123654})

    def test_price(self):
        v = NubeVariant()
        v.price(145.30)
        self.assertDictEqual(v.get_dict(), {'price': 145.30})

    def test_sku(self):
        v = NubeVariant()
        v.sku('1000-01')
        self.assertDictEqual(v.get_dict(), {'sku': '1000-01'})

    def test_values(self):
        """ chequear que agrega los values pero no los duplica
        """
        v = NubeVariant()
        v.values('es', 'mucho')
        v.values('es', 'grande')
        v.values('en', 'big')
        self.assertDictEqual(v.get_dict(),
                             {'values': [{'es': 'mucho'}, {'en': 'big'}]})

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

from product import NubeCategory


class TestNubeCategory(TestCase):
    def test_id(self):
        v = NubeCategory()
        v.id(123456)
        self.assertDictEqual(v.get_dict(), {'id': 123456})

    def test_id1(self):
        v = NubeCategory()
        v.id(0)
        self.assertDictEqual(v.get_dict(), {})

    def test_id1(self):
        v = NubeCategory()
        v.id(False)
        self.assertDictEqual(v.get_dict(), {})

    def test_name(self):
        v = NubeCategory()
        v.name('es', 'este es el nombre ----')
        v.name('es', 'Cuidados de la piel')
        self.assertDictEqual(v.get_dict(), {'name': {'es': 'Cuidados de la piel'}})

    def test_description(self):
        v = NubeCategory()
        v.description('es', 'esta es la descripción ---- ')
        v.description('es', 'esta es la descripción')
        self.assertDictEqual(v.get_dict(), {'description': {'es': 'esta es la descripción'}})

    def test_handle(self):
        v = NubeCategory()
        v.handle('es', 'esta-es-el-handle --------- ')
        v.handle('es', 'esta-es-el-handle')
        self.assertDictEqual(v.get_dict(), {'handle': {'es': 'esta-es-el-handle'}})

    def test_parent(self):
        v = NubeCategory()
        v.parent(123)
        self.assertDictEqual(v.get_dict(), {'parent': 123})

    def test_parent1(self):
        v = NubeCategory()
        v.parent(0)
        self.assertDictEqual(v.get_dict(), {'parent': None})

    def test_parent2(self):
        v = NubeCategory()
        v.parent(False)
        self.assertDictEqual(v.get_dict(), {'parent': None})

    def test_subcategories(self):
        v = NubeCategory()
        v.subcategories([1, 2, 3])
        self.assertDictEqual(v.get_dict(), {'subcategories': [1, 2, 3]})

    def test_seo_title(self):
        v = NubeCategory()
        v.seo_title('en', 'seo title ------- ')
        v.seo_title('en', 'seo title')
        v.seo_title('es', 'seo titulo')
        self.assertDictEqual(v.get_dict(), {'seo_title': {'es': 'seo titulo', 'en': 'seo title'}})

    def test_seo_description(self):
        v = NubeCategory()
        v.seo_description('es', 'seo descripción ---- ')
        v.seo_description('es', 'seo descripción')
        v.seo_description('en', 'seo description')
        self.assertDictEqual(v.get_dict(), {'seo_description': {'es': 'seo descripción', 'en': 'seo description'}})

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

from product import NubeProduct


class TestNubeProduct(TestCase):
    def test_add(self):
        p = NubeProduct()
        self.assertEqual(p.get_dict(), {})

    def test_add_id(self):
        p = NubeProduct()
        p.id('123456')
        self.assertDictEqual(p.get_dict(), {'id': '123456'})

    def test_add_id1(self):
        p = NubeProduct()
        p.id(0)
        self.assertDictEqual(p.get_dict(), {})

    def test_add_id2(self):
        p = NubeProduct()
        p.id(False)
        self.assertDictEqual(p.get_dict(), {})

    def test_add_name(self):
        p = NubeProduct()
        p.name('es', 'nombre')
        p.name('es', 'nombre nuevo')
        p.name('en', 'my name')
        self.assertDictEqual(p.get_dict(), {'name': {'en': 'my name', 'es': 'nombre nuevo'}})

    def test_add_description(self):
        p = NubeProduct()
        p.description('es', 'nombre')
        p.description('es', 'nombre nuevo')
        p.description('en', 'my name')
        self.assertDictEqual(p.get_dict(), {'description': {'en': 'my name', 'es': 'nombre nuevo'}})

    def test_add_handle(self):
        p = NubeProduct()
        p.handle('es', u'sombra-compacta')
        p.handle('es', u'sombra-compacta-repuesto')
        p.handle('en', u'shadow-pack-repuesto')
        self.assertDictEqual(p.get_dict(),
                             {'handle': {'es': u'sombra-compacta-repuesto', 'en': u'shadow-pack-repuesto'}})

    def test_add_attributes(self):
        p = NubeProduct()
        p.attributes('es', u'Tamaño')
        self.assertDictEqual(p.get_dict(), {'attributes': {'es': u'Tamaño'}})

    def test_add_published(self):
        p = NubeProduct()
        p.published(True)
        self.assertDictEqual(p.get_dict(), {'published': 'true'})

    def test_add_free_shipping(self):
        p = NubeProduct()
        p.free_shipping(True)
        self.assertDictEqual(p.get_dict(), {'free_shipping': True})

    def test_add_canonical_url(self):
        p = NubeProduct()
        p.canonical_url(True)
        self.assertDictEqual(p.get_dict(), {'canonical_url': True})

    def test_add_seo_title(self):
        p = NubeProduct()
        p.seo_title('es', u'Esto mejora el seo')
        self.assertDictEqual(p.get_dict(), {'seo_title': {'es': u'Esto mejora el seo'}})

    def test_add_seo_description(self):
        p = NubeProduct()
        p.seo_description('es', u'Esto mejora el seo expllicacion')
        self.assertDictEqual(p.get_dict(), {'seo_description': {'es': u'Esto mejora el seo expllicacion'}})

    def test_add_variants(self):
        p = NubeProduct()
        p.variants([{}, {}])
        self.assertDictEqual(p.get_dict(), {'variants': [{}, {}]})

    def test_add_tags(self):
        p = NubeProduct()
        p.tags('aca van todos los tags')
        self.assertDictEqual(p.get_dict(), {'tags': 'aca van todos los tags'})

    def test_add_images(self):
        p = NubeProduct()
        p.images([{}])
        self.assertDictEqual(p.get_dict(), {'images': [{}]})

    def test_add_categories(self):
        p = NubeProduct()
        p.categories([{}])
        self.assertDictEqual(p.get_dict(), {'categories': [{}]})

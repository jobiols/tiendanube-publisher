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


class NubeObject(object):
    def __init__(self):
        self._p = dict()

    def _check_dict(self, dict_name):
        self._p[dict_name] = self._p.get(dict_name) or dict()

    def _check_list(self, list_name):
        self._p[list_name] = self._p.get(list_name) or []

    def get_dict(self):
        return self._p


class NubeCategory(NubeObject):
    def __init__(self):
        super(NubeCategory, self).__init__()

    def id(self, value):
        if value or value != 0:
            self._p['id'] = value

    def name(self, lang, value):
        self._check_dict('name')
        self._p['name'][lang] = value

    def description(self, lang, value):
        self._check_dict('description')
        self._p['description'][lang] = value

    def handle(self, lang, value):
        self._check_dict('handle')
        self._p['handle'][lang] = value

    def parent(self, value):
        self._p['parent'] = value if (value or value != 0) else None

    def subcategories(self, value):
        self._p['subcategories'] = value

    def seo_title(self, lang, value):
        self._check_dict('seo_title')
        self._p['seo_title'][lang] = value

    def seo_description(self, lang, value):
        self._check_dict('seo_description')
        self._p['seo_description'][lang] = value


class NubeVariant(NubeObject):
    def __init__(self):
        super().__init__()

    def variant_id(self, value):
        self._p['id'] = value

    def image_id(self, value):
        self._v['image_id'] = value

    def product_id(self, value):
        self._p['product_id'] = value

    def position(self, value):
        self._p['position'] = value

    def price(self, value):
        self._p['price'] = value

    def promotional_price(self, value):
        self._p['promotional_price'] = value

    def stock_management(self, value):
        self._p['stock_management'] = value

    def stock(self, value):
        self._p['stock'] = value

    def weight(self, value):
        self._p['weight'] = value

    def width(self, value):
        self._p['width'] = value

    def height(self, value):
        self._p['height'] = value

    def depth(self, value):
        self._p['depth'] = value

    def sku(self, value):
        self._p['sku'] = value

    def values(self, lang, values):
        self._check_list('values')
        for d in self._p['values']:
            if lang in d.keys():
                return
        self._p['values'].append({lang: values})


class NubeProduct(NubeObject):
    def __init__(self):
        super(NubeProduct, self).__init__()

    def id(self, value):
        if value or value != 0:
            self._p['id'] = value

    def name(self, lang, value):
        self._check_dict('name')
        self._p['name'][lang] = value

    def description(self, lang, value):
        self._check_dict('description')
        self._p['description'][lang] = u'<div align="justify">' \
                                       u'{}</div>'.format(value)

    def handle(self, lang, value):
        self._check_dict('handle')
        self._p['handle'][lang] = value

    def attributes(self, lang, value):
        self._check_list('attributes')
        self._p['attributes'].append({lang: value})

    def published(self, value):
        self._p['published'] = 'true' if value else 'false'

    def free_shipping(self, value):
        self._p['free_shipping'] = value

    def canonical_url(self, value):
        self._p['canonical_url'] = value

    def seo_title(self, lang, value):
        self._check_dict('seo_title')
        self._p['seo_title'][lang] = value

    def seo_description(self, lang, value):
        self._check_dict('seo_description')
        self._p['seo_description'][lang] = value

    def variants(self, value):
        self._check_dict('variants')
        self._p['variants'] = value

    def tags(self, value):
        self._p['tags'] = value

    def images(self, value):
        self._p['images'] = value

    def categories(self, value):
        self._p['categories'] = value

    def sku(self, value):
        """ Identificador de producto """

        self._p['sku'] = value


class NubeImage(NubeObject):
    def __init__(self):
        super(NubeImage, self).__init__()

    def attachment(self, value):
        self._p['attachment'] = value

    def filename(self, value):
        self._p['filename'] = value

    def id(self, value):
        self._p['id'] = value

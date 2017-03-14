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
from product import NubeImage

class TestNubeImage(TestCase):
    def test_attachment(self):
        p = NubeImage()
        p.attachment('this is the attachment')
        self.assertDictEqual(p.get_dict(), {'attachment': 'this is the attachment'})

    def test_filename(self):
        p = NubeImage()
        p.filename('test.gif')
        self.assertDictEqual(p.get_dict(), {'filename': 'test.gif'})

    def test_id(self):
        p = NubeImage()
        p.id('123456')
        self.assertDictEqual(p.get_dict(), {'id': '123456'})

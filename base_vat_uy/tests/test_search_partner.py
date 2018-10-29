# - coding: utf-8 -*-
##############################################################################
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
##############################################################################

from odoo.tests import common


class TestSearchPartner(common.TransactionCase):

    def create_partner(self):
        self.partner1 = self.env['res.partner'].create({
            'name': 'PPPARTNERRR1QWERTY',
            'vat': '12345678',
        })
        self.partner2 = self.env['res.partner'].create({
            'name': 'PPPARTNER2',
            'vat': '345',
        })

    def setUp(self):
        super(TestSearchPartner, self).setUp()
        self.create_partner()

    def test_search_partner(self):
        assert self.env['res.partner'].name_search(name='1QW')[0][0] == self.partner1.id
        assert self.env['res.partner'].name_search(name='123456')[0][0] == self.partner1.id
        assert len(self.env['res.partner'].name_search(name='PPPART')) == 2
        assert len(self.env['res.partner'].name_search(name='345')) == 2

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

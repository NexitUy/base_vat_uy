# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo.tests import common
from openerp.exceptions import ValidationError


class TestCheckVatPartner(common.TransactionCase):

    def setUp(self):
        super(TestCheckVatPartner, self).setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test',
            'country_id': self.env.ref('base.uy').id,
            'partner_document_type_id': self.env.ref('base_vat_uy.partner_document_type_ci').id
        })

    def test_partner_check_vat_uy(self):
        self.partner.vat = "60763347"
        with self.assertRaises(ValidationError):
            self.partner.vat = "211975920012"

        self.partner.vat = "60763347"
        with self.assertRaises(ValidationError):
            self.partner.partner_document_type_id = self.env.ref('base_vat_uy.partner_document_type_ruc').id

        with self.assertRaises(ValidationError):
            self.partner.country_id = self.env.ref('base.uy').id,

        self.partner.write({
            'vat': "211975920012",
            'partner_document_type_id': self.env.ref('base_vat_uy.partner_document_type_ruc').id
        })

    def test_partner_check_country(self):

        # Uruguay con DNI
        with self.assertRaises(ValidationError):
            self.partner.partner_document_type_id = self.env.ref('base_vat_uy.partner_document_type_dni').id
            
        self.partner.write({
            'country_id': None,
            'partner_document_type_id': None
        })

        # Sin pais y CI
        with self.assertRaises(ValidationError):
            self.partner.partner_document_type_id = self.env.ref('base_vat_uy.partner_document_type_ci').id

        # Argentino sin DNI
        with self.assertRaises(ValidationError):
            self.partner.country_id = self.env.ref('base.ar').id

        # Argentino con RUC
        with self.assertRaises(ValidationError):
            self.partner.partner_document_type_id = self.env.ref('base_vat_uy.partner_document_type_ruc').id

    def test_partner_with_dni(self):
        with self.assertRaises(ValidationError):
            self.partner.write({
                'partner_document_type_id': self.env.ref('base_vat_uy.partner_document_type_dni').id,
                'country_id': self.env.ref('base.it').id
            })

    def test_commercial_fields(self):
        fields = ['partner_document_type_id', 'vat', 'country_id']
        assert all(field in self.partner._commercial_fields() for field in fields)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

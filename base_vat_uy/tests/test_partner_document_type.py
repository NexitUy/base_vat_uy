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


class TestPartnerDocumentType(common.TransactionCase):

    def setUp(self):
        super(TestPartnerDocumentType, self).setUp()

    def test_set_uy_validation(self):
        self.env.ref('base.uy').validate_document_number = False
        self.env['res.country'].set_uy_vat_validation()
        assert self.env.ref('base.uy').validate_document_number

    def test_assign_foo(self):
        self.env.ref('base_vat_uy.partner_document_type_ruc').verification_required = True
        with self.assertRaises(ValidationError):
            self.env.ref('base_vat_uy.partner_document_type_passport').verification_required = True

    def test_valid_ci(self):
        ci = self.env.ref('base_vat_uy.partner_document_type_ci')
        assert ci.validate_ci("60763347") == 7
        assert ci.validate_ci("55996612") == 2
        assert ci.validate_ci("11631242") == 2
        assert ci.validate_ci("10221240") == 0

    def test_valid_ruc(self):
        ruc = self.env.ref('base_vat_uy.partner_document_type_ruc')
        assert ruc.validate_ruc("211975920012") == 2
        assert ruc.validate_ruc("212687280016") == 6
        assert ruc.validate_ruc("214924890013") == 3
        assert ruc.validate_ruc("211205920010") == 0

    def test_invalid_len(self):
        ci = self.env.ref('base_vat_uy.partner_document_type_ci')
        ruc = self.env.ref('base_vat_uy.partner_document_type_ruc')
        with self.assertRaises(ValidationError):
            ci.validate_ci("607633475")
        with self.assertRaises(ValidationError):
            ci.validate_ci("6076475")
        with self.assertRaises(ValidationError):
            ruc.validate_ruc("2149248900132")
        with self.assertRaises(ValidationError):
            ruc.validate_ruc("2149240013")

    def test_not_int(self):
        ci = self.env.ref('base_vat_uy.partner_document_type_ci')
        ruc = self.env.ref('base_vat_uy.partner_document_type_ruc')
        with self.assertRaises(ValidationError):
            ci.validate_ci("A0763347")
        with self.assertRaises(ValidationError):
            ruc.validate_ruc("A14924890013")

    def test_ruc_format(self):
        ruc = self.env.ref('base_vat_uy.partner_document_type_ruc')
        # Las primeras dos posiciones deben estar entre 01 y 21
        with self.assertRaises(ValidationError):
            ruc.validate_ruc("002687280016")
        with self.assertRaises(ValidationError):
            ruc.validate_ruc("222687280016")

        # de 3 a 9 no deberia haber 0s
        with self.assertRaises(ValidationError):
            ruc.validate_ruc("210000000013")

    def test_invalid_ruc(self):
        ruc = self.env.ref('base_vat_uy.partner_document_type_ruc')
        with self.assertRaises(ValidationError):
            ruc.validate_ruc("211975920013")

    def test_invalid_ci(self):
        ci = self.env.ref('base_vat_uy.partner_document_type_ci')
        with self.assertRaises(ValidationError):
            ci.validate_ci("60763346")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

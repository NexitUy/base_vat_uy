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

from openerp import models, fields, api
from openerp.exceptions import ValidationError


class ResPartner(models.Model):

    _inherit = 'res.partner'

    partner_document_type_id = fields.Many2one('partner.document.type', 'Tipo de documento')
    verification_required = fields.Boolean(related='partner_document_type_id.verification_required')

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        by_name = super(ResPartner, self).name_search(name, args=args, operator=operator, limit=limit)
        by_vat_domain = [('vat', operator, name)]
        by_vat_domain += args
        by_vat = self.search(by_vat_domain, limit=limit)
        return list(set(by_name + by_vat.name_get()))

    @api.constrains("partner_document_type_id", "country_id")
    def check_country_id(self):
        """
        Si el tipo de documento es ruc o ci el pais seleccionado debe ser Uruguay
        Si se selecciona "Otros, pasaporte o NIFE" todos los paises menos Uruguay estan habilitados
        """
        ruc = self.env.ref('base_vat_uy.partner_document_type_ruc')
        ci = self.env.ref('base_vat_uy.partner_document_type_ci')
        dni = self.env.ref('base_vat_uy.partner_document_type_dni')

        for partner in self:

            if partner.partner_document_type_id and not partner.parent_id:
                if partner.partner_document_type_id in [ruc, ci] and partner.country_id != self.env.ref('base.uy'):
                    raise ValidationError("El pais seleccionado debe ser Uruguay si el tipo de documento es RUC o CI")

                if partner.partner_document_type_id not in [ruc, ci] and partner.country_id == self.env.ref('base.uy'):
                    raise ValidationError("No puede seleccionar como pais a Uruguay si el tipo de documento no es RUC o CI")

                valid_dni_countries = self._get_valid_dni_countries()
                if partner.partner_document_type_id == dni and partner.country_id not in valid_dni_countries:
                    raise ValidationError("Solo los paises {} estan habilitados para el tipo de documento DNI".format(
                        ', '.join(valid_dni_countries.mapped('name'))
                    ))

    @api.constrains("vat", "partner_document_type_id", "country_id")
    def check_vat_number(self):
        """ Valida el numero de documento si el pais requiere validacion """
        for partner in self:
            country = partner.parent_id.country_id if partner.parent_id else partner.country_id
            if country.validate_document_number:
                partner.check_vat(partner.vat)

    def check_vat(self, vat_number):
        """
        Verifica que el numero de documento sea correcto
        :param vat_number: str - Numero de documento a validar
        """
        if vat_number and self.partner_document_type_id.verification_required:
            getattr(self.partner_document_type_id, self.partner_document_type_id.foo)(vat_number)

    def _get_valid_dni_countries(self):
        """ Devuelve los paises los cuales tienen numero de DNI """
        countries = self.env.ref('base.br') | self.env.ref('base.ar') \
            | self.env.ref('base.py') | self.env.ref('base.cl')

        return countries

    @api.model
    def _commercial_fields(self):
        return super(ResPartner, self)._commercial_fields() + ['partner_document_type_id', 'country_id']

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

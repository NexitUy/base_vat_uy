# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

{

    'name': u'Uruguayan Localization - RUT number',

    'version': '1.0',

    'summary': 'Type of document and validations for partners for Uruguay',

    'description': """
    Add in Customers and Suppliers (res.partner) the types of documents required for Electronic Billing in Uruguay: RUT, CI, Passport, DNI, NIFE and others.

    -Validates the country / type of document combination

    -Validate the algorithms of RUT and C.I.

    ---

    Agrega en Clientes y Proveedores (res.partner) los tipos de documentos requeridos para Facturación Electrónica en Uruguay: RUT, CI, Pasaporte, DNI, NIFE y otros.

    -Valida la combinación Pais / Tipo de documento

    -Valida los algoritmos de RUT y C.I.
""",
    'author': 'NEXIT',

    'website': 'www.nexit.com.uy',

    'category': 'base',

    'depends': [
        'base_vat_validation'
    ],

    'data': [
        'security/ir.model.access.csv',
        'data/res_country_data.xml',
        'data/partner_document_type_data.xml',
        'views/res_partner_view.xml',
        'views/res_company_view.xml',
        'views/partner_document_type_view.xml'
    ],

    'active': False,

    'installable': True,

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

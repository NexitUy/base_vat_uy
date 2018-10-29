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
ERROR_MESSAGE = "El documento {} es invalido para el tipo de documento {}"


class PartnerDocumentType(models.Model):

    _name = 'partner.document.type'
    
    name = fields.Char('Nombre', required=True)
    verification_required = fields.Boolean('Valida numeracion de documento?')
    foo = fields.Char('Funcion de validacion de documento')

    @api.constrains("verification_required")
    def check_foo(self):
        for document_type in self:
            if document_type.verification_required and not document_type.foo:
                raise ValidationError("No existe funcion asociada para validar este tipo de documento")

    def validate_ruc(self, ruc):
        """
        Validacion de ruc: Modulo 11, Base 43298765432,
        2 Primeras Posiciones entre 01 y 21,de 3 a 9 entre 1 y 999999
        :param ruc: Numero de ruc a validar
        :raise ValidationError: Si el ruc es invalido
        """
        error = ERROR_MESSAGE.format(ruc, self.name)
        # Validamos que sean solo enteros
        try:
            int(ruc)
        except ValueError:
            raise ValidationError(error)
        # Validamos la longitud, las primeras dos posiciones y que de 3 a 9 no sean 0s
        if len(ruc) != 12 or int(ruc[:2]) not in range(1, 22) or ruc[2:8] == ''.zfill(6):
            raise ValidationError(error)

        ruc_no_digit = ruc[:11]
        multipliers = [4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        suma = 0
        for i in range(0, 11):
            suma += int(ruc_no_digit[i]) * multipliers[i]

        rest = suma % 11
        check_dig = 11 - rest
        if check_dig == 11:
            check_dig = 0
        if check_dig == 10 or check_dig != int(ruc[-1:]):
            raise ValidationError(error)

        return check_dig

    def validate_ci(self, ci):
        """
        Valida el numero de C.I.
        https://es.wikipedia.org/wiki/C%C3%A9dula_de_Identidad_de_Uruguay#D.C3.ADgito_verificador
        :param ci: Numero de CI
        :raise ValidationError: Si el ruc es invalido
        """
        error = ERROR_MESSAGE.format(ci, self.name)
        try:
            int(ci)
        except ValueError:
            raise ValidationError(error)
        if len(ci) != 8:
            raise ValidationError(error)

        ci_no_digit = ci[:7]
        multipliers = [2, 9, 8, 7, 6, 3, 4]

        suma = 0
        for i in range(0, 7):
            x = int(ci_no_digit[i]) * multipliers[i]
            suma += (x-(x/10)*10)

        codigo = 10 - (suma-(suma/10)*10)
        if codigo == 10:
            codigo = 0

        # Validamos el ultimo digito con el codigo que deberia ser
        if int(ci[-1:]) != codigo:
            raise ValidationError(error)

        return codigo

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

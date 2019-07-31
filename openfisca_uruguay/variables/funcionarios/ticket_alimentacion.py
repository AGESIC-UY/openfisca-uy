# -*- coding: utf-8 -*-

#
# Definición de las variables y formulas necesarias para calcular el monto de ticket de alimentación
# que coresponde a los funcionarios de la administración pública
#

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_uruguay.entities import *

#
# Definición de las variables de entrada
#
class Aguinaldo_1er_Sem(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = u'Aguinaldo recibido en el 1er Semestre'
    reference = u'' 

class Aguinaldo_2do_Sem(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = u'Aguinaldo recibido en el 2do Semestre'
    reference = u''

class Year_Trabajados(Variable):
    value_type = int
    entity = Person
    definition_period = YEAR
    label = u'Cantidad de años completos trabajados como funcionario público'
    reference = u''
#---------------------------------------------------------------------------------------------

#
# Definición de las variables auxiliares a calcular
#

class Aguinaldo_total(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = u'Total del aguinaldo recibido en un año'

    def formula(person, period):
        aguinaldos_sem1 = person('Aguinaldo_1er_Sem',period)
        aguinaldos_sem2 = person('Aguinaldo_2do_Sem',period)

        return(
            + aguinaldos_sem1
            + aguinaldos_sem2
        )

class Prima_Antiguedad(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = u'Prima por antiguedad'

    def formula(person, period, parameters):
        listado_years_trab = person('Year_Trabajados',period)
        condicion_cump = listado_years_trab >= parameters(period).funcionarios.ticket_alimentacion.minimo_year
        return (
            condicion_cump * listado_years_trab * parameters(period).funcionarios.ticket_alimentacion.prima_antiguedad
        )

class A_B(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = u'Valor base de la comparación'

    def formula(person, period):
        aguinaldos_totales = person('Aguinaldo_total', period)
        primas_por_antiguedad = person('Prima_Antiguedad',period)

        return(
            + aguinaldos_totales
            - primas_por_antiguedad
        )

class BPC_dic(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = u'Expresado a BPC Dic'

    def formula(person, period, parameters):
        list_ab = person('A_B',period)
        return round_(
            +list_ab
            / parameters(period).funcionarios.ticket_alimentacion.bpc
        ,2)
    
#------------------------------------------------------------------------------------------------------------

#
# Variables calculadas a responder
#

class Importe(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = u'Importe final del ticket de alimentacion'

    def formula(person, period, parameters):
        lista_bpc_dic = person('BPC_dic',period.last_year)

        return (
            select(
                [
                    lista_bpc_dic < 5,
                    (lista_bpc_dic >=5) * (lista_bpc_dic < 10),
                    (lista_bpc_dic >= 10) * (lista_bpc_dic <= 20),
                    lista_bpc_dic > 20
                ],
                [
                    parameters(period).funcionarios.ticket_alimentacion.bpc * 2,
                    parameters(period).funcionarios.ticket_alimentacion.bpc,
                    parameters(period).funcionarios.ticket_alimentacion.bpc * 0.5,
                    0
                ]
            )
        )

#-----------------------------------------------------------------------------------------------------
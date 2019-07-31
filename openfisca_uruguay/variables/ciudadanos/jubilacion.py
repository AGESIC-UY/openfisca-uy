# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/key-concepts/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_uruguay.entities import *


class number_of_years_worked(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "Number of years worked"

class number_of_years_computados(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "Numero de años computados para el calculo"

    def formula(person, period, parameters):
            """Cantidad de años trabajados + (Si es mujer 1 año * cada hijo hasta un máximo de 5)"""
            women = (person('gender', period) == 1)
            condicion_cant_hijos = person('number_of_children',period) >= parameters(period).ciudadanos.cantidad_hijos
            child_offset = where(condicion_cant_hijos,5,person('number_of_children',period)) * women
            return (person('number_of_years_worked',period) + child_offset)

class number_of_children(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "Number of children"

class elegible_jubilacion_comun(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Si una persona es elegible para la pensión común"
    reference = u"https://www.bps.gub.uy/3499/jubilacion-comun.html"

    def formula(person, period, parameters):
        condicion_edad = person('age',period) >= parameters(period).ciudadanos.edad_de_jubilacion
        condicion_year_of_work = person('number_of_years_computados', period) >= parameters(period).ciudadanos.year_requeridos_jubilacion
        return condicion_edad * condicion_year_of_work

class elegible_jubilacion_edad_avanzada(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Si una persona es elegible para la jubilación por edad avanzada"
    reference = u"https://www.bps.gub.uy/3500/jubilacion-por-edad-avanzada.html"

    def formula(person, period, parameters):
        edad = person('age', period)
        ywork = person('number_of_years_computados', period)
        min_edad = parameters(period).ciudadanos.edad_avanzada.min_edad
        max_year_worked = parameters(period).ciudadanos.edad_avanzada.max_year
        return select(
            [
            (ywork >= max_year_worked) * (edad >= min_edad),
            (ywork >= (max_year_worked - 2)) * (edad >= (min_edad + 1)),
            (ywork >= (max_year_worked - 4)) * (edad >= (min_edad + 2)),
            (ywork >= (max_year_worked - 6)) * (edad >= (min_edad + 3)),
            (ywork >= (max_year_worked - 8)) * (edad >= (min_edad + 4)),
            (ywork >= (max_year_worked - 10)) * (edad >= (min_edad + 5)),
            ywork < (max_year_worked - 10)
            ],
            [
            True,
            True,
            True,
            True,
            True,
            True,
            False
            ],
            )

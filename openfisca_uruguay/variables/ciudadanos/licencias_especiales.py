# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/key-concepts/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_uruguay.entities import *

class trabaja_act_priv(Variable):
    value_type = bool
    default_value = True
    entity = Person
    label = u"Si el trabajador trabaja en la actividad privada"
    definition_period = MONTH

class es_estudiante(Variable):
    value_type = bool
    default_value = True
    entity = Person
    label = u"Si el trabajador es un estudiante"
    definition_period = MONTH

class antiguedad(Variable):
    value_type = int
    entity = Person
    label = u"Antiguedad en meses trabajados en la empresa"
    definition_period = MONTH

class cantidad_horas_semanales(Variable):
    value_type = int
    entity = Person
    label = u"Cantidad de horas de trabajo semanales"
    definition_period = MONTH

class cantidad_dias_licencia_x_estudio(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = u"Cantidad de días de licencia por estudio que merece"

    def formula(person, period, parameters):
        condicion_necesaria = where (person('trabaja_act_priv', period) *
                              person('es_estudiante', period) *
                              (person('antiguedad', period) >= parameters(period).licencias.estudio.antiguedad_min ),
                              True,
                              False
                              )
        return select (
                [
                condicion_necesaria * (person('cantidad_horas_semanales', period) < 36 ),
                condicion_necesaria * (person('cantidad_horas_semanales', period) > 48 ),
                condicion_necesaria,
                not(condicion_necesaria)
                ],
                [
                6,
                12,
                9,
                0
                ],
        )

class PaternidadStatus(Enum):
    nacimiento = u'Nacimiento de un hijo'
    adopcion = u'Adopción de un hijo'
    leg_adoptiva = u'Se legitimiza una adopcion'
    none = u'No cumple con ninguna de las anteriores'

class paternidad_status(Variable):
    value_type = Enum
    possible_values = PaternidadStatus
    default_value = PaternidadStatus.none  # The default is mandatory
    entity = Person
    definition_period = MONTH
    label = u"Tipo de paternidad"

class cantidad_dias_licencia_x_paternidad(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = u"Cantidad de días de licencia por paternidad que merece"

    def formula(person, period, parameters):
        paternidad = person('paternidad_status',period)
        nacimiento = (paternidad == PaternidadStatus.nacimiento)
        adopcion = (paternidad == PaternidadStatus.adopcion)
        leg_adoptiva = (paternidad == PaternidadStatus.leg_adoptiva)
        none = (paternidad == PaternidadStatus.none)
        condicion_necesaria = where (person('trabaja_act_priv', period) *
                              (nacimiento + adopcion + leg_adoptiva),
                              True,
                              False
                              )
        return where(condicion_necesaria, 3, 0)

class es_matrimonio(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = u"Si contrae matrimonio"

class cantidad_dias_licencia_x_matrimonio(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = u"Cantidad de días de licencia por contraer matrimonio"

    def formula(person, period, parameters):
        return where (
                person('trabaja_act_priv', period) * person('es_matrimonio', period),
                3,
                0
        )
class FallecimientoStatus(Enum):
    padre = u'Fallecimiento del padre'
    madre = u'Fallecimiento de la madre'
    hijo = u'Fallecimiento de un hijo'
    hermano = u'Fallecimiento de un hermano'
    concubino = u"Fallecimiento de un concubino"
    none = u"No tiene ningun fallecimiento"

class fallecimiento_status(Variable):
    value_type = Enum
    possible_values = FallecimientoStatus
    default_value = FallecimientoStatus.none  # The default is mandatory
    entity = Person
    definition_period = MONTH
    label = u"Tipo de fallecimiento"

class cantidad_dias_licencia_x_duelo(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = u"Cantidad de días de licencia por fallecimiento de un ser allegado"

    def formula(person, period, parameters):
        fallecimiento = person('fallecimiento_status',period)
        padre = (fallecimiento == FallecimientoStatus.padre)
        madre = (fallecimiento == FallecimientoStatus.madre)
        hijo = (fallecimiento == FallecimientoStatus.hijo)
        hermano = (fallecimiento == FallecimientoStatus.hermano)
        concubino = (fallecimiento == FallecimientoStatus.concubino)
        none = (fallecimiento == FallecimientoStatus.none)
        condicion_necesaria = where (person('trabaja_act_priv', period) *
                              (padre + madre + hijo + hermano + concubino),
                              True,
                              False
                              )
        return where(condicion_necesaria, 3, 0)

# -*- coding: utf-8 -*-

import json
import os


DIR_PATH = os.path.dirname(os.path.abspath(__file__))


def parse(file_name):
    file_path = os.path.join(DIR_PATH, file_name)
    with open(file_path, 'r') as file:
        return json.loads(file.read())


single = parse('single.json')
couple = parse('couple.json')
single_jubilacion = parse('jubilacion.json')
single_licencia_x_duelo = parse('licencia_x_duelo.json')
single_licencia_x_estudio = parse('licencia_x_estudio.json')
single_licencia_x_matrimonio = parse('licencia_x_matrimonio.json')
single_licencia_x_paternidad = parse('licencia_x_paternidad.json')
couple_ticket_alimentacion = parse('couple_ticket_alimentacion.json')
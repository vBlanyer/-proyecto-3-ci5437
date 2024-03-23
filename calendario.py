from ics import Calendar, Event
from decode_match import decode_match
import json
from datetime import datetime, timedelta

def crear_calendario(partidos, json_data):    

    variables_solucion = []

     # Leer la salida del SAT solver de r.txt y extraer las variables de solución
    with open('r.txt', 'r') as sol_file:
        for line in sol_file:
            if line.startswith('s SATISFIABLE'):
                continue  # Ignoramos la línea que indica que la solución es satisfactoria
            vars = line.split()
            for var in vars:
                if var.isdigit():  # Aseguramos que solo tomamos números positivos
                    variables_solucion.append(int(var))

    # Datos del torneo, obtenidos del archivo JSON
    with open(json_data, 'r') as file:
        torneo_info = json.load(file)

    n = len(torneo_info['participants'])  # Número de participantes
    days = (datetime.strptime(torneo_info['end_date'], '%Y-%m-%d') - datetime.strptime(torneo_info['start_date'], '%Y-%m-%d')).days + 1
    matches_per_day = (datetime.strptime(torneo_info['end_time'], '%H:%M:%S') - datetime.strptime(torneo_info['start_time'], '%H:%M:%S')).seconds // (3600 * 2)  # Asume partidos de 2 horas

    cal = Calendar()

    for var in variables_solucion:
        match_info = decode_match(var, n, days, matches_per_day, torneo_info['start_date'], torneo_info['start_time'], torneo_info['participants'])
        evento = Event()
        evento.name = f"{match_info['local']} vs {match_info['visitante']}"
        evento.begin = match_info['fecha_hora_inicio']
        evento.duration = timedelta(hours=2)  # Asume partidos de 2 horas de duración
        evento.description = f"Partido entre {match_info['local']} (local) y {match_info['visitante']} (visitante)"
        cal.events.add(evento)

    # Guardar el archivo .ics
    with open("calendario_del_torneo.ics", "w") as my_file:
        my_file.writelines(cal)
pass

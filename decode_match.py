from datetime import datetime, timedelta

def decode_match(var, n, days, match_for_day, start_date_str, start_time_str):
    var -= 1  
    l = (var % match_for_day) + 1
    var //= match_for_day
    k = (var % days) + 1
    var //= days
    j = (var % n) + 1
    i = (var // n) + 1

    # Convierte k (día del torneo) y l (bloque horario) a fecha y hora específica
    match_date = datetime.strptime(start_date_str, "%Y-%m-%d") + timedelta(days=k-1)
    match_start_time = datetime.strptime(start_time_str, "%H:%M:%S") + timedelta(hours=2*(l-1))  # Asume partidos de 2 horas de duración

    # Formatea la fecha y hora del partido
    match_datetime = datetime.combine(match_date, match_start_time.time()).strftime('%Y-%m-%d %H:%M:%S')

    return {
        'local': f"Equipo {i}",
        'visitante': f"Equipo {j}",
        'fecha_hora_inicio': match_datetime
    }

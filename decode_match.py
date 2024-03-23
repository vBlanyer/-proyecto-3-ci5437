from datetime import datetime, timedelta

def decode_match(var, n, days, matches_per_day, start_date_str, start_time_str, participants):
    var -= 1  
    l = (var % matches_per_day) + 1
    var //= matches_per_day
    k = (var % days) + 1
    var //= days
    j = (var % n) + 1
    i = (var // n) + 1
 
    # Comprobamos que los índices i y j no sean mayores que el número de participantes - 1
    # y que i no sea igual a j. Si es igual o mayor, lo ajustamos.
    if i >= n:
        i = i % n
    if j >= n:
        j = j % n
    if i == j:
        j = (j + 1) % n

    local = participants[i - 1]  # i-1 porque los índices en la lista de participantes comienzan en 0
    visitante = participants[j - 1]  # j-1 por la misma razón

    # Convierte k (día del torneo) y l (bloque horario) a fecha y hora específica
    match_date = datetime.strptime(start_date_str, "%Y-%m-%d") + timedelta(days=k-1)
    match_start_time = datetime.strptime(start_time_str, "%H:%M:%S") + timedelta(hours=2*(l-1))

    # Formatea la fecha y hora del partido
    match_datetime = datetime.combine(match_date, match_start_time.time()).strftime('%Y-%m-%d %H:%M:%S')

    return {
        'local': local,
        'visitante': visitante,
        'fecha_hora_inicio': match_datetime
    }


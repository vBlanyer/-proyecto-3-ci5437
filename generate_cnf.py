""" 
      Programa que traduce cualquier JSON en el formato 
"""
import json
import datetime

def asignar_variables(n, days, match_for_day, i, j, k, l):
      '''
      Función que asigna un número entero a cada variable del problema, para poder identificarlas

      Parámetros:
      - n: int. Cantidad de participantes
      - days: int. Cantidad de días que dura el torneo
      - match_for_day: int. Cantidad de juegos que se pueden jugar por día
      - i: int. Participante que juega con j
      - j: int. Participante que juega con i
      - k: int. Día en el que juegan i y j
      - l: int. Hora en la que juegan i y j

      Retorna:
      - int. Número entero que representa la variable del problema

      '''

      return (n * (days * match_for_day) * (i - 1)) + (days * match_for_day * (j - 1)) + (match_for_day * (k - 1)) + (l - 1) + 1
l


def generate_cnf(json_data):

      # Abriendo archivo JSON

      try:
            with open(json_data, 'r') as file:
                  data = json.load(file)
      except:
            print("Error al abrir el archivo JSON")
            return
      
      # Cargando datos del JSON, no es necesario validar que los datos sean correctos ya que el JSON ya fue validado al ser cargado

      tournament_name = data["tournament_name"]
      start_date = data["start_date"] 
      end_date = data["end_date"]
      start_time = data["start_time"] 
      end_time = data["end_time"] 
      participants = data["participants"] 

      # Creamos las variables que vamos a necesitar para el problema

      n = len(participants) #Cantidad de participantes
      m = n * (n - 1) # Cantidad de combinaciones de juegos
      days = (datetime.datetime.strptime(end_date, '%Y-%m-%d') - datetime.datetime.strptime(start_date, '%Y-%m-%d')).days + 1 
      hours = int((datetime.datetime.strptime(end_time, '%H:%M:%S') - datetime.datetime.strptime(start_time, '%H:%M:%S')).seconds / 3600) 
      match_for_day = hours // 2

      # Numero total de variables
      total_variables = m * days * match_for_day

      clauses = []

      # las clausulas que representan las restricciones del problema son las siguientes:

      # 0. Todo participante debe jugar al menos una vez con cada uno de los otros participantes

      # for i in range(1, n + 1): # i es el participante que juega con j
      #       for j in range(i + 1, n + 1): # j es el participante que juega con i
      #             if i != j:
      #                   for k in range(1, days + 1):
      #                         for l in range(1, match_for_day + 1):
      #                               if asignar_variables(n, days, match_for_day, i, j, k, l) != asignar_variables(n, days, match_for_day, j, i, k, l):
      #                                     print(asignar_variables(n, days, match_for_day, i, j, k, l), asignar_variables(n, days, match_for_day, j, i, k, l))
      #                               clauses.append([asignar_variables(n, days, match_for_day, i, j, k, l), asignar_variables(n, days, match_for_day, j, i, k, l)])

      # 1. Restricciones de que todos los participantes deben jugar dos veces con cada uno de los otros participantes, una como "visitantes" y la otra como "locales"

      for i in range(1, n + 1): # i es el participante que juega con j
            for j in range(1, n + 1): # j es el participante que juega con i
                  if i != j:
                        for k in range(1, days + 1):
                              for l in range(1, match_for_day + 1):
                                    print(f'secuencia {i} {j} {k} {l} valor unico: {asignar_variables(n, days, match_for_day, i, j, k, l)}')
                                    for m in range(1, days + 1):
                                          for o in range(1, match_for_day + 1):
                                                if k != m or l != o:
                                                      clauses.append([-asignar_variables(n, days, match_for_day, i, j, k, l), -asignar_variables(n, days, match_for_day, i, j, m, o)])

      # 2. Restricciones de que dos juegos no pueden ocurrir al mismo tiempo

      for i in range(1, days + 1):
            for j in range(1, match_for_day + 1):
                  for k in range(1, n + 1): # k es el participante que juega con l
                        for l in range(k + 1, n + 1): # l es el participante que juega con k
                              for m in range(1, n + 1): # m es el participante que juega con o
                                    for o in range(m + 1, n + 1): # o es el participante que juega con m
                                          if k != m or l != o:
                                                clauses.append([-asignar_variables(n, days, match_for_day, k, l, i, j), -asignar_variables(n, days, match_for_day, m, o, i, j)])                                                

      # 3. Restricciones de que un participante puede jugar a lo sumo una vez por día

      for i in range(1, n + 1): # i es el participante que juega con j
            for j in range(i + 1, n + 1): # j es el participante que juega con i
                  if i != j:
                        for k in range(j + 1, n + 1):
                              if j != k:      
                                    for l in range(1, days + 1):
                                          for m in range(1, match_for_day + 1):
                                                for o in range(m + 1, match_for_day + 1):
                                                      clauses.append([-asignar_variables(n, days, match_for_day, i, j, l, m), -asignar_variables(n, days, match_for_day, i, k, l, o)])

      # 4. Restricciones de que un participante no puede jugar de "visitante" en dos días consecutivos, ni de "local" dos días seguidos

      for i in range(1, n + 1): # i es el participante
            for k in range(1, days): # días consecutivos (k, k+1)
                  for j in range(1, n + 1): # j es el otro participante
                        if i != j:
                              for l in range(1, match_for_day + 1):
                                    clauses.append([-asignar_variables(n, days, match_for_day, j, i, k, l), -asignar_variables(n, days, match_for_day, j, i, k + 1, l)])
                                    clauses.append([-asignar_variables(n, days, match_for_day, i, j, k, l), -asignar_variables(n, days, match_for_day, i, j, k + 1, l)])
            

                         

      # 5. Restricciones de que todos los juegos deben empezar en horas "en punto". Restriccion implicita al declarar match_for_day

      # 6. Restricciones de que todos los juegos deben ocurrir entre una fecha inicial y una fecha final especificadas. Restriccion implicita al declarar days

      # 7. Restricciones de que todos los juegos deben ocurrir entre un rango de horas especificado, el cuál será fijo para todos los días del torneo. Restriccion implicita al delcarar days

      # 8. Restricciones de que todos los juegos tienen una duración de dos horas. Restriccion implicita al declarar match_for_days

      # Creamos el archivo .txt con el formato DIMACS CNF

      with open('cfn.txt', 'w') as file:
            file.write(f'p cnf {total_variables} {len(clauses)}\n')
            for clause in clauses:
                  file.write(' '.join(map(str, clause)) + ' 0\n')

      print("Archivo .txt generado exitosamente")

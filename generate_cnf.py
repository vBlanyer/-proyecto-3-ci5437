""" 
      Programa que traduce cualquier JSON en el formato 
"""
import json
import sys
import os
import datetime
import itertools
import numpy as np
from itertools import combinations

def asignar_variables(n, days, hours, i, j, k, l):
      '''
      Función que asigna un número entero a cada variable del problema, para poder identificarlas

      Parámetros:
      - n: int. Cantidad de participantes
      - days: int. Cantidad de días que dura el torneo
      - hours: int. Cantidad de horas que dura el torneo
      - i: int. Participante que juega con j
      - j: int. Participante que juega con i
      - k: int. Día en el que juegan i y j
      - l: int. Hora en la que juegan i y j

      Retorna:
      - int. Número entero que representa la variable del problema
      '''
      # assert i >= 1 and i <= n and j >= 1 and j <= n and k >= 1 and k <= days and l >= 1 and l <= hours
      assert i != j

      return (i - 1) * days * hours * n + (j - 1) * days * hours + (k - 1) * hours + l

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

      n = len(participants) 
      m = n * (n - 1) # Cantidad de juegos que se deben jugar
      days = (datetime.datetime.strptime(end_date, '%Y-%m-%d') - datetime.datetime.strptime(start_date, '%Y-%m-%d')).days + 1
      hours = (datetime.datetime.strptime(end_time, '%H:%M:%S') - datetime.datetime.strptime(start_time, '%H:%M:%S')).seconds / 3600 

      # Numero total de variables
      total_variables = m * days * int(hours // 2)

      clauses = []

      # las clausulas que representan las restricciones del problema son las siguientes:

      # 0. Todo participante debe jugar al menos una vez con cada uno de los otros participantes

      # for i in range(1, n + 1):
      #       for j in range(1, n + 1):
      #             if i != j:
      #                   for k in range(1, days + 1):
      #                         for l in range(1, int(hours // 2) + 1):
      #                               clauses.append([asignar_variables(n, days, int(hours), i, k, j, l), asignar_variables(n, days, int(hours), j, k, i, l)])

      # 1. Restricciones de que todos los participantes deben jugar dos veces con cada uno de los otros participantes, una como "visitantes" y la otra como "locales"

      # for i in range(1, n + 1): 
      #       for j in range(i + 1, n + 1):
      #             if i != j:
      #                   for k in range(1, days + 1):
      #                         for l in range(1, int(hours // 2) + 1): 
      #                               clauses.append([asignar_variables(n, days, int(hours // 2), i, j, k, l), asignar_variables(n, days, int(hours // 2), j, i, k, l)])

      # 2. Restricciones de que dos juegos no pueden ocurrir al mismo tiempo

      for i in range(1, days + 1):
            for j in range(1, int(hours // 2) + 1):
                  for k in range(1, n + 1): # k es el participante que juega con l
                        for l in range(k + 1, n + 1): # l es el participante que juega con k
                              for m in range(1, n + 1): # m es el participante que juega con o
                                    for o in range(1, n+1): # o es el participante que juega con m
                                          if k != l and k != m and l != m and k != o and l != o and m != o: # k, l, m y o son distintos
                                                clauses.append([-asignar_variables(n, days, hours, i, j, k, l), -asignar_variables(n, days, hours, m, o, k, l)])                                                

      # 3. Restricciones de que un participante puede jugar a lo sumo una vez por día

      for i in range(1, n + 1):
            for j in range(1, days + 1):
                  for k in range(1, int(hours // 2) + 1):
                        for l in range(j + 1, days + 1):
                              for m in range(1, int(hours // 2) + 1):
                                    clauses.append(asignar_variables(n, days, hours, i, j, k, l)) 

      # 4. Restricciones de que un participante no puede jugar de "visitante" en dos días consecutivos, ni de "local" dos días seguidos

      # for i in range(1, n + 1): 
      #       for j in range(1, days + 1): 
      #             for k in range(1, int(hours // 2) + 1): 
      #                   for l in range(j + 1, days + 1):
      #                         for m in range(1, int(hours // 2) + 1): 
      #                               clauses.append([-i, -j, -k, -l, -m]) 

      # 5. Restricciones de que todos los juegos deben empezar en horas "en punto"

      # for i in range(1, days + 1):
      #       for j in range(1, int(hours // 2) + 1):
      #             for k in range(1, n + 1):
      #                   for l in range(k + 1, n + 1):
      #                         for m in range(1, n + 1):
      #                               if k != m and l != m:
      #                                     clauses.append([-k, -l, -m, -i, -j])

      # 6. Restricciones de que todos los juegos deben ocurrir entre una fecha inicial y una fecha final especificadas

      # for i in range(1, days + 1):
      #       for j in range(1, int(hours // 2) + 1):
      #             for k in range(1, n + 1):
      #                   for l in range(k + 1, n + 1):
      #                         for m in range(1, n + 1):
      #                               if k != m and l != m:
      #                                     clauses.append([-k, -l, -m, -i, -j])

      # 7. Restricciones de que todos los juegos deben ocurrir entre un rango de horas especificado, el cuál será fijo para todos los días del torneo

      # for i in range(1, days + 1):
      #       for j in range(1, int(hours // 2) + 1):
      #             for k in range(1, n + 1):
      #                   for l in range(k + 1, n + 1):
      #                         for m in range(1, n + 1):
      #                               if k != m and l != m:
      #                                     clauses.append([-k, -l, -m, -i, -j])

      # 8. Restricciones de que todos los juegos tienen una duración de dos horas

      # for i in range(1, days + 1):
      #       for j in range(1, int(hours // 2) + 1):
      #             for k in range(1, n + 1):
      #                   for l in range(k + 1, n + 1):
      #                         for m in range(1, n + 1):
      #                               if k != m and l != m:
      #                                     clauses.append([-k, -l, -m, -i, -j])

      # Creamos el archivo .txt con el formato DIMACS CNF

      with open('cfn.txt', 'w') as file:
            file.write(f'p cnf {total_variables} {len(clauses)}\n')
            for clause in clauses:
                  file.write(' '.join(map(str, clause)) + ' 0\n')

      print("Archivo .txt generado exitosamente")

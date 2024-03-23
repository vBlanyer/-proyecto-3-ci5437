# Traduce archivo json a formato DIMACS CNF

from sys import argv
import sys, json, datetime, os, subprocess, threading, time
import json
import generate_cnf as gc
from ics import Calendar, Event

def main():

      # Llamo generate_cnf y le pase el parametro de entrada

      if len(argv) != 2:
            print("Usage: python main.py <input.json>")
            exit(1)
      
      print("Generando archivo DIMACS CNF...")

      diccionario = gc.generate_cnf(argv[1])

      # Aplicando SAT Solver Glucose-4.2.1 a archivo DIMACS CNF

      print("Aplicando SAT Solver Glucose a archivo DIMACS CNF...")

      # Llamo al SAT Solver

      proc = subprocess.Popen(["./glucose/simp/glucose_static", "cfn.txt", "r.txt"])
      proc.wait()

      # El resultado del SAT Solver se guarda en r.txt. Si el resultado es SAT, se imprime la solucion, si es UNSAT, se imprime que no hay solucion

      with open("r.txt", "r") as file:
            result = file.read().strip()
            if result == "UNSAT":
                  exit(0)

      # Cargando datos del JSON

      try:
            with open(argv[1], 'r') as file:
                  data = json.load(file)
      except:
            print("Error al abrir el archivo JSON")
            return
      
      # Cargando datos del JSON, no es necesario validar que los datos sean correctos ya que el JSON dado el enunciado

      tournament_name = data["tournament_name"]
      start_date = data["start_date"] 
      end_date = data["end_date"]
      start_time = data["start_time"] 
      end_time = data["end_time"] 
      participants = data["participants"] 
      
      # Cargando r.txt

      with open("r.txt", "r") as file:
            result = list(map(int, file.read().strip().split()))

      # Creo el archivo .ics

      c = Calendar()

      for i in range(0, len(diccionario)):
            if result[i] > 0:
                  # Obtengo los valores de i, j, k, l
                  for key, value in diccionario.items():
                        if value == i:
                              i, j, k, l = key
                              break
                  # Creo el evento
                  e = Event()
                  e.name = f"{participants[i - 1]} vs {participants[j - 1]}"
                  # Para el inicio y fin del evento, tomo la fecha y hora de inicio del torneo y le sumo los dias y horas correspondientes, con ayuda de k y l, que son los dias y horas de los partidos
                  e.begin = f"{start_date}T{start_time}"
                  e.begin = (datetime.datetime.strptime(e.begin, '%Y-%m-%d%H:%M:%S') + datetime.timedelta(days=k - 1, hours=(l - 1) * 2)).strftime('%Y-%m-%dT%H:%M:%S')
                  e.end = (datetime.datetime.strptime(e.begin, '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%S')
                  c.events.add(e)


                  
      # Guardo el archivo .ics

      with open("tournament.ics", "w") as file:
            file.writelines(c)
      
if __name__ == "__main__":
      main()
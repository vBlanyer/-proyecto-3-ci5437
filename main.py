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

      # Si el resultado es SAT, se utiliza el archivo r.txt para generar un archivo .ics con la solucion

      with open("r.txt", "r") as file:
            result = list(map(int, file.read().strip().split()))
            
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

      # Creo el archivo .ics
      
if __name__ == "__main__":
      main()
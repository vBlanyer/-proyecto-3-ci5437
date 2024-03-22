# Traduce archivo json a formato DIMACS CNF

from sys import argv
import sys, json, datetime, os, subprocess, threading, time
import json
import generate_cnf as gc
from generate_cnf import asignar_variables as av
from ics import Calendar, Event

def main():

      # Llamo generate_cnf y le pase el parametro de entrada

      if len(argv) != 2:
            print("Usage: python main.py <input.json>")
            exit(1)
      
      print("Generando archivo DIMACS CNF...")

      gc.generate_cnf(argv[1])

      # Aplicando SAT Solver Glucose-4.2.1 a archivo DIMACS CNF

      print("Aplicando SAT Solver Glucose a archivo DIMACS CNF...")

      # Llamo al SAT Solver

      proc = subprocess.Popen(["./glucose/simp/glucose_static", "cfn.txt", "r.txt"])
      proc.wait()

      # El resultado del SAT Solver se guarda en r.txt. Si el resultado es SAT, se imprime la solucion, si es UNSAT, se imprime que no hay solucion

      with open("r.txt", "r") as file:
            result = file.read().strip()
            if result == "UNSAT":
                  print("\n\nNo hay solución")
                  exit(0)
            else:
                  print("\n\nSolución encontrada")

      # Si el resultado es SAT, se utiliza el archivo r.txt para generar un archivo .ics con la solucion

if __name__ == "__main__":
      main()
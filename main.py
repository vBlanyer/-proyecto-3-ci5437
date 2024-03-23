# Traduce archivo json a formato DIMACS CNF

from sys import argv
from datetime import datetime
import subprocess
import generate_cnf as gc
from calendario import crear_calendario
from decode_match import decode_match
import json

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
                  exit(0)

      input_file = argv[1]
      
      # Cargar la información del torneo desde el archivo JSON
      with open(input_file, 'r') as file:
            torneo_info = json.load(file)
      
      print(torneo_info)

      # Definición de las variables basadas en la información del torneo
      n = len(torneo_info['participants'])
      start_date = torneo_info['start_date']
      start_time = torneo_info['start_time']
      end_date = torneo_info['end_date']
      end_time = torneo_info['end_time']

      days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days + 1
      matches_per_day = (datetime.strptime(end_time, '%H:%M:%S') - datetime.strptime(start_time, '%H:%M:%S')).seconds // (3600 * 2)

      #  interpretar la salida del SAT solver
      partidos = []
      with open('r.txt', 'r') as sol_file:
            for line in sol_file.readlines():
                  if line.strip() and line.strip() != "0":  # Ignora líneas vacías y la terminación de las cláusulas
                        vars = line.strip().split()
                        for var in vars:
                              if var != "0":  # Ignora el término de fin de cláusula
                                    var_int = int(var)
                                    if var_int > 0:  # Consideramos solo variables positivas como parte de la solución
                                          partido = decode_match(var_int, n, days, matches_per_day, start_date, start_time)
                                          partidos.append(partido)

    # Crear el calendario con los partidos decodificados
      crear_calendario(partidos, argv[1])

if __name__ == "__main__":
    main()

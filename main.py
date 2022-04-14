import os
import numpy as np
import random
import sys
import time
from datetime import datetime
import csv
import re
from scipy import rand


class AlgorithmGeneric():
    def __init__(self) -> None:
        self.size_population = 100
        self.instances = []
        self.jobs = 10
        self._read_instance()
        self.report = []

    def makespan(self, instancia, solucao):
        nM = len(instancia)
        tempo = [0] * nM
        tarefa = [0] * len(solucao)
        for t in solucao:
            if tarefa[t-1] == 1:
                return "SOLUÇÃO INVÁLIDA: tarefa repetida!"
            else:
                tarefa[t-1] = 1
            for m in range(nM):
                if tempo[m] < tempo[m-1] and m != 0:
                    tempo[m] = tempo[m-1]
                tempo[m] += int(instancia[m][t-1])

        return tempo[nM-1]

    def _read_instance(self):
        path = os.path.abspath(os.getcwd()) + "/flowshop/"
        filenames = next(os.walk(path), (None, None, []))[2]
        for filename in filenames:
            file = "".join(re.findall("(\d+_\d+)", filename))
            file = file.split("_")
            with open(path+filename, 'r') as filehandle:
                aux = []
                for file in filehandle.readlines():
                    aux.append(file.split())
                self.instances.append({ 'filename': filename, 'n_jobs': file[0], 'm_numbers': file[1], 'data': aux })

    def create_inital_population(self):
        population = []
        for _ in range(self.size_population):
            population.append(list(np.random.permutation(self.jobs)))
        return population

    def rate_population(self, instance, population):
        aux = []
        for idx, p in enumerate(population):
            apt = self.makespan(instance['data'], list(p))
            aux.append({'solucao': p, 'aptidao': apt})
        return aux

    def best_solution(self, fit_population):
        return max(fit_population, key=lambda fit_population:fit_population['aptidao'])

    def _binary_tournament(self, population):
        parents = random.choices(population, k=len(population))
        parents = sorted(parents, key=lambda fit_population:fit_population, reverse=True)
        return parents[:50]

    def select_population(self, population):
        return self._binary_tournament(population)

    def crossover(self, pop1):
        pt = random.randint(1, len(pop1)-2)
        return pop1[:pt] + pop1[:pt]

    def mutation(self, n_population):
        mutated_solution = list(n_population)
        solution_length = len(n_population)
        swap_positions = list(np.random.permutation(np.arange(solution_length))[:2])
        first_job = n_population[swap_positions[0]]
        second_job = n_population[swap_positions[1]]
        mutated_solution[swap_positions[0]] = second_job
        mutated_solution[swap_positions[1]] = first_job
        return mutated_solution

    def select_new_generation(self, population, n_population):
        numbers_n_population = len(n_population)
        new_pop = n_population[:numbers_n_population] + population[numbers_n_population:100]
        return new_pop

    def generate_csv(self):
        print("GERANDO CSV.", self.report)
        aux = []
        solutions = self.report
        for l in self.report:
            valor_media = 0
            media_execucao = 0
            qtde = 0
            aptidao = 0
            for s in l['solutions']:
                print('S*******' , s)
                valor_media += s['aptidao']
                media_execucao += s['tempoFinal']
                aptidao += s['aptidao']
                qtde += 1
                
            solution = solutions[0]['solutions']
            aux.append({'X': l['filename'],
                    'lower_bound': min(solution, key=lambda solution:solution['aptidao'])['aptidao'], 
                    'upper_bound': max(solution, key=lambda solution:solution['aptidao'])['aptidao'], 
                    'valor_médio': valor_media/qtde, 
                    'desvio_padrão': np.std(aptidao),
                    'media_execucao': media_execucao / qtde,
                    'media_execucao_d': np.mean(media_execucao)})
            
        with open('IA-ALG_GEN_{}.csv'.format(datetime.now()), 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['X',
                                                         'lower_bound', 
                                                         'upper_bound',  
                                                         'valor_médio', 
                                                         'desvio_padrão', 
                                                         'media_execucao',
                                                         'media_execucao_d'
                                                         ])
            writer.writeheader()
            writer.writerows(aux)
            
            
def main():
    AG = AlgorithmGeneric()
    for instance in AG.instances:
        print("ARQUIVO {}".format(instance['filename']))
        time_max = 30
        solutions = []

        for _ in range(10):
            solution = {'solucao': [], 'aptidao': sys.maxsize, 'tempoFinal': 0}
            start_time = time.time()
            population = AG.create_inital_population()
            g_number = 0
            while time.time() < (start_time + time_max * 1):
                if g_number > 950:
                    break
                
                fit_population = AG.rate_population(instance, population)
                current_solution = AG.best_solution(fit_population)
                
                if solution['aptidao'] > current_solution['aptidao']:
                    solution = current_solution                
                
                selected = AG.select_population(population)
                new_selections = AG.crossover(selected)
                new_selections = AG.mutation(new_selections)
                
                population = AG.select_new_generation(population, new_selections)
                g_number+=1
            solution['tempoFinal'] = time.time() - start_time
            print("melhores solução", solution)
            solutions.append(solution)
        
        
        AG.report.append({
            'solutions': solutions,
            'filename' : instance['filename'],
            'n_jobs'   : instance['n_jobs'],
            'm_numbers': instance['m_numbers']
        })
    AG.generate_csv()

    print("*** END ***")

if __name__ == '__main__':
    main()
    
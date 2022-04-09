import os
import numpy as np
import random


class AlgorithmGeneric():
    def __init__(self) -> None:
        self.instances = [['54 83 15 71 77 36 53 38 27 87 76 91 14 29 12 77 32 87 68 94',
                          '79  3 11 99 56 70 99 60  5 56  3 61 73 75 47 14 21 86  5 77',
                           '16 89 49 15 89 45 60 23 57 64  7  1 63 41 63 47 26 75 77 40',
                           '66 58 31 68 78 91 13 59 49 85 85  9 39 41 56 40 54 77 51 31',
                           '58 56 20 85 53 35 53 41 69 13 86 72  8 49 47 87 58 18 68 28'],
                          ['74 21 58  4 21 28 58 83 31 61 94 44 97 94 66  6 37 22 99 83',
                           '28  3 27 61 34 76 64 87 54 98 76 41 70 43 42 79 88 15 49 72',
                           '89 52 56 13  7 32 32 98 46 60 23 87  7 36 26 85  7 34 36 48',
                           '60 88 26 58 76 98 29 47 79 26 19 48 95 78 77 90 24 10 85 55',
                           '54 66 12 57 70 82 99 84 16 41 23 11 68 58 30  5  5 39 58 31',
                           '92 11 54 97 57 53 65 77 51 36 53 19 54 86 40 56 79 74 24  3',
                           ' 9  8 88 72 27 22 50  2 49 82 93 96 43 13 60 11 37 91 84 67',
                           ' 4 18 25 28 95 51 84 18  6 90 69 61 57  5 75  4 38 28  4 80',
                           '25 15 91 49 56 10 62 70 76 99 58 83 84 64 74 14 18 48 96 86',
                           '15 84  8 30 95 79  9 91 76 26 42 66 70 91 67  3 98  4 71 62']
                          ]
        self.populations = []
        self.create_inital_population()
        self.report = [dict() for _ in range(self.instances)]

        print(self.report)

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
                tempo[m] += instancia[m][t-1]
        return tempo[nM-1]

    def _read_instance(self):
        print("READ INSTANCES")
        path = os.path.abspath(os.getcwd()) + "/arquivos/"
        filenames = next(os.walk(path), (None, None, []))[2]
        for filename in filenames:
            with open(path+filename, 'r') as filehandle:
                # print(filehandle.readlines())
                aux = []
                for file in filehandle.readlines():
                    aux.append(file)
                    # print(file)
                # info = [current_place.rstrip() for current_place in filehandle.readlines()]
                # print(info)
                print(aux)
                self.instances.append(aux)

    def create_inital_population(self):
        population = ([random.choice(self.instances)
                       for x in range(2) for i in range(2)])

        self.populations.append(population)


def main():
    algorithm_generic = AlgorithmGeneric()
    # report = [dict() for instancia in range(instances[0])]
    # # report = {index: value for index, value in enumerate(instances, start=0)}
    # print(report)


if __name__ == '__main__':
    main()


# x = [
#     ['54 83 15 71 77 36 53 38 27 87 76 91 14 29 12 77 32 87 68 94',
#      '79  3 11 99 56 70 99 60  5 56  3 61 73 75 47 14 21 86  5 77',
#      '16 89 49 15 89 45 60 23 57 64  7  1 63 41 63 47 26 75 77 40',
#      '66 58 31 68 78 91 13 59 49 85 85  9 39 41 56 40 54 77 51 31',
#      '58 56 20 85 53 35 53 41 69 13 86 72  8 49 47 87 58 18 68 28'],
#     ['74', 21 58  4 21 28 58 83 31 61 94 44 97 94 66  6 37 22 99 83
# 28  3 27 61 34 76 64 87 54 98 76 41 70 43 42 79 88 15 49 72
# 89 52 56 13  7 32 32 98 46 60 23 87  7 36 26 85  7 34 36 48
# 60 88 26 58 76 98 29 47 79 26 19 48 95 78 77 90 24 10 85 55
# 54 66 12 57 70 82 99 84 16 41 23 11 68 58 30  5  5 39 58 31
# 92 11 54 97 57 53 65 77 51 36 53 19 54 86 40 56 79 74 24  3
#  9  8 88 72 27 22 50  2 49 82 93 96 43 13 60 11 37 91 84 67
#  4 18 25 28 95 51 84 18  6 90 69 61 57  5 75  4 38 28  4 80
# 25 15 91 49 56 10 62 70 76 99 58 83 84 64 74 14 18 48 96 86
# 15 84  8 30 95 79  9 91 76 26 42 66 70 91 67  3 98  4 71 62
# ]
#     ]

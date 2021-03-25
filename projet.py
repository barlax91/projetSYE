__author__ = 'ben' 'elvir' 'barou'

from threading import Thread
from queue import Queue

class TaskSystem():
    def getDependencies(Task):
       listTaskDependencies = list()
       listTaskDependencies.append()
       print(listTaskDependencies)

    def estdiff(v1,v2):
        if (v1 == v2):
            return v1
        return None




'''
 class Parall(Thread):
        def __init__(self, queue, Task):
            Thread.__init__(self)
            self.queue = queue
            self.Task = Task

        def run(self):
            while True:
                #executer la tache
                self.queue.task_done()
'''


class Task:
    def __init__(self):
        self.name = ""
        self.reads = []
        self.writes = []
        self.run = None

    def getName(self):
        return self.name

    def getReads(self):
        return self.reads

    def getWrites(self):
        return self.writes

    def estdep(task1, task2):
        """on vérifie si 2 taches sont indépendantes l'une de l'autre en utilisant les conditions de Bernstein"""
        return (TaskSystem.estdiff(task1.reads, task2.writes)
                and TaskSystem.estdiff(task1.writes, task2.reads)
                and TaskSystem.estdiff(task1.writes, task2.writes))


X = None
Y = None
Z = None


def runT1():
    global X
    X = 1


def runT2():
    global Y
    Y = 4


def runTsomme():
    global X, Y, Z
    Z = X + Y


# liste des taches
listTask = list()
# dictionnaire
dicor = dict({})
dicow = dict({})

t1 = Task()
t1.name = "T1"
t1.writes = ["X"]
t1.run = runT1
listTask.append(t1.name)
dicor[t1.name] = t1.reads
dicow[t1.name] = t1.writes

t2 = Task()
t2.name = "T2"
t2.writes = ["Y"]
t2.run = runT2
listTask.append(t2.name)
dicor[t2.name] = t2.reads
dicow[t2.name] = t2.writes

tSomme = Task()
tSomme.name = "somme"
tSomme.reads = ["X", "Y"]
tSomme.writes = ["Z"]
tSomme.run = runTsomme
listTask.append(tSomme.name)
dicor[tSomme.name] = tSomme.reads
dicow[tSomme.name] = tSomme.writes


for k, v in dicor.items():
    print("Nom de la tâche: {} - lectures : {}".format(k, v))
for k,v in dicow.items():
    print("nom tache : {} - écritures : {}".format(k,v))
t1.run()
t2.run()
tSomme.run()
print(X)
print(Y)
print(Z)
# affiche la liste des tâches
print(listTask)
# affiche le dictionnaire
print(dicor.items())
print(dicow.items())

TaskSystem.getDependencies(t2)

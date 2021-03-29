__author__ = 'ben' 'elvir' 'barou'

from threading import Thread
from queue import Queue


class TaskSystem:

    def __init__(self,listTask,dicofinal):
        self.listTask = listTask
        self.dicofinal = dicofinal
        for i in listTask:
            self.getDependencies(i,dicofinal)

    def getDependencies(self,Tnom,dicofinal):
        dicofinal[Tnom.name] = ""
        for i in dico[Tnom.name]:
            for j in listTask:
                if j.name == i:
                    if self.estinter(Tnom, j) == True:
                        dicofinal[Tnom.name] += i

    def run(self):
        #àfaire
        print()

    # on cherche si les fonctions sont interférentes en utilisant les conditions de bernstein
    def estinter(self,task1,task2):
        for i in task1.writes:
            for j in task2.writes:
                if i == j:
                    return True

        for i in task1.reads:
            for j in task2.writes:
                if i == j:
                    return True

        for i in task1.writes:
            for j in task2.reads:
                if i == j:
                    return True
        return False


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



X = None
Y = None
Z = None


# execution de la tache T1
def runT1():
    global X
    X = 1


# execution de la tache T2
def runT2():
    global Y
    Y = 4


# execution de la tache Tsomme
def runTsomme():
    global X,Y,Z
    Z = X + Y


# liste des taches
listTask = list()


# initialisation de tâches pour faire des tests
t1 = Task()
t1.name = "T1"
t1.writes = ["X"]
t1.run = runT1
listTask.append(t1)


t2 = Task()
t2.name = "T2"
t2.writes = ["Y"]
t2.run = runT2
listTask.append(t2)


tSomme = Task()
tSomme.name = "somme"
tSomme.reads = ["X", "Y"]
tSomme.writes = ["Z"]
tSomme.run = runTsomme
listTask.append(tSomme)


# dictionnaire
dico = {"T1":[],"T2":["T1"],"somme":["T1","T2"]}
#
dicofinal={}

s1 = TaskSystem(listTask,dicofinal)


t1.run()
t2.run()
tSomme.run()
print(X)
print(Y)
print(Z)


# affiche le dictionnaire des reads et writes
print(dico.items())
print(dicofinal.items())




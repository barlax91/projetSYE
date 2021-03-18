__author__ = 'ben' 'elvir'

from threading import Thread
from queue import Queue


def getDependencies(Task):
     for getName in dico :
        print(getName,dico[k])





 #class Parall(Thread):
 #       def __init__(self, queue, Task):
  #          Thread.__init__(self)
  #          self.queue = queue
  #          self.Task = Task

   #     def run(self):
   #         while True:
   #             #executer la tache
   #             self.queue.task_done()


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
dico = dict({})


t1 = Task()
t1.name = "T1"
t1.writes = ["X"]
t1.run = runT1
listTask.append(t1.name)
dico[t1.name]=t1.reads
t2 = Task()
t2.name = "T2"
t2.writes = ["Y"]
t2.run = runT2
listTask.append(t2.name)
dico[t2.name]=t2.reads
tSomme = Task()
tSomme.name = "somme"
tSomme.reads = ["X", "Y"]
tSomme.writes = ["Z"]
tSomme.run = runTsomme
listTask.append(tSomme.name)
dico[tSomme.name] = tSomme.reads


for k,v in dico.items():
	print("Nom de la tâche: {} - précédences : {}".format(k,v))


getDependencies(t1)


t1.run()
t2.run()
tSomme.run()
print(X)
print(Y)
print(Z)
#affiche la liste des tâches
print(listTask)
#affiche le dictionnaire
print(dico.items())




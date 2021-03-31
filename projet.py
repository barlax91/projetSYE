__author__ = 'ben' 'elvir' 'barou'

import threading
import time
import queue

exitFlag = 0


class TaskSystem(threading.Thread):

    def __init__(self,threadID,listTask,dicofinal):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.listTask = listTask
        self.dicofinal = dicofinal
        # pour chaque tâche présente dans la liste des tâches on appelle la fonction getDependencies
        for i in listTask:
            self.getDependencies(i,dicofinal)

    # la fonction getDependencies récupère les nom des tâches interférentes et
    # les ajoute dans le dicofinal(dictionnaire des interférences)
    def getDependencies(self,Tnom,dicofinal):
        dicofinal[Tnom.name] = ""
        for i in dico[Tnom.name]:
            for j in listTask:
                if j.name == i:
                    if self.estinter(Tnom, j):
                        dicofinal[Tnom.name] += i

    def run(self,listTask,dico,dicofinal):
        while not exitFlag:
            print("Starting" + self.name)
            t1 = threading.Thread(target=runT1(),args=())
            t2 = threading.Thread(target=runT2(), args=())
            tsomme = threading.Thread(target=runTsomme(), args=())
            tdiff = threading.Thread(target=runTdifference(), args=())
            t1.start()
            t2.start()
            tsomme.start()
            tdiff.start()

            print("Ending" + self.name)
        time.sleep(2)

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
    print("t1exe")


# execution de la tache T2
def runT2():
    global Y
    Y = 4
    print("t2exe")


# execution de la tache Tsomme
def runTsomme():
    global X,Y,Z
    Z = X + Y
    print("tsommeexe")


def runTdifference():
    global X,Y,D
    D = X - Y
    print("tdiffexe")


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

tDifference = Task()
tDifference.name = "difference"
tDifference.reads = ["X","Y"]
tDifference.writes = ["D"]
tDifference.run = runTdifference
listTask.append(tDifference)

# dictionnaire
dico = {"T1":[],"T2":["T1"],"somme":["T1","T2"],"difference":["T1","T2"]}
dicofinal={}

s1 = TaskSystem(0,listTask,dicofinal)


t1.run()
t2.run()
tSomme.run()
tDifference.run()
print(X)
print(Y)
print(Z)
print(D)


# affiche le dictionnaire initial
print(dico.items())
# affiche le dictionnaire final
print(dicofinal.items())




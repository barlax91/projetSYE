__author__ = 'ben' 'elvir' 'barou'

# le package graphviz permet de représenter des diagrammes et graphes à partie d'informations
from itertools import combinations

from graphviz import Digraph
# ce module va nous permettre d'utiliser des threads ainsi que des fonctions liées aux threads
import threading
# permet d'utiliser les queues et des méthodes sur celles-ci telles que queue.empty() ou queue.get()
import queue
# permet d'utiliser la copie récursive
import copy

exitFlag = 0


class TaskSystem:
    listTask = []
    dico = {}

    def __init__(self, listTask, dico):
        self.listTask_ = listTask
        self.dico = dico
        self.todo = queue.Queue()
        self.done = queue.Queue()
        self.draw_ = listTask
        self.verifinter()

    def __new__(cls, listTask, dico):
        # Test s'il ya des duplications
        if len(listTask) != len(set([i.name for i in listTask])):
            raise Exception('tâche doublon')
        # Test si la tâche existe bien
        if False in (
            [item in [item.name for item in listTask] for item in dico]
            + [item in [item.name for item in listTask] for item in dico
               for item in dico.get(item)]):
            raise Exception('La tâche n existe pas')
        return super().__new__(cls)

    # la fonction getDependencies récupère les nom des tâches interférentes et
    # les ajoute dans le dico(dictionnaire des interférences)
    def getDependencies(self,tache):
        # retourne les préférences de la tache
        return self.dico[tache]

    def verifpreferences(self):
        # vérifie si une tâche a des préférences de précédence
        return True in [(len(i.get('preferences')) != 0)
                        for i in self.listTask_]

    def verifinter(self):
        resultat = []
        # crée une liste stockant la tâche, ses préférences, et si elle est terminée ou non
        for task in self.listTask_:
            resultat.append({"task": task, "preferences": [], "finished": False})
        # crée une liste avec toutes les combinaisons possibles de tâches
        combinaisons = list(combinations(self.listTask_, 2))
        for item in combinaisons:
            # pour chaque combinaison on vérifie si les tâches sont interférentes ou pas
            if self.estinter(item[0], item[1]):
                for v in resultat:
                    if v.get('task') == item[1]:
                        v['preferences'] = self.getDependencies(item[1].name)
        self.listTask_ = resultat
        # on copie également ce résultat de manière récursive pour l'affichage du système ensuite
        self.draw_ = copy.deepcopy(resultat)

    def run(self):
        # Execution du système de tâches
        while True:
            # on crée un liste de threads
            threadslist = []
            # si la task n'a pas été faite on la place dans la queue des tâches à faire
            for i, task in enumerate(self.listTask_):
                if not (task.get('preferences')):
                    if not (task.get('terminé')):
                        self.todo.put(task)
                        self.listTask_[i]['terminé'] = True

            # creation de threads pour chaque tâche
            for k in range(len(self.listTask_)):
                t = threading.Thread(target=self.execute)
                # ajout du thread dans la liste
                threadslist.append(t)
                t.start()

                # attend que les threads se termine
            for t in threadslist:
                t.join()
            # print le résultat de la tâche executée
            while not self.done.empty():
                print(self.done.get())
            if self.verifpreferences():
                for task in self.listTask_:
                    if not (task.get('preferences')):
                        for i, item in enumerate(self.listTask_):
                            if task.get('task').name in item.get('preferences'):
                                self.listTask_[i]['preferences'].remove(task.get('task').name)
            else:
                break

    def execute(self):
        while True:
            try:
                # on essaie de récupèrer la tâche à faire dans la queue.
                # La fonction get_nowait() va supprimer et retourner un objet de la file d'attente(Queue)
                task = self.todo.get_nowait()
            except queue.Empty:
                break
            else:
                # si la queue des tâches à faire est vide renvoie les tâches en cours
                if task.get('conditions'):
                    for t in task.get('conditions'):
                        print(f't is {t}')
                else:
                    task.get('task').run()
                    self.done.put(
                        task.get('task').name + ' est effectuée par ' +
                        threading.current_thread().name)

    def draw(self):
        # méthode pour l'affichage du système de parallélisme maximal
        print('draw start')
        dot = Digraph(name="Systeme de taches", format="png")
        # crée un noeud avec le nom des tâches
        # ici le dot.node créer un noeud avec comme identifiant le nom de la tâche
        # et également le nom de la tâche en tant que label
        for i in self.draw_:
            dot.node(i.get('task').name, i.get('task').name)
            # création des edges(flèches) en fonction des préferences
        for i in self.draw_:
            for preference in i.get('preferences'):
                dot.edge(preference,i.get('task').name)
        # affichage
        dot.render("Systeme de tâches")
        print('draw done')

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


class Task:
    # constructeur de la classe tâche
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
    print("execution de t1 : ",X)


# execution de la tache T2
def runT2():
    global Y
    Y = 4
    print("execution de t2 : ", Y)


# execution de la tache Tsomme
def runTsomme():
    global X,Y,Z
    Z = X + Y
    print("execution de tsomme : ",Z)


def runTdifference():
    global X,Y,D
    D = X - Y
    print("execution de tdifference : ", D)


# initialisation des tâches
t1 = Task()
t1.name = "T1"
t1.writes = ["X"]
t1.run = runT1

t2 = Task()
t2.name = "T2"
t2.writes = ["Y"]
t2.run = runT2

tSomme = Task()
tSomme.name = "somme"
tSomme.reads = ["X", "Y"]
tSomme.writes = ["Z"]
tSomme.run = runTsomme

tDifference = Task()
tDifference.name = "difference"
tDifference.reads = ["X","Y"]
tDifference.writes = ["D"]
tDifference.run = runTdifference



'''
# tests 
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
print(dico.items())
'''
s1 = TaskSystem([t1,t2,tSomme,tDifference],{"T1": [],"T2": ["T1"],"somme": ["T1", "T2"],"difference": ["T1", "T2"]})

s1.run()
s1.draw()


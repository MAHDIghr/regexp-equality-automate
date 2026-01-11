# version 2: correction d'un bug dans la fonction minimisation
import copy as cp


class automate:
    """
    classe de manipulation des automates
    l'alphabet est l'ensemble des caractères alphabétiques minuscules et "E" pour epsilon, 
    et "O" pour l'automate vide
    """
    
    def __init__(self, expr="O"):
        """
        construit un automate élémentaire pour une expression régulière expr 
            réduite à un caractère de l'alphabet, ou automate vide si "O"
        identifiant des états = entier de 0 à n-1 pour automate à n états
        état initial = état 0
        """
        
        # alphabet
        self.alphabet = list("abc")
        # l'expression doit contenir un et un seul caractère de l'alphabet
        if expr not in (self.alphabet + ["O", "E"]):
            raise ValueError("l'expression doit contenir un et un seul\
                           caractère de l'alphabet " + str(self.alphabet))
        # nombre d'états
        if expr == "O":
            # langage vide
            self.n = 1
        elif expr == "E":
            self.n = 1
        else:
            self.n = 2
        # états finals: liste d'états (entiers de 0 à n-1)
        if expr == "O":
            self.final = []
        elif expr == "E":
            self.final = [0]
        else:
            self.final = [1]
        # transitions: dico indicé par (état, caractère) qui donne la liste des états d'arrivée
        self.transition =  {} if (expr in ["O", "E"]) else {(0,expr): [1]}
        # nom de l'automate: obtenu par application des règles de construction
        self.name = "" if expr == "O" else "(" + expr + ")" 
        
    def __str__(self):
        """affichage de l'automate par fonction print"""
        res = "Automate " + self.name + "\n"
        res += "Nombre d'états " + str(self.n) + "\n"
        res += "Etats finals " + str(self.final) + "\n"
        res += "Transitions:\n"
        for k,v in self.transition.items():    
            res += str(k) + ": " + str(v) + "\n"
        res += "*********************************"
        return res
    
    def ajoute_transition(self, q0, a, qlist):
        """ ajoute la liste de transitions (q0, a, q1) pour tout q1 
            dans qlist à l'automate
            qlist est une liste d'états
        """
        if not isinstance(qlist, list):
            raise TypeError("Erreur de type: ajoute_transition requiert une liste à ajouter")
        if (q0, a) in self.transition:
            self.transition[(q0, a)] = self.transition[(q0, a)] + qlist
        else:
            self.transition.update({(q0, a): qlist})
    
    
def concatenation(a1, a2): 
    """Retourne l'automate qui reconnaît la concaténation des 
    langages reconnus par les automates a1 et a2"""
    a2_shifted = decalage(a2, a1.n)
    res = automate()
    res.n = a1.n + a2.n
    res.transition.update(a1.transition)
    res.transition.update(a2_shifted.transition)
    for f in a1.final:
        res.ajoute_transition(f, "E", [a1.n])
    res.final = a2_shifted.final
    res.name = f"({a1.name}.{a2.name})"
    return res

# --- HELPER POUR DECALAGE D'ETATS ---
def decalage(a, offset):
    res = cp.deepcopy(a)
    res.n += 0 
    res.final = [f + offset for f in a.final]
    new_trans = {}
    for (etat, char), cibles in a.transition.items():
        new_trans[(etat + offset, char)] = [c + offset for c in cibles]
    res.transition = new_trans
    return res

def union(a1, a2):
    """Retourne l'automate qui reconnaît l'union des 
    langages reconnus par les automates a1 et a2""" 
    a2_shifted = decalage(a2, a1.n)
    res = automate()
    res.n = a1.n + a2_shifted.n + 2
    start = 0
    final = res.n - 1
    a1_in = decalage(a1, 1)
    a2_in = decalage(a2_shifted, 1)
    res.transition.update(a1_in.transition)
    res.transition.update(a2_in.transition)
    res.ajoute_transition(start, "E", [1, 1 + a1.n])
    for f in a1_in.final:
        res.ajoute_transition(f, "E", [final])
    for f in a2_in.final:
        res.ajoute_transition(f, "E", [final])
    res.final = [final]
    res.name = f"({a1.name}+{a2.name})"
    return res


def etoile(a):
    """Retourne l'automate qui reconnaît l'étoile de Kleene du 
    langage reconnu par l'automate a""" 
    res = automate()
    res.n = a.n + 2
    start = 0
    final = res.n - 1
    a_shifted = decalage(a, 1)
    res.transition.update(a_shifted.transition)
    res.ajoute_transition(start, "E", [1])
    res.ajoute_transition(start, "E", [final])
    for f in a_shifted.final:
        res.ajoute_transition(f, "E", [1])
        res.ajoute_transition(f, "E", [final])
    res.final = [final]
    res.name = f"({a.name})*"
    return res


def acces_epsilon(a):
    """ retourne la liste pour chaque état des états accessibles par epsilon
        transitions pour l'automate a
        res[i] est la liste des états accessible pour l'état i
    """
    # on initialise la liste résultat qui contient au moins l'état i pour chaque état i
    res = [[i] for i in range(a.n)]
    for i in range(a.n):
        candidats = list(range(i)) + list(range(i+1, a.n))
        new = [i]
        while True:
            # liste des epsilon voisins des états ajoutés en dernier:
            voisins_epsilon = []
            for e in new:
                if (e, "E") in a.transition.keys():
                    voisins_epsilon += [j for j in a.transition[(e, "E")]]
            # on calcule la liste des nouveaux états:
            new = list(set(voisins_epsilon) & set(candidats))
            # si la nouvelle liste est vide on arrête:
            if new == []:
                break
            # sinon on retire les nouveaux états ajoutés aux états candidats
            candidats = list(set(candidats) - set(new))
            res[i] += new 
    return res


def supression_epsilon_transitions(a):
    """ retourne l'automate équivalent sans epsilon transitions
    """
    # on copie pour éviter les effets de bord     
    a = cp.deepcopy(a)
    res = automate()
    res.name = a.name
    res.n = a.n
    res.final = a.final
    # pour chaque état on calcule les états auxquels il accède
    # par epsilon transitions.
    acces = acces_epsilon(a)
    # on retire toutes les epsilon transitions
    res.transition = {c: j for c, j in a.transition.items() if c[1] != "E"}
    for i in range(a.n):
        # on ajoute i dans les états finals si accès à un état final:
        if (set(acces[i]) & set(a.final)):
            if i not in res.final:
                res.final.append(i)
        # on ajoute les nouvelles transitions en parcourant toutes les transitions
        for c, v in a.transition.items():
            if c[1] != "E" and c[0] in acces[i]:
                res.ajoute_transition(i, c[1], v)
    return res
        
        
def determinisation(a):
    """ retourne l'automate équivalent déterministe
        la construction garantit que tous les états sont accessibles
        automate d'entrée sans epsilon-transitions
    """        
    res = automate()
    res.name = "Det(" + a.name + ")"
    start_set = frozenset([0])
    subsets = {start_set: 0}
    queue = [start_set]
    res.n = 0
    res.transition = {}
    res.final = []
    
    while queue:
        current_set = queue.pop(0)
        current_id = subsets[current_set]
        res.n += 1
        if not current_set.isdisjoint(a.final):
            res.final.append(current_id)
        for char in a.alphabet:
            target_set = set()
            for state in current_set:
                if (state, char) in a.transition:
                    target_set.update(a.transition[(state, char)])
            if not target_set: continue
            target_froz = frozenset(target_set)
            if target_froz not in subsets:
                subsets[target_froz] = len(subsets)
                queue.append(target_froz)
            res.transition[(current_id, char)] = [subsets[target_froz]]
    return res
    
    
def completion(a):
    """ retourne l'automate a complété
        l'automate en entrée doit être déterministe
    """
    res = cp.deepcopy(a)
    poubelle = res.n
    added_poubelle = False
    for state in range(res.n):
        for char in res.alphabet:
            if (state, char) not in res.transition:
                if not added_poubelle:
                    res.n += 1
                    added_poubelle = True
                res.transition[(state, char)] = [poubelle]
    if added_poubelle:
        for char in res.alphabet:
            res.transition[(poubelle, char)] = [poubelle]
    return res


###################################################
# version corrigée de la fonction de minimisation #
###################################################

def minimisation(a):
    """ retourne l'automate minimum
        a doit être déterministe complet
        algo par raffinement de partition (algo de Moore)
    """
    # on copie pour éviter les effets de bord     
    a = cp.deepcopy(a)
    res = automate()
    res.name = a.name
    
    # Étape 1 : partition initiale = finaux / non finaux
    part = [set(a.final), set(range(a.n)) - set(a.final)]
    # on retire les ensembles vides
    part = [e for e in part if e != set()]  
    
    # Étape 2 : raffinement jusqu’à stabilité
    modif = True
    while modif:
        modif = False
        new_part = []
        for e in part:
            # sous-ensembles à essayer de séparer
            classes = {}
            for q in e:
                # signature = tuple des indices des blocs atteints pour chaque lettre
                signature = []
                for c in a.alphabet:
                    for i, e2 in enumerate(part):
                        if a.transition[(q, c)][0] in e2:
                            signature.append(i)
                # on ajoute l'état q à la clef signature calculée
                classes.setdefault(tuple(signature), set()).add(q)
            if len(classes) > 1:
                # s'il y a >2 signatures différentes on a séparé des états dans e
                modif = True
                new_part.extend(classes.values())
            else:
                new_part.append(e)
        part = new_part
    # on réordonne la partition pour que le premier sous-ensemble soit celui qui contient l'état initial
    for i, e in enumerate(part):
        if 0 in e:
            part[0], part[i] = part[i], part[0]
            break
 
     
    # Étape 3 : on construit le nouvel automate minimal
    mapping = {}
    # on associe à chaque état q le nouvel état i
    # obtenu comme étant l'indice du sous-ensemble de part
    for i, e in enumerate(part):
        for q in e:
            mapping[q] = i

    res.n = len(part)
    res.final = list({mapping[q] for q in a.final if q in mapping})
    for i, e in enumerate(part):
        # on récupère un élément de e:
        representant = next(iter(e))
        for c in a.alphabet:
            q = a.transition[(representant, c)][0]
            res.transition[(i, c)] = [mapping[q]]
    return res
    

def tout_faire(a):
    a1 = supression_epsilon_transitions(a)
    a2 = determinisation(a1)
    a3 = completion(a2)
    a4 = minimisation(a3)
    return a4


def egal(a1, a2):
    """ retourne True si a1 et a2 sont isomorphes
        a1 et a2 doivent être minimaux
    """
    if a1.n != a2.n or len(a1.final) != len(a2.final):
        return False
    def canoniser(aut):
        mapping = {}
        new_id = 0
        queue = [0]
        mapping[0] = 0
        normalized_trans = {}
        normalized_final = set()
        while queue:
            q = queue.pop(0)
            mapped_q = mapping[q]
            for char in sorted(aut.alphabet):
                if (q, char) in aut.transition:
                    target = aut.transition[(q, char)][0]
                    if target not in mapping:
                        new_id += 1
                        mapping[target] = new_id
                        queue.append(target)
                    normalized_trans[(mapped_q, char)] = mapping[target]
            if q in aut.final:
                normalized_final.add(mapped_q)
        return normalized_trans, normalized_final
    t1, f1 = canoniser(a1)
    t2, f2 = canoniser(a2)
    return t1 == t2 and f1 == f2

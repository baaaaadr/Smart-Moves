from typing import Callable
import random
import ast

# Quelques structures de données
Grid = tuple[tuple[int, ...], ...]
State = Grid
Action = tuple[int, int]
Player = int
Score = float
Strategy = Callable[[State, Player], Action] #c'est une fonction qui prends en entrée etat et player, renvoie action

# Quelques constantes
DRAW = 0
EMPTY = 0
X = 1
O = 2

##==========PRELIMINAIRES
def grid_tuple_to_grid_list(grid: Grid) -> list[list[int]]:
    Liste_grid=[]
    for tuple in grid:
        miniListe=[]
        for element in tuple:
            miniListe.append(element)
        Liste_grid.append(miniListe)
    return Liste_grid

def grid_list_to_grid_tuple(grid: list[list[int]]) -> Grid:
    grandtuple_list=[]
    for miniListe in grid:
        grandtuple_list.append(tuple(miniListe))
    return tuple(grandtuple_list)

"""tests
GRID_2: Grid = ((O, 0, X), (X, X, O), (O, X, 0))
print(grid_tuple_to_grid_list(GRID_2))

print(grid_list_to_grid_tuple(grid_tuple_to_grid_list(GRID_2)))
"""


##==========REGLES DE BASES
def legals(grid: State) -> list[Action]:
    possibilites=[]
    numero_ligne = 0
    for ligne in grid:
        numero_colonne = 0
        for colonne in ligne:
            if colonne==0 : #si il y a un 0 dans la case
                possibilites.append(Action([numero_ligne,numero_colonne]))
            numero_colonne+=1
        numero_ligne+=1
    return possibilites

"""tests
GRID_2: Grid = ((O, 0, X), (X, X, O), (O, X, 0))
print(legals(GRID_2))
"""
    #fonction LINE: est ce qu'il y a une ligne complete de ce player sur la grid
def horizontal_line(grid: State, player: Player, numero_ligne: int) -> bool:
    nb_cases_par_ligne= len(grid[0])
    for i in range(nb_cases_par_ligne):
        if grid[numero_ligne][i] != player:
            return False
    return True

def vertical_line(grid: State, player: Player, numero_colonne: int) -> bool:
    nb_cases_par_colonne= len(grid[0])#on suppose qu'on est dans une matrice carrée
    for i in range(nb_cases_par_colonne):
        if grid[i][numero_colonne] != player:
            return False
    return True

def diagonal1_line(grid: State, player: Player) -> bool:
    nb_cases_diagonales= len(grid[0])#on suppose qu'on est dans une matrice carrée
    #diagonal \
    for i in range(nb_cases_diagonales):
        if grid[i][i] != player:
            return False
    return True

def diagonal2_line(grid: State, player: Player) -> bool:
    nb_cases_diagonales= len(grid[0])#on suppose qu'on est dans une matrice carrée
    #diagonal /
    for i in range(nb_cases_diagonales):
        if grid[i][nb_cases_diagonales-i-1] != player:
            return False
    return True

#est-ce qu'il y a une ligne complète d'un même player dans la grille
def line(grid: State, player: Player) -> bool:
    nb_cases_par_ligne= len(grid[0])#on suppose qu'on est dans une matrice carrée
    for i in range(nb_cases_par_ligne):
        if horizontal_line(grid, player,i):
            return True
    for i in range(nb_cases_par_ligne):
        if vertical_line(grid, player, i):
            return True
    if diagonal1_line(grid, player):
        return True
    if diagonal2_line(grid, player):
        return True
    return False

"""tests
GRID_2: Grid = ((O, 0, X), (X, X, O), (X, X, 0))
print(line(GRID_2,O))
"""

#est-ce un état final?
def final(grid: State) -> bool:
    x= line(grid, X)
    y= line(grid, O)
    z=(len(legals(grid))==0) #if there are no legal moves left
    return x or y or z

#retourne le score
def score(grid: State) -> Score:
    #1 si X gagne, -1 si O gagne, 0 sinon
    if line(grid, X):
        return 1
    elif line(grid, O):
        return -1
    else:
        return 0

#affichage pretty de la grid
def pprint(grid: State):
    ligne=0
    for i in grid:
        for j in i:
            ligne+=1
            if j==0:
                print(" . ", end=" ")
            elif j==1:
                print(" X ", end=" ")
            else:
                print(" O ", end=" ")
            if ligne==len(grid[0]):
                print()
                ligne=0
    print()

"""tests
GRID_2: Grid = ((O, 0, X), (X, X, O), (X, X, 0))
pprint((GRID_2))
"""

def play(grid: State, player: Player, action: Action) -> State:
    if grid[action[0]][action[1]] != 0:
        raise ValueError("La position est déjà occupée") #pcq la place est déjà occupé
    
    liste = grid_tuple_to_grid_list(grid)

    liste[action[0]][action[1]] = player
    return grid_list_to_grid_tuple(liste)

"""
GRID_2: Grid = ((O, 0, X), (X, X, O), (X, X, 0))
#pprint((GRID_2))
pprint(play(GRID_2,O,(0,1)))
"""

#=================================================================================
#==========LES STRATEGIES
#joueuer humain
def strategy_brain(grid: State, player: Player) -> Action:
    print("à vous de jouer [format '(x,y)']: ", end="")
    s = input()
    print()
    t = ast.literal_eval(s)

    return t
"""
GRID_2: Grid = ((O, 0, X), (X, X, O), (X, X, 0))
print(strategy_brain(GRID_2, X))
"""

#s'occupe de la séquence du jeu
def tictactoe(strategy_X: Strategy, strategy_O: Strategy) -> Score:
    grid= ((0, 0, 0), (0, 0, 0), (0, 0, 0))

    while len(legals(grid))!=0 and not final(grid):
        #tour de X
        while True:
            try:
                action_X = strategy_X(grid, X)
                grid = play(grid, X, action_X)
                break  # sortir de la boucle si tout se passe bien
            except ValueError as e:
                print(f"Erreur rencontrée : {e}")
        pprint(grid)
        
        #verif
        if len(legals(grid))==0 or final(grid):
            break
        
        #tour de O
        while True:
            try:
                action_O = strategy_O(grid, O)
                grid = play(grid, O, action_O)
                break  # sortir de la boucle si tout se passe bien
            except ValueError as e:
                print(f"Erreur rencontrée : {e}")
        pprint(grid)

    return score(grid)

def strategy_first_legal(grid: State, player: Player) -> Action:
    return legals(grid)[0]

def strategy_random(grid: State, player: Player) -> Action:
    return random.choice(legals(grid))

#print(tictactoe(strategy_random,strategy_first_legal))

#=================================================================================
#JOUEURS INTELLIGENTS

#étant donné un état de jeu renvoie le score optimal de la partie.
def minmax(grid: State, player: Player) -> Score:
    if final(grid):
        return score(grid)
    
    scores = []
    for action in legals(grid):
        new_grid = play(grid, player, action)
        next_player = X if player == O else O
        s = minmax(new_grid, next_player)
        scores.append(s)
    
    return max(scores) if player == X else min(scores)


#étant donné un état de jeu renvoie sous forme de tuple l'action amenant au score optimal de la partie et ce score.
def minmax_action(grid: State, player: Player, depth: int = 0) -> tuple[Score, Action]:
    if final(grid):
        return score(grid), None

    if player == X:
        best_score = float('-inf') #on cherche à maximiser le score
    else: 
        best_score = float('inf') #on cherche à minimiser le score
    best_action = None #variable pour mémoriser l'action qui mène à ce meilleur score

    #on parcourt tous les coups possibles
    for action in legals(grid):
        new_grid = play(grid, player, action)# on simule le coup
        next_player = X if player == O else O
        score_result, _ = minmax_action(new_grid, next_player, depth + 1)
        #^Si l’autre joueur joue parfaitement à partir de cette nouvelle grille, quel score obtiendra-t-on au final ?"
        #à ce niveau de depth, l'action retournée ne nous importe pas

        #choisir la meilleure action:
        if player == X:
            if score_result > best_score: #choisit l’action qui donne le plus grand score_result
                best_score = score_result
                best_action = action
        else:  # player == O
            if score_result < best_score: #choisit l’action qui donne le plus petit score_result
                best_score = score_result
                best_action = action

    return best_score, best_action
"""
GRID_2 = ((O, 0, X), (X, X, O), (O, X, 0))
score_val, best_move = minmax_action(GRID_2, X)
print(f"Score : {score_val}, Meilleure action : {best_move}")
"""

#renvoie l'action optimal
def strategy_minmax(grid: State, player: Player) -> Action:
    _, action = minmax_action(grid, player)
    return action
#a = strategy_minmax(grid, X)

#============== minmax qui avec un état de jeu, renvoie dans un tuple les actions amenant au score optimal de la partie et ce score.
def minmax_actions(
    grid: State, player: Player, depth: int = 0
) -> tuple[Score, list[Action]]:
    if final(grid):
        return score(grid), []

    best_score = None
    best_actions = []

    for action in legals(grid):
        next_grid = play(grid, player, action)
        opponent = X if player == O else O

        # Appel récursif : score de l'adversaire après ce coup
        sub_score, _ = minmax_actions(next_grid, opponent, depth + 1)
        actual_score = -sub_score  # car ce qui est bon pour l'adversaire est mauvais pour nous

        if best_score is None or actual_score > best_score:
            best_score = actual_score
            best_actions = [action]  # on garde cette action car elle est meilleure
        elif actual_score == best_score:
            best_actions.append(action)  # une autre action aussi bonne

    return best_score, best_actions
"""
GRID_2: Grid = ((O, 0, X), (X, X, O), (O, X, 0))
print(minmax_actions(GRID_2, X))
# => peut renvoyer (1, [(0,1), (2,2)]) par exemple
"""

def strategy_minmax_random(grid: State, player: Player) -> Action:
    score, best_actions = minmax_actions(grid, player)
    return random.choice(best_actions)
#^utilise minmax_actions(...) pour obtenir toutes les meilleures actions,
#puis choisit aléatoirement l'une d'entre elles (si plusieurs mènent au même score optimal).
#deterministe= choisit toujours la premiere
"""
GRID_2: Grid = ((O, 0, X), (X, X, O), (O, X, 0))
print(strategy_minmax_random(GRID_2, X))
# Renvoie par exemple : (0, 1) ou (2, 2) de manière aléatoire, si ce sont deux bonnes actions
"""
#==============

#==============ajout d'un cache
#pourquio? Quand l'algorithme explore tous les coups possibles, il peut rencontrer plusieurs fois le même état de grille. En sauvegardant le résultat pour chaque grille rencontrée, on réutilise directement le score optimal sans refaire tous les calculs.
def minmax_action(
    grid: State,
    player: Player,
    depth: int = 0,
    cache: dict[tuple[State, Player], tuple[Score, Action]] = {}
) -> tuple[Score, Action]:

    key = (grid, player)
    if key in cache:
        return cache[key]

    if final(grid):
        result = (score(grid), None)
        cache[key] = result
        return result

    best_score = float("-inf") if player == X else float("inf")
    best_action = None

    for action in legals(grid):
        new_grid = play(grid, player, action)
        opponent = O if player == X else X
        s, _ = minmax_action(new_grid, opponent, depth + 1, cache)
        s = -s  # inverser car score de l’adversaire

        if (
            (player == X and s > best_score)
            or (player == O and s < best_score)
        ):
            best_score = s
            best_action = action

    result = (best_score, best_action)
    cache[key] = result
    return result

def minmax_actions(
    grid: State, player: Player,
    depth: int = 0,
    cache: dict[tuple[State, Player], tuple[Score, list[Action]]] = {}
) -> tuple[Score, list[Action]]:
    
    key = (grid, player)
    if key in cache:
        return cache[key]

    if final(grid):
        result = (score(grid), [])
        cache[key] = result
        return result

    best_score = float("-inf") if player == X else float("inf")
    best_actions: list[Action] = []

    for action in legals(grid):
        new_grid = play(grid, player, action)
        opponent = O if player == X else X
        s, _ = minmax_actions(new_grid, opponent, depth + 1, cache)
        s = -s  # car le score de l'adversaire = - mon score

        if (
            (player == X and s > best_score)
            or (player == O and s < best_score)
        ):
            best_score = s
            best_actions = [action]
        elif s == best_score:
            best_actions.append(action)

    result = (best_score, best_actions)
    cache[key] = result
    return result
"""
def strategy_minmax(grid: State, player: Player) -> Action:
    _, action = minmax_action(grid, player)
    return action
"""

#==============

#==============alpha beta
def minmax_action_alpha_beta(
    grid: State,
    player: Player,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
    depth: int = 0,
    cache: dict[tuple[State, Player], tuple[Score, Action]] = {}
) -> tuple[Score, Action]:

    key = (grid, player)
    if key in cache:
        return cache[key]

    if final(grid):
        result = (score(grid), None)
        cache[key] = result
        return result

    best_action = None
    if player == X:
        best_score = float("-inf")
        for action in legals(grid):
            new_grid = play(grid, player, action)
            s, _ = minmax_action_alpha_beta(new_grid, O, alpha, beta, depth + 1, cache)
            s = -s  # inverser car score adverse
            if s > best_score:
                best_score = s
                best_action = action
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # élagage
    else:  # player == O
        best_score = float("inf")
        for action in legals(grid):
            new_grid = play(grid, player, action)
            s, _ = minmax_action_alpha_beta(new_grid, X, alpha, beta, depth + 1, cache)
            s = -s
            if s < best_score:
                best_score = s
                best_action = action
            beta = min(beta, best_score)
            if beta <= alpha:
                break  # élagage

    result = (best_score, best_action)
    cache[key] = result
    return result


def strategy_minmax_alpha_beta(grid: State, player: Player) -> Action:
    _, action = minmax_action_alpha_beta(grid, player)
    return action

def minmax_actions_alpha_beta(
    grid: State,
    player: Player,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
    depth: int = 0,
    cache: dict[tuple[State, Player], tuple[Score, list[Action]]] = {}
) -> tuple[Score, list[Action]]:

    key = (grid, player)
    if key in cache:
        return cache[key]

    if final(grid):
        result = (score(grid), [])
        cache[key] = result
        return result

    best_actions = []
    if player == X:
        best_score = float("-inf")
        for action in legals(grid):
            new_grid = play(grid, player, action)
            s, _ = minmax_actions_alpha_beta(new_grid, O, alpha, beta, depth + 1, cache)
            s = -s  # car on inverse le joueur

            if s > best_score:
                best_score = s
                best_actions = [action]
            elif s == best_score:
                best_actions.append(action)

            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # élagage alpha-bêta
    else:  # player == O
        best_score = float("inf")
        for action in legals(grid):
            new_grid = play(grid, player, action)
            s, _ = minmax_actions_alpha_beta(new_grid, X, alpha, beta, depth + 1, cache)
            s = -s

            if s < best_score:
                best_score = s
                best_actions = [action]
            elif s == best_score:
                best_actions.append(action)

            beta = min(beta, best_score)
            if beta <= alpha:
                break  # élagage alpha-bêta

    result = (best_score, best_actions)
    cache[key] = result
    return result

def strategy_minmax_random_alpha_beta(grid: State, player: Player) -> Action:
    _, actions = minmax_actions_alpha_beta(grid, player)
    return random.choice(actions)

#==============

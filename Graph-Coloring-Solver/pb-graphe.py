from itertools import combinations

#1.CHAQUE sommet doit avoir au moins une couleur: R ou B ou V
#2.CHAQUE sommet ne peut pas avoir deux couleurs en même temps: 
    #non R ou non B
    #non R ou non V
    #non B ou non V
#3.deux sommets reliés ne doivent pas avoir la même couleur:
    #pour CHAQUE arc(u,v) et CHAQUE couleur c: (sommet S)
        #non u_c ou non v_c


def var(node, color_index):
    return (node - 1) * 3 + color_index + 1

def generate_DIMACS(noeuds,arcs):
    nb_vars = len(noeuds) * 3
    clauses = []

    #1. un noeud = au moins une couleur
    for n in noeuds:
        clauses.append([var(n,0), var(n,1), var(n,2)])
    
    #2. un noeud = une seule couleur
    """
    for n in noeuds:
        for i in range(3):#pour chaque couleur x possible
            for j in range(i+1,3):#les couleurs restantes à associé avec x
                clauses.append([-var(n, i), -var(n, j)])
    """
        #version avec combinaisons:
    for n in noeuds:
        for i, j in combinations(range(3), 2):#combinaisons des nombre de 0 à 2, deux à deux. sans doublons
            clauses.append([-var(n, i), -var(n, j)])

    #3. deux noeuds reliés ne peuvent pas avoir la même couleur
    for (u,v) in arcs:
        for i in range(3):
            clauses.append([-var(u,i), -var(v,i)])

    #ETAPE FINAL: construction de la chaîne dimacs
    dimacs = f"p cnf {nb_vars} {len(clauses)}\n"
    for clause in clauses:
        #on join dans une seule variable
        dimacs += " ".join(map(str, clause)) + " 0\n"
    return dimacs






def decode_dimacs_solution(solution_line, nb_noeuds):
    couleurs = ["Rouge", "Vert", "Bleu"]
    coloration = {}

    # Extraire les entiers de la chaîne (sans le "v" et le dernier 0)
    values = list(map(int, solution_line.strip().split()[1:-1]))

    for val in values:
        if val > 0:
            n = (val - 1) // 3 + 1  # numéro du nœud
            c = (val - 1) % 3       # indice de couleur
            coloration[n] = couleurs[c]

    return coloration


noeuds=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
arcs=[[1,2],[1,5],[1,6],[2,7],[2,3],[3,8],[3,4],[4,9],[4,5],[5,10],[6,8],[6,9],[7,10],[7,9],[8,10]]
nb_noeuds=10
couleurs=["R","V","B"]

#print(generate_DIMACS(noeuds,arcs))

dimacs_line="v -1 2 -3 -4 -5 6 7 -8 -9 -10 11 -12 -13 -14 15 -16 -17 18 -19 20 -21 -22 23 -24 25 -26 -27 28 -29 -30 0"
#print(decode_dimacs_solution(dimacs_line, nb_noeuds))
resultat = decode_dimacs_solution(dimacs_line, nb_noeuds=10)
for n in sorted(resultat.keys()):
    print(f"Noeud {n} : {resultat[n]}")


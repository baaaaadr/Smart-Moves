from typing import List, Dict, Generator

#question 1
def reverse(list):
    reversed_list=[]
    for i in range (len(list)-1,-1,-1):
        reversed_list.append(list[i])
    return reversed_list
def reverse2(list):
    reversed_list=[]
    for x in reversed(list):
        reversed_list.append(x)
    return reversed_list
        

def decomp(n: int, nb_bits: int) -> list[bool]:
    if n<0:
        print("nb negatif invalide")
        return
    if 2**nb_bits<n or nb_bits==0:
        print("nb trop grand pour etre représenté sur ce nb de bits")
        return
    res=[]
    while n>0:
        binaire=bool(n%2)
        res.append(binaire)
        n=n//2
        nb_bits=nb_bits-1
    while nb_bits>0:
        res.append(bool(0)) #ou False
        nb_bits=nb_bits-1
    res=reverse2(res)
    #print(res)
    return res

#decomp(9,4)


#question 2
def interpretation_1(voc: list[str], vals: list[bool]) -> dict[str, bool]:
    if len(voc)!=len(vals):
        print("voc et vals pas la meme longueur, ne peut pas interpreter")
        return
    thisdict={}
    for i in range(len(voc)):
        thisdict[voc[i]]=vals[i]
    #print(thisdict)
    return thisdict

def interpretation(voc: list[str], vals: list[bool]) -> dict[str, bool]:
    thisdict={}
    thisdict=dict(zip(voc,vals))
    #print(thisdict)
    return thisdict

#interpretation_1(["A", "B", "C"],[True, True, False])

#question 3
def gen_interpretations(voc: List[str]) -> Generator[Dict[str, bool], None, None]:
    #on a une liste de n element => il y a 2**n repartitions possibles
    #avec decomp(), on peut avoir tous les chiffres en binaire de 0 à 2**n-1 décomptant ainsi toutes les possibilités
    #on les associes avec interpretation()
    n=len(voc)
    for i in range(2**n):
        yield interpretation(voc,decomp(i,n))

"""
g = gen_interpretations(["A", "B", "C"])
print(next(g))
print(next(g))
print(next(g))

for i in gen_interpretations(["toto", "tutu"]):
    print(i)
"""
#question 4
#The eval() function evaluates the specified expression, if the expression is a legal Python statement, it will be executed.
def valuate(formula: str, interpretation: Dict[str, bool]) -> bool:
    return eval(formula, interpretation)
    #or eval(formula,{}, interpretation)

#print(valuate("(A or B) and not(C)", {"A": True, "B": False, "C": False}))

#question 5
def table_de_verite(formula: str, voc: List[str]): 
    print(f"formule: {formula}")
    for var in voc:
        print(var, end="") #does not skip a line
        print("  ", end="") 
    print("eval")

    for x in gen_interpretations(voc):
        #print(x, end="")
        for var in voc:
            print(f"{int(x[var])}  ", end="") #IMPORTANT AFFICHAGE DICO DU GENERATEUR
         
        print(valuate(formula, x))

table_de_verite("(A or B) and not(C)",["A", "B", "C"])
#0 is false 1 is vrai

#quesstion 6
def formule_valide_2(formula: str, voc: List[str]) -> bool:
    """Renvoie True si la formule est vraie pour toutes les interprétations possibles
       des variables de `voc` (tautologie)."""
    for i in gen_interpretations(voc):
        if valuate(formula, i)==False:
            return False
    return True

def formule_valide(formula: str, voc: List[str]) -> bool:
    return all(valuate(formula, i) for i in gen_interpretations(voc))
    
def formule_contradictoire(formula: str, voc: List[str]) -> bool:
    return all(not valuate(formula, i) for i in gen_interpretations(voc))

def formule_contingente(formula: str, voc: List[str]) -> bool:
    a_vrai = False
    a_faux = False
    for i in gen_interpretations(voc):
        result = valuate(formula, i)
        if result:
            a_vrai = True
        else:
            a_faux = True
        if a_vrai and a_faux:
            return True
    return False

def is_cons(f1: str, f2: str, voc: List[str]) -> bool:
    #check si à chaque fois que f1 true alors f2 is also true
    #ou comme ici: si on a une fois f1 true et f2 false alors FALSE
    for inter in gen_interpretations:
        if valuate(f1, inter) and not valuate(f2, inter):
            return False
    return True
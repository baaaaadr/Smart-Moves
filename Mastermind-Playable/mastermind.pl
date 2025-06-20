%question 1.1
nBienPlace([], [], 0).
nBienPlace([T|Code1], [T|Code2], BP) :- 
    nBienPlace(Code1, Code2, BPRestant),
    BP is BPRestant+1.
nBienPlace([T1|Code1], [T2|Code2], BP) :- 
    T1 \= T2,
    nBienPlace(Code1, Code2, BP).


%==============================question 1.2
    %pour une liste L donne sa longueur N
longueur([], 0).
longueur([_|L], N):-
    longueur(L,NRestant),
    N is NRestant+1.
gagne(Code1, Code2) :- 
    longueur(Code1,N),
    longueur(Code2,N),
    nBienPlace(Code1,Code2,N).


%==============================question 2
    %element E is in L
%element([], _).
element(E, [E|_]).
element(E, [T|L]) :-
    E \= T,
    element(E,L).

    %L2 is L1 sans la premiere occurence de E
enleve(E,[E|R],R). 
enleve(E, [H|L1], [H|L2]):- %on ajoute le H devant L2 la7atta ylaz2o fi bl output
    E \= H,
    enleve(E,L1,L2).

%PS: interdt de mettre predicat = predicat, c est pas des fonctions c des booleen ett
enleveBP([],[], [],[]).
enleveBP([T|Code1], [T|Code2], Code1Bis, Code2Bis):-
    enleveBP(Code1, Code2, Code1Bis, Code2Bis).
enleveBP([T1|Code1], [T2|Code2], [T1|Code1Bis], [T2|Code2Bis]):-
    T1 \= T2,
    enleveBP(Code1,Code2, Code1Bis, Code2Bis).


%==============================question2.4
%!!!!!!!!!!!!!!!!!!!!!!!!!!!!
nMalPlacesAux([], _, 0). %!!!!! underscore not [], sinon it would only work when tous les elements sont communs dans les deux listes
nMalPlacesAux([T|Code1], Code2, MP):-
    element(T, Code2),
    enleve(T,Code2, NewCode2),
    nMalPlacesAux(Code1, NewCode2, MPRestant),
    MP is MPRestant+1.
%on veut savoir, pour les elements commun dans les deux codes, cb d entre eux il y en a (sont MP par défaut, cause here that is what we suppose)
nMalPlacesAux([T|Code1], Code2, MP):-
    \+ element(T, Code2),
    nMalPlacesAux(Code1, Code2, MP).
%basically, addesh fi mal placé? yaane kam number mawjoud b une ou des posiitons qui sont fausses

nMalPlaces(Code1, Code2, MP):-
    enleveBP(Code1, Code2, Code1Bis, Code2Bis),
    nMalPlacesAux(Code1Bis, Code2Bis, MP).

%==============================question3
%produit random code de taille N, et de M couleurs
codeur(M,N,Code):-
    codeur_aux(M,N,[],Code). % on utilise un accumulateur, appel initial avec Acc=liste vide

codeur_aux(_,0,Acc,Code):-	 % Quand N = 0, on retourne la liste construite en unifiant Code avec Acc
	Code=Acc.

codeur_aux(M, N, Acc, Code):-
    %N>0,
    M1 is M+1,
    random(1, M1, Number),
    N1 is N-1,
    codeur_aux(M, N1, [Number|Acc], Code). % On ajoute Number à Acc

codeur2(_,0,[]).
codeur2(NbCouleurs, Taille, [Number|Code]):-
    NbCouleurs2 is NbCouleurs+1,
    random(1,NbCouleurs2, Number),
    Taille2 is Taille-1,
    codeur2(NbCouleurs, Taille2, Code).

codeur3(_, 0, []) :- !.
codeur3(NbCouleurs, Taille, [New|Code]) :-
    Max is NbCouleurs + 1,
    random(1, Max, New),
    Taille2 is Taille - 1,
    codeur(NbCouleurs, Taille2, Code).

%==============================question4
jouons(NbCouleurs, Taille, Max) :-
    codeur(NbCouleurs, Taille, CodeATrouver),
    play(NbCouleurs, Max, [], [], CodeATrouver).

play(_, 0, _, _, _) :-
    print('Perdu !'), nl, !.

play(NbCouleurs, EssaisRestants, Propositions, Resultats, CodeATrouver) :-
    format('Il reste ~d coup(s).~n', [EssaisRestants]),
    write('Donner un code : '),
    read(CodeCourant),

    nBienPlace(CodeCourant, CodeATrouver, BP),
    nMalPlaces(CodeCourant, CodeATrouver, MP),

    format('BP: ~d/MP: ~d~n', [BP, MP]),

    (   gagne(CodeCourant, CodeATrouver)
    ->  print('Gagné !!!'), nl
    ;   EssaisRestants1 is EssaisRestants - 1,
        play(NbCouleurs, EssaisRestants1, [CodeCourant|Propositions], [(MP, BP)|Resultats], CodeATrouver)
    ).
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
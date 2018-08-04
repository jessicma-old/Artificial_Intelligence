male(phil).
male(chas).
male(harry).
male(bob).

female(liz).
female(jo).

parent(harry,bob).

parent(phil,chas).
parent(liz, chas).
parent(phil,jo).
parent(liz,jo).
parent(chas,harry).

offspring(C,P):- parent(P,C).

mother(M,C):- female(M), parent(M,C).
father(F,C):- male(F), parent(F,C).

grandmother(GM,C):- mother(GM,P), parent(P,C).

sibling(X,Y):- mother(M,X), mother(M,Y), father(F,X), father(F,Y).

brother(B,X):- sibling(B,X), male(B).
sister(S,X):- sibling(S,X), female(S).

son(S,P):- male(S), parent(P,S).
daughter(D,P):- female(D), parent(P,D).

ancestor(A,X):- parent(A,X).
ancestor(A,X):- parent(A,Z), ancestor(Z,X).




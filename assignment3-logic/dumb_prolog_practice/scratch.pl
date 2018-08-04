
weeknight(monday).
weeknight(tuesday).
%weeknight(wednesday).
%weeknight(thursday).
%weeknight(friday).

follows(monday, tuesday).
%follows(tuesday, wednesday).
%follows(wednesday, thursday).
%follows(thursday, friday).

later(X,Y) :- follows(X,Y).
later(X,Y) :- follows(X,A), later(A,Y).

fruit(apple).
fruit(banana).
%fruit(pear).
%fruit(peach).
%fruit(pineapple).

snack(D, F) :- weeknight(D), fruit(F).

alldiff([H | T]) :- member(H, T), !, fail.
alldiff([_ | T]) :- alldiff(T).
alldiff([_]).

test([Da, Db, Dpi, Dpch, Dpr]) :-
snack(Da, apple), snack(Db, banana), snack(Dpi, pineapple), snack(Dpch, peach), snack(Dpr, pear),
alldiff([Da, Db, Dpi, Dpch, Dpr]), 
later(Dpi, Da),
later(Db, Dpr).
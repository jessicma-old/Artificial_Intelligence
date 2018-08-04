digit(Item):- member(Item,[0,1,2,3,4,5,6,7,8,9]).

alldigit([H | T]) :- digit(H), alldigit(T).
alldigit([]).

alldiff([H | T]) :- member(H, T), !, fail.
alldiff([_ | T]) :- alldiff(T).
alldiff([_]).


valid([H | T]) :- valid(T), alldigit([H | T]), alldiff([H | T]).
valid([X]) :- digit(X).


first(X) :- not(X=0).

% [a,b,c] -> a*100 + b*10 + c
word2num([X],S) :- S is X.
word2num([H | T], X) :- length(T,L), word2num(T,S), X is S+H*10**L.


twoplustwo([T,W,O,F,U,R]) :- valid([T,W,O,F,U,R]), first(T),first(F),
word2num([T,W,O],Two), word2num([F,O,U,R],Four), Four is Two+Two, 
write([T,W,O,F,U,R]).

sendmoney([S,E,N,D,T,H,M,O,Y]) :- valid([S,E,N,D,T,H,M,O,Y]), first(S), first(T), first(M),
word2num([S,E,N,D],Send), word2num([T,H,E],The), word2num([M,O,N,E,Y], Money),
Money is Send+The, write([S,E,N,D,T,H,M,O,Y]).




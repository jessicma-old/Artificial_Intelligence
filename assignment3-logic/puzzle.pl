% --------------------
weeknight(monday).
weeknight(tuesday).
weeknight(wednesday).
weeknight(thursday).
weeknight(friday).

follows(monday, tuesday).
follows(tuesday, wednesday).
follows(wednesday, thursday).
follows(thursday, friday).

% Y is any day later than X
later(X,Y) :- follows(X,Y).
later(X,Y) :- follows(X,A), later(A,Y).

%earlier(X,Y) :- later(Y,X).

% ---------------------
fruit(apple).
fruit(banana).
fruit(pear).
fruit(peach).
fruit(pineapple).

nuts(almonds).
nuts(brazil_nuts).
nuts(cashews).
nuts(pecans).
nuts(walnuts).

allnuts([H | T]) :- nuts(H), allnuts(T).
allnuts([]).

allfruit([H | T]) :- fruit(H), allfruit(T).
allfruit([]).

allweeknight([H | T]) :- weeknight(H), allweeknight(T).
allweeknight([]).

alldiff([H | T]) :- member(H, T), !, fail.
alldiff([_ | T]) :- alldiff(T).
alldiff([_]).

validFruit([H | T]) :- validFruit(T), allfruit([H | T]), alldiff([H | T]).
validFruit([X]) :- fruit(X).

validNuts([H | T]) :- validNuts(T), allnuts([H | T]), alldiff([H | T]).
validNuts([X]) :- nuts(X).

validWeeknight([H | T]) :- validWeeknight(T), allweeknight([H | T]), alldiff([H | T]).
validWeeknight([X]) :- weeknight(X).

% ---------------------
snack(D, S) :- weeknight(D),(fruit(S); nuts(S)).


answer([Dapl, Dban, Dpch, Dpr, Dpin], [Dalm, Dbrz, Dcas, Dpec, Dwal]):- 

	snack(Dapl, apple), snack(Dban, banana), snack(Dpch, peach), 
	snack(Dpr, pear), snack(Dpin, pineapple),

	snack(Dalm, almonds), snack(Dbrz, brazil_nuts), snack(Dcas, cashews),
	snack(Dpec, pecans), snack(Dwal, walnuts),

	later(Dpin, Dapl),
	later(Dalm, Dban),
	later(Dbrz, Dban),
	later(Dban, Dpr),
	later(Dcas, Dban), 
	later(Dcas, Dpch), 
	later(Dbrz, Dcas),
	\+follows(Dalm, Dpec),
	validWeeknight([Dapl, Dban, Dpch, Dpr, Dpin]),
	validWeeknight([Dalm, Dbrz, Dcas, Dpec, Dwal]),

	write([Dapl, Dban, Dpch, Dpr, Dpin]),
	write([Dalm, Dbrz, Dcas, Dpec, Dwal]).




















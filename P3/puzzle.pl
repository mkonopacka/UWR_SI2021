:- use_module(library(clpfd)).

solve(Vars) :- 
    Vars = [S,E,N,D,M,O,R,Y],
    Vars ins 0..9,
    all_different(Vars),
        S*1000 + E*100 + N*10 + D + 
        M*1000 + O*100 + R*10 + E #=
    M*10000 + O*1000 + N*100 + E*10 + Y,
    M #\= O, S #\= O.

    labeling([ff], S,E,N,D,M,O,R,Y).

:- solve(Vars), write(Vars), nl.

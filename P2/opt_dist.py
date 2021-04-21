from typing import * 

def opt_dist(seq: list, parts: list) -> int:
    ''' Dla listy zer i jedynek i listy dlugosci kolejnych blokow zwraca minimalna liczbe operacji zamiany bitu 
        Pomysł: sprawdzić wszystkie możliwe podziały na bloki i porównać ich sumaryczne wyniki '''

    return 2

def where_ones(parts: list, start: int, end: int) -> List[list]:
    ''' Zwraca liste list mozliwych indeksow jedynek w ciagu, gdzie `parts` to dlugosci kolejnych, oddzielonych od siebie blokow jedynek 
        `start`, `end`: numery pierwszego i ostatniego indeksu do wykorzystania
        `results`: lista indeksow do ktorej bedziemy dopisywac jakies nowe rekurencyjnie '''
    if end - start + 1 < sum(parts) + len(parts) - 1: 
        raise ValueError('Sumaryczna dlugosc czesci nie moze przekraczac dlugosci listy z')

    pass

def test_opt_dist(seq, parts, correct):
    result = opt_dist(seq, parts) 
    assert result == correct, f"Should be {correct} instead of {result}"

if __name__ == "__main__":
    tests = [
        ([1,0,1,1,0,1,1,0,0,1], [2,2,2], 2),
        ([1,1,1,1,1,1,1,1,1,1], [5,3], 2),
        ([0,1,0,1,1,0,0,1,1,0], [3,4], 4),
        ([0,0,1,0,1,1,0,1,0,1], [4,2], 3),
        ([0,0,0,0,0,0,0,0,0,0], [1,1,1], 3)
    ]

    # for seq, parts, correct in tests:
    #     test_opt_dist(seq, parts, correct)

    test = tests[3][0]
    parts = tests[3][1]
    print(test)
    print(parts)
    where_ones(parts, 0, len(test)-1)

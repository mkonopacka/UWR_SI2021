from typing import * 

def opt_dist(seq: list, parts: list) -> int:
    ''' Dla listy zer i jedynek i listy dlugosci kolejnych blokow zwraca minimalna liczbe operacji zamiany bitu 
        Pomysł: sprawdzić wszystkie możliwe podziały na bloki i porównać ich sumaryczne wyniki '''

    return 2

def possible_ones(n: int, parts: list) -> List[list]:
    ''' Zwraca listę możliwych do ustawienia ciągów długości `n` z długościami bloków podanymi w `parts`'''
    p = len(parts)
    if (sum(parts) + p - 1 > n):
        raise ValueError('Sumaryczna długość bloków z przerwami przekracza długość ciągu')
    
    # długość pierwszej części się przyda
    l = parts[0]

    # jeśli został już tylko jeden blok
    if p == 1:
        # end = start + l - 1 < n => start < n + 1 - l
        return [[0]*start + [1]*l + [0]*(n-l-start) for start in range(n + 1 - l)]
    
    else:
        # dla każdego możliwego początku dołączyć wszystkie możliwe końce
        # obl. max. indeks końca pierwszego ciągu; musi zostać r_min miejsc na resztę ciągu (przed każdym z bloków wolne miejsce)
        r_min = sum(parts[1:]) + len(parts[1:])
        max = n - r_min
        heads = [[0]* x + [1]*l for x in range(0,max - l + 1)]
        merged = []
        for head in heads:
            tails = possible_ones(n - len(head) - 1, parts[1:])
            # print(f'Tails for head {head}: {tails}')
            for tail in tails:
                merged.append(head + [0] + tail)
        return merged


def test_opt_dist(seq, parts, correct):
    result = opt_dist(seq, parts) 
    assert result == correct, f"Should be {correct} instead of {result}"

if __name__ == "__main__":
    print(possible_ones(100, [2,2,2]))
    tests = [
        ([1,0,1,1,0,1,1,0,0,1], [2,2,2], 2),
        ([1,1,1,1,1,1,1,1,1,1], [5,3], 2),
        ([0,1,0,1,1,0,0,1,1,0], [3,4], 4),
        ([0,0,1,0,1,1,0,1,0,1], [4,2], 3),
        ([0,0,0,0,0,0,0,0,0,0], [1,1,1], 3)
    ]

    # for seq, parts, correct in tests:
    #     test_opt_dist(seq, parts, correct)

    # test = tests[3][0]
    # parts = tests[3][1]
    # print(test)
    # print(parts)


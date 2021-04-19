# 2/2 ZALICZONE
''' Obrazki logiczne P1 (uproszczone)
    Wejście: lista zer i jedynek i D długość bloku np. 10000010 5
    Wyjście: minimalna liczba operacji zamiany bitu która da blok jedynek o długości D '''

def opt_dist(seq: list, D: int) -> int:
    if type(seq) != list: 
        seq = list(seq)
    seq += [0]
    min_moves = 1000000000
    start, end = 0, D
    subseq_sum = sum(seq[:end])
    all_sum = subseq_sum + sum(seq[end:])
    while end < len(seq):
        subseq_difference = abs(D-subseq_sum)
        remaining_difference = all_sum - subseq_sum
        min_moves = min(min_moves, subseq_difference + remaining_difference)
        subseq_sum = subseq_sum + seq[end] - seq[start]
        start += 1
        end += 1
    return min_moves

if __name__ == '__main__':
    inputs = []
    with open('zad4_input.txt', "r") as f1:
        for line in f1.read().splitlines():
            inputs.append([p for p in line])
    
    with open('zad4_output.txt', 'w') as f2:
        for input in inputs:
            sequence = list(map(int, input[:-2]))
            D = int(input[-1])
            result = opt_dist(sequence, D)
            f2.write(str(result) + '\n')
    

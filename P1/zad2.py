# ZALICZONE
# AI 3/P1 (słowa) (Zmieniłam kod sprawdzaczki)
with open('polish_words.txt') as f1:
    words = set(f1.read().splitlines())

with open('zad2_input.txt') as f2:
    lines = f2.read().splitlines()

def best_split(line):
    # Tablica na max. wynik do danego miejsca (Indeksy liter są od 1 do n)
    max_scores = [-1]*(len(line)+1)
    max_scores[0] = 0
    # Tablica na indeksy spacji postawionych dla najlepszego wyniku (po którym znaku)
    last_space = [-1]*(len(line)+1)
    # Brzegi subwyrazu WŁĄCZNIE, tzn. right = left to jedna litera na miejscu left (numerowane od 1)
    for right in range(1, len(line)+1):
        for left in range(1, right+1):
            sub = line[left-1:right]
            # jeśli istnieje takie słowo, a poprzednią część da się podzielić:
            if sub in words and max_scores[left-1] != -1:
                sub_score = len(sub)**2 + max_scores[left-1] # wynik nowego słowa + max. z podziałów do tego miejsca
                if sub_score > max_scores[right]: 
                    max_scores[right] = sub_score
                    last_space[right] = left # przed którą była spacja z lewej
    
    # Wstawianie spacji
    # Sprawdzam przed którym indeksem ma być spacja
    i = last_space[-1]
    while i != 1:
        # Wstawiam tam spację
        line = line[: i-1]+ ' ' + line[i-1:]
        # Przesuwam się do końca poprzedniego słowa
        i = last_space[i-1]
        # Powtarzam, aż dojdzie do pierwszej litery
    
    return(line)

with open('zad2_output.txt', 'w') as f3:
    for line in lines:
        f3.write(best_split(line)+'\n')
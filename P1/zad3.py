# ZALICZONE
# (SI 2021) Rozwiązania zadania o pokerze z listy 1 na pracownię i listy 1 na ćwiczenia 
import numpy as np

suits = ['C', 'D', 'H', 'S']
deck_F = [{'rank': rank, 'suit':suit} for rank in range(11,15) for suit in suits] 
deck_B = [{'rank': rank, 'suit': suit} for rank in range(2,11) for suit in suits]

def value(hand):
    """ Zwraca liczbową reprezentację wykrytego układu dla danej ręki. (Poker królewski nie wymaga implementacji w tym zadaniu)
    poker - 8 
    kareta - 7
    full - 6
    kolor - 5
    strit - 4
    trójka - 3
    dwie pary - 2
    para - 1
    nic - 0
    """
    # sortowanie wg. ranków i wydobycie ich oraz kolorów
    hand = sorted(hand, key = lambda card: card['rank'])
    ranks = [card['rank'] for card in hand]
    suits = [card['suit'] for card in hand]
    
    # czy mamy schodki, czy karty są w kolorze?
    straight = all([ranks[i]+1 == ranks[i+1] for i in range(4)])
    flush = all([suits[0] == suits[i] for i in range(1, 5)])

    # zliczanie ilości kart w tym samym kolorze w optymalny sposób
    four = max(ranks.count(ranks[0]), ranks.count(ranks[1]))
    three = max(four, ranks.count(ranks[2]))
    two = max(three, ranks.count(ranks[3]))
    
    # zamiana na wartości logiczne
    four = four >= 4
    three = three >= 3
    two = two >= 2
    
    # ile różnych ranków mamy?
    diff_ranks = len(set(ranks))

    # obliczanie wartości
    if straight and flush: return 8          # poker
    if four: return 7                        # kareta
    if three and diff_ranks == 2: return 6   # full
    if flush and not straight: return 5      # kolor
    if straight and not flush: return 4      # strit   
    if three and diff_ranks == 3: return 3   # trójka
    if two and diff_ranks == 3: return 2     # dwie pary
    if two and diff_ranks == 4: return 1     # para
    else: return 0

def zadanie_pracownia(deck_B, deck_F, games = 10000):
    ''' Symuluje [games] gier i wyświetla komunikat o odsetku gier wygranych przez gracza z talią B z graczem z talią F.'''
    B_wins = 0
    for _ in range(games):
        hand_F = np.random.choice(deck_F, 5, replace = False)
        hand_B = np.random.choice(deck_B, 5, replace = False)
        if value(hand_B) > value(hand_F): B_wins += 1

    print(f'[PR] Talia B wygrywa z talią F {B_wins} na {games} możliwych rozdań, co daje mu wynik {B_wins/games:.2%}')

def get_all_hands(deck):
    ''' Generuje wszystkie możliwe karty w danej talii. (Na potrzeby zliczania liczby możliwych rąk)'''
    l = len(deck)
    for a in range(0, l):
        for b in range(a+1, l):
            for c in range(b+1, l):
                for d in range(c+1, l):
                    for e in range(d+1, l):
                        yield [deck[a], deck[b], deck[c], deck[d], deck[e]]

def get_counts(deck):
    ''' Funkcja zliczająca wystąpienia wszystkich układów od najniższego w danej talii (na potrzeby zadania z Ćwiczeń 1)'''
    counts = [0]*9
    for hand in get_all_hands(deck): counts[value(hand)] += 1
    return counts

def zadanie_cwiczenia(deck_B, deck_F): 
    ''' Wylicza wystąpienia rąk w obu taliach, liczbę wszystkich możliwych kombinacji rąk obu graczy i odpowiedni iloraz.
        Zamiast całej zdefiniowanej u góry talii można jako argument podać jakąś inną, np. jej podzbiór, gdy Blotkarz cośtam wywalił.'''
    counts_B = get_counts(deck_B)
    counts_F = get_counts(deck_F)
    
    # zliczamy wszystkie sytuacje, gdy wygrywa Blotkarz, czyli jego układ jest większy
    B_wins = 0
    for i, count in enumerate(counts_B):
        # dodaj ilość wystąpień danego układu Blotkarza pomnożoną razy sumę gorszych układów Figuranta
        B_wins += sum(counts_F[:i])*count 
    
    # ile w ogóle mogą utworzyć różnych układów?
    all_B = sum(counts_B)
    all_F = sum(counts_F)
    all = all_B * all_F

    print(f'[CW] Talia B wygrywa z talią F {B_wins} na {all} możliwych rozdań, co daje mu wynik {B_wins/all:.2%}')

# zadanie_cwiczenia(deck_B, deck_F) # 8.45%
zadanie_pracownia(deck_B, deck_F)

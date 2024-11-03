import random

# Valorile bomboanelor
ELEMENT_GOL = 0
B_ROSIE = 1
B_GALBENA = 2
B_VERDE = 3
B_ALBASTRA = 4

# Scoruri pentru fiecare tip de formatiune
SCORURI = {
    'linie_3': 5,
    'linie_4': 10,
    'linie_5': 50,
    'L': 20,
    'T': 30
}

# Setarea dimensiunii matricii și a obiectivului punctajului
DIMENSIUNE = 11
OBIECTIV = 10000
JOCURI_TOTAL = 100

# Funcția pentru generarea unei matrici noi
def genereaza_board():
    return [[random.choice([B_ROSIE, B_GALBENA, B_VERDE, B_ALBASTRA]) for _ in range(DIMENSIUNE)] for _ in range(DIMENSIUNE)]

# Funcția pentru afișarea matricii
def afiseaza_board(board):
    for linie in board:
        print(" ".join(str(x) for x in linie))
    print()

# Funcția pentru identificarea formațiunilor în ordinea optima
def identifica_formatiuni(board):
    formatiuni = []

    # 1. Identificare linii de 5
    for i in range(DIMENSIUNE):
        for j in range(DIMENSIUNE - 4):
            if len(set(board[i][j:j+5])) == 1:
                formatiuni.append(('linie_5', [(i, k) for k in range(j, j+5)]))
    for j in range(DIMENSIUNE):
        for i in range(DIMENSIUNE - 4):
            if len({board[x][j] for x in range(i, i+5)}) == 1:
                formatiuni.append(('linie_5', [(x, j) for x in range(i, i+5)]))

    # 2. Identificare formațiuni T
    for i in range(1, DIMENSIUNE - 1):
        for j in range(DIMENSIUNE - 2):
            if (board[i][j] == board[i][j+1] == board[i][j+2] ==
                board[i-1][j+1] == board[i+1][j+1]):
                formatiuni.append(('T', [(i, j), (i, j+1), (i, j+2), (i-1, j+1), (i+1, j+1)]))

    # 3. Identificare formațiuni L
    for i in range(DIMENSIUNE - 2):
        for j in range(DIMENSIUNE - 2):
            if (board[i][j] == board[i+1][j] == board[i+2][j] ==
                board[i+2][j+1] == board[i+2][j+2]):
                formatiuni.append(('L', [(i, j), (i+1, j), (i+2, j), (i+2, j+1), (i+2, j+2)]))

    # 4. Identificare linii de 4
    for i in range(DIMENSIUNE):
        for j in range(DIMENSIUNE - 3):
            if len(set(board[i][j:j+4])) == 1:
                formatiuni.append(('linie_4', [(i, k) for k in range(j, j+4)]))
    for j in range(DIMENSIUNE):
        for i in range(DIMENSIUNE - 3):
            if len({board[x][j] for x in range(i, i+4)}) == 1:
                formatiuni.append(('linie_4', [(x, j) for x in range(i, i+4)]))

    # 5. Identificare linii de 3
    for i in range(DIMENSIUNE):
        for j in range(DIMENSIUNE - 2):
            if len(set(board[i][j:j+3])) == 1:
                formatiuni.append(('linie_3', [(i, k) for k in range(j, j+3)]))
    for j in range(DIMENSIUNE):
        for i in range(DIMENSIUNE - 2):
            if len({board[x][j] for x in range(i, i+3)}) == 1:
                formatiuni.append(('linie_3', [(x, j) for x in range(i, i+3)]))

    return formatiuni

# Funcția pentru a elimina și puncta formațiunile găsite
def elimina_formatiuni(board, formatiuni):
    scor = 0
    for tip, celule in formatiuni:
        for (i, j) in celule:
            board[i][j] = ELEMENT_GOL
        scor += SCORURI[tip]
    return scor

# Funcția pentru a coborî bomboanele după eliminare
def coboara_bomboane(board):
    for col in range(DIMENSIUNE):
        stack = [board[row][col] for row in range(DIMENSIUNE) if board[row][col] != ELEMENT_GOL]
        for row in range(DIMENSIUNE - len(stack)):
            board[row][col] = ELEMENT_GOL
        for row in range(DIMENSIUNE - len(stack), DIMENSIUNE):
            board[row][col] = stack[row - (DIMENSIUNE - len(stack))]

# Funcția principală de joc candycrush
def joaca_candy_crush():
    scor_total = 0
    interschimbari = 0
    board = genereaza_board()
    while scor_total < OBIECTIV:
        afiseaza_board(board)
        formatiuni = identifica_formatiuni(board)

        # Dacă nu sunt formațiuni, încheie jocul
        if not formatiuni:
            print("Nu mai sunt formațiuni valabile! Jocul s-a terminat.")
            break

        # Elimină formațiunile și calculează scorul adăugat în această rundă
        scor_curent = elimina_formatiuni(board, formatiuni)

        # Adăugare la scorul total fără a depăși obiectivul
        if scor_total + scor_curent >= OBIECTIV:
            scor_curent = OBIECTIV - scor_total  # Adaugă doar cât e necesar pentru a ajunge la obiectiv
            scor_total = OBIECTIV  # Setează scorul total exact la obiectiv
            print(f"Obiectivul de {OBIECTIV} puncte a fost atins!")
            break
        else:
            scor_total += scor_curent

        interschimbari += 1
        print(f"Scor curent: {scor_total}, după {interschimbari} interschimbari ")

        # Coborârea bomboanelor și reumplerea elementelor
        coboara_bomboane(board)

    return scor_total, interschimbari

# Simularea a 100 de jocuri și calculul scorului mediu
total_scor = 0
total_interschimbari = 0
for joc in range(JOCURI_TOTAL):
    scor, interschimbari = joaca_candy_crush()
    total_scor += scor
    total_interschimbari += interschimbari
    print(f"Jocul {joc + 1}: Scor final {scor} puncte în {interschimbari} interschimbari. ")

print(f"\nScorul mediu după {JOCURI_TOTAL} jocuri este {total_scor / JOCURI_TOTAL}")
print(f"Numărul mediu de interschimbari este {total_interschimbari / JOCURI_TOTAL}")

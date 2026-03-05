from poker import resolve_game

board = "7c 7d 7h 2s 3d"
players = {
    "Alice": "As Ks",
    "Bob": "Qs Js"
}

winners = resolve_game(board, players)

print("--- RÉSULTAT DE LA PARTIE ---")
for winner in winners:
    print(f"Gagnant : {winner['name']}")
    print(f"Main : {winner['hand']}")
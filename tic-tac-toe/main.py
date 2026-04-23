import random


class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol


class Board:
    def __init__(self):
        self.board = [" " for _ in range(9)]

    def show(self):
        print()
        for i in range(3):
            print(
                self.board[i * 3] + " | " +
                self.board[i * 3 + 1] + " | " +
                self.board[i * 3 + 2]
            )
            if i < 2:
                print("--+---+--")
        print()

    def make_move(self, position, symbol):
        if self.board[position] == " ":
            self.board[position] = symbol
            return True
        return False

    def is_full(self):
        return " " not in self.board

    def check_winner(self, symbol):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for combo in win_combinations:
            if all(self.board[i] == symbol for i in combo):
                return True

        return False


class Game:
    def __init__(self):
        self.board = Board()
        self.players = []

    def create_players(self):
        name1 = input("Имя игрока 1 (X): ")
        name2 = input("Имя игрока 2 (O): ")

        self.players.append(Player(name1, "X"))
        self.players.append(Player(name2, "O"))

    def play(self):
        current = 0

        while True:
            self.board.show()
            player = self.players[current]

            try:
                move = int(input(f"{player.name} ({player.symbol}) ход (0-8): "))
            except ValueError:
                print("Введите число")
                continue

            if move < 0 or move > 8:
                print("Неверная позиция")
                continue

            if not self.board.make_move(move, player.symbol):
                print("Ячейка занята")
                continue

            if self.board.check_winner(player.symbol):
                self.board.show()
                print(f"Победил {player.name}")
                break

            if self.board.is_full():
                self.board.show()
                print("🤝 Ничья")
                break

            current = 1 - current


def main():
    game = Game()
    game.create_players()
    game.play()


if __name__ == "__main__":
    main()
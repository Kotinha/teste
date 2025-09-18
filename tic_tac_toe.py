"""Simple console Tic Tac Toe game for two players.

Run the script and follow the on-screen prompts to play.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class GameState:
    """Represents the state of a Tic Tac Toe game."""

    board: List[List[str]]
    current_player: str = "X"

    def switch_player(self) -> None:
        self.current_player = "O" if self.current_player == "X" else "X"

    def make_move(self, row: int, col: int) -> bool:
        """Attempt to place the current player's mark on the board."""
        if self.board[row][col] != " ":
            return False
        self.board[row][col] = self.current_player
        return True

    def winner(self) -> Optional[str]:
        """Return the winner symbol if the game has been won, otherwise None."""
        lines = self.board + list(map(list, zip(*self.board)))  # rows + columns
        lines.append([self.board[i][i] for i in range(3)])
        lines.append([self.board[i][2 - i] for i in range(3)])

        for line in lines:
            if line[0] != " " and all(cell == line[0] for cell in line):
                return line[0]
        return None

    def is_draw(self) -> bool:
        return all(cell != " " for row in self.board for cell in row) and self.winner() is None


class TicTacToe:
    def __init__(self) -> None:
        board = [[" " for _ in range(3)] for _ in range(3)]
        self.state = GameState(board)

    def display_board(self) -> None:
        print("\n  1   2   3")
        for idx, row in enumerate(self.state.board, 1):
            print(f"{idx} " + " | ".join(row))
            if idx < 3:
                print("  ---+---+---")
        print()

    def parse_move(self, raw: str) -> Optional[Tuple[int, int]]:
        try:
            row_str, col_str = raw.strip().split()
            row = int(row_str) - 1
            col = int(col_str) - 1
        except ValueError:
            return None

        if 0 <= row <= 2 and 0 <= col <= 2:
            return row, col
        return None

    def play(self) -> None:
        print("Bem-vindo ao Jogo da Velha!")
        while True:
            self.display_board()
            move = self.get_player_move()
            if move is None:
                continue

            row, col = move
            if not self.state.make_move(row, col):
                print("Posição já ocupada. Tente novamente.")
                continue

            winner = self.state.winner()
            if winner:
                self.display_board()
                print(f"Parabéns! Jogador {winner} venceu!")
                break

            if self.state.is_draw():
                self.display_board()
                print("O jogo empatou!")
                break

            self.state.switch_player()

    def get_player_move(self) -> Optional[Tuple[int, int]]:
        prompt = f"Jogador {self.state.current_player}, informe linha e coluna (1-3) separados por espaço: "
        user_input = input(prompt)
        move = self.parse_move(user_input)
        if move is None:
            print("Entrada inválida. Digite dois números entre 1 e 3, separados por espaço.")
            return None
        return move


def main() -> None:
    game = TicTacToe()
    game.play()


if __name__ == "__main__":
    main()

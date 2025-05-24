import tkinter as tk
from tkinter import messagebox, simpledialog
import random

EMPTY = " "
PLAYER1 = "X"
PLAYER2 = "O"
COMPUTER = "O"

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = [EMPTY] * 9
        self.buttons = []
        self.current_player = PLAYER1
        self.winner = None
        self.mode = 2  # Default: 2 players
        self.label = tk.Label(self.root, text="Welcome to Tic-Tac-Toe", font=("Arial", 14))
        self.label.grid(row=3, column=0, columnspan=3)

        for i in range(9):
            btn = tk.Button(root, text="", font=("Arial", 20), width=5, height=2,
                            command=lambda i=i: self.button_click(i))
            btn.grid(row=i // 3, column=i % 3)
            self.buttons.append(btn)

        self.start_button = tk.Button(root, text="Start Game", command=self.select_mode)
        self.start_button.grid(row=4, column=0, columnspan=3)

    def select_mode(self):
        mode_choice = messagebox.askquestion("Game Mode", "Do you want to play Single Player?")
        self.mode = 1 if mode_choice == "yes" else 2
        self.start_game()

    def start_game(self):
        self.start_button.grid_remove()
        self.current_player = PLAYER1
        self.winner = None
        self.board = [EMPTY] * 9
        for btn in self.buttons:
            btn.config(text="", bg="SystemButtonFace", state=tk.NORMAL)
        self.label.config(text="Your turn (X)" if self.mode == 1 else "Player 1's turn (X)")
        if self.mode == 1 and self.current_player == COMPUTER:
            self.computer_move()

    def button_click(self, index):
        if self.board[index] == EMPTY and self.winner is None:
            self.make_move(index, self.current_player)
            self.check_game_state()
            if self.mode == 2:
                self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1
                self.label.config(text=f"Player {1 if self.current_player == PLAYER1 else 2}'s turn ({self.current_player})")
            elif self.winner is None:
                self.root.after(500, self.computer_move)

    def make_move(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player)

    def computer_move(self):
        if self.board[4] == EMPTY:
            self.make_move(4, COMPUTER)
        else:
            move = random.choice([i for i in range(9) if self.board[i] == EMPTY])
            self.make_move(move, COMPUTER)
        self.check_game_state()

    def check_winner(self):
        combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in combos:
            if self.board[a] != EMPTY and self.board[a] == self.board[b] == self.board[c]:
                for i in (a, b, c):
                    self.buttons[i].config(bg="lightgreen")
                return self.board[a]
        if EMPTY not in self.board:
            return "tie"
        return None

    def check_game_state(self):
        self.winner = self.check_winner()
        if self.winner:
            message = {
                PLAYER1: "You win!" if self.mode == 1 else "Player 1 wins!",
                PLAYER2: "Player 2 wins!",
                COMPUTER: "Computer wins!",
                "tie": "It's a tie!"
            }.get(self.winner, "")
            messagebox.showinfo("Game Over", message)
            self.reset_game()

    def reset_game(self):
        for btn in self.buttons:
            btn.config(text="", bg="SystemButtonFace", state=tk.DISABLED)
        self.label.config(text="")
        self.start_button.grid(row=4, column=0, columnspan=3)

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()

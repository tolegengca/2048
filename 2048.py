import tkinter as tk
import random
import time
CELL_SIZE = 100
BG_COLOR = "#92877d"
EMPTY_CELL_COLOR = "#9e948a"
FONT = ("Verdana", 20, "bold")
GAME_OVER_FONT = ("Verdana", 30, "bold")

class Game2048:
    def __init__(self, game_size):
        self.game_size = game_size

        self.window = tk.Tk()
        self.window.title("2048")
        self.window.geometry(f"{self.game_size * CELL_SIZE}x{self.game_size * CELL_SIZE + 120}")

        self.board = [[0] * self.game_size for _ in range(self.game_size)]
        self.score = 0
        self.highest_score = 0
        self.game_over = False

        self.canvas = tk.Canvas(self.window, bg=BG_COLOR, width=self.game_size * CELL_SIZE, height=self.game_size * CELL_SIZE)
        self.canvas.pack()

        self.score_label = tk.Label(self.window, text="Score: 0", font=("Verdana", 16, "bold"))
        self.score_label.pack()

        self.highest_score_label = tk.Label(self.window, text="Highest Score: 0", font=("Verdana", 16, "bold"))
        self.highest_score_label.pack()

        self.replay_button = tk.Button(self.window, text="Replay", command=self.replay_game)
        self.replay_button.pack()

        self.auto_play_button = tk.Button(self.window, text="Auto Play", command=self.auto_play_game)
        self.auto_play_button.pack()
        
        self.draw_board()
        self.place_random_tile()
        self.place_random_tile()

        self.window.bind("<Key>", self.key_pressed)
        self.window.mainloop()
    

    def auto_play_game(self):
        while not self.game_over:
            directions = ["Up", "Down", "Left", "Right"]
            direction = random.choice(directions)
            self.move(direction)
            time.sleep(0.2)  # Add a small delay between moves for visual effect
            self.place_random_tile()


    
    def draw_board(self):
        self.canvas.delete("tile")
        for row in range(self.game_size):
            for col in range(self.game_size):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                value = self.board[row][col]
                color = self.get_tile_color(value)
                self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=color, tags="tile")
                if value != 0:
                    self.canvas.create_text(x + CELL_SIZE//2, y + CELL_SIZE//2, text=str(value), font=FONT, tags="tile")

        self.canvas.update()

        self.score_label.config(text=f"Score: {self.score}")  # New line
        self.highest_score_label.config(text=f"Highest Score: {self.highest_score}")  # New line


    def get_tile_color(self, value):
        colors = {
            0: EMPTY_CELL_COLOR,
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e"
        }
        return colors.get(value, "#ff0000")

    def place_random_tile(self):
        if not any(0 in row for row in self.board):
            return

        while True:
            row = random.randint(0, self.game_size - 1)
            col = random.randint(0, self.game_size - 1)
            if self.board[row][col] == 0:
                self.board[row][col] = 2 if random.random() < 0.9 else 4
                break

    def move(self, direction):
        if self.game_over:
            return
        if direction == "Random":
            directions = ["Up", "Down", "Left", "Right"]
            direction = random.choice(directions)
        if direction == "Up":
            self.board = self.transpose(self.board)
            self.move_left()
            self.board = self.transpose(self.board)
            
        elif direction == "Down":
            self.board = self.transpose(self.board)
            self.move_right()
            self.board = self.transpose(self.board)
        elif direction == "Left":
            self.move_left()
        elif direction == "Right":
                self.move_right()

        self.draw_board()

        if self.is_game_over():
            self.game_over = True
            self.canvas.create_text(
                self.game_size * CELL_SIZE // 2,
                self.game_size * CELL_SIZE // 2,
                text="Game Over",
                font=GAME_OVER_FONT,
                fill="white"
            )

    def move_left(self):
        for row in range(self.game_size):
            merged = False
            for col in range(1, self.game_size):
                if self.board[row][col] != 0:
                    for i in range(col, 0, -1):
                        if self.board[row][i - 1] == 0:
                            self.board[row][i - 1] = self.board[row][i]
                            self.board[row][i] = 0
                        elif self.board[row][i - 1] == self.board[row][i] and not merged:
                            self.board[row][i - 1] *= 2
                            self.board[row][i] = 0
                            self.score += self.board[row][i + 1]
                            if self.score > self.highest_score:
                                self.highest_score = self.score
                            merged = True
                        else:
                            break

    def move_right(self):
        for row in range(self.game_size):
            merged = False
            for col in range(self.game_size - 2, -1, -1):
                if self.board[row][col] != 0:
                    for i in range(col, self.game_size - 1):
                        if self.board[row][i + 1] == 0:
                            self.board[row][i + 1] = self.board[row][i]
                            self.board[row][i] = 0
                        elif self.board[row][i + 1] == self.board[row][i] and not merged:
                            self.board[row][i + 1] *= 2
                            self.board[row][i] = 0
                            self.score += self.board[row][i + 1]
                            if self.score > self.highest_score:
                                self.highest_score = self.score
                            merged = True
                        else:
                            break

    def transpose(self, board):
        return [[board[j][i] for j in range(self.game_size)] for i in range(self.game_size)]

    def is_game_over(self):
        for row in range(self.game_size):
            for col in range(self.game_size):
                if self.board[row][col] == 0:
                    return False
                if col != self.game_size - 1 and self.board[row][col] == self.board[row][col + 1]:
                    return False
                if row != self.game_size - 1 and self.board[row][col] == self.board[row + 1][col]:
                    return False
        return True

    def key_pressed(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.move(event.keysym)
            if not self.game_over:
                self.place_random_tile()
            self.update_score()
            self.update_highest_score()
            if self.is_game_over():
                self.game_over = True
                self.canvas.create_text(
                    self.game_size * CELL_SIZE // 2,
                    self.game_size * CELL_SIZE // 2,
                    text="Game Over",
                    font=GAME_OVER_FONT,
                    fill="white"
                )
    def replay_game(self):
        self.board = [[0] * self.game_size for _ in range(self.game_size)]
        self.score = 0
        self.game_over = False
        self.draw_board()
        self.place_random_tile()
        self.place_random_tile()
        self.update_score()
        self.update_highest_score()

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")
    

    def update_highest_score(self):
        self.highest_score = max(self.score, self.highest_score)
        self.highest_score_label.config(text=f"Highest Score: {self.highest_score}")

    

def main():
    def start_game(game_size):
        game = Game2048(game_size)

    def on_easy_mode():
        start_game(4)

    def on_medium_mode():
        start_game(5)

    def on_hard_mode():
        start_game(6)
        
    def replay_game(self):
        self.board = [[0] * self.game_size for _ in range(self.game_size)]
        self.score = 0
        self.game_over = False
        self.update_score()
        self.draw_board()
        self.place_random_tile()
        self.place_random_tile()



    window = tk.Tk()
    window.title("2048")

    easy_button = tk.Button(window, text="Easy (4x4)", command=on_easy_mode)
    easy_button.pack()

    medium_button = tk.Button(window, text="Medium (5x5)", command=on_medium_mode)
    medium_button.pack()

    hard_button = tk.Button(window, text="Hard (6x6)", command=on_hard_mode)
    hard_button.pack()
    
    window.mainloop()

if __name__ == "__main__":
    main()
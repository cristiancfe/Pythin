import tkinter as tk
from tkinter import messagebox
import random
import time
import csv

class QuebraCabeca:
    def __init__(self, root):
        # Configuração inicial
        self.root = root
        self.puzzle = list(range(9))
        self.attempts = 0
        self.shuffle_button = None
        self.move_counter_label = None
        self.completed = False
        self.start_time = None
        self.end_time = None
        self.create_buttons()

    def count_inversions(self):
        # Conta o número de inversões para determinar se o quebra-cabeça é solucionável
        inversions = 0
        for i in range(len(self.puzzle)):
            for j in range(i+1, len(self.puzzle)):
                if self.puzzle[i] > self.puzzle[j] and self.puzzle[i] != 0 and self.puzzle[j] != 0:
                    inversions += 1
        return inversions

    def is_solvable(self):
        # Verifica se o quebra-cabeça é solucionável com base no número de inversões e na posição do espaço vazio
        size = int(len(self.puzzle) ** 0.5)
        inversions = self.count_inversions()
        empty_row = self.puzzle.index(0) // size
        return (size % 2 == 1 and inversions % 2 == 0) or (size % 2 == 0 and (inversions % 2 == 0) == (empty_row % 2 == 0))

    def shuffle_puzzle(self):
        # Embaralha o quebra-cabeça
        self.attempts = 0
        self.completed = False
        self.start_time = None
        self.end_time = None
        random.shuffle(self.puzzle)
        while not self.is_solvable():
            random.shuffle(self.puzzle)
        self.create_buttons()
        self.update_move_counter()

    def button_click(self, index):
        # Manipula o clique nos botões do quebra-cabeça
        if not self.completed:
            if self.start_time is None:
                self.start_time = time.time()

            row, col = divmod(index, 3)
            empty_row, empty_col = divmod(self.puzzle.index(0), 3)

            if (row == empty_row and abs(col - empty_col) == 1) or (col == empty_col and abs(row - empty_row) == 1):
                self.puzzle[index], self.puzzle[empty_row * 3 + empty_col] = self.puzzle[empty_row * 3 + empty_col], self.puzzle[index]
                self.attempts += 1
                self.create_buttons()
                self.update_move_counter()

                if self.check_completed():
                    self.end_time = time.time()
                    self.completed = True
                    self.show_congratulations()

    def check_completed(self):
        # Verifica se o quebra-cabeça foi resolvido
        return self.puzzle == list(range(1, 9)) + [0]

    def show_congratulations(self):
        # Exibe uma mensagem de parabéns quando o quebra-cabeça é resolvido
        total_time = round(self.end_time - self.start_time, 2)
        message = f"Parabéns!\nVocê completou o quebra-cabeça em {self.attempts} movimentos e {total_time} segundos."
        messagebox.showinfo("Parabéns!", message)

        with open('game_results.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.attempts, total_time])

        total_games = 0
        total_time = 0
        total_moves = 0

        with open('game_results.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                total_games += 1
                total_time += float(row[1])
                total_moves += int(row[0])

        average_time = total_time / total_games
        if total_games > 0:
            average_moves = total_moves / total_games
            print(f'Average Moves: {average_moves:.2f} moves')
            print(f'Average Time: {average_time:.2f} ')

    def update_move_counter(self):
        # Atualiza a contagem de movimentos na interface gráfica
        if self.move_counter_label is not None:
            self.move_counter_label.config(text=f"Movimentos: {self.attempts}")

    def create_buttons(self):
        # Cria os botões do quebra-cabeça na interface gráfica
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                label = str(self.puzzle[index])
                if label == '0':
                    tk.Button(self.root, text='', state=tk.DISABLED, width=10, height=5, highlightthickness=0).grid(
                        row=i, column=j)
                else:
                    tk.Button(self.root, text=label, command=lambda index=index: self.button_click(index), width=10,
                              height=5, font=('Arial', 20), highlightthickness=0).grid(row=i, column=j)

        if self.shuffle_button is None:
            self.shuffle_button = tk.Button(self.root, text='Embaralhar', command=self.shuffle_puzzle, height=2,
                                            width=15, font=('Arial', 12))
            self.shuffle_button.grid(row=3, column=0, columnspan=3, pady=10)

        if self.move_counter_label is None:
            self.move_counter_label = tk.Label(self.root, text="Movimentos: 0", font=('Arial', 12))
            self.move_counter_label.grid(row=4, column=0, columnspan=3, pady=10)

        self.record_time_label = tk.Label(self.root, font=('Arial', 12), bg="#2C3E50", fg="white")
        self.record_time_label.grid(row=5, column=0, columnspan=3, pady=(10, 0), sticky='w')

        # Atualiza o rótulo de recorde de tempo
        fastest_time = self.get_fastest_time()
        if fastest_time != float('inf'):
            self.record_time_label.config(text=f"Recorde de tempo: {fastest_time} segundos")
        else:
            self.record_time_label.config(text="Nenhum recorde registrado ainda")

    def get_fastest_time(self):
        # Obtém o tempo mais rápido registrado
        fastest_time = float('inf')

        with open('game_results.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                time = float(row[1])
                if time < fastest_time:
                    fastest_time = time

        return fastest_time

root = tk.Tk()
root.title("Quebra-Cabeça")
quebra_cabeca = QuebraCabeca(root)
quebra_cabeca.shuffle_puzzle()
root.configure(bg="#2C3E50")
fastest_time = quebra_cabeca.get_fastest_time()
if fastest_time != float('inf'):
    print(f"The fastest time is: {fastest_time} seconds.")
else:
    print("No records in the CSV file yet.")
root.mainloop()

import tkinter as tk
from tkinter import messagebox

class SudokuSolver(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sudoku Solver")
        self.geometry("370x400")

        self.grid_input = tk.StringVar()
        self.solution = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        input_label = tk.Label(self, text="Enter Sudoku grid (81 characters):")
        input_label.pack(pady=10)

        self.grid_input_entry = tk.Entry(self, textvariable=self.grid_input, width=50)
        self.grid_input_entry.pack(pady=5)

        solve_button = tk.Button(self, text="Solve", command=self.solve_sudoku)
        solve_button.pack(pady=5)

        self.solution_text = tk.Text(self, height=15, width=50)
        self.solution_text.pack(pady=5)

        self.solution_text.config(state='normal')
        self.solution_text.insert(tk.END, self.solution.get())
        self.solution_text.config(state='disabled')

    def solve_sudoku(self):
        grid_string = self.grid_input.get()

        if len(grid_string) != 81:
            messagebox.showerror("Error", "Invalid grid length. It should be 81 characters.")
            return

        grid = []
        for i in range(0, 81, 9):
            row = []
            for j in range(i, i + 9):
                if grid_string[j] == '.':
                    row.append(0)
                else:
                    row.append(int(grid_string[j]))
            grid.append(row)

        if self.solve(grid):
            solution_string = ""
            for row in grid:
                for num in row:
                    solution_string += str(num)
            self.solution.set(solution_string)
            self.solution_text.config(state='normal')
            self.solution_text.delete(1.0, tk.END)
            self.solution_text.insert(tk.END, self.solution.get())
            self.solution_text.config(state='disabled')
        else:
            messagebox.showerror("Error", "No solution exists.")

    def solve(self, grid):
        find = find_empty(grid)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid(i, (row, col), grid):
                grid[row][col] = i

                if self.solve(grid):
                    return True

                grid[row][col] = 0

        return False

    def valid(self, num, pos, grid):

        for i in range(len(grid[0])):
            if grid[pos[0]][i] == num and pos[1] != i:
                return False

        for i in range(len(grid)):
            if grid[i][pos[1]] == num and pos[0] != i:
                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if grid[i][j] == num and (i,j) != pos:
                    return False

        return True

def find_empty(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return (i, j) 

    return None

if __name__ == "__main__":
    app = SudokuSolver()
    app.mainloop()
import tkinter as tk

class MapVisualization(tk.Tk):
    def __init__(self, solution):
        super().__init__()
        self.title("Map CSP")
        self.geometry("580x420")
        self.canvas = tk.Canvas(self, width=580, height=420)
        self.canvas.pack()
        self.solution = solution
        self.region_shapes = {
            'WA': [(200, 100), (160, 80), (120, 120), (70, 180), (110, 260), (200, 230), (200, 100)],
            'NT': [(200, 180), (330, 180), (330, 120), (280, 80), (320, 50), (220, 50), (200, 80)],
            'SA': [(200, 180), (360, 180), (360, 300), (200, 230), (200, 180)],
            'Q': [(330, 180), (330, 120), (400, 40), (510, 220), (360, 220), (360, 180), (330, 180)],
            'NSW': [(360, 220), (510, 220), (480, 290), (360, 260)],
            'V': [(360, 260), (360, 300), (480, 300), (480, 290)],
            'T': [(390, 340), (450, 340), (450, 380), (390, 380)]
        }
        self.colors = {'R': 'red', 'G': 'green', 'B': 'blue'}
        self.draw_map()

    def draw_map(self):
        for region, shape in self.region_shapes.items():
            color = self.colors[self.solution[region]]
            self.canvas.create_polygon(shape, fill=color, outline='black')
            x = [point[0] for point in shape]
            y = [point[1] for point in shape]
            cent_x = sum(x) / len(shape)
            cent_y = sum(y) / len(shape)
            self.canvas.create_text(cent_x, cent_y, text = region,
                                    fill = 'black', font = ('Helvetica 15 bold'))

class MapCSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables # list of variables
        self.domains = domains # dict of domains for each variable
        self.constraints = constraints # list of constraints (functions)
        self.solutions = []

    def is_consistent(self, variable, assignment):
        """Check if the current assignment is consistent."""
        for constraint in self.constraints:
            if not constraint(variable, assignment):
                return False
        return True

    def backtrack(self, assignment):
        """Backtrack search to find a solution."""
        if len(assignment) == len(self.variables):
            self.solutions.append(assignment.copy())
            return assignment

        unassigned = [v for v in self.variables if v not in assignment]
        first = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            if self.is_consistent(first, local_assignment):
                self.backtrack(local_assignment)

    def solve(self):
        """Solve the CSP."""
        self.backtrack({})
        return self.solutions


def map_constraints(region, assignment):
    """Define constraints for map csp."""
    for neighbor in assignment:
        if neighbor != region and neighbor in adjacency[region]:
            if assignment[neighbor] == assignment[region]:
                return False
    return True

# map adjacency list
adjacency = {
    'WA': ['NT', 'SA'],
    'NT': ['WA', 'SA', 'Q'],
    'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
    'Q': ['NT', 'SA', 'NSW'],
    'NSW': ['SA', 'Q', 'V'],
    'V': ['SA', 'NSW'],
    'T': []
}

# Variables and domains for a map csp using the example from the slides for Australia
variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
domains = {var: ['R', 'G', 'B'] for var in variables}
constraints = [map_constraints]

# Map CSP instance
map_csp = MapCSP(variables, domains, constraints)
solutions = map_csp.solve()

for idx, solution in enumerate(solutions):
    print(f"Solution {idx + 1}: {solution}")

app = MapVisualization(solutions[0])
app.mainloop()

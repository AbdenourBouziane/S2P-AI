from constraint import Problem, AllDifferentConstraint
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from operator import eq, ne, lt, le, gt, ge

class CSPSolver(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('S2P-CSP Solver')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.variables_label = QLabel("Variables:")
        self.layout.addWidget(self.variables_label)

        self.variables_textedit = QTextEdit()
        self.layout.addWidget(self.variables_textedit)

        self.domains_label = QLabel("Domains:")
        self.layout.addWidget(self.domains_label)

        self.domains_textedit = QTextEdit()
        self.layout.addWidget(self.domains_textedit)

        self.constraints_label = QLabel("Constraints:")
        self.layout.addWidget(self.constraints_label)

        self.constraints_textedit = QTextEdit()
        self.layout.addWidget(self.constraints_textedit)

        solve_button = QPushButton('Solve')
        solve_button.clicked.connect(self.solve_csp)
        self.layout.addWidget(solve_button)

        self.solution_label = QLabel()
        self.layout.addWidget(self.solution_label)

    def solve_csp(self):
        problem = Problem()

        variables = self.variables_textedit.toPlainText().split()
        domains = self.domains_textedit.toPlainText().split('\n')

        for variable, domain in zip(variables, domains):
            problem.addVariable(variable, domain.split())

        constraints = self.constraints_textedit.toPlainText().split('\n')

        for constraint in constraints:
            if constraint.strip():
                split_constraint = constraint.split()
                if len(split_constraint) == 3:
                    var1, operator, var2 = split_constraint
                    if operator in ('!=', '==', '<', '<=', '>', '>='):
                        func = self.get_comparison_function(operator)
                        problem.addConstraint(func, (var1, var2))
                elif len(split_constraint) == 4:
                    var1, _, operator, var2 = split_constraint
                    if operator == '!=':
                        func = self.get_comparison_function(operator)
                        problem.addConstraint(func, (var1, var2))

        solution = problem.getSolution()

        if solution is not None:
            self.solution_label.setText(f"Solution: {solution}")
        else:
            self.solution_label.setText("No solution found.")

    def get_comparison_function(self, operator):
        operators = {
            '==': eq,
            '!=': ne,
            '<': lt,
            '<=': le,
            '>': gt,
            '>=': ge
        }

        return lambda a, b: operators[operator](a, b)

if __name__ == '__main__':
    app = QApplication([])
    window = CSPSolver()
    window.show()
    app.exec()

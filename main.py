import networkx as nx
import math
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from collections import defaultdict
from Search_Algorithms.uninformed_search import depth_first_search, breadth_first_search, uniform_cost_search, depth_limited_search
from Search_Algorithms.informed import greedy_best_first_search, a_star_search, hill_climbing_search
from Search_Algorithms.local_search import hill_climbing_search
from CSP.csp import CSPSolver
from Games.games_gui import GameSelectionGUI


class GraphProblem:
    def __init__(self, graph, costs=None):
        self.graph = graph
        self.costs = costs

    def initial_state(self):
        return None

    def is_goal(self, state):
        return state is not None and state == self.goal_state()

    def goal_state(self):
        return None

    def actions(self, state):
        if state is None:
            return []
        if state not in self.graph:
            return []
        return self.graph[state]

    def cost(self, state, action):
        if not self.costs or (state, action) not in self.costs:
            return 1  # Default cost for graphs without costs
        return self.costs[(state, action)]

    def set_goal_state(self, goal_state):
        self.goal_state = goal_state


class SearchAlgorithmUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("S2P - Search Algorithm")

        self.dfs_button = QtWidgets.QPushButton("DFS")
        self.bfs_button = QtWidgets.QPushButton("BFS")
        self.ucs_button = QtWidgets.QPushButton("UCS")
        self.dls_button = QtWidgets.QPushButton("DLS")
        self.greedy_button = QtWidgets.QPushButton("Greedy BFS")
        self.a_star_button = QtWidgets.QPushButton("A*")
        self.hill_climbing_button = QtWidgets.QPushButton("Hill Climbing")


        self.from_label = QtWidgets.QLabel("Start:")
        self.from_entry = QtWidgets.QLineEdit()
        self.to_label = QtWidgets.QLabel("Goal:")
        self.to_entry = QtWidgets.QLineEdit()

        self.heuristic_label = QtWidgets.QLabel("Select Heuristic:")
        self.heuristic_combo = QtWidgets.QComboBox()
        self.heuristic_combo.addItem("Heuristic 1")
        self.heuristic_combo.addItem("Heuristic 2")
        self.heuristic_combo.addItem("Heuristic 3")

        self.graph_label = QtWidgets.QLabel("Enter Graph:")
        self.graph_text_edit = QtWidgets.QTextEdit()

        self.search_button = QtWidgets.QPushButton("Search")
        self.visualize_button = QtWidgets.QPushButton("Visualize")
        self.csp_solver_button = QtWidgets.QPushButton("CSP Solver")
        self.game_button = QtWidgets.QPushButton("Try Games")
        self.result_label = QtWidgets.QLabel()

        self.algo_func = None
        self.POPULATION_SIZE = 10 


        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
            QComboBox, QLineEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QPushButton {
                font-size: 14px;
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
                color: #fff;
                background-color: #4CAF50;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTextEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QLabel#result_label {
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
        """)

        self.algo_combo = QtWidgets.QComboBox()
        self.algo_combo.addItem("DFS")
        self.algo_combo.addItem("BFS")
        self.algo_combo.addItem("UCS")
        self.algo_combo.addItem("DLS")
        self.algo_combo.addItem("Greedy BFS")
        self.algo_combo.addItem("A*")

        self.from_label = QtWidgets.QLabel("Start:")
        self.from_entry = QtWidgets.QLineEdit()

        self.to_label = QtWidgets.QLabel("Goal:")
        self.to_entry = QtWidgets.QLineEdit()

        self.heuristic_label = QtWidgets.QLabel("Select Heuristic:")
        self.heuristic_combo = QtWidgets.QComboBox()
        self.heuristic_combo.addItem("Heuristic 1")
        self.heuristic_combo.addItem("Heuristic 2")
        self.heuristic_combo.addItem("Heuristic 3")

        self.graph_label = QtWidgets.QLabel("Enter Graph:")
        self.graph_text_edit = QtWidgets.QTextEdit()

        self.search_button = QtWidgets.QPushButton("Search")
        self.visualize_button = QtWidgets.QPushButton("Visualize")
        self.csp_solver_button = QtWidgets.QPushButton("Solve a Csp problem")
        self.game_button = QtWidgets.QPushButton("Games")
        self.result_label = QtWidgets.QLabel()

        layout = QtWidgets.QGridLayout()

        # Informed Search Algorithms
        informed_label = QtWidgets.QLabel("Informed Search:")
        layout.addWidget(informed_label, 0, 0, 1, 2)

        informed_layout = QtWidgets.QVBoxLayout()
        informed_layout.addWidget(self.greedy_button)
        informed_layout.addWidget(self.a_star_button)

        informed_container = QtWidgets.QWidget()
        informed_container.setLayout(informed_layout)
        layout.addWidget(informed_container, 1, 0, 1, 2)

        # Uninformed Search Algorithms
        uninformed_label = QtWidgets.QLabel("Uninformed Search:")
        layout.addWidget(uninformed_label, 0, 2, 1, 1)

        uninformed_layout = QtWidgets.QVBoxLayout()
        uninformed_layout.addWidget(self.dfs_button)
        uninformed_layout.addWidget(self.bfs_button)
        uninformed_layout.addWidget(self.ucs_button)
        uninformed_layout.addWidget(self.dls_button)

        uninformed_container = QtWidgets.QWidget()
        uninformed_container.setLayout(uninformed_layout)
        layout.addWidget(uninformed_container, 1, 2, 1, 2)

        # Local search Layouts

        local_label = QtWidgets.QLabel("Local Search:")
        layout.addWidget(local_label, 0, 5, 1, 1)

        local_layout = QtWidgets.QVBoxLayout()
        local_layout.addWidget(self.hill_climbing_button)

        local_container = QtWidgets.QWidget()
        local_container.setLayout(local_layout)
        layout.addWidget(local_container, 1, 5, 1, 1)

        # Other UI elements
        layout.addWidget(self.from_label, 3, 0)
        layout.addWidget(self.from_entry, 3, 1)
        layout.addWidget(self.to_label, 4, 0)
        layout.addWidget(self.to_entry, 4, 1)
        layout.addWidget(self.heuristic_label, 5, 0)
        layout.addWidget(self.heuristic_combo, 5, 1)
        layout.addWidget(self.graph_label, 6, 0)
        layout.addWidget(self.graph_text_edit, 6, 1, 1, 6)
        layout.addWidget(self.search_button, 7, 0, 1, 2)
        layout.addWidget(self.visualize_button, 7, 2, 1, 2)
        layout.addWidget(self.csp_solver_button, 7, 4, 1, 2)
        layout.addWidget(self.game_button, 7, 6, 1, 2)
        layout.addWidget(self.result_label, 8, 0, 1, 8)

        self.setLayout(layout)
        self.dfs_button.clicked.connect(self.set_algo_dfs)
        self.bfs_button.clicked.connect(self.set_algo_bfs)
        self.ucs_button.clicked.connect(self.set_algo_ucs)
        self.dls_button.clicked.connect(self.set_algo_dls)
        self.greedy_button.clicked.connect(self.set_algo_greedy)
        self.a_star_button.clicked.connect(self.set_algo_a_star)
        self.search_button.clicked.connect(self.search)
        self.visualize_button.clicked.connect(self.visualize)
        self.csp_solver_button.clicked.connect(self.open_csp_solver)
        self.game_button.clicked.connect(self.open_games_gui)
        self.hill_climbing_button.clicked.connect(self.set_algo_hill_climbing)
        # self.genetic_algorithm_button.clicked.connect(self.set_algo_genetic_algorithm)


    def open_csp_solver(self):
        self.csp_solver = CSPSolver()
        self.csp_solver.show()

    def open_games_gui(self):
        self.game = GameSelectionGUI()
        self.game.show()

    

    def set_algo_dfs(self):
        self.algo_func = depth_first_search

    def set_algo_bfs(self):
        self.algo_func = breadth_first_search

    def set_algo_ucs(self):
        self.algo_func = uniform_cost_search

    def set_algo_dls(self):
        depth_limit, ok = QtWidgets.QInputDialog.getInt(
            self, "Set Depth Limit", "Enter depth limit:"
        )
        if ok:
            self.algo_func = lambda problem, start, end: depth_limited_search(
                problem, start, end, depth_limit
            )

    def set_algo_greedy(self):
        heuristic_func = self.get_selected_heuristic_func()
        self.algo_func = lambda problem, start, end: greedy_best_first_search(
        problem, start, end, heuristic_func
        )

    def set_algo_a_star(self):
        heuristic_func = self.get_selected_heuristic_func()
        self.algo_func = lambda problem, start, end: a_star_search(
        problem, start, end, heuristic_func
        )
    def set_algo_hill_climbing(self):
        self.algo_func = hill_climbing_search




    def get_selected_heuristic_func(self):
        heuristic = self.heuristic_combo.currentIndex()
        if heuristic == 0:
            return heuristic_1
        elif heuristic == 1:
            return heuristic_2
        elif heuristic == 2:
            return heuristic_3
        else:
            return heuristic_1


    def search(self):
        start = self.from_entry.text()
        end = self.to_entry.text()
        graph_input = self.graph_text_edit.toPlainText()

        graph, costs = self.parse_graph(graph_input)

        if graph is None:
            self.result_label.setText("Invalid graph input.")
            return

        problem = GraphProblem(graph, costs)

        if self.algo_func:
            path = self.algo_func(problem, start, end)
            if path:
                path_str = " -> ".join(path)
                self.result_label.setText(path_str)
            else:
                self.result_label.setText("No path found.")
        else:
            self.result_label.setText("Please select an algorithm.")


    def visualize(self):
        graph_input = self.graph_text_edit.toPlainText()
        graph, costs = self.parse_graph(graph_input)

        if graph is None:
            self.result_label.setText("Invalid graph input.")
            return

        G = nx.DiGraph()
        for node, neighbors in graph.items():
            G.add_node(node)
            for neighbor in neighbors:
                if costs and (node, neighbor) in costs:
                    cost = str(costs[(node, neighbor)])
                else:
                    cost = '1'  # Default cost for edges without costs
                G.add_edge(node, neighbor, weight=cost)

        pos = nx.spring_layout(G)
        edge_labels = nx.get_edge_attributes(G, 'weight')

        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.title('Graph Visualization')
        plt.show()

    def parse_graph(self, graph_input):
        graph = defaultdict(list)
        costs = {}

        lines = graph_input.split('\n')
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split('->')
                node1 = parts[0].strip()
                if len(parts) > 1:
                    node2 = parts[1].strip()
                    if ':' in node2:
                        node2, cost = node2.split(':')
                        cost = int(cost.strip())
                        costs[(node1, node2)] = cost
                else:
                    node2 = None
                graph[node1].append(node2)

        return graph, costs

    def calculate_node_positions(self, graph):
        node_positions = {}
        num_nodes = len(graph)
        radius = 200
        center_x = self.graph_view.width() / 2
        center_y = self.graph_view.height() / 2

        for i, node in enumerate(graph.keys()):
            angle = (2 * i * 3.14159) / num_nodes
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            node_positions[node] = (x, y)

        return node_positions

    def draw_graph(self, graph, node_positions):
        node_size = 30
        node_font_size = 10

        for node, connections in graph.items():
            x, y = node_positions[node]
            self.scene.addEllipse(x - node_size / 2, y - node_size / 2, node_size, node_size, QtGui.QPen(), QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            self.scene.addText(node, QtGui.QFont("Arial", node_font_size)).setPos(x - node_font_size * 0.4, y - node_font_size * 0.4)

            for connection in connections:
                if connection in node_positions:
                    x2, y2 = node_positions[connection]
                    self.scene.addLine(x, y, x2, y2, QtGui.QPen(QtGui.QColor(0, 0, 0), 1))

        self.graph_view.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)



def heuristic_1(node, goal):
    # Ensure that node is a tuple with two values
    if isinstance(node, tuple):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])
    else:
        node = node.split(' -> ')[0]  # Extract the node name from the string
        goal = goal.split(' -> ')[0]  # Extract the goal name from the string
        return 0 if node == goal else 1  # Heuristic always returns 0 if node is the goal, else 1


def heuristic_2(node, goal):
    # Calculate the Euclidean distance between the current node and the goal node
    if isinstance(node, tuple):
        return math.sqrt((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2)
    else:
        node = node.split(' -> ')[0]  # Extract the node name from the string
        goal = goal.split(' -> ')[0]  # Extract the goal name from the string
        return 0 if node == goal else 1  # Heuristic always returns 0 if node is the goal, else 1


def heuristic_3(node, goal):
    # Calculate the Chebyshev distance between the current node and the goal node
    if isinstance(node, tuple):
        return max(abs(node[0] - goal[0]), abs(node[1] - goal[1]))
    else:
        return float('inf')  # Return infinity as the heuristic value for all string nodes



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = SearchAlgorithmUI()
    window.show()
    sys.exit(app.exec_())



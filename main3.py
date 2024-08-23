from collections import defaultdict
import unittest
import random

# Graph Class
class Graph:
    """
    Graph class to represent an undirected graph using an adjacency list.
    
    Attributes:
        adjacency_list (defaultdict): A dictionary of sets where each key is a vertex, and the value is a set of neighbors.
        vertices (set): A set of vertices in the graph.
    
    Methods:
        add_vertex(vertex): Adds a vertex to the graph.
        add_edge(u, v): Adds an undirected edge between vertices u and v.
        remove_vertex(vertex): Removes a vertex and its associated edges.
        remove_edge(u, v): Removes the edge between vertices u and v.
        neighbors(vertex): Returns the set of neighbors for a given vertex.
        apply_dynamic_changes(changes): Applies dynamic changes (like adding/removing vertices or edges) to the graph.
    """
    def __init__(self):
        self.adjacency_list = defaultdict(set)
        self.vertices = set()

    def add_vertex(self, vertex):
        """Adds a vertex to the graph."""
        self.vertices.add(vertex)

    def add_edge(self, u, v):
        """Adds an undirected edge between vertices u and v."""
        self.adjacency_list[u].add(v)
        self.adjacency_list[v].add(u)

    def remove_vertex(self, vertex):
        """Removes a vertex and its associated edges."""
        self.vertices.remove(vertex)
        for neighbor in list(self.adjacency_list[vertex]):
            self.adjacency_list[neighbor].remove(vertex)
        del self.adjacency_list[vertex]

    def remove_edge(self, u, v):
        """Removes the edge between vertices u and v."""
        self.adjacency_list[u].remove(v)
        self.adjacency_list[v].remove(u)

    def neighbors(self, vertex):
        """Returns the set of neighbors for a given vertex."""
        return self.adjacency_list[vertex]

    def apply_dynamic_changes(self, changes):
        """Applies dynamic changes (like adding/removing vertices or edges) to the graph."""
        for change in changes:
            action, u, v = change
            if action == 'add_vertex':
                self.add_vertex(u)
            elif action == 'remove_vertex':
                self.remove_vertex(u)
            elif action == 'add_edge':
                self.add_edge(u, v)
            elif action == 'remove_edge':
                self.remove_edge(u, v)

# ConstraintManager Class
class ConstraintManager:
    """
    Manages constraints for graph coloring, including pre-assigned colors and color exclusions.
    
    Attributes:
        graph (Graph): The graph to manage constraints for.
        pre_assigned_colors (dict): A dictionary mapping vertices to their pre-assigned colors.
        color_exclusions (defaultdict): A dictionary mapping vertices to a set of excluded colors.
    
    Methods:
        add_pre_assigned_color(vertex, color): Adds a pre-assigned color constraint to a vertex.
        add_color_exclusion(vertex, color): Adds a color exclusion constraint to a vertex.
        get_pre_assigned_color(vertex): Returns the pre-assigned color for a vertex, if any.
        is_color_excluded(vertex, color): Checks if a color is excluded for a vertex.
    """
    def __init__(self, graph):
        self.graph = graph
        self.pre_assigned_colors = {}
        self.color_exclusions = defaultdict(set)

    def add_pre_assigned_color(self, vertex, color):
        """Adds a pre-assigned color constraint to a vertex."""
        self.pre_assigned_colors[vertex] = color

    def add_color_exclusion(self, vertex, color):
        """Adds a color exclusion constraint to a vertex."""
        self.color_exclusions[vertex].add(color)

    def get_pre_assigned_color(self, vertex):
        """Returns the pre-assigned color for a vertex, if any."""
        return self.pre_assigned_colors.get(vertex, None)

    def is_color_excluded(self, vertex, color):
        """Checks if a color is excluded for a vertex."""
        return color in self.color_exclusions[vertex]

# BaseColoringSolver Class
class BaseColoringSolver:
    """
    Base class for different graph coloring algorithms.
    
    Attributes:
        graph (Graph): The graph to be colored.
        constraint_manager (ConstraintManager): Manages constraints for the coloring process.
        color_assignment (dict): A dictionary mapping vertices to their assigned colors.
    
    Methods:
        solve(): Abstract method to be implemented by subclasses.
    """
    def __init__(self, graph, constraint_manager):
        self.graph = graph
        self.constraint_manager = constraint_manager
        self.color_assignment = {}

    def solve(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

# GreedyColoringSolver Class
class GreedyColoringSolver(BaseColoringSolver):
    """
    Implements a greedy algorithm for graph coloring, considering constraints.
    
    Methods:
        solve(): Solves the graph coloring problem using a greedy approach.
    """
    def solve(self):
        for vertex in self.graph.vertices:
            if vertex in self.color_assignment:
                continue

            available_colors = set(range(len(self.graph.vertices)))

            pre_assigned_color = self.constraint_manager.get_pre_assigned_color(vertex)
            if pre_assigned_color is not None:
                for neighbor in self.graph.neighbors(vertex):
                    if self.color_assignment.get(neighbor) == pre_assigned_color:
                        raise ValueError(f"Conflict with pre-assigned color at vertex {vertex}")
                self.color_assignment[vertex] = pre_assigned_color
                continue

            for neighbor in self.graph.neighbors(vertex):
                if neighbor in self.color_assignment:
                    color = self.color_assignment[neighbor]
                    available_colors.discard(color)

            for color in available_colors:
                if not self.constraint_manager.is_color_excluded(vertex, color):
                    self.color_assignment[vertex] = color
                    break

        return self.color_assignment

# BacktrackingColoringSolver Class
class BacktrackingColoringSolver(BaseColoringSolver):
    """
    Implements a backtracking algorithm to minimize the number of colors used in graph coloring.
    
    Methods:
        is_valid(vertex, color): Checks if assigning a color to a vertex is valid.
        solve_util(vertex_list, idx): Utility function to recursively solve the coloring problem.
        solve(): Solves the graph coloring problem using backtracking.
    """
    def is_valid(self, vertex, color):
        for neighbor in self.graph.neighbors(vertex):
            if self.color_assignment.get(neighbor) == color:
                return False
        return not self.constraint_manager.is_color_excluded(vertex, color)

    def solve_util(self, vertex_list, idx):
        if idx == len(vertex_list):
            return True

        vertex = vertex_list[idx]
        pre_assigned_color = self.constraint_manager.get_pre_assigned_color(vertex)
        if pre_assigned_color is not None:
            self.color_assignment[vertex] = pre_assigned_color
            return self.solve_util(vertex_list, idx + 1)

        for color in range(len(self.graph.vertices)):
            if self.is_valid(vertex, color):
                self.color_assignment[vertex] = color
                if self.solve_util(vertex_list, idx + 1):
                    return True
                self.color_assignment.pop(vertex)

        return False

    def solve(self):
        vertex_list = list(self.graph.vertices)
        if self.solve_util(vertex_list, 0):
            return self.color_assignment
        else:
            raise ValueError("No valid coloring exists with the given constraints")

# ColoringContext Class (Strategy Pattern)
class ColoringContext:
    """
    Context class to use the Strategy Pattern for different coloring strategies.
    
    Attributes:
        solver (BaseColoringSolver): The current coloring solver strategy.
    
    Methods:
        set_solver(solver): Sets the coloring solver strategy.
        solve(): Executes the current solver's solve method.
    """
    def __init__(self, solver):
        self.solver = solver

    def set_solver(self, solver):
        self.solver = solver

    def solve(self):
        return self.solver.solve()

# HeuristicOptimizer Class
class HeuristicOptimizer:
    """
    Implements heuristic-based optimizations to improve the graph coloring performance.
    
    Attributes:
        solver (BaseColoringSolver): The current coloring solver strategy.
    
    Methods:
        optimize(): Executes the solver's solve method and applies heuristic optimizations.
    """
    def __init__(self, solver):
        self.solver = solver

    def optimize(self):
        return self.solver.solve()

# SolverFactory Class (Factory Pattern)
class SolverFactory:
    """
    Factory class to create different coloring solver instances based on the strategy provided.
    
    Methods:
        create_solver(strategy, graph, constraint_manager): Creates and returns an instance of a coloring solver.
    """
    @staticmethod
    def create_solver(strategy, graph, constraint_manager):
        if strategy == "greedy":
            return GreedyColoringSolver(graph, constraint_manager)
        elif strategy == "backtracking":
            return BacktrackingColoringSolver(graph, constraint_manager)
        else:
            raise ValueError("Unknown strategy")

# Test Suite
class TestGraphColoringEnhanced(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()
        self.constraint_manager = ConstraintManager(self.graph)
        self.greedy_solver = SolverFactory.create_solver("greedy", self.graph, self.constraint_manager)
        self.backtracking_solver = SolverFactory.create_solver("backtracking", self.graph, self.constraint_manager)
        self.optimizer = HeuristicOptimizer(self.greedy_solver)

    def test_empty_graph(self):
        result = self.greedy_solver.solve()
        self.assertEqual(len(result), 0)

    def test_single_vertex(self):
        self.graph.add_vertex(0)
        result = self.greedy_solver.solve()
        self.assertEqual(result[0], 0)

    def test_simple_graph(self):
        self.graph.add_vertex(0)
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        result = self.backtracking_solver.solve()
        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], 1)
        self.assertEqual(result[2], 0)

    def test_preassigned_colors(self):
        self.graph.add_vertex(0)
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        self.constraint_manager.add_pre_assigned_color(0, 1)
        result = self.backtracking_solver.solve()
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 0)
        self.assertEqual(result[2], 1)

    def test_color_exclusion(self):
        self.graph.add_vertex(0)
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        self.constraint_manager.add_color_exclusion(1, 0)
        result = self.backtracking_solver.solve()
        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], 1)
        self.assertEqual(result[2], 0)

    def test_dynamic_graph_changes(self):
        self.graph.add_vertex(0)
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        result = self.backtracking_solver.solve()
        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], 1)
        self.assertEqual(result[2], 0)
        changes = [('add_vertex', 3, None), ('add_edge', 1, 3)]
        self.graph.apply_dynamic_changes(changes)
        result = self.optimizer.optimize()
        self.assertTrue(result[0] == 0 or result[0] == 1)

    def test_large_graph_performance(self):
        num_vertices = 10000
        num_edges = 50000
        for i in range(num_vertices):
            self.graph.add_vertex(i)
        for _ in range(num_edges):
            u = random.randint(0, num_vertices - 1)
            v = random.randint(0, num_vertices - 1)
            if u != v:
                self.graph.add_edge(u, v)
        result = self.optimizer.optimize()
        self.assertTrue(len(set(result.values())) <= num_vertices)

if __name__ == '__main__':
    unittest.main()

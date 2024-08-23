Advanced Graph Coloring with Constraints:

Project Description:
This project implements an advanced graph coloring algorithm that satisfies multiple constraints, including minimizing the number of colors used, respecting pre-assigned colors, handling color exclusions, adapting to dynamic changes in the graph, and optimizing the solution using heuristics. The project is developed using Object-Oriented Programming (OOP) principles in Python and incorporates design patterns such as Strategy and Factory.

Project Structure:
main.py: Contains the implementation of the Graph, ConstraintManager, ColoringSolver, HeuristicOptimizer, and various coloring strategies (e.g., GreedyColoring, BacktrackingColoring).
main.py: A comprehensive test suite to validate the graph coloring solution against various scenarios, including edge cases and large graphs.


README.md: This file, providing instructions and documentation.
Performance_Report.md: A report detailing the performance analysis and design decisions.
Setup Instructions

Prerequisites:
Python 3.8 or higher
No external libraries are required.

Installation:
Clone the repository or download the .zip file and extract it.
Navigate to the project directory.
bash
Copy code
cd main
Running the Code
Running the Main Script
To run the graph coloring algorithm, you can execute the main script:

bash
Copy code
main.py
This will run the default implementation of the algorithm and output the results.

Running the Test Suite
To validate the solution and check for correctness, run the test suite:

bash
Copy code
python -m unittest main.py 
This will execute all test cases and provide a summary of the results.

Explanation of Files:
graph_coloring.py: Contains all the classes and logic for the graph coloring solution.
main.py: Includes unit tests that cover various constraints, dynamic changes, and performance under large graphs.
README.md: Documentation and instructions.
Performance_Report.md: Detailed performance analysis and design choices.


How It Works:
The Graph class manages vertices and edges.
The ConstraintManager handles pre-assigned colors, color exclusions, and dynamic changes.
The ColoringSolver uses different strategies like GreedyColoring and BacktrackingColoring to solve the coloring problem.
The HeuristicOptimizer improves the solution by applying heuristic methods.
The Factory Pattern is used for creating solver objects dynamically.

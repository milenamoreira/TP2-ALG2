# Algoritmo branch and bound
import networkx as nx

def bnb_tsp(graph):
    with open("output.txt", 'w') as file:
        def calculate_partial_cost(path):
            return sum(graph[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))

        def calculate_total_cost(path):
            return calculate_partial_cost(path) + graph[path[-1]][path[0]]['weight']

        def create_node(unvisited_nodes, path, partial_cost):
            return {
                'unvisited_nodes': unvisited_nodes,
                'path': path,
                'partial_cost': partial_cost
            }

        best_solution = float('inf')
        best_path = []
        stack = [create_node(list(graph.nodes), [], 0)]

        while stack:
            current_node = stack.pop()

            if current_node['partial_cost'] >= best_solution:
                continue

            if not current_node['unvisited_nodes']:
                total_cost = calculate_total_cost(current_node['path'])
                if total_cost < best_solution:
                    best_solution = total_cost
                    best_path = current_node['path']
                    file.write(f"Best solution:{best_solution} Best path:{best_path}\n")
                continue

            for node in current_node['unvisited_nodes']:
                new_path = current_node['path'] + [node]
                new_partial_cost = calculate_partial_cost(new_path)

                new_node = create_node(
                    unvisited_nodes=[c for c in current_node['unvisited_nodes'] if c != node],
                    path=new_path,
                    partial_cost=new_partial_cost
                )

                stack.append(new_node)

        return best_solution

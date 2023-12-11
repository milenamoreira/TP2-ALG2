# Algoritmo de Christofides
import networkx as nx

def minimum_spanning_tree(G):
    return nx.minimum_spanning_tree(G)

def find_odd_degree_vertices(T):
    return [v for v, degree in T.degree() if degree % 2 != 0]

def minimum_weight_perfect_matching(G, odd_vertices):
    subgraph = G.subgraph(odd_vertices)
    return nx.algorithms.matching.min_weight_matching(subgraph)

def eulerian_circuit(H):
    return list(nx.eulerian_circuit(H))

def christofides(G):
    
    # Step 1: Create a minimum spanning tree T of G
    T = minimum_spanning_tree(G)
    
    # Step 2: Identify the set O of vertices with odd degree in T
    odd_vertices = find_odd_degree_vertices(T)
    
    # Step 3: Find a minimum-weight perfect matching M in the induced subgraph given by the vertices from O
    M = minimum_weight_perfect_matching(G, odd_vertices)
    
    # Step 4: Combine the edges of M and T to form a connected multigraph H
    H = nx.MultiGraph(T)
    H.add_edges_from(M)
    
    # Step 5: Form an Eulerian circuit in H
    eulerian_circuit_edges = eulerian_circuit(H)
    
    # Step 6: Make the circuit found in the previous step into a Hamiltonian circuit
    hamiltonian_circuit = [eulerian_circuit_edges[0][0]]
    for edge in eulerian_circuit_edges:
        if edge[1] not in hamiltonian_circuit:
            hamiltonian_circuit.append(edge[1])
    #print(hamiltonian_circuit)

    total = 0
    size = len(hamiltonian_circuit)
    for i in range(0,size):
        total += G.adj[hamiltonian_circuit[i]][hamiltonian_circuit[(i+1)%size]]['weight']
        #print(f"{hamiltonian_circuit[i]}:{hamiltonian_circuit[(i+1)%52]}:{total}")
    
    #print(total)
    return total

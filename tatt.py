# Algoritmo Twice around the tree
import networkx as nx

def dfs_preorder_mst(graph, node, parent, visited, preorder_order, weight):
    visited[node] = True

    preorder_order.append(node)

    for neighbor, edge_data in graph.adj[node].items():
        if not visited[neighbor] and neighbor != parent:
            weight[0] += edge_data['weight']
            dfs_preorder_mst(graph, neighbor, node, visited, preorder_order, weight)

def dfs_mst_preorder(graph, root):
    visited = {node: False for node in graph.nodes}
    order = []
    weight = [0]
    dfs_preorder_mst(graph, root, None, visited, order, weight)
    return order, weight[0]

def twice_around_the_tree(graph):
    # Passo 1: Selecionar um vértice v como raiz
    root = list(graph.nodes)[0]

    # Passo 2: Calcular a Árvore Geradora Mínima usando o algoritmo de Prim
    mst = nx.minimum_spanning_tree(graph, algorithm='prim', weight='weight')
    
    # Passo 3: Visitar os nós em pré-ordem usando DFS
    dfs_order = list(nx.dfs_preorder_nodes(mst, source=root))

    # Passo 4: Obter o tamanho do ciclo hamiltoniano
    total = 0
    size = len(dfs_order)
    for i in range(0,size):
        total += graph.adj[dfs_order[i]][dfs_order[(i+1)%size]]['weight']
    
    return total

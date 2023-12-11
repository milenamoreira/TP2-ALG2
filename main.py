import sys
import os
import math
import time
import networkx as nx
from memory_profiler import *
from tatt import twice_around_the_tree
from cr import christofides
from bnb import bnb_tsp

def read_tsp_instance(file_path, dimension):
    with open(file_path, "r") as file:
        lines = file.readlines()
    node_coordinates = [
        list(map(float, line.split()[1:])) for line in lines[6 : 6 + dimension]
    ]

    return node_coordinates


def create_graph(dimension, node_coordinates):
    G = nx.Graph()

    for i in range(1, dimension + 1):
        node_a = (node_coordinates[i - 1][0], node_coordinates[i - 1][1])
        G.add_node(i, pos=node_a)
        for j in range(1, dimension + 1):
            if i != j:
                node_b = (node_coordinates[j - 1][0], node_coordinates[j - 1][1])
                G.add_edge(i, j, weight=math.dist(node_a, node_b))

    return G

@profile
def run_twice(graph, bound, dataset):
    tempo_inicio = time.time()

    result = twice_around_the_tree(graph)

    tempo_fim = time.time()
    approximation = result / bound
    
    print(f"{dataset};twice around the tree;{bound};{result:.2f};{approximation:.2f};{(tempo_fim-tempo_inicio):.4f}")

@profile
def run_christofides(graph, bound, dataset):
    tempo_inicio = time.time()

    result = christofides(graph)

    tempo_fim = time.time()
    approximation = result / bound

    print(f"{dataset};christofides;{bound};{result:.2f};{approximation:.2f};{(tempo_fim-tempo_inicio):.4f}")

def load_dataset(nome, nodes, bound):
    nome_arquivo = f"raw/{nome}.tsp"
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "r") as dataset_file:
            node_coordinates = read_tsp_instance(nome_arquivo, nodes)
            graph = create_graph(nodes, node_coordinates)
            run_twice(graph, bound, nome)
            #run_christofides(graph, bound, nome)

    else:
        print(f"Arquivo {nome_arquivo} não encontrado.")


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_tsp_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    print("dataset;algoritmo;limiar;resultado;aproximacao;tempo")
    # Abra o arquivo com a lista de datasets
    with open(file_path, "r") as datasets_file:
        # Leia cada linha do arquivo
        for linha in datasets_file:
            # Divida a linha nodes espaços em branco
            partes = linha.split()

            # Verifique se a linha está no formato correto
            if len(partes) == 3:
                # Extraia as informações relevantes
                dataset_title, nodes, bound = partes

                # Chame a função para processar o dataset
                load_dataset(dataset_title, int(nodes), int(bound))
            else:
                print("Formato inválido na linha:", linha)


if __name__ == "__main__":
    main()

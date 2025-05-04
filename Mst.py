import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def Chiffrement(texte):
    texte = texte.lower()
    message = [ord(char) for char in texte]

    G = nx.Graph()
    G.add_nodes_from(range(len(message)))  # Utiliser indices pour les sommets
    for i in range(len(message)-1):
        poids = message[i] - message[i+1]
        G.add_edge(i, i+1, weight=poids)

    adj_matrix = nx.to_numpy_array(G, weight="weight")

    mst = nx.minimum_spanning_tree(G, algorithm="kruskal")
    mst_matrix = nx.to_numpy_array(mst, weight="weight")

    mat = np.dot(adj_matrix, mst_matrix)

    n = len(texte)
    K = np.array([[random.randint(1, 10) if j >= i else 0 for j in range(n)] for i in range(n)])

    final = np.dot(mat, K)

    return G, mst, final, adj_matrix, mst_matrix, K, message

def Dechiffrement(final, mst_matrix, K):
    K_inv = np.linalg.inv(K)
    mst_inv = np.linalg.inv(mst_matrix)

    approx_adj = np.dot(np.dot(final, K_inv), mst_inv)
    approx_adj = np.round(approx_adj).astype(int)

    n = approx_adj.shape[0]
    G_rec = nx.from_numpy_array(approx_adj)

    results = []
    for start in range(n):
        try:
            path = list(nx.dfs_preorder_nodes(G_rec, source=start))
        except:
            continue

        for start_val in range(97, 123):
            valeurs = {path[0]: start_val}
            valid = True
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                poids = approx_adj[u][v]
                valeurs[v] = valeurs[u] - poids

            ascii_values = [valeurs[i] for i in sorted(valeurs)]
            if all(97 <= val <= 122 for val in ascii_values):
                try:
                    texte = ''.join(chr(val) for val in ascii_values)
                    results.append(texte)
                except:
                    continue
    return list(set(results))  # Éliminer les doublons

def Visualiser(G, title):
    pos = nx.circular_layout(G)
    plt.figure(figsize=(4, 4))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=1000, edge_color="gray", font_size=12)
    edge_labels = {(u, v): d["weight"] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color="red")
    plt.title(title)
    plt.show()

# Exécution
texte = "crypto"
G, mst, final, adj_matrix, mst_matrix, K, message = Chiffrement(texte)
dechiffre = Dechiffrement(final, mst_matrix, K)

print("Texte original :", texte)
print("Texte déchiffré :", dechiffre)

# Visualisation
Visualiser(G, "Graphe original")
Visualiser(mst, "Arbre couvrant minimal")



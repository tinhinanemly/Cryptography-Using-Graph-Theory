import networkx as nx
import matplotlib.pyplot as plt
import random

def generate_graph(n,p):

  G = nx.erdos_renyi_graph(n, p)  # Génération du graphe

  return G



def insert_clique(G , size):

    nodes = list(G.nodes)
    print (nodes)
    #size of the clique
    clique_nodes = random.sample(nodes,size)

    for i in clique_nodes:
      for j in clique_nodes:
        if i!=j:
          G.add_edge(i,j)
    return clique_nodes

# je vais faire passer le message -> binaire
#bob connait clique nodes il sait comment dechiffrer et extraire le message

def chiffrement(message, clique_nodes):
  binary_message = ''.join(format(ord(c), '08b') for c in message)
  #print(binary_message)
    # Convertir en binaire
  if len(binary_message) > len(clique_nodes):
    print('message trop long')
  clique_nodes = sorted(clique_nodes) #pour que quand on dechiffre on le fait dans lordre aussi et donc le message est correct
  publicKey = {node: bit for node, bit in zip(clique_nodes, binary_message)}  # Associer bits et sommets
  print('public key',publicKey)
  return publicKey

def dechiffrement(encoded):
    # bob connait la clique
    binary_message = ''.join(encoded[node] for node in sorted(encoded.keys()))

    if len(binary_message) % 8 != 0:
      print('Error')

    chars = []
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]  # Extraire 8 bits
        #print(f"Bloc binaire extrait: {byte} → {int(byte, 2)} → {chr(int(byte, 2))}")  # Debug
        decimal_value = int(byte, 2)
        character = chr(decimal_value)
        chars.append(character)
    decoded_message = ''.join(chars)
    print("Message décodé:", decoded_message)
    return decoded_message


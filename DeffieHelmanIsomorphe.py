import networkx as nx
import random
import numpy as np
from hashlib import sha256
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

class DiffieHellmanGraphIsomorphism:
    def __init__(self, n_nodes=20, edge_probability=0.5):
        """
        Initialisation avec un graphe public G.
        n_nodes: nombre de sommets du graphe
        edge_probability: probabilité de création d'une arête entre deux sommets
        """
        # Création d'un graphe aléatoire public
        self.G_public = nx.gnp_random_graph(n_nodes, edge_probability)
        self.n_nodes = n_nodes
    
    def generate_permutation(self):
        """Génère une permutation aléatoire des nœuds"""
        return np.random.permutation(self.n_nodes)
    
    def apply_permutation(self, graph, permutation):
        """Applique une permutation aux nœuds d'un graphe"""
        mapping = {i: permutation[i] for i in range(self.n_nodes)}
        return nx.relabel_nodes(graph, mapping)
    
    def alice_key_generation(self):
        """Alice génère sa clé privée (permutation) et son graphe public"""
        self.alice_private_key = self.generate_permutation()
        self.alice_public_graph = self.apply_permutation(self.G_public, self.alice_private_key)
        return self.alice_public_graph
    
    def bob_key_generation(self):
        """Bob génère sa clé privée (permutation) et son graphe public"""
        self.bob_private_key = self.generate_permutation()
        self.bob_public_graph = self.apply_permutation(self.G_public, self.bob_private_key)
        return self.bob_public_graph
    
    def alice_compute_shared_key(self, bob_public_graph):
        """Alice calcule la clé partagée en appliquant sa permutation au graphe de Bob"""
        self.alice_shared_graph = self.apply_permutation(bob_public_graph, self.alice_private_key)
        return self.graph_to_key(self.alice_shared_graph)
    
    def bob_compute_shared_key(self, alice_public_graph):
        """Bob calcule la clé partagée en appliquant sa permutation au graphe d'Alice"""
        self.bob_shared_graph = self.apply_permutation(alice_public_graph, self.bob_private_key)
        return self.graph_to_key(self.bob_shared_graph)
    
    def graph_to_key(self, graph):
        """Convertit un graphe en clé cryptographique (hash)"""
        # Convertir la matrice d'adjacence en représentation binaire
        adj_matrix = nx.to_numpy_array(graph)
        binary_repr = ''.join(str(int(x)) for x in adj_matrix.flatten())
        
        # Appliquer une fonction de hachage pour obtenir une clé de longueur fixe
        return sha256(binary_repr.encode()).hexdigest()
    
    def visualize_graphs(self):
        """Visualise tous les graphes du protocole"""
        # Créer une figure avec une grille de sous-plots
        fig = plt.figure(figsize=(15, 10))
        gs = GridSpec(2, 2, figure=fig)
        
        # Positions des nœuds pour le graphe public
        # Utiliser le même layout pour tous les graphes pour mieux voir les changements
        pos_public = nx.spring_layout(self.G_public, seed=42)
        
        # 1. Graphe public initial
        ax1 = fig.add_subplot(gs[0, 0])
        nx.draw(self.G_public, pos_public, with_labels=True, node_color='lightblue', 
                node_size=500, font_weight='bold', ax=ax1)
        ax1.set_title('Graphe Public Initial (G)', fontsize=14)
        
        # 2. Graphe public d'Alice après permutation
        ax2 = fig.add_subplot(gs[0, 1])
        pos_alice = {i: pos_public[list(self.G_public.nodes())[i]] for i in range(self.n_nodes)}
        nx.draw(self.alice_public_graph, pos_alice, with_labels=True, node_color='lightgreen', 
                node_size=500, font_weight='bold', ax=ax2)
        ax2.set_title('Graphe Public d\'Alice (GA)', fontsize=14)
        
        # 3. Graphe public de Bob après permutation
        ax3 = fig.add_subplot(gs[1, 0])
        pos_bob = {i: pos_public[list(self.G_public.nodes())[i]] for i in range(self.n_nodes)}
        nx.draw(self.bob_public_graph, pos_bob, with_labels=True, node_color='salmon', 
                node_size=500, font_weight='bold', ax=ax3)
        ax3.set_title('Graphe Public de Bob (GB)', fontsize=14)
        
        # 4. Graphe de la clé partagée (selon Alice)
        ax4 = fig.add_subplot(gs[1, 1])
        pos_shared = {i: pos_public[list(self.G_public.nodes())[i]] for i in range(self.n_nodes)}
        nx.draw(self.alice_shared_graph, pos_shared, with_labels=True, node_color='gold', 
                node_size=500, font_weight='bold', ax=ax4)
        ax4.set_title('Graphe de la Clé Partagée', fontsize=14)
        
        plt.tight_layout()
        plt.suptitle('Visualisation du Protocole Diffie-Hellman basé sur l\'Isomorphisme de Graphes', fontsize=16)
        plt.subplots_adjust(top=0.9)
        plt.show()
        
        # Vérifier si les graphes partagés d'Alice et Bob sont isomorphes
        print("\nVérification de l'isomorphisme des graphes partagés:")
        if nx.is_isomorphic(self.alice_shared_graph, self.bob_shared_graph):
            print("✓ Les graphes partagés sont bien isomorphes.")
        else:
            print("✗ Erreur: Les graphes partagés ne sont pas isomorphes.")
        
        # Comparer les clés dérivées
        alice_key = self.graph_to_key(self.alice_shared_graph)
        bob_key = self.graph_to_key(self.bob_shared_graph)
        print(f"\nClé d'Alice: {alice_key[:16]}...")
        print(f"Clé de Bob:   {bob_key[:16]}...")
        if alice_key == bob_key:
            print("✓ Les clés cryptographiques sont identiques.")
        else:
            print("✗ Erreur: Les clés cryptographiques sont différentes.")

# Démonstration du protocole avec visualisation
def demo_protocol_with_visualization():
    print("Démonstration du protocole Diffie-Hellman basé sur l'isomorphisme de graphes")
    
    # Initialisation avec un nombre réduit de nœuds pour une meilleure visualisation
    protocol = DiffieHellmanGraphIsomorphism(n_nodes=8, edge_probability=0.4)
    print(f"Graphe public créé avec {protocol.n_nodes} nœuds")
    
    # Alice génère sa clé privée et son graphe public
    alice_public = protocol.alice_key_generation()
    print("Alice a généré sa clé privée (permutation) et son graphe public")
    
    # Bob génère sa clé privée et son graphe public
    bob_public = protocol.bob_key_generation()
    print("Bob a généré sa clé privée (permutation) et son graphe public")
    
    # Échange de graphes publics
    print("Alice et Bob échangent leurs graphes publics")
    
    # Alice calcule la clé partagée
    alice_shared_key = protocol.alice_compute_shared_key(bob_public)
    print(f"Alice a calculé la clé partagée: {alice_shared_key[:16]}...")
    
    # Bob calcule la clé partagée
    bob_shared_key = protocol.bob_compute_shared_key(alice_public)
    print(f"Bob a calculé la clé partagée: {bob_shared_key[:16]}...")
    
    # Vérification que les clés partagées sont identiques
    if alice_shared_key == bob_shared_key:
        print("Les clés partagées sont identiques !")
    else:
        print("Erreur: les clés partagées sont différentes.")
    
    # Visualisation des graphes
    print("\nAffichage des graphes...")
    protocol.visualize_graphs()

if __name__ == "__main__":
    # Définir une graine aléatoire pour la reproductibilité
    np.random.seed(42)
    random.seed(42)
    
    demo_protocol_with_visualization()
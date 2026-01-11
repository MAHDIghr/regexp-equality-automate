"""
Module simple de visualisation pour les automates
"""
import graphviz
import os

def draw_simple_automate(dot, automate, title):
    """Dessine un automate simplement dans un subgraph"""
    # Créer un nom unique pour le subgraph
    safe_title = ''.join(c if c.isalnum() else '_' for c in title)
    sub_name = f"cluster_{safe_title}"
    
    with dot.subgraph(name=sub_name) as sub:
        # Titre du subgraph
        sub.attr(label=title, fontsize='10', labelloc='t')
        sub.attr(rankdir='LR')
        
        # Nœud invisible pour l'état initial
        sub.node(f"{sub_name}_start", '', shape='none')
        
        # Dessiner tous les états
        for i in range(automate.n):
            node_name = f"{sub_name}_q{i}"
            is_final = i in automate.final
            shape = 'doublecircle' if is_final else 'circle'
            
            # Style spécial pour l'état initial (0)
            if i == 0:
                sub.node(node_name, str(i), shape=shape, style='bold')
            else:
                sub.node(node_name, str(i), shape=shape)
        
        # Flèche de l'état initial
        sub.edge(f"{sub_name}_start", f"{sub_name}_q0")
        
        # Regrouper les transitions
        transitions_by_pair = {}
        for (src, char), dests in automate.transition.items():
            for dest in dests:
                pair = (src, dest)
                if pair not in transitions_by_pair:
                    transitions_by_pair[pair] = []
                # Remplacer 'E' par epsilon
                label = char if char != 'E' else 'ε'
                transitions_by_pair[pair].append(label)
        
        # Dessiner les transitions
        for (src, dest), labels in transitions_by_pair.items():
            # Simplifier le label
            if len(labels) == 1:
                edge_label = labels[0]
            else:
                edge_label = ','.join(sorted(labels))
            
            sub.edge(f"{sub_name}_q{src}", f"{sub_name}_q{dest}", 
                    label=edge_label, fontsize='8')

def save_pdf(automates_list, filename="tests_automates.pdf"):
    """
    Crée un PDF avec tous les automates de la liste
    
    Args:
        automates_list: liste de tuples (titre, automate)
        filename: chemin du fichier PDF à créer
    """
    print(f"📊 Création du PDF: {filename}")
    
    # Créer le graphe
    dot = graphviz.Digraph(comment='Tests des automates')
    dot.attr(compound='true')
    dot.attr(ranksep='0.8')
    dot.attr(nodesep='0.5')
    
    # Organiser en grille 2xN
    for i, (title, aut) in enumerate(automates_list):
        draw_simple_automate(dot, aut, title)
    
    # Configurer la taille
    dot.attr(size='11,16.5')  # Format A4 paysage
    dot.attr(dpi='200')
    
    # Sauvegarder
    dot.render(filename.replace('.pdf', ''), format='pdf', cleanup=True)
    print(f"✅ PDF sauvegardé: {filename}")

"""
Programme principal pour tester les classes Mot et Langage.
"""

from interface import InterfaceMotLangage

def main():
    """Fonction principale."""
    print("Bienvenue dans le programme de test des classes Mot et Langage!")
    print("Lancement de l'interface en ligne de commande...\n")
    
    # Création et lancement de l'interface
    interface = InterfaceMotLangage()
    interface.cmdloop()

if __name__ == "__main__":
    main()
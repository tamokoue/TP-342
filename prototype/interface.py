"""
Module implémentant une interface simple pour tester les classes Mot et Langage.
"""

import cmd
from Mot import Mot
from Langage import Langage, LangageReconnaissable
from Automate import AFND, AFDC, AFNS

class InterfaceMotLangage(cmd.Cmd):
    """Interface en ligne de commande pour tester les classes Mot et Langage."""
    
    intro = "Interface pour tester les classes Mot et Langage. Tapez 'help' pour la liste des commandes."
    prompt = "(mot/langage)> "
    
    def __init__(self):
        super().__init__()
        self.mots = {}
        self.langages = {}
        self.automates = {}
    
    def do_creer_mot(self, arg):
        """Crée un mot: creer_mot <nom> <contenu> [alphabet]"""
        args = arg.split()
        if len(args) < 2:
            print("Usage: creer_mot <nom> <contenu> [alphabet]")
            return
        
        nom = args[0]
        contenu = args[1]
        alphabet = set(args[2:]) if len(args) > 2 else None
        
        self.mots[nom] = Mot(contenu, alphabet)
        print(f"Mot '{nom}' créé: {contenu}")
    
    def do_iteration(self, arg):
        """Étoile de Kleene d'un langage: iteration <nom_source> <nom_resultat>"""
        args = arg.split()
        if len(args) != 2:
            print("Usage: iteration <nom_source> <nom_resultat>")
            return
        
        source, resultat = args
        if source not in self.langages:
            print(f"Langage '{source}' non trouvé.")
            return
        
        self.langages[resultat] = self.langages[source].iteration_sur_langages()
        print(f"Itération de Kleene enregistrée dans '{resultat}'")

    def do_taille(self, arg):
        """Affiche la taille d'un langage: taille <nom_langage>"""
        if arg not in self.langages:
            print(f"Langage '{arg}' non trouvé.")
            return
        
        taille = self.langages[arg].taille_du_langage()
        print(f"Taille du langage '{arg}': {taille}")
    
    def do_afficher_mot(self, arg):
        """Affiche un mot: afficher_mot <nom>"""
        if arg not in self.mots:
            print(f"Mot '{arg}' non trouvé.")
            return
        print(f"Mot '{arg}': {self.mots[arg]}")
    
    def do_longueur_mot(self, arg):
        """Affiche la longueur d'un mot: longueur_mot <nom>"""
        if arg not in self.mots:
            print(f"Mot '{arg}' non trouvé.")
            return
        print(f"Longueur de '{arg}': {self.mots[arg].longueur()}")
    
    def do_creer_langage(self, arg):
        """Crée un langage: creer_langage <nom> <mot1> <mot2> ... [--alphabet a b c]"""
        args = arg.split()
        if not args:
            print("Usage: creer_langage <nom> <mot1> <mot2> ... [--alphabet a b c]")
            return
        
        nom = args[0]
        mots_args = []
        alphabet = None
        i = 1
        
        # Traitement des arguments optionnels
        while i < len(args):
            if args[i] == "--alphabet":
                alphabet = set(args[i+1:])
                break
            mots_args.append(args[i])
            i += 1
        
        # Création des mots
        mots = set()
        for mot_str in mots_args:
            # Vérifie si le mot existe déjà dans la collection
            if mot_str in self.mots:
                mots.add(self.mots[mot_str])
            else:
                # Crée un nouveau mot avec l'alphabet spécifié ou déduit
                new_mot = Mot(mot_str, alphabet)
                self.mots[mot_str] = new_mot  # Stocke le mot pour réutilisation
                mots.add(new_mot)
        
        self.langages[nom] = Langage(mots, alphabet)
        print(f"Langage '{nom}' créé avec {len(mots)} mots.")
    
    def do_afficher_langage(self, arg):
        """Affiche un langage: afficher_langage <nom>"""
        if arg not in self.langages:
            print(f"Langage '{arg}' non trouvé.")
            return
        print(f"Langage '{arg}': {self.langages[arg]}")
    
    def do_concatenation(self, arg):
        """Concatène deux langages: concatenation <nom1> <nom2> <resultat>"""
        args = arg.split()
        if len(args) != 3:
            print("Usage: concatenation <nom1> <nom2> <resultat>")
            return
        
        nom1, nom2, resultat = args
        if nom1 not in self.langages or nom2 not in self.langages:
            print("Un des langages n'existe pas.")
            return
        
        self.langages[resultat] = self.langages[nom1] * self.langages[nom2]
        print(f"Résultat de la concaténation enregistré dans '{resultat}'")
    
    def do_union(self, arg):
        """Union de deux langages: union <nom1> <nom2> <resultat>"""
        args = arg.split()
        if len(args) != 3:
            print("Usage: union <nom1> <nom2> <resultat>")
            return
        
        nom1, nom2, resultat = args
        if nom1 not in self.langages or nom2 not in self.langages:
            print("Un des langages n'existe pas.")
            return
        
        self.langages[resultat] = self.langages[nom1] + self.langages[nom2]
        print(f"Résultat de l'union enregistré dans '{resultat}'")
    
    def do_quitter(self, arg):
        """Quitte l'interface: quitter"""
        print("Au revoir!")
        return True
    
    def do_creer_automate(self, arg):
        """Crée un automate interactivement: creer_automate <nom> <type> <alphabet> <états> <initial> <finaux> <nb_transitions>"""
        args = arg.split()
        if len(args) < 7:
            print("Usage: creer_automate <nom> <type> <alphabet> <états> <initial> <finaux> <nb_transitions>")
            print("Types disponibles: AFD, AFN, AFNS")
            return
        
        nom = args[0]
        type_auto = args[1].upper()
        alphabet = set(args[2].split(','))
        etats = set(args[3].split(','))
        initial = args[4]
        finaux = set(args[5].split(','))
        nb_transitions = int(args[6])

        # Validation des données
        if initial not in etats:
            print(f"Erreur: l'état initial '{initial}' n'existe pas")
            return
        if not finaux.issubset(etats):
            print(f"Erreur: des états finaux {finaux - etats} n'existent pas")
            return

        # Création de l'automate
        if type_auto == "AFD":
            self.automates[nom] = AFDC(alphabet, etats, initial, finaux)
        elif type_auto == "AFN":
            self.automates[nom] = AFND(alphabet, etats, initial, finaux)
        elif type_auto == "AFNS":
            self.automates[nom] = AFNS(alphabet, etats, initial, finaux)
        else:
            print("Type d'automate invalide")
            return

        # Ajout interactif des transitions
        print(f"\nCréation de l'automate {type_auto} '{nom}'")
        print("Alphabet:", alphabet)
        print("États:", etats)
        print(f"Ajout des {nb_transitions} transitions (format: source symbole cible):")
        
        for i in range(1, nb_transitions + 1):
            while True:
                transition = input(f"Transition {i}/{nb_transitions} > ")
                if transition.lower() == 'annuler':
                    del self.automates[nom]
                    print("Création annulée")
                    return
                
                parts = transition.split()
                if len(parts) != 3:
                    print("Format invalide. Utilisez: source symbole cible")
                    continue
                    
                source, symbole, cible = parts
                if source not in etats:
                    print(f"Erreur: état source '{source}' invalide")
                    continue
                if symbole not in alphabet and not (type_auto == "AFNS" and symbole == 'ε'):
                    print(f"Erreur: symbole '{symbole}' invalide")
                    continue
                if cible not in etats:
                    print(f"Erreur: état cible '{cible}' invalide")
                    continue
                    
                self.automates[nom].ajouter_transition(source, symbole, cible)
                print(f"Ajoutée: {source} --{symbole}--> {cible}")
                break

        print(f"\nAutomate '{nom}' créé avec {nb_transitions} transitions")
        print("Utilisez 'afficher_automate' pour voir sa structure")

    def do_ajouter_transition(self, arg):
        """Ajoute une transition: ajouter_transition <automate> <source> <symbole> <cible>"""
        args = arg.split()
        if len(args) != 4:
            print("Usage: ajouter_transition <automate> <source> <symbole> <cible>")
            return
        
        nom, source, symbole, cible = args
        if nom not in self.automates:
            print(f"Automate '{nom}' non trouvé")
            return
        
        self.automates[nom].ajouter_transition(source, symbole, cible)
        print(f"Transition ajoutée: {source} --{symbole}--> {cible}")
        
        
   
                
    def do_afficher_automate(self, arg):
        """Affiche la structure d'un automate: afficher_automate <nom>"""
        if not arg:
            print("Usage: afficher_automate <nom>")
            return
        
        if arg not in self.automates:
            print(f"Automate '{arg}' non trouvé")
            return
        
        automate = self.automates[arg]
        
        # Déterminer le type de l'automate
        if isinstance(automate, AFDC):
            type_auto = "AFD"
        elif isinstance(automate, AFND):
            type_auto = "AFND"
        elif isinstance(automate, AFNS):
            type_auto = "AFNS"
        else:
            type_auto = "Automate"
        
        print(f"\nAutomate {arg} ({type_auto}):")
        print(f"Alphabet: {automate.alphabet}")
        print(f"États: {automate.etats}")
        print(f"État initial: {automate.etat_initial}")
        print(f"États finaux: {automate.etats_finaux}")
        
        print("\nTransitions:")
        for source in automate.transitions:
            for symbole in automate.transitions[source]:
                for cible in automate.transitions[source][symbole]:
                    print(f"  {source} --{symbole}--> {cible}")
                    
                
    def do_supprimer_automate(self, arg):
        """Supprime un automate: supprimer_automate <nom>"""
        if arg in self.automates:
            del self.automates[arg]
            print(f"Automate '{arg}' supprimé")
        else:
            print(f"Automate '{arg}' non trouvé")

    def do_chemin_mot(self, arg):
        """Affiche le chemin pour un mot: chemin_mot <automate> <mot>"""
        args = arg.split()
        if len(args) < 2:
            print("Usage: chemin_mot <automate> <mot>")
            return
        
        nom = args[0]
        mot = ''.join(args[1:])
        
        if nom not in self.automates:
            print(f"Automate '{nom}' non trouvé")
            return
        
        accepte, chemin = self.automates[nom].reconnaitre_mot_avec_chemin(mot)
        print(f"Chemin pour '{mot}':")
        for step in chemin:
            print(f"{step[0]} --{step[1]}--> {step[2]}")
        print(f"Le mot est {'accepté' if accepte else 'rejeté'}")
            
        
    def do_reconnaitre_mot(self, arg):
        """Teste la reconnaissance d'un mot: reconnaitre_mot <automate> <mot>"""
        args = arg.split()
        if len(args) < 2:
            print("Usage: reconnaitre_mot <automate> <mot>")
            return
        
        nom = args[0]
        mot = ''.join(args[1:])
        
        if nom not in self.automates:
            print(f"Automate '{nom}' non trouvé")
            return
        
        resultat = self.automates[nom].reconnaitre_mot(mot)
        print(f"Le mot '{mot}' est {'reconnu' if resultat else 'non reconnu'} par l'automate '{nom}'")
     
        
    def do_help(self, arg):
        """Affiche l'aide: help [commande]"""
        if arg:
            super().do_help(arg)
        else:
            print("\nCommandes disponibles:")
            print("=== Opérations sur les mots ===")
            print("  creer_mot <nom> <contenu> [alphabet] - Crée un mot")
            print("  afficher_mot <nom> - Affiche un mot")
            print("  longueur_mot <nom> - Affiche la longueur d'un mot")
            
            print("\n=== Opérations sur les langages ===")
            print("  creer_langage <nom> <mot1> <mot2> ... [--alphabet a b c] - Crée un langage")
            print("  afficher_langage <nom> - Affiche un langage")
            print("  taille <nom> - Affiche la taille du langage")
            print("  iteration <source> <resultat> - Étoile de Kleene d'un langage")
            print("  concatenation <nom1> <nom2> <resultat> - Concatène deux langages")
            print("  union <nom1> <nom2> <resultat> - Union de deux langages")
            
            print("\n=== Commandes Automates ===")
            print("  creer_automate <nom> <type> <a,b> <q0,q1> <q0> <q1> <nombre de transistion> - Crée un automate")
            print("  reconnaitre_mot <nom> <mot> - Teste un mot")
            print("  chemin_mot <nom> <mot> - Affiche le chemin d'un mot")
            
            print("\n=== Général ===")
            print("  quitter - Quitte l'interface")
            print("\nTapez 'help <commande>' pour plus d'informations sur une commande.")
            

def main():
    """Fonction principale pour lancer l'interface."""
    interface = InterfaceMotLangage()
    interface.cmdloop()

if __name__ == "__main__":
    main()
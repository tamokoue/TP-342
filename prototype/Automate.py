from typing import Set, Dict, List, Optional ,Tuple

class Automate:
    """Classe de base pour tous les types d'automates."""
    
    def __init__(self, alphabet: Set[str], etats: Set[str], etat_initial: str, etats_finaux: Set[str]):
        self.alphabet = alphabet
        self.etats = etats
        self.etat_initial = etat_initial
        self.etats_finaux = etats_finaux
        self.transitions: Dict[str, Dict[str, Set[str]]] = {
            etat: {symb: set() for symb in alphabet}
            for etat in etats
        }
    
    def ajouter_transition(self, source: str, symbole: str, cible: str) -> None:
        """Ajoute une transition à l'automate."""
        if symbole not in self.alphabet:
            raise ValueError(f"Symbole {symbole} non présent dans l'alphabet")
        if source not in self.etats or cible not in self.etats:
            raise ValueError("État source ou cible invalide")
        self.transitions[source][symbole].add(cible)
    
    
    def obtenir_transitions(self, etat: str, symbole: str) -> Set[str]:
        """Retourne les états cibles pour une transition donnée (nouvelle méthode)"""
        return self.transitions[etat].get(symbole, set()).copy()  # Retourne une copie
    
    def reconnaitre_mot(self, mot: str) -> bool:
        """Version corrigée qui ne modifie pas les transitions"""
        etat_courant = {self.etat_initial}
        
        for symbole in mot:
            if symbole not in self.alphabet:
                return False
            
            nouveaux_etats = set()
            for etat in etat_courant:
                nouveaux_etats.update(self.obtenir_transitions(etat, symbole))
            
            if not nouveaux_etats:
                return False
            etat_courant = nouveaux_etats
        
        return any(etat in self.etats_finaux for etat in etat_courant)
    
    def reconnaitre_mot_avec_chemin(self, mot: str) -> Tuple[bool, List[Tuple[str, str, str]]]:
        """Version corrigée avec chemin"""
        chemin = []
        current_states = {self.etat_initial}
        
        for symbole in mot:
            next_states = set()
            for state in current_states:
                targets = self.obtenir_transitions(state, symbole)
                next_states.update(targets)
                for target in targets:
                    chemin.append((state, symbole, target))
            if not next_states:
                return False, chemin
            current_states = next_states
        
        accepte = any(state in self.etats_finaux for state in current_states)
        return accepte, chemin
    
    
class AFDC(Automate):
    """Automate Fini Déterministe Complet."""
    
    def ajouter_transition(self, source: str, symbole: str, cible: str) -> None:
        if len(self.transitions[source][symbole]) > 0:
            raise ValueError("Un ADC ne peut avoir qu'une transition par symbole")
        super().ajouter_transition(source, symbole, cible)
    
    def reconnaitre_mot(self, mot: str) -> bool:
        etat_courant = self.etat_initial
        
        for symbole in mot:
            if symbole not in self.alphabet:
                return False
            next_states = self.obtenir_transitions(etat_courant, symbole)
            if len(next_states) != 1:
                return False
            etat_courant = next(iter(next_states))  # Ne modifie pas l'ensemble
        
        return etat_courant in self.etats_finaux
    
class AFND(Automate):
    """Automate Fini Non Déterministe."""
    
    def reconnaitre_mot(self, mot: str) -> bool:
        """Reconnaît un mot dans un AFND."""
        etat_courant = {self.etat_initial}
        
        for symbole in mot:
            if symbole not in self.alphabet:
                return False
            
            nouveaux_etats = set()
            for etat in etat_courant:
                nouveaux_etats.update(self.transitions[etat][symbole])
            
            if not nouveaux_etats:
                return False
            etat_courant = nouveaux_etats
        
        return any(etat in self.etats_finaux for etat in etat_courant)

class AFNS(Automate):
    """Automate Fini Non Déterministe avec ε-transitions."""
    
    def __init__(self, alphabet: Set[str], etats: Set[str], etat_initial: str, etats_finaux: Set[str]):
        super().__init__(alphabet, etats, etat_initial, etats_finaux)
        self.epsilon = 'ε'
        self.alphabet.add(self.epsilon)
    
    def fermeture_epsilon(self, etats: Set[str]) -> Set[str]:
        """Calcule la fermeture ε d'un ensemble d'états."""
        fermeture = set(etats)
        pile = list(etats)
        
        while pile:
            etat = pile.pop()
            for etat_cible in self.transitions[etat][self.epsilon]:
                if etat_cible not in fermeture:
                    fermeture.add(etat_cible)
                    pile.append(etat_cible)
        
        return fermeture
    
    def reconnaitre_mot(self, mot: str) -> bool:
        """Reconnaît un mot dans un AFNS."""
        etat_courant = self.fermeture_epsilon({self.etat_initial})
        
        for symbole in mot:
            if symbole not in self.alphabet:
                return False
            
            # Transition normale
            nouveaux_etats = set()
            for etat in etat_courant:
                nouveaux_etats.update(self.transitions[etat][symbole])
            
            # Fermeture epsilon après transition
            etat_courant = self.fermeture_epsilon(nouveaux_etats)
            
            if not etat_courant:
                return False
        
        return any(etat in self.etats_finaux for etat in etat_courant)
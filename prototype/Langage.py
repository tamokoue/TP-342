"""
Module implémentant la classe Langage et ses opérations.
Un langage est un ensemble de mots sur un alphabet donné.
"""

from typing import Set, List, Dict, Optional, Union, Any, Tuple
from Mot import Mot

class Langage:
    """
    Classe représentant un langage (ensemble de mots).
    """
    
    def __init__(self, mots: Optional[Set[Mot]] = None, alphabet: Optional[Set[str]] = None) -> None:
        """
        Initialise un langage.
        
        Args:
            mots: Ensemble de mots du langage (peut être None)
            alphabet: Alphabet du langage (peut être None)
        """
        self.mots = mots if mots else set()
        self.alphabet = alphabet if alphabet else self._calculer_alphabet()
        
    def _calculer_alphabet(self) -> Set[str]:
        """Calcule l'alphabet à partir des mots du langage."""
        alphabet = set()
        for mot in self.mots:
            alphabet.update(mot.alphabet())
        return alphabet
    
    def taille_du_langage(self) -> Union[int, float]:
        """Retourne la taille du langage (peut être infinie)."""
        return len(self.mots)
    
    def reunion_finie_des_langages(self, autres_langages: List['Langage']) -> 'Langage':
        """Réunion finie de langages."""
        nouveaux_mots = set(self.mots)
        nouveau_alphabet = set(self.alphabet)
        for langage in autres_langages:
            nouveaux_mots.update(langage.mots)
            nouveau_alphabet.update(langage.alphabet)
        return Langage(nouveaux_mots, nouveau_alphabet)
    
    def concatenation_des_langages(self, autre_langage: 'Langage') -> 'Langage':
        """Concaténation de deux langages."""
        nouveaux_mots = set()
        nouveau_alphabet = self.alphabet.union(autre_langage.alphabet)
        for mot1 in self.mots:
            for mot2 in autre_langage.mots:
                nouveaux_mots.add(mot1.concatenation(mot2))
        return Langage(nouveaux_mots, nouveau_alphabet)
    
    def iteration_sur_langages(self) -> 'Langage':
        """Étoile de Kleene du langage."""
        # Implémentation simplifiée (ne gère pas toutes les puissances)
        nouveaux_mots = {Mot("", self.alphabet)}  # Mot vide
        for mot in self.mots:
            nouveaux_mots.add(mot)
            nouveaux_mots.add(mot.concatenation(mot))  # Seulement le carré pour l'exemple
        return Langage(nouveaux_mots, self.alphabet)
    
    def quotient_de_langages(self, autre_langage: 'Langage') -> 'Langage':
        """Quotient de langages (simplifié)."""
        # Implémentation simplifiée
        nouveaux_mots = set()
        for mot1 in self.mots:
            for mot2 in autre_langage.mots:
                if mot1.contenu.endswith(mot2.contenu):
                    nouveaux_mots.add(Mot(mot1.contenu[:-len(mot2.contenu)], self.alphabet))
        return Langage(nouveaux_mots, self.alphabet)
    
    def lemme_darden(self) -> bool:
        """Application simplifiée du lemme d'Arden."""
        # Implémentation simplifiée pour l'exemple
        mot_vide = Mot("", self.alphabet)
        return mot_vide in self.mots
    
    def resolution_partielle_gauss(self, systeme_equations: List[str]) -> Dict[str, 'Langage']:
        """Résolution partielle par méthode de Gauss (simplifiée)."""
        # Implémentation simplifiée pour l'exemple
        solutions = {}
        for eq in systeme_equations:
            solutions[eq] = self
        return solutions
    
    def substitution_gauss(self, variable: str, expression: 'Langage') -> 'Langage':
        """Substitution dans un système d'équations (simplifiée)."""
        # Implémentation simplifiée pour l'exemple
        return self
    
    def type_de_langage(self) -> str:
        """Détermine le type du langage dans la hiérarchie de Chomsky (simplifié)."""
        # Implémentation simplifiée
        return "Type 3 (Régulier)"  # Toujours régulier dans cette implémentation simplifiée
    
    def __add__(self, autre: 'Langage') -> 'Langage':
        """Surcharge de + pour l'union."""
        return self.reunion_finie_des_langages([autre])
    
    def __mul__(self, autre: 'Langage') -> 'Langage':
        """Surcharge de * pour la concaténation."""
        return self.concatenation_des_langages(autre)
    
    def __sub__(self, autre: 'Langage') -> 'Langage':
        """Surcharge de - pour la différence."""
        nouveaux_mots = self.mots - autre.mots
        return Langage(nouveaux_mots, self.alphabet)
    
    def __and__(self, autre: 'Langage') -> 'Langage':
        """Surcharge de & pour l'intersection."""
        nouveaux_mots = self.mots & autre.mots
        return Langage(nouveaux_mots, self.alphabet)
    
    def __or__(self, autre: 'Langage') -> 'Langage':
        """Surcharge de | pour l'union."""
        return self.__add__(autre)
    
    def __str__(self) -> str:
        """Représentation textuelle du langage."""
        mots_str = [str(mot) for mot in self.mots]
        return f"Langage(mots={mots_str}, alphabet={self.alphabet})"


class LangageReconnaissable(Langage):
    """
    Langage reconnaissable (régulier).
    Hérite de Langage et implémente les propriétés de clôture.
    """
    
    def __init__(self, mots: Optional[Set[Mot]] = None, alphabet: Optional[Set[str]] = None,
                 automate: Optional[Any] = None) -> None:
        """Initialise un langage reconnaissable."""
        super().__init__(mots, alphabet)
        self.automate = automate
    
    def complementation(self) -> 'LangageReconnaissable':
        """Clôture par complémentation (simplifiée)."""
        # Implémentation simplifiée
        tous_mots_possibles = {Mot("a"), Mot("b")}  # Exemple simplifié
        nouveaux_mots = tous_mots_possibles - self.mots
        return LangageReconnaissable(nouveaux_mots, self.alphabet)
    
    def union_ensembliste(self, autre: 'LangageReconnaissable') -> 'LangageReconnaissable':
        """Clôture par union ensembliste."""
        return LangageReconnaissable(self.mots.union(autre.mots), self.alphabet.union(autre.alphabet))
    
    def intersection_ensembliste(self, autre: 'LangageReconnaissable') -> 'LangageReconnaissable':
        """Clôture par intersection ensembliste."""
        return LangageReconnaissable(self.mots.intersection(autre.mots), self.alphabet)
    
    def miroir(self) -> 'LangageReconnaissable':
        """Clôture par miroir."""
        nouveaux_mots = {Mot(mot.contenu[::-1], mot.alphabet()) for mot in self.mots}
        return LangageReconnaissable(nouveaux_mots, self.alphabet)
    
    def concatenation(self, autre: 'LangageReconnaissable') -> 'LangageReconnaissable':
        """Clôture par concaténation."""
        return LangageReconnaissable(super().concatenation_des_langages(autre).mots, self.alphabet.union(autre.alphabet))
    
    def etoile(self) -> 'LangageReconnaissable':
        """Clôture par étoile (étoile de Kleene)."""
        return LangageReconnaissable(super().iteration_sur_langages().mots, self.alphabet)
    
    def regex_vers_langage(self, expression_reguliere: str) -> None:
        """Construit le langage depuis une expression régulière (simplifié)."""
        # Implémentation simplifiée
        if expression_reguliere == "a*":
            self.mots = {Mot(""), Mot("a"), Mot("aa")}  # Exemple simplifié
            self.alphabet = {"a"}
    
    def langage_vers_regex(self) -> str:
        """Convertit le langage en expression régulière (simplifié)."""
        # Implémentation simplifiée
        if len(self.mots) == 1 and Mot("") in self.mots:
            return "ε"
        return "a*"  # Exemple simplifié
    
    def theoreme_kleene_construction(self, automate: Any) -> str:
        """Application du théorème de Kleene pour la construction (simplifié)."""
        return "a*"  # Exemple simplifié
    
    def lemme_pompage_verification(self, mot: Mot) -> Tuple[bool, Dict[str, Any]]:
        """Vérifie le lemme de pompage pour un mot (simplifié)."""
        # Implémentation simplifiée
        return (True, {"x": "a", "y": "b", "z": "c"})  # Exemple
    
    def lemme_pompage_application(self) -> bool:
        """Application du lemme de pompage au langage (simplifié)."""
        return True  # Exemple
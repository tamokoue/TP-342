"""
Module implémentant la classe Mot et ses opérations.
Un mot est une séquence de symboles sur un alphabet donné.
"""

from typing import Set, List, Optional, Dict, Any, Tuple
from abc import ABC, abstractmethod

class Mot:
    """
    Classe représentant un mot sur un alphabet.
    """
    
    def __init__(self, contenu: str = "", alphabet: Optional[Set[str]] = None) -> None:
        """
        Initialise un mot.
        
        Args:
            contenu: Chaîne de caractères représentant le mot
            alphabet: Alphabet du mot (peut être None si non spécifié)
        """
        self.contenu = contenu
        self.alphabet_mot = alphabet if alphabet else set(contenu)
        
    def longueur(self) -> int:
        """Retourne la longueur du mot."""
        return len(self.contenu)
    
    def adjonction_occurrence_droite(self, symbole: str) -> 'Mot':
        """Ajoute une occurrence d'un symbole à droite."""
        if symbole not in self.alphabet_mot:
            self.alphabet_mot.add(symbole)
        return Mot(self.contenu + symbole, self.alphabet_mot)
    
    def adjonction_occurrence_gauche(self, symbole: str) -> 'Mot':
        """Ajoute une occurrence d'un symbole à gauche."""
        if symbole not in self.alphabet_mot:
            self.alphabet_mot.add(symbole)
        return Mot(symbole + self.contenu, self.alphabet_mot)
    
    def concatenation(self, autre_mot: 'Mot') -> 'Mot':
        """Concatène avec un autre mot."""
        nouvel_alphabet = self.alphabet_mot.union(autre_mot.alphabet())
        return Mot(self.contenu + autre_mot.contenu, nouvel_alphabet)
    
    def liste_sous_mots(self) -> List['Mot']:
        """Retourne la liste de tous les sous-mots."""
        sous_mots = [Mot("", self.alphabet_mot)]
        n = len(self.contenu)
        for i in range(n):
            for j in range(i + 1, n + 1):
                sous_mots.append(Mot(self.contenu[i:j], self.alphabet_mot))
        return sous_mots
    
    def facteur_gauche(self, longueur: int) -> 'Mot':
        """Retourne le facteur gauche de longueur donnée."""
        if longueur > len(self.contenu):
            return Mot(self.contenu, self.alphabet_mot)
        return Mot(self.contenu[:longueur], self.alphabet_mot)
    
    def facteur_droit(self, longueur: int) -> 'Mot':
        """Retourne le facteur droit de longueur donnée."""
        if longueur > len(self.contenu):
            return Mot(self.contenu, self.alphabet_mot)
        return Mot(self.contenu[-longueur:], self.alphabet_mot)
    
    def est_periodique(self, periode: int) -> bool:
        """Vérifie si le mot est périodique avec la période donnée."""
        if periode <= 0 or periode > len(self.contenu):
            return False
        for i in range(len(self.contenu) - periode):
            if self.contenu[i] != self.contenu[i + periode]:
                return False
        return True
    
    def est_primitif(self) -> bool:
        """Vérifie si le mot est primitif (non puissance d'un autre mot)."""
        n = len(self.contenu)
        for p in range(1, n // 2 + 1):
            if n % p == 0 and self.est_periodique(p):
                return False
        return True
    
    def alphabet(self) -> Set[str]:
        """Retourne l'alphabet du mot."""
        return self.alphabet_mot
    
    def est_reconnaissable(self, automate: Any) -> bool:
        """Vérifie si le mot est reconnaissable par un automate (à implémenter)."""
        # Cette méthode nécessite une implémentation d'automate
        return False
    
    def sont_equivalents(self, autre_mot: 'Mot', automate: Any) -> bool:
        """Vérifie si deux mots sont équivalents relativement à un automate."""
        # Cette méthode nécessite une implémentation d'automate
        return False
    
    def __str__(self) -> str:
        """Représentation textuelle du mot."""
        return self.contenu
    
    def __eq__(self, autre: 'Mot') -> bool:
        """Égalité entre mots."""
        return self.contenu == autre.contenu
    
    def __add__(self, autre: 'Mot') -> 'Mot':
        """Surcharge de + pour la concaténation."""
        return self.concatenation(autre)
    def __hash__(self):
        """Permet d'utiliser Mot comme clé de dictionnaire ou dans des sets."""
        return hash(self.contenu)

    def __repr__(self):
        """Représentation officielle pour le débogage."""
        return f"Mot('{self.contenu}')"
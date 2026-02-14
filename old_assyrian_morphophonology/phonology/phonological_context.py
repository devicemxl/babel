"""
Contexto fonológico para aplicación de reglas de consonantes débiles.

Este módulo define las estructuras necesarias para capturar el contexto
fonológico completo donde ocurre una consonante débil.
"""

from dataclasses import dataclass
from typing import Optional, List, Tuple
from .phoneme import Phoneme, Consonant, Vowel
from .weak_enums import (
    WeakPosition,
    SyllablePosition,
    WordPosition,
    WeakVerbClass,
    SpecialSpelling
)


@dataclass
class PhonologicalContext:
    """
    Contexto fonológico para aplicar reglas de consonantes débiles.
    
    Captura toda la información necesaria para decidir si una consonante
    débil se preserva, se pierde, se contrae, etc.
    """
    # Contexto inmediato (ventana de 1 fonema)
    preceding: Optional[Phoneme] = None
    target: Optional[Phoneme] = None  # La consonante débil en cuestión (si reconstruida)
    following: Optional[Phoneme] = None
    
    # Contexto extendido (ventana de 2-3 fonemas)
    preceding_2: Optional[Phoneme] = None
    following_2: Optional[Phoneme] = None
    
    # Posiciones
    syllable_position: Optional[SyllablePosition] = None
    word_position: Optional[WordPosition] = None
    weak_position: Optional[WeakPosition] = None
    
    # Información ortográfica
    original_spelling: Optional[str] = None  # Spelling ORACC original
    is_broken_spelling: bool = False
    is_glide_spelling: bool = False
    is_plene_spelling: bool = False
    special_spelling: Optional[SpecialSpelling] = None
    
    # Información morfológica (para iteraciones futuras)
    verb_class: Optional[WeakVerbClass] = None
    morpheme_boundary: bool = False
    is_imperative: bool = False  # Importante para contracción -Cyi-
    
    # Metadata
    position_in_word: Optional[int] = None  # Índice en secuencia de fonemas
    
    def __post_init__(self):
        """Validación y cálculo automático de posiciones."""
        if self.target and self.preceding and self.following:
            self._infer_positions()
    
    def _infer_positions(self):
        """Infiere posiciones a partir del contexto fonológico."""
        # Determinar WeakPosition
        if self.weak_position is None:
            self.weak_position = self._infer_weak_position()
        
        # Determinar WordPosition si no está establecido
        if self.word_position is None:
            if self.preceding is None:
                self.word_position = WordPosition.INITIAL
            elif self.following is None:
                self.word_position = WordPosition.FINAL
            else:
                self.word_position = WordPosition.MEDIAL
    
    def _infer_weak_position(self) -> Optional[WeakPosition]:
        """Infiere WeakPosition a partir de fonemas adyacentes."""
        if not self.target or not isinstance(self.target, Consonant):
            return None
        
        # Word-initial
        if self.preceding is None and isinstance(self.following, Vowel):
            return WeakPosition.WORD_INITIAL
        
        # Intervocálico
        if isinstance(self.preceding, Vowel) and isinstance(self.following, Vowel):
            # Vocales idénticas vs diferentes
            if self.preceding.quality == self.following.quality:
                return WeakPosition.INTERVOCALIC_IDENTICAL
            else:
                return WeakPosition.INTERVOCALIC_DIFFERENT
        
        # Post-consonántico
        if isinstance(self.preceding, Consonant) and isinstance(self.following, Vowel):
            return WeakPosition.POST_CONSONANTAL
        
        # Syllable-final
        if isinstance(self.preceding, Vowel) and isinstance(self.following, Consonant):
            return WeakPosition.SYLLABLE_FINAL
        
        # Casos especiales para glides
        if self.target.symbol == 'w' and isinstance(self.preceding, Vowel):
            if self.preceding.quality.value == 'u':
                return WeakPosition.AFTER_U_BEFORE_VOWEL
        
        if self.target.symbol == 'y' and isinstance(self.preceding, Vowel):
            if self.preceding.quality.value in ['i', 'e']:
                return WeakPosition.AFTER_I_BEFORE_VOWEL
        
        # Antes de vocal homorgánica
        if isinstance(self.following, Vowel):
            if self.target.symbol == 'w' and self.following.quality.value == 'u':
                return WeakPosition.BEFORE_HOMORGANIC_VOWEL
            if self.target.symbol == 'y' and self.following.quality.value in ['i', 'e']:
                return WeakPosition.BEFORE_HOMORGANIC_VOWEL
        
        return None
    
    def is_intervocalic(self) -> bool:
        """True si la débil está entre vocales."""
        return (isinstance(self.preceding, Vowel) and 
                isinstance(self.following, Vowel))
    
    def is_post_consonantal(self) -> bool:
        """True si la débil está después de consonante."""
        return isinstance(self.preceding, Consonant)
    
    def has_identical_vowels(self) -> bool:
        """True si vocales adyacentes son idénticas."""
        if not (isinstance(self.preceding, Vowel) and 
                isinstance(self.following, Vowel)):
            return False
        return self.preceding.quality == self.following.quality
    
    def is_before_homorganic_vowel(self) -> bool:
        """True si débil está antes de vocal homorgánica."""
        if not isinstance(self.following, Vowel):
            return False
        
        if not self.target or not isinstance(self.target, Consonant):
            return False
        
        if self.target.symbol == 'w':
            return self.following.quality.value == 'u'
        elif self.target.symbol == 'y':
            return self.following.quality.value in ['i', 'e']
        
        return False
    
    def get_vowel_sequence(self) -> Optional[Tuple[Vowel, Vowel]]:
        """Retorna par de vocales si contexto es V_V."""
        if self.is_intervocalic():
            return (self.preceding, self.following)
        return None
    
    def __repr__(self) -> str:
        """Representación legible del contexto."""
        pre = self.preceding.symbol if self.preceding else '#'
        tar = self.target.symbol if self.target else '∅'
        fol = self.following.symbol if self.following else '#'
        
        context_str = f"{pre}_{tar}_{fol}"
        
        if self.weak_position:
            context_str += f" [{self.weak_position.value}]"
        
        if self.is_broken_spelling:
            context_str += " (broken)"
        
        return f"PhonologicalContext({context_str})"


@dataclass
class MorphologicalInfo:
    """
    Información morfológica para ayudar en reconstrucción de débiles.
    
    Esta información será completamente desarrollada en iteraciones futuras,
    pero necesitamos la estructura básica ahora.
    """
    # Tipo de palabra
    is_verb: bool = False
    is_noun: bool = False
    is_adjective: bool = False
    
    # Para verbos
    verb_class: Optional[WeakVerbClass] = None
    stem: Optional[str] = None  # G, D, Š, N, etc.
    tense_aspect: Optional[str] = None  # Pres, Pret, Perf, Stat, Imp
    person: Optional[int] = None  # 1, 2, 3
    number: Optional[str] = None  # Sg, Du, Pl
    gender: Optional[str] = None  # Masc, Fem
    
    # Para sustantivos
    noun_pattern: Optional[str] = None  # PaRS, PiRS, PuRS, etc.
    case: Optional[str] = None  # Nom, Gen, Acc
    state: Optional[str] = None  # Abs, Cst
    
    # Raíz (si conocida)
    root: Optional[str] = None  # Raíz triconsonántica (ej: "√qbʾ")
    
    # Contexto especial
    is_imperative: bool = False  # Importante para contracción
    is_proper_name: bool = False
    is_loanword: bool = False
    
    def __repr__(self) -> str:
        """Representación legible."""
        if self.is_verb and self.verb_class:
            return f"MorphInfo(verb={self.verb_class.value})"
        elif self.root:
            return f"MorphInfo(root={self.root})"
        return "MorphInfo(unknown)"


def create_context_from_sequence(
    phonemes: List[Phoneme],
    target_index: int,
    morphology: Optional[MorphologicalInfo] = None,
    original_spelling: Optional[str] = None
) -> PhonologicalContext:
    """
    Crea un PhonologicalContext a partir de una secuencia de fonemas.
    
    Args:
        phonemes: Secuencia completa de fonemas
        target_index: Índice del fonema objetivo (puede ser débil reconstruida)
        morphology: Información morfológica opcional
        original_spelling: Spelling ORACC original opcional
    
    Returns:
        PhonologicalContext completo
    """
    # Extraer ventana de contexto
    preceding = phonemes[target_index - 1] if target_index > 0 else None
    target = phonemes[target_index] if 0 <= target_index < len(phonemes) else None
    following = phonemes[target_index + 1] if target_index < len(phonemes) - 1 else None
    
    preceding_2 = phonemes[target_index - 2] if target_index > 1 else None
    following_2 = phonemes[target_index + 2] if target_index < len(phonemes) - 2 else None
    
    # Crear contexto
    context = PhonologicalContext(
        preceding=preceding,
        target=target,
        following=following,
        preceding_2=preceding_2,
        following_2=following_2,
        original_spelling=original_spelling,
        position_in_word=target_index,
        is_imperative=morphology.is_imperative if morphology else False,
        verb_class=morphology.verb_class if morphology else None,
    )
    
    return context


def create_broken_spelling_context(
    vowel1: Vowel,
    vowel2: Vowel,
    morphology: Optional[MorphologicalInfo] = None,
    original_spelling: Optional[str] = None
) -> PhonologicalContext:
    """
    Crea contexto para un broken spelling V-V (débil no visible).
    
    Args:
        vowel1: Primera vocal
        vowel2: Segunda vocal
        morphology: Información morfológica
        original_spelling: Spelling ORACC
    
    Returns:
        PhonologicalContext con target=None (débil a reconstruir)
    """
    context = PhonologicalContext(
        preceding=vowel1,
        target=None,  # A reconstruir
        following=vowel2,
        original_spelling=original_spelling,
        is_broken_spelling=True,
        verb_class=morphology.verb_class if morphology else None,
        is_imperative=morphology.is_imperative if morphology else False,
    )
    
    return context

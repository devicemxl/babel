"""
Contextos para reglas vocálicas del Old Assyrian.

Define estructuras para capturar información fonológica y morfológica
necesaria para aplicar reglas vocálicas.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from ...phonology import Vowel, Consonant, Phoneme
from .enums import (
    ConditioningPosition,
    VowelMorphologicalContext,
)


@dataclass
class VowelContext:
    """
    Contexto fonológico y morfológico para reglas vocálicas.
    
    Captura información sobre vocales, consonantes condicionantes,
    posición silábica y contexto morfológico.
    """
    # Vocal principal
    vowel: Vowel
    
    # Vocales adicionales (para asimilación/contracción)
    preceding_vowel: Optional[Vowel] = None
    following_vowel: Optional[Vowel] = None
    
    # Consonantes condicionantes
    preceding_consonant: Optional[Consonant] = None
    following_consonant: Optional[Consonant] = None
    intervening_consonant: Optional[Consonant] = None  # Entre V₁ y V₂
    
    # Posición en palabra
    is_word_initial: bool = False
    is_word_final: bool = False
    is_penultimate: bool = False  # Penúltima sílaba
    is_antepenultimate: bool = False  # Antepenúltima
    
    # Información silábica
    syllable_position: int = 0  # Posición de sílaba en palabra
    total_syllables: int = 1
    is_open_syllable: bool = True
    is_stressed: bool = False
    
    # Contexto morfológico
    morphological_context: VowelMorphologicalContext = VowelMorphologicalContext.ROOT
    crosses_morpheme_boundary: bool = False
    
    # Para asimilación vocálica asiria
    is_in_grammatical_morpheme: bool = False
    morpheme_is_case_ending: bool = False
    morpheme_is_ventive: bool = False
    
    # Metadata
    original_form: Optional[str] = None
    
    def has_guttural(self) -> bool:
        """True si hay consonante gutural condicionante."""
        from .enums import is_guttural_consonant
        
        for c in [self.preceding_consonant, self.following_consonant]:
            if c and is_guttural_consonant(c.symbol):
                return True
        return False
    
    def get_guttural_position(self) -> Optional[ConditioningPosition]:
        """Retorna posición de gutural si presente."""
        from .enums import is_guttural_consonant
        
        if self.preceding_consonant and is_guttural_consonant(self.preceding_consonant.symbol):
            return ConditioningPosition.PRECEDING
        if self.following_consonant and is_guttural_consonant(self.following_consonant.symbol):
            return ConditioningPosition.FOLLOWING
        return None
    
    def has_r_conditioning(self) -> bool:
        """True si hay r condicionante."""
        for c in [self.preceding_consonant, self.following_consonant]:
            if c and c.symbol == 'r':
                return True
        return False
    
    def get_r_position(self) -> Optional[ConditioningPosition]:
        """Retorna posición de r si presente."""
        if self.preceding_consonant and self.preceding_consonant.symbol == 'r':
            return ConditioningPosition.PRECEDING
        if self.following_consonant and self.following_consonant.symbol == 'r':
            return ConditioningPosition.FOLLOWING
        return None
    
    def requires_assimilation(self) -> bool:
        """
        True si contexto requiere asimilación vocálica (regla asiria).
        
        Regla: penúltima sílaba de palabra 3+ sílabas con a corta
               asimila a vocal de sílaba final.
        """
        from .enums import requires_vowel_assimilation
        
        if not self.is_penultimate:
            return False
        
        if not self.following_vowel:
            return False
        
        return requires_vowel_assimilation(
            self.vowel.symbol,
            self.following_vowel.symbol,
            self.total_syllables
        )
    
    def vowels_are_adjacent(self) -> bool:
        """True si vocales están directamente adyacentes (sin consonante)."""
        return (
            self.following_vowel is not None and
            self.intervening_consonant is None
        )
    
    def vowels_match_quality(self) -> bool:
        """True si vocal actual y siguiente tienen misma calidad."""
        if not self.following_vowel:
            return False
        
        from .enums import vowels_match_quality
        return vowels_match_quality(self.vowel.symbol, self.following_vowel.symbol)


@dataclass
class SyllableSequence:
    """
    Secuencia de sílabas para análisis de síncope y asimilación.
    
    Útil para reglas que operan sobre secuencias de sílabas.
    """
    syllables: List[List[Phoneme]] = field(default_factory=list)
    
    def count_short_syllables(self, exclude_final: bool = True) -> int:
        """
        Cuenta sílabas cortas en secuencia.
        
        Args:
            exclude_final: Si True, excluye sílaba final del conteo
        
        Returns:
            Número de sílabas cortas
        """
        count = 0
        end_idx = len(self.syllables) - 1 if exclude_final else len(self.syllables)
        
        for i in range(end_idx):
            syllable = self.syllables[i]
            # Sílaba corta: CV (consonante + vocal corta)
            if len(syllable) == 2:
                phoneme = syllable[1]
                if isinstance(phoneme, Vowel) and phoneme.length.value == 'short':
                    count += 1
        
        return count
    
    def should_apply_syncope(self) -> bool:
        """
        True si síncope vocálica debe aplicar.
        
        Regla: Si secuencia contiene 2+ sílabas cortas (excluyendo final),
               última vocal de secuencia se sincopa.
        """
        return self.count_short_syllables(exclude_final=True) >= 2
    
    def get_syncope_target_index(self) -> Optional[int]:
        """
        Retorna índice de sílaba donde debe aplicar síncope.
        
        Returns:
            Índice de sílaba objetivo, o None si no aplica
        """
        if not self.should_apply_syncope():
            return None
        
        # Última sílaba corta de la secuencia (excluyendo final)
        for i in range(len(self.syllables) - 2, -1, -1):
            syllable = self.syllables[i]
            if len(syllable) == 2:
                phoneme = syllable[1]
                if isinstance(phoneme, Vowel) and phoneme.length.value == 'short':
                    return i
        
        return None


def create_vowel_context(
    vowel: Vowel,
    preceding_consonant: Optional[Consonant] = None,
    following_consonant: Optional[Consonant] = None,
    following_vowel: Optional[Vowel] = None,
    syllable_position: int = 0,
    total_syllables: int = 1,
    morphological_context: VowelMorphologicalContext = VowelMorphologicalContext.ROOT,
) -> VowelContext:
    """
    Crea contexto vocálico con información básica.
    
    Args:
        vowel: Vocal principal
        preceding_consonant: Consonante precedente (opcional)
        following_consonant: Consonante siguiente (opcional)
        following_vowel: Vocal siguiente para asimilación (opcional)
        syllable_position: Posición de sílaba en palabra
        total_syllables: Total de sílabas en palabra
        morphological_context: Contexto morfológico
    
    Returns:
        VowelContext configurado
    """
    # Determinar posiciones
    is_penultimate = (syllable_position == total_syllables - 2)
    is_antepenultimate = (syllable_position == total_syllables - 3)
    is_word_final = (syllable_position == total_syllables - 1)
    is_word_initial = (syllable_position == 0)
    
    return VowelContext(
        vowel=vowel,
        preceding_consonant=preceding_consonant,
        following_consonant=following_consonant,
        following_vowel=following_vowel,
        is_word_initial=is_word_initial,
        is_word_final=is_word_final,
        is_penultimate=is_penultimate,
        is_antepenultimate=is_antepenultimate,
        syllable_position=syllable_position,
        total_syllables=total_syllables,
        morphological_context=morphological_context,
    )


def create_assimilation_context(
    penultimate_vowel: Vowel,
    final_vowel: Vowel,
    total_syllables: int,
    is_verb_form: bool = False,
) -> VowelContext:
    """
    Crea contexto específico para asimilación vocálica asiria.
    
    Args:
        penultimate_vowel: Vocal en penúltima sílaba
        final_vowel: Vocal en sílaba final
        total_syllables: Total de sílabas
        is_verb_form: True si es forma verbal
    
    Returns:
        VowelContext configurado para asimilación
    """
    morphological_ctx = (
        VowelMorphologicalContext.VERB_ENDING if is_verb_form
        else VowelMorphologicalContext.CASE_ENDING
    )
    
    return create_vowel_context(
        vowel=penultimate_vowel,
        following_vowel=final_vowel,
        syllable_position=total_syllables - 2,
        total_syllables=total_syllables,
        morphological_context=morphological_ctx,
    )

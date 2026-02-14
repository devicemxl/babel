"""
I/w Stems - Verbos con w como R₁.

ITERACIÓN 9 - Verbos I-débil

Implementa I/w Fientivo para verbos como wasābum, wabālum.

Basado en Kouwenberg (2017) § 18.2.

Autor: Claude
Fecha: 2026-02-12
"""

from typing import List, Optional
import sys
import os

# Ajustar path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from phonology import Phoneme, Vowel, Consonant
from phonology.inventory import get_consonant
from phonology.enums import VowelQuality, VowelLength
from phonology.features import VowelFeatures
from phonology.verbal.g_stem import G_Stem
from phonology.verbal.weak_root import WeakRoot
from phonology.verbal.enums import VerbFormType, VowelClass, WeakVerbType


# ============================================================================
# I/W FIENTIVE STEM
# ============================================================================

class I_w_Fientive_Stem(G_Stem):
    """
    I/w Fientive Stem - Verbos de acción con w como R₁.
    
    Características fonológicas:
    - Presente: w + i → u (corta) + geminación R₂
    - Pretérito: w + i → ū (larga sin ending, corta con ending)
    - Perfect: w + i → u + geminación -tt-
    - Imperativo: w → Ø (pérdida total)
    
    Referencias: § 18.2.1, Tabla 18.1
    
    Ejemplos:
        wasābum (a/i) 'sentar':
            Presente 3sm: uššab
            Pretérito 3sm: ūšib
            Perfect 3sm: uttašab
            Imperativo sm: šib
    """
    
    def __init__(self, root: WeakRoot):
        """Inicializa I/w Fientive Stem."""
        if root.weak_type != WeakVerbType.I_W_FIENTIVE:
            raise ValueError(
                f"I_w_Fientive_Stem requiere I_W_FIENTIVE, got {root.weak_type}"
            )
        super().__init__(root=root)
    
    # ========================================================================
    # Helper methods override
    # ========================================================================
    
    def _get_R1_for_present(self) -> Optional[Consonant]:
        """R₁ (w) no aparece por contracción."""
        return None
    
    def _get_R1_for_preterite(self, assimilate_n: bool = False) -> List[Consonant]:
        """R₁ (w) no aparece por contracción."""
        return []
    
    def _get_R1_for_perfect(self, assimilate_n: bool = False) -> List[Consonant]:
        """R₁ (w) no aparece por contracción."""
        return []
    
    def _get_R1_for_imperative(self) -> Optional[Consonant]:
        """R₁ (w) desaparece en imperativo."""
        return None
    
    def _should_geminate_R2_in_present(self) -> bool:
        """I/w fientivo SÍ gemina R₂."""
        return True
    
    def _should_geminate_infix_t_in_perfect(self) -> bool:
        """I/w fientivo SÍ gemina infix-t."""
        return True
    
    # ========================================================================
    # Form methods override
    # ========================================================================
    
    def form_present(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma presente de I/w fientivo.
        
        Examples:
            wasābum Pres 3sm: uššab
            wasābum Pres 2sm: tuššab
            wasābum Pres 1s: uššab
        """
        phonemes = []
        
        # Prefijo con contracción w+i→u
        if person == 3:
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U, length=VowelLength.SHORT
            )))
        elif person == 2:
            phonemes.append(get_consonant('t'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U, length=VowelLength.SHORT
            )))
        elif person == 1:
            if number == 'pl':
                phonemes.append(get_consonant('n'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U, length=VowelLength.SHORT
            )))
        
        # R₂ geminada
        phonemes.append(self.root.R2)
        phonemes.append(self.root.R2)
        
        # Vocal de presente
        pres_vowel = self.root.vowel_class.present_vowel
        quality_map = {'a': VowelQuality.A, 'i': VowelQuality.I, 'u': VowelQuality.U}
        phonemes.append(Vowel(features=VowelFeatures(
            quality=quality_map[pres_vowel],
            length=VowelLength.SHORT
        )))
        
        # R₃
        phonemes.append(self.root.R3)
        
        # Endings
        if number == 'pl' and gender == 'm':
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U, length=VowelLength.LONG
            )))
        
        return phonemes
    
    def form_preterite(self, person: int = 3, number: str = 'sg',
                       gender: str = 'm') -> List[Phoneme]:
        """
        Forma pretérito de I/w fientivo.
        
        Examples:
            wasābum Pret 3sm: ūšib (vocal larga)
            wasābum Pret 3pm: ušbū (vocal corta + ending)
        """
        phonemes = []
        has_ending = self._has_vocalic_ending(number, gender)
        
        # Prefijo con contracción w+i→ū/u
        length = VowelLength.SHORT if has_ending else VowelLength.LONG
        
        if person == 3:
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U, length=length
            )))
        elif person == 2:
            phonemes.append(get_consonant('t'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U, length=length
            )))
        elif person == 1:
            if number == 'pl':
                phonemes.append(get_consonant('n'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U, length=length
            )))
        
        # R₂ (sin geminación)
        phonemes.append(self.root.R2)
        
        # Vocal de pretérito (síncope si hay ending)
        if not has_ending:
            pret_vowel = self.root.vowel_class.preterite_vowel
            quality_map = {'a': VowelQuality.A, 'i': VowelQuality.I, 'u': VowelQuality.U}
            phonemes.append(Vowel(features=VowelFeatures(
                quality=quality_map[pret_vowel],
                length=VowelLength.SHORT
            )))
        
        # R₃
        phonemes.append(self.root.R3)
        
        # Endings
        if number == 'pl' and gender == 'm':
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U, length=VowelLength.LONG
            )))
        
        return phonemes
    
    def form_perfect(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma perfect de I/w fientivo.
        
        Examples:
            wasābum Perf 3sm: uttašab
        """
        phonemes = []
        
        # Prefijo con contracción w+i→u
        if person == 3:
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U, length=VowelLength.SHORT
            )))
        elif person == 2:
            phonemes.append(get_consonant('t'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U, length=VowelLength.SHORT
            )))
        elif person == 1:
            if number == 'pl':
                phonemes.append(get_consonant('n'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U, length=VowelLength.SHORT
            )))
        
        # Infix-t GEMINADO
        phonemes.append(get_consonant('t'))
        phonemes.append(get_consonant('t'))
        
        # Vocal a
        phonemes.append(Vowel(features=VowelFeatures(
            quality=VowelQuality.A, length=VowelLength.SHORT
        )))
        
        # R₂
        phonemes.append(self.root.R2)
        
        # Vocal a
        phonemes.append(Vowel(features=VowelFeatures(
            quality=VowelQuality.A, length=VowelLength.SHORT
        )))
        
        # R₃
        phonemes.append(self.root.R3)
        
        return phonemes
    
    def form_imperative(self, number: str = 'sg',
                        gender: str = 'm') -> List[Phoneme]:
        """
        Forma imperativo de I/w fientivo.
        
        Examples:
            wasābum Imp sm: šib
            wasābum Imp pm: šibā
        """
        phonemes = []
        
        # R₁ (w) se omite
        
        # R₂
        phonemes.append(self.root.R2)
        
        # Vocal de pretérito
        pret_vowel = self.root.vowel_class.preterite_vowel
        quality_map = {'a': VowelQuality.A, 'i': VowelQuality.I, 'u': VowelQuality.U}
        phonemes.append(Vowel(features=VowelFeatures(
            quality=quality_map[pret_vowel],
            length=VowelLength.SHORT
        )))
        
        # R₃
        phonemes.append(self.root.R3)
        
        # Endings
        if number == 'pl':
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.A, length=VowelLength.LONG
            )))
        
        return phonemes

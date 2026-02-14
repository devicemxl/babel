"""
atawwum Stem - Verbo doblemente débil (I/w + III/w).

ITERACIÓN 9 - PASO 9: Verbo doblemente débil

Implementa atawwum (< *ʔatawwum), único verbo doblemente débil
documentado en Old Assyrian con w en R₁ y R₃.

Basado en Kouwenberg (2017) § 18.2.3.

Autor: Claude
Fecha: 2026-02-12
"""

from typing import List, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from phonology import Phoneme, Vowel, Consonant
from phonology.inventory import get_consonant
from phonology.enums import VowelQuality, VowelLength
from phonology.features import VowelFeatures
from phonology.verbal.g_stem import G_Stem
from phonology.verbal.weak_root import WeakRoot
from phonology.verbal.enums import VerbFormType, VowelClass, WeakVerbType


# ============================================================================
# ATAWWUM STEM (DOBLEMENTE DÉBIL)
# ============================================================================

class Atawwum_Stem(G_Stem):
    """
    atawwum Stem - Verbo doblemente débil (I/voc + II/gem).
    
    CORRECCIÓN: atawwum es I/voc + II/gem, no I/w + III/w
    
    Raíz real: √ʔww (< *ʔatawwum)
    - R₁ = Ø (gutural perdida → vocal compensatoria)
    - R₂ = w
    - R₃ = w (geminación)
    
    Solo atestiguado en Gt y N stems.
    Paradigma parcialmente reconstruido.
    
    Referencias: § 18.3.2.2
    
    Ejemplos:
        atawwum Gt: se comporta como I/voc con complicaciones
    
    NOTA: Implementación simplificada basada en I/w fientivo
    como aproximación. La forma real es más compleja.
    
    Attributes:
        root: WeakRoot con weak_type = I_ATAWWUM
    """
    
    def __init__(self, root: WeakRoot):
        """
        Inicializa atawwum Stem.
        
        Args:
            root: WeakRoot con weak_type = I_ATAWWUM
        
        Raises:
            ValueError: Si root no es I_ATAWWUM
        """
        if root.weak_type != WeakVerbType.I_ATAWWUM:
            raise ValueError(
                f"Atawwum_Stem requiere I_ATAWWUM, got {root.weak_type}"
            )
        
        # Inicializar como I/w fientivo (hereda comportamiento R₁)
        super().__init__(root=root)
    
    # ========================================================================
    # Helper methods override (adicionales a I/w fientivo)
    # ========================================================================
    
    def _get_R3_for_present(self) -> Optional[Consonant]:
        """
        R₃ (w) en presente tiene tratamiento especial.
        
        En verbos doblemente débiles, R₃=w puede:
        - Convertirse en vocal (w → ū)
        - Perderse completamente
        - Asimilarse
        
        Returns:
            None (R₃ se convierte en vocal o desaparece)
        """
        return None
    
    def _get_R3_for_preterite(self) -> Optional[Consonant]:
        """
        R₃ (w) en pretérito se convierte en vocal.
        
        w final → ī (vocal larga)
        
        Returns:
            None (R₃ se convierte en vocal)
        """
        return None
    
    def _get_R3_for_imperative(self) -> Optional[Consonant]:
        """
        R₃ (w) en imperativo se convierte en vocal.
        
        Returns:
            None (R₃ se convierte en vocal)
        """
        return None
    
    # ========================================================================
    # Form methods override
    # ========================================================================
    
    def form_present(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma presente de atawwum.
        
        Proceso (reconstruido):
            1. Prefijo i- + contracción w+i → u
            2. R₂ (t) geminada → tt
            3. Vocal a
            4. R₃ (w) → ū (vocal larga final)
        
        *u-ttaw → u-ttū (?)
        
        Args:
            person: 1, 2, 3
            number: 'sg', 'pl'
            gender: 'm', 'f'
        
        Returns:
            Lista de fonemas
        
        Examples:
            atawwum Pres 3sm: uttū (reconstruido)
        """
        phonemes = []
        
        # Prefijo con contracción w+i→u (heredado de I/w)
        if person == 3:
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U,
                length=VowelLength.SHORT
            )))
        elif person == 2:
            phonemes.append(get_consonant('t'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U,
                length=VowelLength.SHORT
            )))
        elif person == 1:
            if number == 'pl':
                phonemes.append(get_consonant('n'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U,
                length=VowelLength.SHORT
            )))
        
        # R₁ se omite (w desaparece en contracción)
        
        # R₂ (t) geminada
        phonemes.append(self.root.R2)
        phonemes.append(self.root.R2)
        
        # Vocal a (presente)
        phonemes.append(Vowel(features=VowelFeatures(
            quality=VowelQuality.A,
            length=VowelLength.SHORT
        )))
        
        # R₃ (w) → ū (vocal larga)
        # En verbos III/w, w final → vocal larga
        phonemes.append(Vowel(features=VowelFeatures(
            quality=VowelQuality.U,
            length=VowelLength.LONG
        )))
        
        return phonemes
    
    def form_preterite(self, person: int = 3, number: str = 'sg',
                       gender: str = 'm') -> List[Phoneme]:
        """
        Forma pretérito de atawwum.
        
        Proceso (reconstruido):
            1. Prefijo i- + contracción w+i → ū
            2. R₂ (t)
            3. Vocal i
            4. R₃ (w) → ī (vocal larga)
        
        *ū-tiw → ū-tī (?)
        
        Args:
            person: 1, 2, 3
            number: 'sg', 'pl'
            gender: 'm', 'f'
        
        Returns:
            Lista de fonemas
        
        Examples:
            atawwum Pret 3sm: ūtī (reconstruido)
        """
        phonemes = []
        has_ending = self._has_vocalic_ending(number, gender)
        
        # Prefijo con contracción w+i→ū (heredado)
        length = VowelLength.SHORT if has_ending else VowelLength.LONG
        
        if person == 3:
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U,
                length=length
            )))
        elif person == 2:
            phonemes.append(get_consonant('t'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U,
                length=length
            )))
        elif person == 1:
            if number == 'pl':
                phonemes.append(get_consonant('n'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U,
                length=length
            )))
        
        # R₁ se omite
        
        # R₂ (t) sin geminación en pretérito
        phonemes.append(self.root.R2)
        
        # Vocal i (pretérito)
        phonemes.append(Vowel(features=VowelFeatures(
            quality=VowelQuality.I,
            length=VowelLength.SHORT
        )))
        
        # R₃ (w) → ī (vocal larga)
        phonemes.append(Vowel(features=VowelFeatures(
            quality=VowelQuality.I,
            length=VowelLength.LONG
        )))
        
        return phonemes
    
    def form_perfect(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma perfect de atawwum.
        
        Proceso (altamente reconstruido):
            1. Prefijo i- + contracción w+i → u
            2. Infix-t geminado → tt
            3. Vocal a
            4. R₂ (t)
            5. Vocal a
            6. R₃ (w) → ū
        
        *ut-tat-w → ut-tat-ū (?)
        
        NOTA: Forma muy incierta, pocas atestaciones.
        
        Args:
            person: 1, 2, 3
            number: 'sg', 'pl'
            gender: 'm', 'f'
        
        Returns:
            Lista de fonemas
        
        Examples:
            atawwum Perf 3sm: uttatū (altamente reconstruido)
        """
        phonemes = []
        
        # Prefijo con contracción
        if person == 3:
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U,
                length=VowelLength.SHORT
            )))
        elif person == 2:
            phonemes.append(get_consonant('t'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U,
                length=VowelLength.SHORT
            )))
        elif person == 1:
            if number == 'pl':
                phonemes.append(get_consonant('n'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.U,
                length=VowelLength.SHORT
            )))
        
        # Infix-t geminado (heredado de I/w fientivo)
        phonemes.append(get_consonant('t'))
        phonemes.append(get_consonant('t'))
        
        # Vocal a
        phonemes.append(Vowel(features=VowelFeatures(
            quality=VowelQuality.A,
            length=VowelLength.SHORT
        )))
        
        # R₂ (t)
        phonemes.append(self.root.R2)
        
        # Vocal a
        phonemes.append(Vowel(features=VowelFeatures(
            quality=VowelQuality.A,
            length=VowelLength.SHORT
        )))
        
        # R₃ (w) → ū
        phonemes.append(Vowel(features=VowelFeatures(
            quality=VowelQuality.U,
            length=VowelLength.LONG
        )))
        
        return phonemes
    
    def form_imperative(self, number: str = 'sg',
                        gender: str = 'm') -> List[Phoneme]:
        """
        Forma imperativo de atawwum.
        
        Proceso (reconstruido):
            1. R₁ (w) → Ø (pérdida)
            2. R₂ (t)
            3. Vocal i
            4. R₃ (w) → ī
        
        *tiw → tī (?)
        
        Args:
            number: 'sg', 'pl'
            gender: 'm', 'f'
        
        Returns:
            Lista de fonemas
        
        Examples:
            atawwum Imp sm: tī (reconstruido)
        """
        phonemes = []
        
        # R₁ se omite (w desaparece)
        
        # R₂ (t)
        phonemes.append(self.root.R2)
        
        # Vocal i
        phonemes.append(Vowel(features=VowelFeatures(
            quality=VowelQuality.I,
            length=VowelLength.SHORT
        )))
        
        # R₃ (w) → ī
        phonemes.append(Vowel(features=VowelFeatures(
            quality=VowelQuality.I,
            length=VowelLength.LONG
        )))
        
        # Endings para plural
        if number == 'pl':
            # Plural: agregar ā
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.A,
                length=VowelLength.LONG
            )))
        
        return phonemes


# create_atawwum_root ya existe en phonology.verbal.weak_root
# Importar en vez de redefinir
from phonology.verbal.weak_root import create_atawwum_root


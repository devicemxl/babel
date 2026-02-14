"""
I/n Stems - Verbos con n como R₁.

ITERACIÓN 9 - Verbos I-débil

Implementa I/n con asimilación n+C → CC.

Basado en Kouwenberg (2017) § 18.4.

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
# I/N STEM
# ============================================================================

class I_n_Stem(G_Stem):
    """
    I/n Stem - Verbos con n como R₁.
    
    Características fonológicas:
    - Presente: paradigma casi idéntico a verbos fuertes
    - Pretérito: asimilación n + C → CC (geminación de R₂)
    - Perfect: asimilación n + t → tt
    - Imperativo: pérdida #n + i/u → #i/u
    
    Asimilación de n:
        n + consonante → CC (consonante geminada)
        Excepciones: n + w/m/r/l NO asimilan
    
    Referencias: § 18.4, Tabla 18.13
    
    Ejemplos:
        naṣārum (a/u) 'guardar, proteger':
            Presente 3sm: inaṣṣar
            Pretérito 3sm: iṣṣur (< *inṣur)
            Perfect 3sm: ittaṣar (< *intaṣar)
            Imperativo sm: uṣur (< *nuṣur)
        
        nadā'um (i/i) 'depositar, poner':
            Presente 3sm: inaddi
            Pretérito 3sm: iddi (< *indi)
            Perfect 3sm: ittadi (< *intadi)
        
        nakārum (a/u) 'ser hostil':
            Presente 3sm: inakkar
            Pretérito 3sm: ikker (< *inker)
    
    EXCEPCIÓN - našā'um:
        N-stem tiene asimilación variable (ver I_n_Nasaum_Stem)
    
    Atributos:
        root: WeakRoot con R₁ = WeakConsonant('n')
    """
    
    def __init__(self, root: WeakRoot):
        """
        Inicializa I/n Stem.
        
        Args:
            root: WeakRoot con weak_type = I_N
        """
        if root.weak_type not in [WeakVerbType.I_N, WeakVerbType.I_N_NASAUM]:
            raise ValueError(
                f"I_n_Stem requiere I_N o I_N_NASAUM, got {root.weak_type}"
            )
        super().__init__(root=root)
    
    # ========================================================================
    # Helper methods override
    # ========================================================================
    
    def _get_R1_for_present(self) -> Optional[Consonant]:
        """
        R₁ (n) aparece en presente (NO asimila).
        
        i-naṣṣar (con n)
        
        Returns:
            Consonant('n')
        """
        return get_consonant('n')
    
    def _get_R1_for_preterite(self, assimilate_n: bool = False) -> List[Consonant]:
        """
        R₁ (n) asimila a R₂ en pretérito.
        
        *i-nṣur → i-ṣṣur (n + ṣ → ṣṣ)
        
        Args:
            assimilate_n: Si True, asimilar n a R₂
        
        Returns:
            [R₂, R₂] si asimilate_n=True, [n] si False
        """
        if assimilate_n:
            # Verificar excepciones (n + w/m/r/l NO asimilan)
            if self.root.R2.symbol in ['w', 'm', 'r', 'l']:
                return [get_consonant('n')]
            else:
                # Asimilación: n → R₂ (geminación)
                return [self.root.R2, self.root.R2]
        else:
            return [get_consonant('n')]
    
    def _get_R1_for_perfect(self, assimilate_n: bool = False) -> List[Consonant]:
        """
        R₁ (n) asimila a infix-t en perfect.
        
        *i-n-taṣar → i-ttaṣar (n + t → tt)
        
        Returns:
            [] (n asimila completamente al infix-t que se gemina)
        """
        # n + t → tt (la n desaparece, t se gemina)
        # Esto se maneja devolviendo lista vacía aquí
        # y luego geminando t en form_perfect
        return []
    
    def _get_R1_for_imperative(self) -> Optional[Consonant]:
        """
        R₁ (n) desaparece en imperativo antes de vocal alta.
        
        #n + u → #u (uṣur < *nuṣur)
        
        Returns:
            None (pérdida de n)
        """
        return None
    
    def _should_geminate_R2_in_present(self) -> bool:
        """
        I/n SÍ gemina R₂ en presente (como verbos fuertes).
        
        i-naṣṣar (no *inaṣar)
        
        Returns:
            True
        """
        return True
    
    # ========================================================================
    # Form methods override
    # ========================================================================
    
    def form_present(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma presente de I/n.
        
        Proceso:
            1. Prefijo personal (i/t/n)
            2. R₁ (n) - SIN asimilación
            3. R₂ geminada
            4. Vocal de presente
            5. R₃
        
        Examples:
            naṣārum Pres 3sm: inaṣṣar
            naṣārum Pres 2sm: tanaṣṣar
        """
        phonemes = []
        
        # Prefijo personal
        if person == 3:
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.I, length=VowelLength.SHORT
            )))
        elif person == 2:
            phonemes.append(get_consonant('t'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.A, length=VowelLength.SHORT
            )))
        elif person == 1:
            if number == 'pl':
                phonemes.append(get_consonant('n'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.I if number == 'sg' else VowelQuality.I,
                length=VowelLength.SHORT
            )))
        
        # R₁ (n) aparece
        phonemes.append(get_consonant('n'))
        
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
        Forma pretérito de I/n.
        
        Proceso:
            1. Prefijo personal
            2. Asimilación: n + R₂ → R₂R₂
            3. Vocal de pretérito
            4. R₃
        
        Examples:
            naṣārum Pret 3sm: iṣṣur (< *inṣur)
            naṣārum Pret 2sm: taṣṣur
        """
        phonemes = []
        has_ending = self._has_vocalic_ending(number, gender)
        
        # Prefijo personal
        if person == 3:
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.I, length=VowelLength.SHORT
            )))
        elif person == 2:
            phonemes.append(get_consonant('t'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.A, length=VowelLength.SHORT
            )))
        elif person == 1:
            if number == 'pl':
                phonemes.append(get_consonant('n'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.I, length=VowelLength.SHORT
            )))
        
        # R₁ con asimilación: n + R₂ → R₂R₂
        # Verificar excepciones
        if self.root.R2.symbol not in ['w', 'm', 'r', 'l']:
            # Asimilación: geminación R₂
            phonemes.append(self.root.R2)
            phonemes.append(self.root.R2)
        else:
            # Excepción: preservar n
            phonemes.append(get_consonant('n'))
            phonemes.append(self.root.R2)
        
        # Vocal de pretérito (con posible síncope)
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
        Forma perfect de I/n.
        
        Proceso:
            1. Prefijo personal
            2. Asimilación: n + t → tt (infix-t geminado)
            3. Vocal a
            4. R₂
            5. Vocal a
            6. R₃
        
        Examples:
            naṣārum Perf 3sm: ittaṣar (< *intaṣar)
        """
        phonemes = []
        
        # Prefijo personal
        if person == 3:
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.I, length=VowelLength.SHORT
            )))
        elif person == 2:
            phonemes.append(get_consonant('t'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.A, length=VowelLength.SHORT
            )))
        elif person == 1:
            if number == 'pl':
                phonemes.append(get_consonant('n'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.I, length=VowelLength.SHORT
            )))
        
        # n + t → tt (asimilación)
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
        Forma imperativo de I/n.
        
        Proceso:
            1. Pérdida: #n + vocal alta → #vocal alta
            2. Vocal u/i (según pretérito)
            3. R₂
            4. Vocal de pretérito
            5. R₃
        
        Examples:
            naṣārum Imp sm: uṣur (< *nuṣur)
            nadā'um Imp sm: idi (< *nidi)
        """
        phonemes = []
        
        # n desaparece, aparece vocal u o i
        # Determinar cual vocal según clase
        pret_vowel = self.root.vowel_class.preterite_vowel
        
        # Vocal inicial (típicamente u para a/u, i para i/i)
        if pret_vowel == 'u':
            initial_vowel = VowelQuality.U
        else:
            initial_vowel = VowelQuality.I
        
        phonemes.append(Vowel(features=VowelFeatures(
            quality=initial_vowel,
            length=VowelLength.SHORT
        )))
        
        # R₂
        phonemes.append(self.root.R2)
        
        # Vocal de pretérito
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


# ============================================================================
# I/N NAŠĀUM STEM (CASO ESPECIAL)
# ============================================================================

class I_n_Nasaum_Stem(I_n_Stem):
    """
    I/n Našāʔum Stem - Caso especial con asimilación variable.
    
    našāʔum 'transportar, llevar' tiene comportamiento especial
    en N-stem donde la asimilación de n es variable.
    
    Referencias: § 18.4, nota sobre našāʔum
    
    Por ahora, comportamiento idéntico a I_n_Stem regular.
    La diferencia aparece principalmente en N-stem derivado.
    
    Ejemplos:
        našāʔum (i/i) 'transportar':
            Presente 3sm: inašši
            Pretérito 3sm: išši (< *inši)
            
        N-stem (variable):
            - innašši (con asimilación)
            - inašši (sin asimilación)
    """
    
    def __init__(self, root: WeakRoot):
        """Inicializa našāʔum stem."""
        if root.weak_type != WeakVerbType.I_N_NASAUM:
            raise ValueError(
                f"I_n_Nasaum_Stem requiere I_N_NASAUM, got {root.weak_type}"
            )
        # Inicializar como I_n regular
        # Las diferencias aparecen en stems derivados (N)
        super().__init__(root=root)
    
    # Por ahora, comportamiento idéntico a I_n_Stem
    # La especialización ocurre en N-stem

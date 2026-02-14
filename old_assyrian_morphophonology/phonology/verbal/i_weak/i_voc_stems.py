"""
I/voc Stems - Verbos con gutural perdida como R₁.

ITERACIÓN 9 - Verbos I-débil

Implementa dos tipos de I/voc:
- I/a: ahāzum, amārum (< *ʔ, *h)
- I/e: epāšum, erābum (< *ʕ, *ḥ)

Basado en Kouwenberg (2017) § 18.3.

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
# I/VOC A STEM
# ============================================================================

class I_a_Stem(G_Stem):
    """
    I/voc a Stem - Verbos con vocal inicial 'a' por gutural perdida.
    
    Características fonológicas:
    - Proto-semítico: *ʔaḥuz, *hakal → OA: ahāzum, akālum
    - Pretérito: vocal larga compensatoria (ā-, ē-)
    - Perfect: vocal larga compensatoria
    - Presente: probablemente vocal larga (ortografía ambigua)
    - Imperativo: vocal inicial + R₂R₃
    
    Referencias: § 18.3.1, Tabla 18.6
    
    Ejemplos:
        ahāzum (a/u) 'tomar, agarrar':
            Presente 3sm: aḥḥaz (vocal larga probable)
            Pretérito 1s: āḥuz
            Pretérito 3sm: ēḥuz
            Perfect 3sm: ītaḥaz
            Imperativo sm: ḥuz
        
        amārum (a/u) 'ver':
            Presente 3sm: ammar
            Pretérito 1s: āmur
            Pretérito 3sm: ēmur
        
        akālum (a/u) 'comer':
            Presente 3sm: akkal
            Pretérito 1s: ākul
            Pretérito 3sm: ēkul
    
    Atributos:
        root: WeakRoot con R₁ = WeakConsonant('Ø')
        initial_vowel: 'a' (vocal que aparece por gutural perdida)
    """
    
    def __init__(self, root: WeakRoot):
        """
        Inicializa I/a Stem.
        
        Args:
            root: WeakRoot con weak_type = I_VOC_A
        """
        if root.weak_type != WeakVerbType.I_VOC_A:
            raise ValueError(
                f"I_a_Stem requiere I_VOC_A, got {root.weak_type}"
            )
        super().__init__(root=root)
        self.initial_vowel = 'a'  # Vocal inicial que reemplaza gutural
    
    # ========================================================================
    # Helper methods override
    # ========================================================================
    
    def _get_R1_for_present(self) -> Optional[Consonant]:
        """
        R₁ (gutural) no aparece, reemplazado por vocal.
        
        Returns:
            None (gutural perdida)
        """
        return None
    
    def _get_R1_for_preterite(self, assimilate_n: bool = False) -> List[Consonant]:
        """
        R₁ (gutural) no aparece, reemplazado por vocal larga.
        
        Returns:
            [] (gutural perdida)
        """
        return []
    
    def _get_R1_for_perfect(self, assimilate_n: bool = False) -> List[Consonant]:
        """
        R₁ (gutural) no aparece, reemplazado por vocal larga.
        
        Returns:
            [] (gutural perdida)
        """
        return []
    
    def _get_R1_for_imperative(self) -> Optional[Consonant]:
        """
        R₁ (gutural) no aparece en imperativo.
        
        Returns:
            None (gutural perdida)
        """
        return None
    
    def _should_geminate_R2_in_present(self) -> bool:
        """
        I/voc SÍ gemina R₂ en presente (como verbos fuertes).
        
        a-ḥḥaz (no *aḥaz)
        
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
        Forma presente de I/voc a.
        
        Proceso:
            1. Prefijo personal (i/t/n)
            2. Vocal inicial 'a' (probablemente larga)
            3. R₂ geminada
            4. Vocal de presente
            5. R₃
        
        Examples:
            ahāzum Pres 3sm: aḥḥaz (< *yaʔḥaz)
            ahāzum Pres 2sm: taḥḥaz
            ahāzum Pres 1s: aḥḥaz
        """
        phonemes = []
        
        # Prefijo personal + vocal 'a' compensatoria
        # La vocal suele ser larga por compensación
        if person == 3:
            # i + a → a (la i se asimila o vocal larga aparece)
            # Simplificado: solo vocal 'a' larga
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.A,
                length=VowelLength.LONG  # Probablemente larga
            )))
        elif person == 2:
            phonemes.append(get_consonant('t'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.A,
                length=VowelLength.LONG
            )))
        elif person == 1:
            if number == 'pl':
                phonemes.append(get_consonant('n'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.A,
                length=VowelLength.LONG
            )))
        
        # R₁ se omite (gutural perdida)
        
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
                quality=VowelQuality.U,
                length=VowelLength.LONG
            )))
        
        return phonemes
    
    def form_preterite(self, person: int = 3, number: str = 'sg',
                       gender: str = 'm') -> List[Phoneme]:
        """
        Forma pretérito de I/voc a.
        
        Proceso:
            1. Prefijo personal con VOCAL LARGA compensatoria
               - 1s: ā-ḥuz
               - 3s: ē-ḥuz (< *yaʔḥuz)
               - 2s: tā-ḥuz
            2. R₂
            3. Vocal de pretérito
            4. R₃
        
        Examples:
            ahāzum Pret 1s: āḥuz
            ahāzum Pret 3sm: ēḥuz
            ahāzum Pret 2sm: tāḥuz
        """
        phonemes = []
        has_ending = self._has_vocalic_ending(number, gender)
        
        # Prefijo con vocal larga compensatoria
        if person == 1:
            # 1s/1p: ā- (a larga)
            if number == 'pl':
                phonemes.append(get_consonant('n'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.A,
                length=VowelLength.LONG
            )))
        elif person == 3:
            # 3s/3p: ē- (e larga < *ya-)
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.E,
                length=VowelLength.LONG
            )))
        elif person == 2:
            # 2s/2p: t + ā-
            phonemes.append(get_consonant('t'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.A,
                length=VowelLength.LONG
            )))
        
        # R₁ se omite
        
        # R₂ (sin geminación)
        phonemes.append(self.root.R2)
        
        # Vocal de pretérito (puede tener síncope)
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
                quality=VowelQuality.U,
                length=VowelLength.LONG
            )))
        
        return phonemes
    
    def form_perfect(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma perfect de I/voc a.
        
        Proceso:
            1. Prefijo con vocal larga (ī/tā/nē)
            2. Infix-t
            3. Vocal a
            4. R₂
            5. Vocal a
            6. R₃
        
        Examples:
            ahāzum Perf 3sm: ītaḥaz
            ahāzum Perf 2sm: tātaḥaz
        """
        phonemes = []
        
        # Prefijo con vocal larga
        if person == 3:
            # ī- (i larga)
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.I,
                length=VowelLength.LONG
            )))
        elif person == 2:
            # tā-
            phonemes.append(get_consonant('t'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.A,
                length=VowelLength.LONG
            )))
        elif person == 1:
            # nē- o ā-
            if number == 'pl':
                phonemes.append(get_consonant('n'))
                phonemes.append(Vowel(features=VowelFeatures(
                    quality=VowelQuality.E,
                    length=VowelLength.LONG
                )))
            else:
                phonemes.append(Vowel(features=VowelFeatures(
                    quality=VowelQuality.A,
                    length=VowelLength.LONG
                )))
        
        # Infix-t (no geminado en I/voc)
        phonemes.append(get_consonant('t'))
        
        # Vocal a
        phonemes.append(Vowel(features=VowelFeatures(
            quality=VowelQuality.A,
            length=VowelLength.SHORT
        )))
        
        # R₂
        phonemes.append(self.root.R2)
        
        # Vocal a
        phonemes.append(Vowel(features=VowelFeatures(
            quality=VowelQuality.A,
            length=VowelLength.SHORT
        )))
        
        # R₃
        phonemes.append(self.root.R3)
        
        return phonemes
    
    def form_imperative(self, number: str = 'sg',
                        gender: str = 'm') -> List[Phoneme]:
        """
        Forma imperativo de I/voc a.
        
        Proceso:
            1. R₂
            2. Vocal de pretérito
            3. R₃
        
        Examples:
            ahāzum Imp sm: ḥuz
            ahāzum Imp pm: ḥuzā
        """
        phonemes = []
        
        # R₁ se omite
        
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
                quality=VowelQuality.A,
                length=VowelLength.LONG
            )))
        
        return phonemes


# ============================================================================
# I/VOC E STEM
# ============================================================================

class I_e_Stem(I_a_Stem):
    """
    I/voc e Stem - Verbos con vocal inicial 'e' por gutural perdida.
    
    Fonológicamente IDÉNTICO a I/a Stem, solo difiere la vocal inicial.
    
    Características:
    - Proto-semítico: *ʕapaš, *ḥarab → OA: epāšum, erābum
    - Vocal inicial: 'e' (no 'a')
    - Todo lo demás igual que I/a
    
    Referencias: § 18.3.1
    
    Ejemplos:
        epāšum (a/u) 'hacer, crear':
            Presente 3sm: eppeš
            Pretérito 1s: ēpuš
            Pretérito 3sm: ēpuš (mismo que 1s en este caso)
            Imperativo sm: puš
        
        erābum (a/u) 'entrar':
            Presente 3sm: errab
            Pretérito 3sm: ērub
    
    Note:
        Hereda de I_a_Stem y solo cambia initial_vowel.
    """
    
    def __init__(self, root: WeakRoot):
        """
        Inicializa I/e Stem.
        
        Args:
            root: WeakRoot con weak_type = I_VOC_E
        """
        if root.weak_type != WeakVerbType.I_VOC_E:
            raise ValueError(
                f"I_e_Stem requiere I_VOC_E, got {root.weak_type}"
            )
        # Inicializar como I_a pero cambiar vocal
        # Hack temporal: cambiar weak_type para pasar validación I_a_Stem
        original_type = root.weak_type
        root.weak_type = WeakVerbType.I_VOC_A
        super().__init__(root=root)
        root.weak_type = original_type
        
        # La diferencia clave: vocal 'e' en vez de 'a'
        self.initial_vowel = 'e'
    
    # ========================================================================
    # Override methods para usar 'e' en vez de 'a'
    # ========================================================================
    
    def form_present(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma presente con vocal 'e' inicial.
        
        Examples:
            epāšum Pres 3sm: eppeš
        """
        phonemes = []
        
        # Prefijo + vocal 'e' compensatoria (larga)
        if person == 3:
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.E,
                length=VowelLength.LONG
            )))
        elif person == 2:
            phonemes.append(get_consonant('t'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.E,
                length=VowelLength.LONG
            )))
        elif person == 1:
            if number == 'pl':
                phonemes.append(get_consonant('n'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.E,
                length=VowelLength.LONG
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
                quality=VowelQuality.U,
                length=VowelLength.LONG
            )))
        
        return phonemes
    
    def form_preterite(self, person: int = 3, number: str = 'sg',
                       gender: str = 'm') -> List[Phoneme]:
        """
        Forma pretérito con 'ē' para persona 1 y 3.
        
        Examples:
            epāšum Pret 1s: ēpuš
            epāšum Pret 3sm: ēpuš
            epāšum Pret 2sm: tēpuš
        """
        phonemes = []
        has_ending = self._has_vocalic_ending(number, gender)
        
        # Vocal larga compensatoria
        if person == 1:
            # 1s: ē- (e larga)
            if number == 'pl':
                phonemes.append(get_consonant('n'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.E,
                length=VowelLength.LONG
            )))
        elif person == 3:
            # 3s: ē-
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.E,
                length=VowelLength.LONG
            )))
        elif person == 2:
            # 2s: t + ē-
            phonemes.append(get_consonant('t'))
            phonemes.append(Vowel(features=VowelFeatures(
                quality=VowelQuality.E,
                length=VowelLength.LONG
            )))
        
        # R₂
        phonemes.append(self.root.R2)
        
        # Vocal de pretérito
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
                quality=VowelQuality.U,
                length=VowelLength.LONG
            )))
        
        return phonemes
    
    # form_perfect e form_imperative heredan de I_a_Stem
    # (son idénticos, solo cambia la vocal de prefijo en perfect)

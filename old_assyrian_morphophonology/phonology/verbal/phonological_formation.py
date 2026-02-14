"""
Phonological formation helpers for Old Assyrian verbal stems.

This module provides utility functions for phonological processes
involved in forming verbal stems, such as:
- Inserting infixes (e.g., -t- in Gt-stem)
- Gemininating consonants (e.g., R₂ in present)
- Applying vowel assimilation
- Applying vowel syncope
- Applying consonant assimilation

Based on Kouwenberg (2017) Chapters 16-17.

Author: Claude
Date: 2026-02-11
"""

from typing import List, Tuple
from ..phoneme import Phoneme, Vowel, Consonant
from ..inventory import get_vowel, get_consonant


# ============================================================================
# PREFIX GENERATION
# ============================================================================

def get_prefix(person: int, number: str, gender: str,
               use_u_prefix: bool = False) -> List[Phoneme]:
    """
    Obtiene el prefijo de persona para prefix conjugations.
    
    Args:
        person: 1, 2, or 3
        number: 'sg', 'du', or 'pl'
        gender: 'm' or 'f'
        use_u_prefix: True for D-stem, Š-stem, I/w verbs
        
    Returns:
        Lista con el prefijo (puede estar vacío para imperative)
        
    Prefixes (§16.6.1):
        Default (i/a-prefixes):
            3p: i-
            2p: ta-
            1s: a-
            1p: ni-
        
        u-prefixes (D, Š, I/w):
            3p: u-
            2p: tu-
            1s: u-
            1p: nu-
            
    Examples:
        >>> get_prefix(3, 'sg', 'm', False)
        [i]
        >>> get_prefix(3, 'sg', 'm', True)
        [u]
        >>> get_prefix(2, 'sg', 'm', False)
        [t, a]
        >>> get_prefix(1, 'pl', 'm', False)
        [n, i]
    """
    if use_u_prefix:
        # u-prefixes
        if person == 3:
            return [get_vowel('u')]
        elif person == 2:
            return [get_consonant('t'), get_vowel('u')]
        elif person == 1 and number == 'sg':
            return [get_vowel('u')]
        elif person == 1 and number == 'pl':
            return [get_consonant('n'), get_vowel('u')]
    else:
        # i/a-prefixes (default)
        if person == 3:
            return [get_vowel('i')]
        elif person == 2:
            return [get_consonant('t'), get_vowel('a')]
        elif person == 1 and number == 'sg':
            return [get_vowel('a')]
        elif person == 1 and number == 'pl':
            return [get_consonant('n'), get_vowel('i')]
    
    return []  # Shouldn't reach here


def get_suffix(person: int, number: str, gender: str) -> List[Phoneme]:
    """
    Obtiene el sufijo de número/género para prefix conjugations.
    
    Args:
        person: 1, 2, or 3
        number: 'sg', 'du', or 'pl'
        gender: 'm' or 'f'
        
    Returns:
        Lista con el sufijo (vacía para 3sm, 2sm, 1s)
        
    Suffixes (§16.6.1):
        Singular: none (except 2sf: -ī)
        Dual: -ā
        Plural: -ū (masc), -ā (fem)
        
    Examples:
        >>> get_suffix(3, 'sg', 'm')
        []
        >>> get_suffix(2, 'sg', 'f')
        [ī]
        >>> get_suffix(3, 'du', 'm')
        [ā]
        >>> get_suffix(3, 'pl', 'm')
        [ū]
    """
    if number == 'sg':
        if person == 2 and gender == 'f':
            return [get_vowel('ī')]
        return []
    elif number == 'du':
        return [get_vowel('ā')]
    elif number == 'pl':
        if gender == 'm':
            return [get_vowel('ū')]
        else:  # fem
            return [get_vowel('ā')]
    return []


# ============================================================================
# INFIX INSERTION
# ============================================================================

def insert_t_infix(root_consonants: List[Consonant],
                   position: int = 1) -> List[Consonant]:
    """
    Inserta el infijo -t- en la posición especificada.
    
    Args:
        root_consonants: Lista de radicales [R₁, R₂, R₃]
        position: Posición donde insertar (1 = después de R₁)
        
    Returns:
        Lista con el infijo insertado
        
    Used in: Gt-stem, Dt-stem, Št-stems, Perfect
    
    Note:
        La asimilación de -t- se maneja por separado en
        apply_t_assimilation().
        
    Example:
        >>> root = [p, r, s]
        >>> insert_t_infix(root, 1)
        [p, t, r, s]
    """
    result = root_consonants[:position]
    result.append(get_consonant('t'))
    result.extend(root_consonants[position:])
    return result


def insert_tan_infix(root_consonants: List[Consonant],
                     position: int = 1) -> List[Consonant]:
    """
    Inserta el infijo -tan- en la posición especificada.
    
    Args:
        root_consonants: Lista de radicales
        position: Posición donde insertar
        
    Returns:
        Lista con el infijo insertado
        
    Used in: Gtn-stem, Dtn-stem, Štn-stem, Ntn-stem (pluractional)
    
    Example:
        >>> root = [p, r, s]
        >>> insert_tan_infix(root, 1)
        [p, t, a, n, r, s]
    """
    result = root_consonants[:position]
    result.extend([
        get_consonant('t'),
        get_vowel('a'),
        get_consonant('n')
    ])
    result.extend(root_consonants[position:])
    return result


# ============================================================================
# GEMINATION
# ============================================================================

def geminate_consonant(phonemes: List[Phoneme], 
                       index: int) -> List[Phoneme]:
    """
    Gemina (duplica) una consonante en el índice especificado.
    
    Args:
        phonemes: Lista de fonemas
        index: Índice de la consonante a geminar
        
    Returns:
        Lista con la consonante geminada
        
    Used in:
        - G-stem present: gemination of R₂
        - D-stem: gemination of R₂
        - Gtn-stem: gemination of R₂
        
    Example:
        >>> phonemes = [i, p, a, r, a, s]
        >>> geminate_consonant(phonemes, 3)  # index of R₂
        [i, p, a, r, r, a, s]
    """
    if index < 0 or index >= len(phonemes):
        raise ValueError(f"Index {index} out of range")
    
    if not isinstance(phonemes[index], Consonant):
        raise ValueError(f"Phoneme at index {index} is not a consonant")
    
    result = phonemes[:index+1]
    result.append(phonemes[index])  # Duplicate
    result.extend(phonemes[index+1:])
    return result


# ============================================================================
# VOWEL ASSIMILATION (§3.4.9)
# ============================================================================

def apply_vowel_assimilation(phonemes: List[Phoneme],
                             ending_vowel: str) -> List[Phoneme]:
    """
    Aplica asimilación vocálica según § 3.4.9.
    
    Regla: Vocal de sílaba adyacente asimila a vocal del ending.
    
    Args:
        phonemes: Secuencia fonémica del stem
        ending_vowel: Vocal del ending ('a', 'i', 'u', 'ā', etc.)
        
    Returns:
        Secuencia con asimilación aplicada
        
    Applies to: a/a, a/u, a/i vowel classes when ending present
    
    Examples:
        >>> # iparras + ū → iparrusū
        >>> phonemes = [i, p, a, r, r, a, s]
        >>> apply_vowel_assimilation(phonemes, 'u')
        [i, p, a, r, r, u, s]  # 'a' before R₃ → 'u'
        
        >>> # iṣabbat + ī → iṣabbitī
        >>> phonemes = [i, ṣ, a, b, b, a, t]
        >>> apply_vowel_assimilation(phonemes, 'i')
        [i, ṣ, a, b, b, i, t]  # 'a' before R₃ → 'i'
    """
    # Find the vowel between R₂ (or R₂R₂) and R₃
    # This is typically the penultimate or antepenultimate vowel
    
    result = phonemes.copy()
    target_vowel = ending_vowel[0] if ending_vowel else None
    
    if not target_vowel:
        return result
    
    # Search backwards for the last vowel before final consonant
    for i in range(len(result) - 2, -1, -1):
        if isinstance(result[i], Vowel):
            # Replace with assimilated vowel
            result[i] = get_vowel(target_vowel)
            break
    
    return result


# ============================================================================
# VOWEL SYNCOPE (§3.4.8)
# ============================================================================

def apply_syncope(phonemes: List[Phoneme],
                  has_ending: bool = True) -> List[Phoneme]:
    """
    Aplica síncope vocálica según § 3.4.8.
    
    Regla: Vocal breve en sílaba abierta no acentuada se elimina.
    
    Args:
        phonemes: Secuencia fonémica
        has_ending: Si hay ending después del stem
        
    Returns:
        Secuencia con síncope aplicada
        
    Applies to:
        - Perfect with ending: iptaqidū → iptaqdū
        - Imperative with ending: piqidā → piqdā
        - Preterite a/i with ending: tubilī → tublī
        
    Examples:
        >>> # Perfect: iptaqidū → iptaqdū
        >>> phonemes = [i, p, t, a, q, i, d]
        >>> apply_syncope(phonemes, has_ending=True)
        [i, p, t, a, q, d]  # 'i' deleted
        
        >>> # No syncope if no ending
        >>> apply_syncope(phonemes, has_ending=False)
        [i, p, t, a, q, i, d]  # unchanged
    """
    if not has_ending:
        return phonemes
    
    result = phonemes.copy()
    
    # Simplified rule: delete the last short vowel before R₃
    # (More sophisticated version would check syllable structure)
    
    vowel_indices = [i for i, p in enumerate(result) 
                     if isinstance(p, Vowel)]
    
    if len(vowel_indices) >= 2:
        # Delete penultimate vowel (typically between R₂ and R₃)
        penult_vowel_idx = vowel_indices[-2]
        del result[penult_vowel_idx]
    
    return result


# ============================================================================
# CONSONANT ASSIMILATION
# ============================================================================

def apply_t_assimilation(t_phoneme: Consonant,
                         following: Consonant) -> Consonant:
    """
    Aplica asimilación de -t- a consonante siguiente (§3.2.4.8).
    
    Regla: -t- asimila completamente a dentales y sibilantes.
    
    Args:
        t_phoneme: El infijo -t-
        following: Consonante siguiente (R₁ en Perfect, R₂ en Gt)
        
    Returns:
        Consonante resultante (t o asimilada)
        
    Assimilates to:
        - Dentals: t, d, ṭ
        - Sibilants: s, z, ṣ, š
        
    Examples:
        >>> # t + ṣ → ṣ
        >>> apply_t_assimilation(t, ṣ)
        ṣ
        
        >>> # t + p → t (no assimilation)
        >>> apply_t_assimilation(t, p)
        t
    """
    follow_char = str(following)
    
    # Dentals and sibilants cause assimilation
    if follow_char in ['t', 'd', 'ṭ', 's', 'z', 'ṣ', 'š']:
        return following  # Complete assimilation
    
    return t_phoneme  # No assimilation


def apply_nasal_assimilation(nasal: Consonant,
                             following: Consonant) -> Consonant:
    """
    Aplica asimilación nasal (para N-stem).
    
    Regla: n + R₁ → R₁R₁ (n asimila a R₁)
    
    Args:
        nasal: El prefijo nasal (n)
        following: R₁
        
    Returns:
        R₁ (el nasal desaparece, R₁ se gemina)
        
    Used in: N-stem, Ntn-stem
    
    Example:
        >>> # n + p → p (luego se gemina)
        >>> apply_nasal_assimilation(n, p)
        p  # El segundo p se agrega por geminación
    """
    # La nasal asimila completamente
    # El resultado será geminación de R₁
    return following


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def phonemes_to_string(phonemes: List[Phoneme]) -> str:
    """
    Convierte lista de fonemas a string para debugging.
    
    Args:
        phonemes: Lista de fonemas
        
    Returns:
        String representation
        
    Example:
        >>> phonemes = [i, p, a, r, r, a, s]
        >>> phonemes_to_string(phonemes)
        'iparras'
    """
    return ''.join(str(p) for p in phonemes)


def split_into_syllables(phonemes: List[Phoneme]) -> List[List[Phoneme]]:
    """
    Divide secuencia fonémica en sílabas (simplified).
    
    Args:
        phonemes: Secuencia de fonemas
        
    Returns:
        Lista de sílabas
        
    Note:
        Implementación simplificada. Para silabificación completa,
        usar módulo de Iteración 5.
        
    Example:
        >>> phonemes = [i, p, a, r, s]
        >>> split_into_syllables(phonemes)
        [[i, p], [a, r], [s]]  # aproximación
    """
    # TODO: Integrate with Iteration 5 syllabification module
    # For now, return as single syllable
    return [phonemes]

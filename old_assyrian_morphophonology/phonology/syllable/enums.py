"""
Enumeraciones para estructura silábica del Old Assyrian.

Basado en Kouwenberg (2017) § 3.5.1.
"""

from enum import Enum, auto


# ============================================================================
# PESO SILÁBICO
# ============================================================================

class SyllableWeight(Enum):
    """
    Peso silábico en morae.
    
    LIGHT (μ): CV
    HEAVY (μμ): CV̄, CVC
    SUPERHEAVY (μμμ): CV̄C
    """
    LIGHT = 1         # μ: CV
    HEAVY = 2         # μμ: CV̄, CVC
    SUPERHEAVY = 3    # μμμ: CV̄C


# ============================================================================
# POSICIÓN SILÁBICA
# ============================================================================

class SyllablePosition(Enum):
    """Posición de sílaba en palabra."""
    INITIAL = "initial"          # Primera sílaba
    MEDIAL = "medial"           # Sílaba interna
    FINAL = "final"             # Última sílaba
    PENULTIMATE = "penult"      # Penúltima (importante para estrés)
    ANTEPENULTIMATE = "antepenult"  # Antepenúltima


# ============================================================================
# TIPO DE SÍLABA
# ============================================================================

class SyllableType(Enum):
    """
    Tipo de sílaba por estructura.
    
    Los 4 tipos permitidos en OA.
    """
    CV = "CV"           # Ligera abierta: consonante + vocal corta
    CVV = "CV̄"          # Pesada abierta: consonante + vocal larga
    CVC = "CVC"         # Pesada cerrada: consonante + vocal corta + consonante
    CVVC = "CV̄C"        # Super-pesada: consonante + vocal larga + consonante
    
    def get_weight(self) -> SyllableWeight:
        """Retorna peso correspondiente a este tipo."""
        if self == SyllableType.CV:
            return SyllableWeight.LIGHT
        elif self == SyllableType.CVV:
            return SyllableWeight.HEAVY
        elif self == SyllableType.CVC:
            return SyllableWeight.HEAVY
        else:  # CVVC
            return SyllableWeight.SUPERHEAVY


# ============================================================================
# TIPO DE CLUSTER
# ============================================================================

class ClusterType(Enum):
    """Tipo de cluster consonántico."""
    GEMINATE = "geminate"           # Geminada: pp, rr, etc.
    HETEROGENEOUS = "heterogeneous"  # Diferentes: nt, pr, etc.
    LIQUID_C = "liquid_c"           # Líquida + consonante (r/l + C)
    C_LIQUID = "c_liquid"           # Consonante + líquida (C + r/l)
    NASAL_C = "nasal_c"             # Nasal + consonante (n/m + C)
    C_NASAL = "c_nasal"             # Consonante + nasal (C + n/m)
    H_C = "h_c"                     # h + consonante
    C_H = "c_h"                     # Consonante + h
    SIBILANT_C = "sibilant_c"       # Sibilante + consonante
    C_SIBILANT = "c_sibilant"       # Consonante + sibilante


# ============================================================================
# CONTEXTO DE EPÉNTESIS
# ============================================================================

class EpenthesisContext(Enum):
    """Contexto donde ocurre epéntesis."""
    CLUSTER_RESOLUTION = "cluster"     # Romper cluster difícil
    IMPERATIVE = "imperative"          # Imperativo con terminación
    TRIPLE_CLUSTER = "triple"          # Prevenir cluster triple
    CONSTRUCT_STATE = "construct"      # Estado constructo + sufijo
    SYLLABIFICATION = "syllabification" # Para silabificación legal


# ============================================================================
# TIPO DE VOCAL EPENTÉTICA
# ============================================================================

class EpentheticVowel(Enum):
    """Tipo de vocal insertada en epéntesis."""
    I = "i"     # Más común
    U = "u"     # Menos común
    E = "e"     # Con líquidas (por i → e / _r)
    A = "a"     # Excepcional (probables errores)


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def is_light_syllable(syllable_type: SyllableType) -> bool:
    """True si sílaba es ligera (1 mora)."""
    return syllable_type == SyllableType.CV


def is_heavy_syllable(syllable_type: SyllableType) -> bool:
    """True si sílaba es pesada (2 morae)."""
    return syllable_type in [SyllableType.CVV, SyllableType.CVC]


def is_superheavy_syllable(syllable_type: SyllableType) -> bool:
    """True si sílaba es super-pesada (3 morae)."""
    return syllable_type == SyllableType.CVVC


def is_open_syllable(syllable_type: SyllableType) -> bool:
    """True si sílaba es abierta (sin coda)."""
    return syllable_type in [SyllableType.CV, SyllableType.CVV]


def is_closed_syllable(syllable_type: SyllableType) -> bool:
    """True si sílaba es cerrada (con coda)."""
    return syllable_type in [SyllableType.CVC, SyllableType.CVVC]


def get_syllable_type_from_structure(
    has_onset: bool,
    vowel_length: str,
    has_coda: bool
) -> SyllableType:
    """
    Determina tipo de sílaba desde estructura.
    
    Args:
        has_onset: True si tiene onset consonántico
        vowel_length: 'short' o 'long'
        has_coda: True si tiene coda consonántica
    
    Returns:
        SyllableType correspondiente
    """
    # OA: onset siempre presente (ʾ si no hay consonante visible)
    # Aquí asumimos onset presente
    
    if vowel_length == 'short':
        if has_coda:
            return SyllableType.CVC
        else:
            return SyllableType.CV
    else:  # 'long'
        if has_coda:
            return SyllableType.CVVC
        else:
            return SyllableType.CVV


def cluster_needs_epenthesis(c1_symbol: str, c2_symbol: str) -> bool:
    """
    Determina si cluster necesita epéntesis.
    
    Clusters que típicamente requieren epéntesis:
      - r/l + C (líquida + consonante)
      - h + C
      - Algunos C + n/m
    
    Args:
        c1_symbol: Primera consonante
        c2_symbol: Segunda consonante
    
    Returns:
        True si epéntesis típicamente necesaria
    """
    # Líquida + consonante
    if c1_symbol in ['r', 'l']:
        return True
    
    # h + consonante
    if c1_symbol == 'h':
        return True
    
    # Nasal + consonante (pero muchos asimilan, ver Iter 3)
    # Solo si no asimilan
    if c1_symbol in ['n', 'm']:
        # n típicamente asimila (Iter 3)
        # Pero algunos contextos pueden requerir epéntesis
        return False  # Default: asimilación
    
    return False


def get_cluster_type(c1_symbol: str, c2_symbol: str) -> ClusterType:
    """
    Determina tipo de cluster.
    
    Args:
        c1_symbol: Primera consonante
        c2_symbol: Segunda consonante
    
    Returns:
        ClusterType
    """
    # Geminada
    if c1_symbol == c2_symbol:
        return ClusterType.GEMINATE
    
    # Líquida + C
    if c1_symbol in ['r', 'l']:
        return ClusterType.LIQUID_C
    
    # C + líquida
    if c2_symbol in ['r', 'l']:
        return ClusterType.C_LIQUID
    
    # Nasal + C
    if c1_symbol in ['n', 'm']:
        return ClusterType.NASAL_C
    
    # C + nasal
    if c2_symbol in ['n', 'm']:
        return ClusterType.C_NASAL
    
    # h + C
    if c1_symbol == 'h':
        return ClusterType.H_C
    
    # C + h
    if c2_symbol == 'h':
        return ClusterType.C_H
    
    # Sibilante + C
    if c1_symbol in ['s', 'z', 'ṣ', 'š']:
        return ClusterType.SIBILANT_C
    
    # C + sibilante
    if c2_symbol in ['s', 'z', 'ṣ', 'š']:
        return ClusterType.C_SIBILANT
    
    # Default: heterogéneo
    return ClusterType.HETEROGENEOUS

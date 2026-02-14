"""
Enumeraciones para procesos vocálicos del Old Assyrian.

Basado en Kouwenberg (2017) § 3.4.2-3.4.11.
"""

from enum import Enum, auto


# ============================================================================
# TIPOS DE REGLA VOCÁLICA
# ============================================================================

class VowelRuleType(Enum):
    """Tipo de regla de cambio vocálico."""
    ALTERNATION = "alternation"          # a/e, i/e, etc.
    ASSIMILATION = "assimilation"        # V₁ → V₂ por influencia
    CONTRACTION = "contraction"          # VV → V̂
    LENGTHENING = "lengthening"          # V → V̄ (compensatorio, etc.)
    SHORTENING = "shortening"            # V̄ → V
    DELETION = "deletion"                # V → ∅ (síncope, apócope)
    CONDITIONING = "conditioning"        # Cambio por consonante adyacente


# ============================================================================
# DIRECCIÓN DE CAMBIO VOCÁLICO
# ============================================================================

class VowelChangeDirection(Enum):
    """Dirección del cambio vocálico."""
    PROGRESSIVE = "progressive"          # V₁ → V₂ (primer vocal influye)
    REGRESSIVE = "regressive"            # V₁ ← V₂ (segunda vocal influye)
    BIDIRECTIONAL = "bidirectional"      # Puede ir ambas direcciones
    CONTEXTUAL = "contextual"            # Por contexto consonántico


# ============================================================================
# POSICIÓN DE ELEMENTO CONDICIONANTE
# ============================================================================

class ConditioningPosition(Enum):
    """Posición del elemento que condiciona cambio vocálico."""
    PRECEDING = "preceding"              # _CV (consonante precede)
    FOLLOWING = "following"              # VC_ (consonante sigue)
    BOTH = "both"                       # CVC (ambos lados)
    INTERVENING = "intervening"          # V₁CV₂ (entre vocales)
    DISTANT = "distant"                 # Armonía a distancia
    ADJACENT = "adjacent"               # Directamente adyacente


# ============================================================================
# TIPOS DE ALTERNANCIA
# ============================================================================

class AlternationType(Enum):
    """Tipos específicos de alternancia vocálica."""
    A_E = "a_e"                         # a ~ e
    A_I = "a_i"                         # a ~ i
    A_U = "a_u"                         # a ~ u
    U_I_E = "u_i_e"                     # u ~ i/e
    I_E = "i_e"                         # i ~ e (cortas)
    II_EE = "ii_ee"                     # ī ~ ē (largas)
    AA_EE = "aa_ee"                     # ā ~ ē (largas)


# ============================================================================
# TIPOS DE ASIMILACIÓN VOCÁLICA
# ============================================================================

class VowelAssimilationType(Enum):
    """Tipos de asimilación vocálica."""
    TOTAL = "total"                      # Asimilación completa
    PARTIAL_HEIGHT = "height"            # Solo altura vocálica
    PARTIAL_BACKNESS = "backness"        # Solo anterioridad/posterioridad
    HARMONY = "harmony"                  # Armonía vocálica general


# ============================================================================
# TIPOS DE CONTRACCIÓN
# ============================================================================

class ContractionType(Enum):
    """Tipos de contracción vocálica."""
    IDENTICAL = "identical"              # VV → V̂ (idénticas)
    HETEROGENEOUS = "heterogeneous"      # V₁V₂ → V̂ (diferentes)
    WITH_GLIDE = "with_glide"           # V₁wV₂ → V̂ (con débil)
    ACROSS_BOUNDARY = "cross_boundary"   # A través de frontera morfológica


# ============================================================================
# CONTEXTOS MORFOLÓGICOS
# ============================================================================

class VowelMorphologicalContext(Enum):
    """Contexto morfológico para reglas vocálicas."""
    ROOT = "root"                        # Dentro de raíz
    SUFFIX = "suffix"                    # En sufijo
    PREFIX = "prefix"                    # En prefijo
    ACROSS_MORPHEME = "across_morpheme"  # A través de frontera
    CASE_ENDING = "case_ending"          # Terminación de caso
    VERB_ENDING = "verb_ending"          # Terminación verbal
    CONSTRUCT_STATE = "construct"        # Estado constructo
    FINAL_SYLLABLE = "final"            # Sílaba final


# ============================================================================
# OBLIGATORIEDAD DE REGLA
# ============================================================================

class RuleObligatoriness(Enum):
    """Obligatoriedad de aplicación de regla."""
    OBLIGATORY = "obligatory"            # Siempre aplica
    OPTIONAL = "optional"                # Variable
    INCONSISTENT = "inconsistent"        # Sin patrón claro
    SPORADIC = "sporadic"               # Esporádico, posibles errores
    DIALECTAL = "dialectal"             # Variación dialectal


# ============================================================================
# NIVEL DE EVIDENCIA
# ============================================================================

class VowelEvidenceLevel(Enum):
    """Nivel de evidencia para regla vocálica."""
    EXPLICIT = "explicit"                # Spelling claro
    PLENE = "plene"                     # Spellings plenos
    BROKEN = "broken"                   # Broken spellings
    COMPARATIVE = "comparative"          # Comparación dialectal
    THEORETICAL = "theoretical"          # Inferencia teórica
    MINIMAL_PAIRS = "minimal_pairs"      # Pares mínimos


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def get_vowel_quality_from_symbol(symbol: str) -> str:
    """
    Obtiene calidad vocálica desde símbolo.
    
    Args:
        symbol: Símbolo de vocal (a, ā, i, ī, e, ē, u, ū)
    
    Returns:
        Calidad base (a, i, e, u)
    """
    return symbol.rstrip('̄')  # Remueve macron si presente


def is_long_vowel(symbol: str) -> bool:
    """
    Determina si vocal es larga.
    
    Args:
        symbol: Símbolo de vocal
    
    Returns:
        True si es larga (tiene macron o circumflejo)
    """
    return '̄' in symbol or '̂' in symbol


def is_contracted_vowel(symbol: str) -> bool:
    """
    Determina si vocal es producto de contracción.
    
    Args:
        symbol: Símbolo de vocal
    
    Returns:
        True si tiene circumflejo (marca contracción)
    """
    return '̂' in symbol


def vowels_match_quality(v1_symbol: str, v2_symbol: str) -> bool:
    """
    Determina si dos vocales tienen misma calidad.
    
    Args:
        v1_symbol: Símbolo primera vocal
        v2_symbol: Símbolo segunda vocal
    
    Returns:
        True si tienen misma calidad base
    """
    q1 = get_vowel_quality_from_symbol(v1_symbol)
    q2 = get_vowel_quality_from_symbol(v2_symbol)
    return q1 == q2


def get_alternation_type(v1_quality: str, v2_quality: str) -> AlternationType:
    """
    Determina tipo de alternancia entre dos calidades vocálicas.
    
    Args:
        v1_quality: Primera calidad (a, i, e, u)
        v2_quality: Segunda calidad
    
    Returns:
        AlternationType correspondiente
    """
    pair = tuple(sorted([v1_quality, v2_quality]))
    
    mapping = {
        ('a', 'e'): AlternationType.A_E,
        ('a', 'i'): AlternationType.A_I,
        ('a', 'u'): AlternationType.A_U,
        ('e', 'i'): AlternationType.I_E,
        ('e', 'u'): AlternationType.U_I_E,
        ('i', 'u'): AlternationType.U_I_E,
    }
    
    return mapping.get(pair, AlternationType.A_E)  # Default


def is_guttural_consonant(consonant_symbol: str) -> bool:
    """
    Determina si consonante es gutural.
    
    Gutturales: ḫ, ʾ, ʿ, h, ḥ
    
    Args:
        consonant_symbol: Símbolo de consonante
    
    Returns:
        True si es gutural
    """
    gutturals = {'ḫ', 'ʾ', 'ʿ', 'h', 'ḥ'}
    return consonant_symbol in gutturals


def requires_vowel_assimilation(
    penultimate_vowel: str,
    final_vowel: str,
    syllable_count: int
) -> bool:
    """
    Determina si se requiere asimilación vocálica (regla asiria).
    
    Regla: Si penúltima sílaba de palabra 3+ sílabas termina en a corta,
           asimila a vocal de sílaba final.
    
    Args:
        penultimate_vowel: Vocal penúltima ('a' corta)
        final_vowel: Vocal final
        syllable_count: Número de sílabas
    
    Returns:
        True si debe aplicar asimilación
    """
    if syllable_count < 3:
        return False
    
    if penultimate_vowel != 'a':
        return False
    
    # a corta (no larga)
    if is_long_vowel(penultimate_vowel):
        return False
    
    return True

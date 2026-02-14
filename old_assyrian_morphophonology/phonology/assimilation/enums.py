"""
Enumeraciones para asimilación consonántica del Old Assyrian.

Basado en Kouwenberg (2017) § 3.2.4-3.2.7.
"""

from enum import Enum, auto


# ============================================================================
# DIRECCIÓN DE ASIMILACIÓN
# ============================================================================

class AssimilationDirection(Enum):
    """
    Dirección de la asimilación.
    
    Ejemplos:
        PROGRESSIVE: n + p → pp (C₁ → C₂)
        REGRESSIVE: -q + k → kk (C₁ ← C₂)
        RECIPROCAL: Ambos cambian
        COALESCENCE: C₁ + C₂ → C₃ (nuevo segmento)
    """
    PROGRESSIVE = "progressive"      # C₁C₂ → C₂C₂
    REGRESSIVE = "regressive"        # C₁C₂ → C₁C₁
    RECIPROCAL = "reciprocal"        # Ambos cambian
    COALESCENCE = "coalescence"      # Fusión en nuevo segmento


# ============================================================================
# TIPO DE ASIMILACIÓN
# ============================================================================

class AssimilationType(Enum):
    """
    Tipo/grado de asimilación.
    
    TOTAL: Consonante completa asimila (n + p → pp)
    PARTIAL: Solo algunos rasgos asimilan (b → p / _[voiceless])
    """
    TOTAL = "total"                  # Asimilación completa
    PARTIAL_VOICING = "voicing"      # Solo sonoridad
    PARTIAL_PLACE = "place"          # Solo punto de articulación
    PARTIAL_MANNER = "manner"        # Solo modo de articulación
    DEVOICING = "devoicing"          # Caso especial: ensordecimiento
    VOICING = "voicing_assim"        # Caso especial: sonorización


# ============================================================================
# CONTEXTOS MORFOLÓGICOS
# ============================================================================

class MorphologicalBoundary(Enum):
    """
    Tipo de frontera morfológica donde ocurre asimilación.
    
    Asimilación más común en fronteras morfológicas que dentro de raíz.
    """
    PREFIX_ROOT = "prefix_root"          # in-paras → ipparas
    ROOT_SUFFIX = "root_suffix"          # qāt-šu → qāssu
    PROCLITIC_HOST = "proclitic_host"    # in(a) Kaneš → ikKaneš
    COMPOUND = "compound"                # šaman šammem → šamaššammū
    WORD_BOUNDARY = "word_boundary"      # Entre palabras (raro)
    INTRA_ROOT = "intra_root"           # Dentro de raíz (muy raro)
    INFIX = "infix"                     # Infijo -t- verbal


class MorphemeType(Enum):
    """Tipo de morfema involucrado en asimilación."""
    VERBAL_PREFIX = "verbal_prefix"      # in-, ta-
    VERBAL_INFIX = "verbal_infix"        # -t-
    CASE_ENDING = "case_ending"          # -um, -am, -em
    PRONOMINAL_SUFFIX = "pronominal"     # -šu, -ka, etc.
    FEMININE_SUFFIX = "feminine"         # -t-
    ENCLITIC = "enclitic"               # -ma
    PREPOSITION = "preposition"          # ina, ana
    ROOT = "root"                        # Raíz léxica


# ============================================================================
# ESTADOS DE ASIMILACIÓN
# ============================================================================

class AssimilationStatus(Enum):
    """Estado de aplicación de asimilación."""
    OBLIGATORY = "obligatory"            # Siempre aplica
    OPTIONAL = "optional"                # Variable (ej: b + ma)
    BLOCKED = "blocked"                  # Bloqueada (ej: n radical)
    DIALECT_VARIABLE = "dialectal"       # Variación dialectal


# ============================================================================
# TIPOS DE PÉRDIDA
# ============================================================================

class ConsonantLossType(Enum):
    """Tipo de pérdida consonántica."""
    WORD_FINAL = "word_final"            # -m#, -n# en morfemas
    SYLLABLE_FINAL = "syllable_final"    # r, s en _C
    INTERVOCALIC = "intervocalic"        # r entre vocales (raro)
    CLUSTER_SIMPLIFICATION = "cluster"   # CCC → CC
    DISSIMILATORY = "dissimilatory"      # Por disimilación


class LossContext(Enum):
    """Contexto de pérdida."""
    GRAMMATICAL_MORPHEME = "grammatical"  # Solo morfemas gramaticales
    STEM = "stem"                         # Raíz (muy raro)
    ANY = "any"                          # Cualquier contexto


# ============================================================================
# TIPOS DE METÁTESIS
# ============================================================================

class MetathesisType(Enum):
    """Tipo de metátesis."""
    CLUSTER = "cluster"                  # Dentro de cluster (loanwords)
    DISTANT = "distant"                  # Sibilante...t (verbos)
    VOWEL_CONSONANT = "vowel_consonant"  # V-C (ej: gubabtum ~ ugbabtum)


# ============================================================================
# TIPOS DE DISIMILACIÓN
# ============================================================================

class DissimilationType(Enum):
    """Tipo de disimilación."""
    DISTANT = "distant"                  # C...C (ej: ma- → na-)
    ADJACENT = "adjacent"                # CC (muy raro)
    CONSONANT_TO_CONSONANT = "C_to_C"   # C₁ → C₂
    CONSONANT_TO_ZERO = "C_to_zero"     # C → ∅


# ============================================================================
# NIVELES DE EVIDENCIA
# ============================================================================

class EvidenceLevel(Enum):
    """
    Nivel de evidencia para una regla fonológica.
    
    EXPLICIT: Spelling muestra claramente el resultado
    COMPARATIVE: Basado en comparación con otros dialectos
    THEORETICAL: Inferido teóricamente
    """
    EXPLICIT = "explicit"                # Spelling claro
    COMPARATIVE = "comparative"          # Comparación dialectal
    THEORETICAL = "theoretical"          # Inferencia teórica
    SPORADIC = "sporadic"               # Casos esporádicos (¿errores?)


# ============================================================================
# PRECEDENCIA DE REGLAS
# ============================================================================

class RulePrecedence(Enum):
    """
    Nivel de precedencia para ordenamiento de reglas.
    
    Números más altos = aplica primero
    """
    MORPHOLOGY = 1000        # Inserción de morfemas
    SYNCOPE = 900           # Síncope vocálica (crea clusters)
    OBLIGATORY_ASSIM = 800  # Asimilaciones obligatorias
    METATHESIS = 700        # Metátesis
    OPTIONAL_ASSIM = 600    # Asimilaciones opcionales
    LOSS = 500             # Pérdida de consonantes
    PHONETIC = 400         # Cambios fonéticos menores


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def get_assimilation_direction_from_context(
    trigger_position: str,
    target_position: str
) -> AssimilationDirection:
    """
    Determina dirección de asimilación basándose en posiciones.
    
    Args:
        trigger_position: 'first' o 'second' en cluster
        target_position: 'first' o 'second' en cluster
    
    Returns:
        AssimilationDirection apropiada
    """
    if trigger_position == 'first' and target_position == 'second':
        return AssimilationDirection.PROGRESSIVE
    elif trigger_position == 'second' and target_position == 'first':
        return AssimilationDirection.REGRESSIVE
    else:
        return AssimilationDirection.RECIPROCAL


def is_morphological_boundary_transparent(boundary: MorphologicalBoundary) -> bool:
    """
    Determina si frontera morfológica es "transparente" para asimilación.
    
    Args:
        boundary: Tipo de frontera
    
    Returns:
        True si asimilación puede cruzar esta frontera
    """
    transparent = {
        MorphologicalBoundary.PREFIX_ROOT,
        MorphologicalBoundary.ROOT_SUFFIX,
        MorphologicalBoundary.PROCLITIC_HOST,
        MorphologicalBoundary.COMPOUND,
    }
    
    return boundary in transparent


def requires_blocking_for_transparency(
    morpheme: MorphemeType,
    consonant_is_radical: bool
) -> bool:
    """
    Determina si asimilación debe bloquearse para preservar transparencia.
    
    Ejemplo: n radical en verbos N-stem NO asimila.
    
    Args:
        morpheme: Tipo de morfema
        consonant_is_radical: True si consonante es parte de raíz
    
    Returns:
        True si asimilación debe bloquearse
    """
    if not consonant_is_radical:
        return False
    
    # n radical en stems verbales específicos
    if morpheme == MorphemeType.ROOT:
        return True
    
    return False

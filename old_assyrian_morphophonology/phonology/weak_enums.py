"""
Enumeraciones específicas para consonantes débiles del Old Assyrian.

Este módulo extiende los enums de la Iteración 1 con tipos específicos
para el comportamiento de ʾ, w, y.
"""

from enum import Enum, auto


# ============================================================================
# POSICIONES DE CONSONANTES DÉBILES
# ============================================================================

class WeakPosition(Enum):
    """
    Posiciones donde aparecen consonantes débiles.
    
    Cada posición tiene reglas específicas de preservación/elisión.
    """
    # Posiciones generales
    WORD_INITIAL = "word_initial"              # #_V (ej: ʾālum)
    INTERVOCALIC = "intervocalic"              # V_V general
    POST_CONSONANTAL = "post_consonantal"      # C_V (ej: merʾum)
    SYLLABLE_FINAL = "syllable_final"          # V_C (ej: raʾš- → rēš-)
    WORD_FINAL = "word_final"                  # V_# (ej: kalāʾum)
    
    # Posiciones específicas (intervocálicas)
    INTERVOCALIC_IDENTICAL = "intervocalic_identical"  # V[same]_V[same] (ej: šaʾālum)
    INTERVOCALIC_DIFFERENT = "intervocalic_different"  # V₁_V₂ donde V₁≠V₂
    
    # Posiciones específicas para glides
    AFTER_U_BEFORE_VOWEL = "after_u"           # u_V (específico para w)
    AFTER_I_BEFORE_VOWEL = "after_i"           # i_V (específico para y)
    BEFORE_HOMORGANIC_VOWEL = "before_homorganic"  # y_i/e, w_u
    
    # Contextos especiales
    PROCLITIC_BOUNDARY = "proclitic"           # Después de preposición proclítica
    COMPOUND_BOUNDARY = "compound"             # En nombres compuestos


class SyllablePosition(Enum):
    """Posición dentro de la sílaba."""
    ONSET = "onset"           # Inicio de sílaba
    NUCLEUS = "nucleus"       # Núcleo (vocal)
    CODA = "coda"            # Final de sílaba
    AMBISYLLABIC = "ambisyllabic"  # Entre dos sílabas


class WordPosition(Enum):
    """Posición dentro de la palabra."""
    INITIAL = "initial"       # Inicio de palabra
    MEDIAL = "medial"        # Medio de palabra
    FINAL = "final"          # Final de palabra


# ============================================================================
# ESTADOS DE PRESERVACIÓN
# ============================================================================

class PreservationStatus(Enum):
    """Estado de preservación de una consonante débil."""
    ALWAYS_PRESERVED = "always_preserved"      # ʾ intervocálico
    ALWAYS_LOST = "always_lost"                # y inicial
    VARIABLY_PRESERVED = "variable"            # ʾ post-consonántico
    CONTEXT_DEPENDENT = "context_dependent"    # w intervocálico
    COMPENSATORY_LENGTHENING = "compensatory"  # ʾ final sílaba → V̄
    CONTRACTED = "contracted"                  # -Cyi- → -Cī-
    FUSED = "fused"                           # ʾ + dental → ṭ


# ============================================================================
# TIPOS DE EVIDENCIA
# ============================================================================

class EvidenceType(Enum):
    """Tipo de evidencia para reconstrucción de débiles."""
    MORPHOLOGICAL = "morphological"      # Basado en clase verbal/nominal
    ETYMOLOGICAL = "etymological"        # Basado en raíz Proto-Semítica
    CONTEXTUAL = "contextual"           # Basado en contexto fonológico
    SPELLING_VARIANT = "spelling_variant"  # Spelling alternativo atestiguado
    PARADIGMATIC = "paradigmatic"       # Otras formas del paradigma
    COMPARATIVE = "comparative"         # Comparación con otros dialectos


# ============================================================================
# MODOS DE RECONSTRUCCIÓN
# ============================================================================

class ReconstructMode(Enum):
    """Modo de reconstrucción de consonantes débiles."""
    NONE = "none"               # No reconstruir, solo parsear lo visible
    AUTO = "auto"              # Usar tabla de decisión automática
    FORCE_ALEPH = "force_aleph"  # Forzar ʾ en casos ambiguos
    FORCE_WAW = "force_waw"      # Forzar w en casos ambiguos
    FORCE_YOD = "force_yod"      # Forzar y en casos ambiguos
    PRESERVE_ALL = "preserve_all"  # Reconstruir todas las débiles posibles


class ContractionMode(Enum):
    """Modo de manejo de contracciones."""
    PRESERVE_WEAK = "preserve"       # Reconstruir débil aunque contraída
    APPLY_CONTRACTION = "contract"   # Asumir contracción en spellings defectivos
    CONTEXT_DEPENDENT = "context"    # Decidir por contexto morfológico


# ============================================================================
# CLASES DE VERBOS DÉBILES
# ============================================================================

class WeakVerbClass(Enum):
    """
    Clasificación de verbos según consonantes débiles en la raíz.
    
    Nomenclatura: I/II/III indica posición de la débil en raíz triconsonántica.
    """
    # Verbos con ʾ
    I_ALEPH = "I_aleph"        # ʾ como R1 (ej: ʾakālum "comer")
    II_ALEPH = "II_aleph"      # ʾ como R2 (ej: šaʾālum "preguntar")
    III_ALEPH = "III_aleph"    # ʾ como R3 (ej: qabāʾum "hablar")
    
    # Verbos con w
    I_W = "I_w"               # w como R1 (ej: wabālum "llevar")
    II_W = "II_w"             # w como R2 (ej: lawāʾum "envolver")
    III_W = "III_w"           # w como R3 (raro, mayormente → III_ū)
    
    # Verbos con y
    I_Y = "I_y"               # y como R1 (perdido en OA, → I_∅)
    II_Y = "II_y"             # y como R2 (ej: qiāpum < *qiyāp-)
    III_Y = "III_y"           # y como R3 (ej: banāyum "construir")
    
    # Verbos con vocales largas (de débiles)
    II_U_LONG = "II_ū"        # ū como R2 (ej: tuārum "regresar")
    III_U_LONG = "III_ū"      # ū como R3 (ej: zakāʾum "estar listo")
    II_I_LONG = "II_ī"        # ī como R2 (ej: diānum "juzgar")
    III_I_LONG = "III_ī"      # ī como R3 (ej: banāyum → bani)
    
    # Verbos fuertes (para comparación)
    STRONG = "strong"         # Sin consonantes débiles


# ============================================================================
# TIPOS DE CAMBIO HISTÓRICO
# ============================================================================

class HistoricalChange(Enum):
    """Tipos de cambios históricos que afectan débiles."""
    # Cambios de diptongos
    AY_TO_E_LONG = "ay>ē"     # *ay → ē (completado)
    AW_TO_U_LONG = "aw>ū"     # *aw → ū (completado)
    IY_TO_I_LONG = "iy>ī"     # *iy → ī (completado)
    IW_TO_I_LONG = "iw>ī"     # *iw → ī (completado)
    UY_TO_U_LONG = "uy>ū"     # *uy → ū (hipotético)
    UW_TO_U_LONG = "uw>ū"     # uw → ū (completado)
    
    # Cambios de consonantes débiles
    Y_INITIAL_LOSS = "y>#∅"   # *y- → ∅ (completado)
    W_INITIAL_LOSS = "w>u"    # wa- → u- (en progreso)
    ALEPH_COMPENSATORY = "ʾ>V̄"  # ʾ_C → V̄C
    
    # Fusiones
    ALEPH_AYIN_MERGER = "ʿ>ʾ"  # *ʿ → ʾ (completado)
    ALEPH_DENTAL_FUSION = "ʾ+t>ṭ"  # ʾ + dental → glotálica
    
    # Asimilaciones/contracciones
    W_TO_M = "w>m"            # w → m (esporádico, influencia babilónica)
    Y_CONTRACTION = "yi>ī"    # -Cyi- → -Cī-


# ============================================================================
# SPELLINGS ESPECIALES
# ============================================================================

class SpecialSpelling(Enum):
    """Tipos especiales de spelling para débiles."""
    BROKEN = "broken"              # V-V (puede ser ʾ, w, y, o simple hiato)
    GLIDE = "glide"               # Ci/Cu para y/w post-consonántico
    PLENE = "plene"               # Vocal repetida (ú-ú para ū)
    DEFECTIVE = "defective"       # Sin indicación de débil/vocal larga
    SANDHI = "sandhi"             # Fusión de palabras
    FUSION = "fusion"             # TA/DU/DÍ para dental+ʾ


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def is_weak_position_for(consonant_symbol: str, position: WeakPosition) -> bool:
    """
    Determina si una posición es relevante para una consonante débil específica.
    
    Args:
        consonant_symbol: 'ʾ', 'w', o 'y'
        position: WeakPosition a verificar
    
    Returns:
        True si la posición es relevante para esa consonante
    """
    # Todas las débiles pueden aparecer en estas posiciones
    universal_positions = {
        WeakPosition.WORD_INITIAL,
        WeakPosition.INTERVOCALIC,
        WeakPosition.POST_CONSONANTAL,
    }
    
    if position in universal_positions:
        return True
    
    # Posiciones específicas
    if consonant_symbol == 'ʾ':
        return position in {
            WeakPosition.SYLLABLE_FINAL,
            WeakPosition.WORD_FINAL,
            WeakPosition.INTERVOCALIC_IDENTICAL,
            WeakPosition.PROCLITIC_BOUNDARY,
        }
    elif consonant_symbol == 'w':
        return position in {
            WeakPosition.AFTER_U_BEFORE_VOWEL,
            WeakPosition.BEFORE_HOMORGANIC_VOWEL,
        }
    elif consonant_symbol == 'y':
        return position in {
            WeakPosition.AFTER_I_BEFORE_VOWEL,
            WeakPosition.BEFORE_HOMORGANIC_VOWEL,
        }
    
    return False


def get_expected_preservation(
    consonant_symbol: str,
    position: WeakPosition
) -> PreservationStatus:
    """
    Retorna el estado de preservación esperado para una débil en una posición.
    
    Args:
        consonant_symbol: 'ʾ', 'w', o 'y'
        position: Posición de la débil
    
    Returns:
        Estado de preservación esperado
    """
    # ʾ
    if consonant_symbol == 'ʾ':
        if position == WeakPosition.INTERVOCALIC_IDENTICAL:
            return PreservationStatus.ALWAYS_PRESERVED
        elif position == WeakPosition.SYLLABLE_FINAL:
            return PreservationStatus.COMPENSATORY_LENGTHENING
        elif position == WeakPosition.POST_CONSONANTAL:
            return PreservationStatus.VARIABLY_PRESERVED
        else:
            return PreservationStatus.CONTEXT_DEPENDENT
    
    # w
    elif consonant_symbol == 'w':
        if position == WeakPosition.WORD_INITIAL:
            return PreservationStatus.VARIABLY_PRESERVED  # wa- → u- en progreso
        elif position == WeakPosition.BEFORE_HOMORGANIC_VOWEL:
            return PreservationStatus.CONTRACTED  # -Cwu- → -Cū-
        else:
            return PreservationStatus.CONTEXT_DEPENDENT
    
    # y
    elif consonant_symbol == 'y':
        if position == WeakPosition.WORD_INITIAL:
            return PreservationStatus.ALWAYS_LOST  # Completado en OA
        elif position == WeakPosition.BEFORE_HOMORGANIC_VOWEL:
            return PreservationStatus.CONTRACTED  # -Cyi- → -Cī-
        else:
            return PreservationStatus.CONTEXT_DEPENDENT
    
    return PreservationStatus.CONTEXT_DEPENDENT

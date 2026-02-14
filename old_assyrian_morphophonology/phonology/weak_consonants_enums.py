"""
Enumeraciones específicas para consonantes débiles del Old Assyrian.

Basado en Kouwenberg (2017) § 3.3.
"""

from enum import Enum, auto


# ============================================================================
# POSICIONES DE CONSONANTES DÉBILES
# ============================================================================

class WeakPosition(Enum):
    """
    Posiciones donde pueden aparecer consonantes débiles.
    
    Cada posición tiene reglas diferentes de preservación/elisión.
    """
    # Posiciones generales
    WORD_INITIAL = "word_initial"                      # #_V (ej: ʾālum)
    INTERVOCALIC = "intervocalic"                      # V_V (general)
    INTERVOCALIC_IDENTICAL = "intervocalic_identical"  # V[same]_V[same] (ej: šaʾālum)
    INTERVOCALIC_DIFFERENT = "intervocalic_different"  # V₁_V₂ (ej: beʾālum)
    POST_CONSONANTAL = "post_consonantal"              # C_ (ej: nadʾāku)
    SYLLABLE_FINAL = "syllable_final"                  # _C (ej: raʾšum → rēšum)
    WORD_FINAL = "word_final"                          # _# (ej: kalāʾum)
    
    # Posiciones específicas para w
    AFTER_U_BEFORE_VOWEL = "after_u"                   # u_V (ej: itūwar)
    AFTER_U_BEFORE_U = "after_u_before_u"              # u_u (ej: zakwū → zakû)
    
    # Posiciones específicas para y
    AFTER_I_BEFORE_VOWEL = "after_i"                   # i_V (ej: panium)
    AFTER_I_BEFORE_I = "after_i_before_i"              # i_i (ej: niqyī → niqī)
    AFTER_E_BEFORE_E = "after_e_before_e"              # e_e (similar)
    
    # Posiciones específicas para ʾ
    BEFORE_HOMORGANIC_VOWEL = "before_homorganic"      # General (y_i/e, w_u)
    AFTER_GLOTTALIC = "after_glottalic"                # ṭ/ṣ/q + ʾ


# ============================================================================
# ESTADOS DE PRESERVACIÓN
# ============================================================================

class WeakPreservation(Enum):
    """Estado de preservación de una consonante débil."""
    ALWAYS_PRESERVED = "always_preserved"              # ʾ intervocálico
    ALWAYS_LOST = "always_lost"                        # y inicial
    VARIABLY_PRESERVED = "variable"                    # ʾ post-consonántico
    CONTEXT_DEPENDENT = "context_dependent"            # w intervocálico
    COMPENSATORY_LENGTHENING = "compensatory"          # ʾ final sílaba → V̄
    CONTRACTED = "contracted"                          # -Cyi- → -Cī-
    FUSED = "fused"                                    # dental + ʾ → ṭ


# ============================================================================
# TIPOS DE EVIDENCIA PARA RECONSTRUCCIÓN
# ============================================================================

class EvidenceType(Enum):
    """Tipo de evidencia para reconstruir una consonante débil."""
    MORPHOLOGICAL = "morphological"        # Basado en clase verbal/nominal
    ETYMOLOGICAL = "etymological"          # Basado en raíz conocida
    CONTEXTUAL = "contextual"              # Basado en contexto fonológico
    ORTHOGRAPHIC = "orthographic"          # Basado en spelling específico
    PARADIGMATIC = "paradigmatic"          # Basado en otras formas del paradigma
    COMPARATIVE = "comparative"            # Basado en dialectos relacionados


# ============================================================================
# MODO DE RECONSTRUCCIÓN
# ============================================================================

class ReconstructMode(Enum):
    """Modo de reconstrucción de consonantes débiles."""
    NONE = "none"                  # No reconstruir, solo parsear visible
    AUTO = "auto"                  # Usar tabla de decisión automática
    FORCE_ALEPH = "force_aleph"    # Forzar ʾ en casos ambiguos
    FORCE_WAW = "force_waw"        # Forzar w en casos ambiguos
    FORCE_YOD = "force_yod"        # Forzar y en casos ambiguos
    ALL_WEAK = "all_weak"          # Reconstruir todos los débiles posibles


# ============================================================================
# MODO DE CONTRACCIÓN
# ============================================================================

class ContractionMode(Enum):
    """Modo de aplicación de contracciones."""
    PRESERVE_WEAK = "preserve"     # Reconstruir débil aunque spelling sea defectivo
    APPLY_CONTRACTION = "contract" # Asumir contracción cuando defectivo
    CONTEXT_DEPENDENT = "context"  # Decidir por contexto (imperativos → contraído)


# ============================================================================
# CLASES DE VERBOS DÉBILES
# ============================================================================

class WeakVerbClass(Enum):
    """
    Clases de verbos débiles según posición de la consonante débil.
    
    Nomenclatura estándar: I/II/III indica posición del radical débil.
    """
    # Verbos I-weak (R1 débil)
    I_ALEPH = "I/ʾ"                # ʾakālum "comer"
    I_WAW = "I/w"                  # wabālum "llevar"
    I_YOD = "I/y"                  # (raro en OA, ya → i)
    
    # Verbos II-weak (R2 débil)
    II_ALEPH = "II/ʾ"              # šaʾālum "preguntar"
    II_WAW = "II/w"                # lawāʾum "envolver"
    II_YOD = "II/i"                # (II/voc, originalmente *y)
    II_U = "II/ū"                  # tuārum "regresar"
    
    # Verbos III-weak (R3 débil)
    III_ALEPH = "III/ʾ"            # kalāʾum "sostener"
    III_WAW = "III/w"              # (raro, mayoría → III/ū)
    III_YOD = "III/i"              # banāyum "construir"
    III_U = "III/ū"                # zakāʾum "estar listo"
    
    # Verbos doblemente débiles
    I_WAW_III_YOD = "I/w-III/i"    # wasāyum?
    
    # Verbos no débiles (para comparación)
    STRONG = "strong"               # paršum "separar"


# ============================================================================
# TIPOS DE CAMBIO FONOLÓGICO
# ============================================================================

class PhonologicalChange(Enum):
    """Tipos de cambios fonológicos que afectan a consonantes débiles."""
    ELISION = "elision"                      # Pérdida sin compensación
    COMPENSATORY_LENGTHENING = "comp_length" # Pérdida con alargamiento
    CONTRACTION = "contraction"              # Fusión de segmentos
    ASSIMILATION = "assimilation"            # Asimilación a adyacente
    FUSION = "fusion"                        # Fusión completa (ʾ + dental → ṭ)
    GLIDE_INSERTION = "glide_insertion"      # Inserción predecible
    VOWEL_INSERTION = "vowel_insertion"      # Epéntesis vocálica


# ============================================================================
# ESTADOS DE DESARROLLO HISTÓRICO
# ============================================================================

class HistoricalStage(Enum):
    """Etapas de desarrollo de consonantes débiles."""
    PROTO_SEMITIC = "proto_semitic"          # Estado original PS
    PROTO_AKKADIAN = "proto_akkadian"        # Acadio temprano
    OLD_ASSYRIAN = "old_assyrian"            # OA (variación sincrónica)
    MIDDLE_ASSYRIAN = "middle_assyrian"      # MA (cambios completados)
    
    # Estados específicos de OA
    OA_CONSERVATIVE = "oa_conservative"      # Formas tradicionales
    OA_INNOVATIVE = "oa_innovative"          # Formas innovadoras


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def is_intervocalic_position(pos: WeakPosition) -> bool:
    """Determina si una posición es intervocálica."""
    return pos in {
        WeakPosition.INTERVOCALIC,
        WeakPosition.INTERVOCALIC_IDENTICAL,
        WeakPosition.INTERVOCALIC_DIFFERENT,
        WeakPosition.AFTER_U_BEFORE_VOWEL,
        WeakPosition.AFTER_I_BEFORE_VOWEL,
    }


def is_post_consonantal_position(pos: WeakPosition) -> bool:
    """Determina si una posición es post-consonántica."""
    return pos == WeakPosition.POST_CONSONANTAL


def requires_reconstruction(pos: WeakPosition, weak_type: str) -> bool:
    """
    Determina si una posición típicamente requiere reconstrucción.
    
    Args:
        pos: Posición de la débil
        weak_type: 'ʾ', 'w', o 'y'
    
    Returns:
        True si suele requerir reconstrucción (no escrita)
    """
    if weak_type == 'ʾ':
        # ʾ raramente escrito
        return True
    elif weak_type == 'w':
        # w a veces omitido después de u
        return pos == WeakPosition.AFTER_U_BEFORE_VOWEL
    elif weak_type == 'y':
        # y raramente escrito intervocálico
        return is_intervocalic_position(pos)
    
    return False

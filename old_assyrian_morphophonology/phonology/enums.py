"""
Enumeraciones para el sistema fonológico del Old Assyrian.

Este módulo define todos los tipos enumerados usados en la representación
fonológica del Old Assyrian, basado en Kouwenberg (2017).
"""

from enum import Enum, auto


# ============================================================================
# ENUMS PARA CONSONANTES
# ============================================================================

class PlaceOfArticulation(Enum):
    """Lugar de articulación de consonantes."""
    BILABIAL = "bilabial"
    DENTAL = "dental"
    ALVEOLAR = "alveolar"
    VELAR = "velar"
    LATERAL = "lateral"
    PALATAL = "palatal"
    LARYNGEAL = "laryngeal"


class MannerOfArticulation(Enum):
    """Modo de articulación de consonantes."""
    STOP = "stop"              # Oclusivas: p, b, t, d, k, g, ṭ, q, ʾ
    AFFRICATE = "affricate"    # Africadas: s, z, ṣ
    FRICATIVE = "fricative"    # Fricativas: š, ḫ
    NASAL = "nasal"            # Nasales: m, n
    APPROXIMANT = "approximant" # Aproximantes: w, r, l, y


class Voicing(Enum):
    """Sonoridad de consonantes."""
    VOICELESS = "voiceless"    # Sordas: p, t, k, s, š, ṣ, ṭ, q
    VOICED = "voiced"          # Sonoras: b, d, g, z, m, n, r, l, w, y
    GLOTTALIC = "glottalic"    # Glotálicas: ṭ, ṣ, q
    GLOTTAL = "glottal"        # Glotal: ʾ


# ============================================================================
# ENUMS PARA VOCALES
# ============================================================================

class VowelQuality(Enum):
    """Cualidad vocálica (timbre)."""
    A = "a"  # Baja central
    E = "e"  # Media frontal (secundaria)
    I = "i"  # Alta frontal
    U = "u"  # Alta posterior


class VowelLength(Enum):
    """Cantidad vocálica."""
    SHORT = "short"    # Vocales cortas: a, e, i, u
    LONG = "long"      # Vocales largas: ā, ē, ī, ū


class VowelHeight(Enum):
    """Altura vocálica."""
    HIGH = "high"      # i, u
    MID = "mid"        # e
    LOW = "low"        # a


class VowelBackness(Enum):
    """Posición anterior-posterior de vocales."""
    FRONT = "front"    # i, e
    CENTRAL = "central" # a
    BACK = "back"      # u


# ============================================================================
# ENUMS PARA ACENTUACIÓN (ORACC)
# ============================================================================

class AccentType(Enum):
    """
    Tipos de acento/diacríticos en ORACC.
    
    Nota: Kouwenberg no marca acento en su transcripción.
    Estos son específicos del estándar ORACC.
    """
    NONE = "none"              # Sin acento
    ACUTE = "acute"            # Acento agudo: á, é, í, ú (estrés)
    GRAVE = "grave"            # Acento grave: à, è, ì, ù (función unclear en OA)
    CIRCUMFLEX = "circumflex"  # Acento circunflejo: â, ê, î, û (contracción)


# ============================================================================
# ENUMS PARA METADATA TEXTUAL (ORACC)
# ============================================================================

class TextStatus(Enum):
    """
    Estado de preservación del texto en tablillas.
    
    Usado en ORACC para indicar condición del material cuneiforme.
    """
    CLEAR = "clear"            # Texto claro y legible
    DAMAGED = "damaged"        # Texto dañado pero legible (⸢ ⸣)
    RESTORED = "restored"      # Texto restaurado por editor (⸤ ⸥)
    BROKEN = "broken"          # Completamente ilegible (u)
    UNCERTAIN = "uncertain"    # Lectura incierta (X)


# ============================================================================
# ENUMS PARA CLASIFICACIÓN DE CONSONANTES
# ============================================================================

class ConsonantClass(Enum):
    """
    Clases naturales de consonantes para reglas fonológicas.
    """
    WEAK = "weak"              # Consonantes débiles: ʾ, w, y
    SIBILANT = "sibilant"      # Sibilantes: s, z, š, ṣ
    EMPHATIC = "emphatic"      # Enfáticas/glotálicas: ṭ, ṣ, q
    GUTTURAL = "guttural"      # Guturales: ḫ, ʾ
    SONORANT = "sonorant"      # Sonorantes: m, n, l, r, w, y
    NASAL = "nasal"            # Nasales: m, n
    LIQUID = "liquid"          # Líquidas: l, r


# ============================================================================
# ENUMS PARA ORIGEN HISTÓRICO
# ============================================================================

class HistoricalOrigin(Enum):
    """
    Origen histórico de fonemas (especialmente para e/ē).
    """
    PROTO_SEMITIC = "proto_semitic"        # Heredado de PS
    FROM_GUTTURAL = "from_guttural"        # e < a/i por gutural
    FROM_DIPHTHONG = "from_diphthong"      # ē < *ay, ū < *aw
    FROM_CONTRACTION = "from_contraction"  # Vocales contraídas
    LOANWORD = "loanword"                  # Préstamo (ej: sumerio)
    UNKNOWN = "unknown"                    # Origen desconocido


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_vowel_height(quality: VowelQuality) -> VowelHeight:
    """Devuelve la altura de una vocal según su cualidad."""
    mapping = {
        VowelQuality.I: VowelHeight.HIGH,
        VowelQuality.U: VowelHeight.HIGH,
        VowelQuality.E: VowelHeight.MID,
        VowelQuality.A: VowelHeight.LOW,
    }
    return mapping[quality]


def get_vowel_backness(quality: VowelQuality) -> VowelBackness:
    """Devuelve la posición anterior-posterior de una vocal."""
    mapping = {
        VowelQuality.I: VowelBackness.FRONT,
        VowelQuality.E: VowelBackness.FRONT,
        VowelQuality.A: VowelBackness.CENTRAL,
        VowelQuality.U: VowelBackness.BACK,
    }
    return mapping[quality]

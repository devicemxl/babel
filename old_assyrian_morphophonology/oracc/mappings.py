"""
Mapeo completo de caracteres ORACC a fonemas del Old Assyrian.

Este módulo define la conversión bidireccional entre:
- Caracteres Unicode usados en ORACC
- Objetos Phoneme (Consonant/Vowel) del sistema interno
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phonology import (
    get_consonant,
    get_vowel,
    Vowel,
    VowelFeatures,
    VowelQuality,
    VowelLength,
    AccentType,
)


# ============================================================================
# MAPEO ORACC → FONEMAS
# ============================================================================

def create_accented_vowel(quality: VowelQuality, length: VowelLength, 
                         accent: AccentType) -> Vowel:
    """Helper para crear vocales con acento específico."""
    features = VowelFeatures(quality=quality, length=length)
    is_stressed = (accent == AccentType.ACUTE)
    return Vowel(features=features, accent=accent, is_stressed=is_stressed)


# Mapeo de caracteres ORACC individuales a fonemas
ORACC_TO_PHONEME_MAP = {
    # ========================================================================
    # CONSONANTES
    # ========================================================================
    
    # Labiales
    'p': get_consonant('p'),
    'b': get_consonant('b'),
    'm': get_consonant('m'),
    'w': get_consonant('w'),
    
    # Dentales
    't': get_consonant('t'),
    'd': get_consonant('d'),
    'ṭ': get_consonant('ṭ'),  # U+1E6D
    'n': get_consonant('n'),
    'r': get_consonant('r'),
    
    # Alveolares (sibilantes)
    's': get_consonant('s'),
    'z': get_consonant('z'),
    'ṣ': get_consonant('ṣ'),  # U+1E63
    'š': get_consonant('š'),  # U+0161
    
    # Velares
    'k': get_consonant('k'),
    'g': get_consonant('g'),
    'q': get_consonant('q'),
    'ḫ': get_consonant('ḫ'),  # U+1E2B
    
    # Lateral
    'l': get_consonant('l'),
    
    # Palatal
    'y': get_consonant('y'),
    
    # Laringeal
    'ʾ': get_consonant('ʾ'),  # U+02BE (glottal stop)
    
    # ========================================================================
    # VOCALES CORTAS SIN ACENTO
    # ========================================================================
    
    'a': get_vowel('a'),
    'e': get_vowel('e'),
    'i': get_vowel('i'),
    'u': get_vowel('u'),
    
    # ========================================================================
    # VOCALES LARGAS (MACRON)
    # ========================================================================
    
    'ā': get_vowel('ā'),  # U+0101
    'ē': get_vowel('ē'),  # U+0113
    'ī': get_vowel('ī'),  # U+012B
    'ū': get_vowel('ū'),  # U+016B
    
    # ========================================================================
    # VOCALES CON ACENTO AGUDO (marca estrés en ORACC)
    # ========================================================================
    
    # Cortas con agudo
    'á': create_accented_vowel(VowelQuality.A, VowelLength.SHORT, AccentType.ACUTE),  # U+00E1
    'é': create_accented_vowel(VowelQuality.E, VowelLength.SHORT, AccentType.ACUTE),  # U+00E9
    'í': create_accented_vowel(VowelQuality.I, VowelLength.SHORT, AccentType.ACUTE),  # U+00ED
    'ú': create_accented_vowel(VowelQuality.U, VowelLength.SHORT, AccentType.ACUTE),  # U+00FA
    
    # Largas con agudo (menos común, pero posible en ORACC)
    # ORACC a veces marca acento incluso en vocales ya largas
    
    # ========================================================================
    # VOCALES CON ACENTO GRAVE (función unclear en OA)
    # ========================================================================
    
    'à': create_accented_vowel(VowelQuality.A, VowelLength.SHORT, AccentType.GRAVE),  # U+00E0
    'è': create_accented_vowel(VowelQuality.E, VowelLength.SHORT, AccentType.GRAVE),  # U+00E8
    'ì': create_accented_vowel(VowelQuality.I, VowelLength.SHORT, AccentType.GRAVE),  # U+00EC
    'ù': create_accented_vowel(VowelQuality.U, VowelLength.SHORT, AccentType.GRAVE),  # U+00F9
    
    # ========================================================================
    # VOCALES CON CIRCUMFLEX (indica contracción)
    # ========================================================================
    
    'â': create_accented_vowel(VowelQuality.A, VowelLength.LONG, AccentType.CIRCUMFLEX),  # U+00E2
    'ê': create_accented_vowel(VowelQuality.E, VowelLength.LONG, AccentType.CIRCUMFLEX),  # U+00EA
    'î': create_accented_vowel(VowelQuality.I, VowelLength.LONG, AccentType.CIRCUMFLEX),  # U+00EE
    'û': create_accented_vowel(VowelQuality.U, VowelLength.LONG, AccentType.CIRCUMFLEX),  # U+00FB
}


# Mayúsculas (usadas en logograms o énfasis)
ORACC_UPPERCASE_MAP = {
    'A': get_vowel('a'),
    'E': get_vowel('e'),
    'I': get_vowel('i'),
    'U': get_vowel('u'),
    'B': get_consonant('b'),
    'D': get_consonant('d'),
    'G': get_consonant('g'),
    'K': get_consonant('k'),
    'L': get_consonant('l'),
    'M': get_consonant('m'),
    'N': get_consonant('n'),
    'P': get_consonant('p'),
    'Q': get_consonant('q'),
    'R': get_consonant('r'),
    'S': get_consonant('s'),
    'T': get_consonant('t'),
    'W': get_consonant('w'),
    'Y': get_consonant('y'),
    'Z': get_consonant('z'),
    'Š': get_consonant('š'),  # U+0160
    'Ṣ': get_consonant('ṣ'),  # U+1E62
    'Ṭ': get_consonant('ṭ'),  # U+1E6C
    'Ḫ': get_consonant('ḫ'),  # U+1E2A
}

# Combinar mapeos
ORACC_TO_PHONEME_MAP.update(ORACC_UPPERCASE_MAP)


# ============================================================================
# MAPEO INVERSO: FONEMA → ORACC
# ============================================================================

def phoneme_to_oracc(phoneme) -> str:
    """
    Convierte un fonema a su representación ORACC.
    
    Usa el método to_oracc() del fonema, que maneja diacríticos.
    """
    return phoneme.to_oracc()


# ============================================================================
# CARACTERES ESPECIALES ORACC
# ============================================================================

# Subíndices numéricos (para homofonía de signos cuneiformes)
ORACC_SUBSCRIPTS = {
    '₀': 0,  # U+2080
    '₁': 1,  # U+2081
    '₂': 2,  # U+2082
    '₃': 3,  # U+2083
    '₄': 4,  # U+2084
    '₅': 5,  # U+2085
    '₆': 6,  # U+2086
    '₇': 7,  # U+2087
    '₈': 8,  # U+2088
    '₉': 9,  # U+2089
    'ₓ': 'x',  # U+2093 (valor desconocido)
}

# Inverso: número → subíndice
SUBSCRIPT_TO_NUMBER = {v: k for k, v in ORACC_SUBSCRIPTS.items()}

# Marcadores de preservación textual
ORACC_TEXT_MARKERS = {
    '⸢': 'damaged_open',     # U+2E22 (texto dañado pero legible)
    '⸣': 'damaged_close',    # U+2E23
    '⸤': 'restored_open',    # U+2E24 (texto restaurado)
    '⸥': 'restored_close',   # U+2E25
}

# Marcadores de palabra rota/incierta
ORACC_SPECIAL_WORDS = {
    'u': 'broken',      # Palabra completamente ilegible
    'X': 'uncertain',   # Lectura incierta
}

# Separadores
ORACC_SEPARATORS = {
    '-': 'syllable_divider',  # Entre sílabas
    '.': 'morpheme_boundary', # Frontera morfológica
    ' ': 'word_divider',      # Entre palabras
}


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def is_oracc_subscript(char: str) -> bool:
    """Determina si un carácter es un subíndice numérico ORACC."""
    return char in ORACC_SUBSCRIPTS


def is_oracc_text_marker(char: str) -> bool:
    """Determina si un carácter es un marcador de preservación textual."""
    return char in ORACC_TEXT_MARKERS


def is_oracc_separator(char: str) -> bool:
    """Determina si un carácter es un separador ORACC."""
    return char in ORACC_SEPARATORS


def get_phoneme_from_oracc(char: str):
    """
    Obtiene el fonema correspondiente a un carácter ORACC.
    
    Raises:
        KeyError: Si el carácter no está en el mapeo
    """
    if char not in ORACC_TO_PHONEME_MAP:
        raise KeyError(f"Carácter ORACC desconocido: '{char}' (U+{ord(char):04X})")
    return ORACC_TO_PHONEME_MAP[char]

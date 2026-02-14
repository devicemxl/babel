"""
Inventarios completos de consonantes y vocales del Old Assyrian.

Basado en Kouwenberg (2017):
- § 3.2.1: Inventario consonántico (20 consonantes)
- § 3.4.1: Inventario vocálico (4 cualidades × 2 cantidades)
"""

from .phoneme import Consonant, Vowel
from .features import ConsonantFeatures, VowelFeatures
from .enums import (
    PlaceOfArticulation as Place,
    MannerOfArticulation as Manner,
    Voicing,
    VowelQuality,
    VowelLength,
    HistoricalOrigin
)


# ============================================================================
# INVENTARIO CONSONÁNTICO (20 fonemas)
# ============================================================================

# --- LABIALES ---

CONSONANT_P = Consonant(
    _symbol='p',
    features=ConsonantFeatures(
        place=Place.BILABIAL,
        manner=Manner.STOP,
        voicing=Voicing.VOICELESS,
    ),
    ipa='/p/'
)

CONSONANT_B = Consonant(
    _symbol='b',
    features=ConsonantFeatures(
        place=Place.BILABIAL,
        manner=Manner.STOP,
        voicing=Voicing.VOICED,
        is_sonorant=False,
    ),
    ipa='/b/'
)

CONSONANT_M = Consonant(
    _symbol='m',
    features=ConsonantFeatures(
        place=Place.BILABIAL,
        manner=Manner.NASAL,
        voicing=Voicing.VOICED,
        is_sonorant=True,
        is_nasal=True,
    ),
    ipa='/m/'
)

CONSONANT_W = Consonant(
    _symbol='w',
    features=ConsonantFeatures(
        place=Place.BILABIAL,
        manner=Manner.APPROXIMANT,
        voicing=Voicing.VOICED,
        is_weak=True,
        is_sonorant=True,
    ),
    ipa='/w/',
    historical_note="Consonante débil; tiende a perderse o convertirse en glide"
)

# --- DENTALES ---

CONSONANT_T = Consonant(
    _symbol='t',
    features=ConsonantFeatures(
        place=Place.DENTAL,
        manner=Manner.STOP,
        voicing=Voicing.VOICELESS,
    ),
    ipa='/t/'
)

CONSONANT_D = Consonant(
    _symbol='d',
    features=ConsonantFeatures(
        place=Place.DENTAL,
        manner=Manner.STOP,
        voicing=Voicing.VOICED,
    ),
    ipa='/d/'
)

CONSONANT_TETH = Consonant(
    _symbol='ṭ',
    features=ConsonantFeatures(
        place=Place.DENTAL,
        manner=Manner.STOP,
        voicing=Voicing.GLOTTALIC,
        is_emphatic=True,
    ),
    unicode_codepoint='U+1E6D',
    ipa="/t'/",
    historical_note="Post-glottalizada; cluster dental+ʾ puede realizarse como ṭ"
)

CONSONANT_N = Consonant(
    _symbol='n',
    features=ConsonantFeatures(
        place=Place.DENTAL,
        manner=Manner.NASAL,
        voicing=Voicing.VOICED,
        is_sonorant=True,
        is_nasal=True,
    ),
    ipa='/n/'
)

CONSONANT_R = Consonant(
    _symbol='r',
    features=ConsonantFeatures(
        place=Place.DENTAL,
        manner=Manner.APPROXIMANT,
        voicing=Voicing.VOICED,
        is_sonorant=True,
        is_liquid=True,
    ),
    ipa='/r/',
    historical_note="Vibrante; condiciona i→e en contextos específicos"
)

# --- ALVEOLARES (Africadas/Sibilantes) ---

CONSONANT_S = Consonant(
    _symbol='s',
    features=ConsonantFeatures(
        place=Place.ALVEOLAR,
        manner=Manner.AFFRICATE,
        voicing=Voicing.VOICELESS,
        is_sibilant=True,
    ),
    ipa='/ᵗs/',
    historical_note="Africada sorda; en proceso de des-africación"
)

CONSONANT_Z = Consonant(
    _symbol='z',
    features=ConsonantFeatures(
        place=Place.ALVEOLAR,
        manner=Manner.AFFRICATE,
        voicing=Voicing.VOICED,
        is_sibilant=True,
    ),
    ipa='/ᵈz/',
    historical_note="Africada sonora; en proceso de des-africación"
)

CONSONANT_SADHE = Consonant(
    _symbol='ṣ',
    features=ConsonantFeatures(
        place=Place.ALVEOLAR,
        manner=Manner.AFFRICATE,
        voicing=Voicing.GLOTTALIC,
        is_sibilant=True,
        is_emphatic=True,
    ),
    unicode_codepoint='U+1E63',
    ipa="/ᵗs'/",
    historical_note="Africada post-glottalizada; cluster ṣ+ʾ puede fusionarse"
)

CONSONANT_SHIN = Consonant(
    _symbol='š',
    features=ConsonantFeatures(
        place=Place.ALVEOLAR,
        manner=Manner.FRICATIVE,
        voicing=Voicing.VOICELESS,
        is_sibilant=True,
    ),
    unicode_codepoint='U+0161',
    ipa='/s/',
    historical_note="Fusión de PS *ŝ, *ś y *θ; probablemente fricativa /s/"
)

# --- VELARES ---

CONSONANT_K = Consonant(
    _symbol='k',
    features=ConsonantFeatures(
        place=Place.VELAR,
        manner=Manner.STOP,
        voicing=Voicing.VOICELESS,
    ),
    ipa='/k/'
)

CONSONANT_G = Consonant(
    _symbol='g',
    features=ConsonantFeatures(
        place=Place.VELAR,
        manner=Manner.STOP,
        voicing=Voicing.VOICED,
    ),
    ipa='/g/'
)

CONSONANT_QOPH = Consonant(
    _symbol='q',
    features=ConsonantFeatures(
        place=Place.VELAR,
        manner=Manner.STOP,
        voicing=Voicing.GLOTTALIC,
        is_emphatic=True,
    ),
    ipa="/k'/",
    historical_note="Post-glottalizada velar"
)

CONSONANT_HET = Consonant(
    _symbol='ḫ',
    features=ConsonantFeatures(
        place=Place.VELAR,
        manner=Manner.FRICATIVE,
        voicing=Voicing.VOICELESS,
        is_guttural=True,
    ),
    unicode_codepoint='U+1E2B',
    ipa='/x/',
    historical_note="Fricativa velar, NO uvular; mismo lugar que k"
)

# --- LATERAL ---

CONSONANT_L = Consonant(
    _symbol='l',
    features=ConsonantFeatures(
        place=Place.LATERAL,
        manner=Manner.APPROXIMANT,
        voicing=Voicing.VOICED,
        is_sonorant=True,
        is_liquid=True,
    ),
    ipa='/l/'
)

# --- PALATAL ---

CONSONANT_Y = Consonant(
    _symbol='y',
    features=ConsonantFeatures(
        place=Place.PALATAL,
        manner=Manner.APPROXIMANT,
        voicing=Voicing.VOICED,
        is_weak=True,
        is_sonorant=True,
    ),
    ipa='/j/',
    historical_note="Consonante débil; glide palatal"
)

# --- LARINGEAL ---

CONSONANT_ALEPH = Consonant(
    _symbol='ʾ',
    features=ConsonantFeatures(
        place=Place.LARYNGEAL,
        manner=Manner.STOP,
        voicing=Voicing.GLOTTAL,
        is_weak=True,
        is_guttural=True,
    ),
    unicode_codepoint='U+02BE',
    ipa='/ʔ/',
    historical_note="Glottal stop; consonante débil, a menudo no escrita"
)


# Diccionario organizado por lugar de articulación
CONSONANT_INVENTORY = {
    'labials': {
        'p': CONSONANT_P,
        'b': CONSONANT_B,
        'm': CONSONANT_M,
        'w': CONSONANT_W,
    },
    'dentals': {
        't': CONSONANT_T,
        'd': CONSONANT_D,
        'ṭ': CONSONANT_TETH,
        'n': CONSONANT_N,
        'r': CONSONANT_R,
    },
    'alveolars': {
        's': CONSONANT_S,
        'z': CONSONANT_Z,
        'ṣ': CONSONANT_SADHE,
        'š': CONSONANT_SHIN,
    },
    'velars': {
        'k': CONSONANT_K,
        'g': CONSONANT_G,
        'q': CONSONANT_QOPH,
        'ḫ': CONSONANT_HET,
    },
    'laterals': {
        'l': CONSONANT_L,
    },
    'palatals': {
        'y': CONSONANT_Y,
    },
    'laryngeals': {
        'ʾ': CONSONANT_ALEPH,
    },
}

# Diccionario plano para acceso rápido
CONSONANTS_BY_SYMBOL = {
    'p': CONSONANT_P, 'b': CONSONANT_B, 'm': CONSONANT_M, 'w': CONSONANT_W,
    't': CONSONANT_T, 'd': CONSONANT_D, 'ṭ': CONSONANT_TETH, 'n': CONSONANT_N, 'r': CONSONANT_R,
    's': CONSONANT_S, 'z': CONSONANT_Z, 'ṣ': CONSONANT_SADHE, 'š': CONSONANT_SHIN,
    'k': CONSONANT_K, 'g': CONSONANT_G, 'q': CONSONANT_QOPH, 'ḫ': CONSONANT_HET,
    'l': CONSONANT_L,
    'y': CONSONANT_Y,
    'ʾ': CONSONANT_ALEPH,
}


# ============================================================================
# INVENTARIO VOCÁLICO (4 cualidades × 2 cantidades = 8 fonemas)
# ============================================================================

# --- VOCALES CORTAS ---

VOWEL_A_SHORT = Vowel(
    features=VowelFeatures(
        quality=VowelQuality.A,
        length=VowelLength.SHORT,
    ),
    origin=HistoricalOrigin.PROTO_SEMITIC
)

VOWEL_E_SHORT = Vowel(
    features=VowelFeatures(
        quality=VowelQuality.E,
        length=VowelLength.SHORT,
    ),
    origin=HistoricalOrigin.FROM_GUTTURAL,
    # Nota: e es secundaria y marginal; puede ser estable o alófono
)

VOWEL_I_SHORT = Vowel(
    features=VowelFeatures(
        quality=VowelQuality.I,
        length=VowelLength.SHORT,
    ),
    origin=HistoricalOrigin.PROTO_SEMITIC
)

VOWEL_U_SHORT = Vowel(
    features=VowelFeatures(
        quality=VowelQuality.U,
        length=VowelLength.SHORT,
    ),
    origin=HistoricalOrigin.PROTO_SEMITIC
)

# --- VOCALES LARGAS ---

VOWEL_A_LONG = Vowel(
    features=VowelFeatures(
        quality=VowelQuality.A,
        length=VowelLength.LONG,
    ),
    origin=HistoricalOrigin.PROTO_SEMITIC
)

VOWEL_E_LONG = Vowel(
    features=VowelFeatures(
        quality=VowelQuality.E,
        length=VowelLength.LONG,
    ),
    origin=HistoricalOrigin.FROM_DIPHTHONG,
    # Nota: ē típicamente de *ay, o de guturales *aʿ, *aḥ
)

VOWEL_I_LONG = Vowel(
    features=VowelFeatures(
        quality=VowelQuality.I,
        length=VowelLength.LONG,
    ),
    origin=HistoricalOrigin.PROTO_SEMITIC
)

VOWEL_U_LONG = Vowel(
    features=VowelFeatures(
        quality=VowelQuality.U,
        length=VowelLength.LONG,
    ),
    origin=HistoricalOrigin.PROTO_SEMITIC
    # Nota: ū también puede venir de *aw
)


# Diccionario organizado por cantidad
VOWEL_INVENTORY = {
    'short': {
        'a': VOWEL_A_SHORT,
        'e': VOWEL_E_SHORT,
        'i': VOWEL_I_SHORT,
        'u': VOWEL_U_SHORT,
    },
    'long': {
        'ā': VOWEL_A_LONG,
        'ē': VOWEL_E_LONG,
        'ī': VOWEL_I_LONG,
        'ū': VOWEL_U_LONG,
    },
}

# Diccionario plano para acceso rápido
VOWELS_BY_SYMBOL = {
    'a': VOWEL_A_SHORT,
    'e': VOWEL_E_SHORT,
    'i': VOWEL_I_SHORT,
    'u': VOWEL_U_SHORT,
    'ā': VOWEL_A_LONG,
    'ē': VOWEL_E_LONG,
    'ī': VOWEL_I_LONG,
    'ū': VOWEL_U_LONG,
}


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def get_consonant(symbol: str) -> Consonant:
    """Obtiene consonante por símbolo."""
    if symbol not in CONSONANTS_BY_SYMBOL:
        raise ValueError(f"Consonante desconocida: {symbol}")
    return CONSONANTS_BY_SYMBOL[symbol]


def get_vowel(symbol: str) -> Vowel:
    """Obtiene vocal por símbolo."""
    if symbol not in VOWELS_BY_SYMBOL:
        raise ValueError(f"Vocal desconocida: {symbol}")
    return VOWELS_BY_SYMBOL[symbol]


def get_consonants_by_feature(**kwargs) -> list[Consonant]:
    """
    Filtra consonantes por rasgos.
    
    Ejemplo:
        get_consonants_by_feature(is_sibilant=True)
        get_consonants_by_feature(is_weak=True)
    """
    results = []
    for c in CONSONANTS_BY_SYMBOL.values():
        match = all(
            getattr(c.features, key) == value
            for key, value in kwargs.items()
        )
        if match:
            results.append(c)
    return results


def get_vowels_by_feature(**kwargs) -> list[Vowel]:
    """
    Filtra vocales por rasgos.
    
    Ejemplo:
        get_vowels_by_feature(is_long=True)
        get_vowels_by_feature(is_front=True)
    """
    results = []
    for v in VOWELS_BY_SYMBOL.values():
        match = all(
            getattr(v, key) == value
            for key, value in kwargs.items()
        )
        if match:
            results.append(v)
    return results


# Conjuntos útiles para reglas fonológicas
WEAK_CONSONANTS = get_consonants_by_feature(is_weak=True)       # ʾ, w, y
SIBILANTS = get_consonants_by_feature(is_sibilant=True)         # s, z, š, ṣ
EMPHATICS = get_consonants_by_feature(is_emphatic=True)         # ṭ, ṣ, q
GUTTURALS = get_consonants_by_feature(is_guttural=True)         # ḫ, ʾ
NASALS = get_consonants_by_feature(is_nasal=True)               # m, n
LIQUIDS = get_consonants_by_feature(is_liquid=True)             # l, r
SONORANTS = get_consonants_by_feature(is_sonorant=True)         # m, n, l, r, w, y

FRONT_VOWELS = get_vowels_by_feature(is_front=True)             # i, e (+ largas)
BACK_VOWELS = get_vowels_by_feature(is_back=True)               # u (+ larga)
HIGH_VOWELS = get_vowels_by_feature(is_high=True)               # i, u (+ largas)
LOW_VOWELS = get_vowels_by_feature(is_low=True)                 # a (+ larga)

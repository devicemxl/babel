"""
Módulo de fonología del Old Assyrian.

Este módulo proporciona la representación fonológica completa del Old Assyrian
basada en Kouwenberg (2017) "A Grammar of Old Assyrian".

Componentes principales:
- Phoneme, Consonant, Vowel: Clases base para fonemas
- CONSONANT_INVENTORY, VOWEL_INVENTORY: Inventarios completos
- Enums: Tipos para clasificación fonológica
- Features: Rasgos distintivos
- Weak Consonants: Comportamiento de ʾ, w, y (NUEVO Iteración 2)
"""

from .phoneme import Phoneme, Consonant, Vowel
from .inventory import (
    CONSONANT_INVENTORY,
    VOWEL_INVENTORY,
    CONSONANTS_BY_SYMBOL,
    VOWELS_BY_SYMBOL,
    get_consonant,
    get_vowel,
    get_consonants_by_feature,
    get_vowels_by_feature,
    WEAK_CONSONANTS,
    SIBILANTS,
    EMPHATICS,
    GUTTURALS,
    NASALS,
    LIQUIDS,
    SONORANTS,
    FRONT_VOWELS,
    BACK_VOWELS,
    HIGH_VOWELS,
    LOW_VOWELS,
)
from .features import ConsonantFeatures, VowelFeatures
from .enums import (
    PlaceOfArticulation,
    MannerOfArticulation,
    Voicing,
    VowelQuality,
    VowelLength,
    VowelHeight,
    VowelBackness,
    AccentType,
    TextStatus,
    ConsonantClass,
    HistoricalOrigin,
)

# NUEVO en Iteración 2
from .weak_enums import (
    WeakPosition,
    SyllablePosition,
    WordPosition,
    PreservationStatus,
    EvidenceType,
    ReconstructMode,
    ContractionMode,
    WeakVerbClass,
    HistoricalChange,
    SpecialSpelling,
)
from .phonological_context import (
    PhonologicalContext,
    MorphologicalInfo,
    create_context_from_sequence,
    create_broken_spelling_context,
)
from .weak_consonants import (
    WeakConsonantBehavior,
    WeakConsonantExample,
    PhonologicalRule,
    get_behavior,
    get_applicable_rules,
    WEAK_BEHAVIORS,
)

# NUEVO en Iteración 5
from .syllable import (
    # Enums
    SyllableWeight,
    SyllablePosition as SyllablePos,  # Alias para evitar conflicto con weak_enums
    SyllableType,
    ClusterType,
    EpenthesisContext,
    EpentheticVowel,
    # Clases
    Syllable,
    SyllableStructure,
    # Funciones
    syllabify,
    validate_syllable_structure,
    syllabify_with_geminate_split,
    needs_epenthesis,
    apply_epenthesis,
    assign_stress,
    get_stressed_syllable,
    predict_stress_position,
    get_stress_pattern,
)

# NUEVO en Iteración 6
from .nominal import (
    # Enums
    Gender,
    Number as NominalNumber,  # Alias
    State,
    PatternType,
    NominalFunction,
    # Clases
    NominalRoot,
    NominalPattern,
    DerivedNominal,
    # Templates
    PARS,
    PIRS,
    PURS,
    PARAS,
    PARRAAS,
    # Funciones
    create_root_from_string,
    apply_pattern_to_root,
    derive_from_string,
)

__all__ = [
    # Clases principales
    'Phoneme',
    'Consonant',
    'Vowel',
    
    # Inventarios
    'CONSONANT_INVENTORY',
    'VOWEL_INVENTORY',
    'CONSONANTS_BY_SYMBOL',
    'VOWELS_BY_SYMBOL',
    
    # Funciones de acceso
    'get_consonant',
    'get_vowel',
    'get_consonants_by_feature',
    'get_vowels_by_feature',
    
    # Conjuntos útiles
    'WEAK_CONSONANTS',
    'SIBILANTS',
    'EMPHATICS',
    'GUTTURALS',
    'NASALS',
    'LIQUIDS',
    'SONORANTS',
    'FRONT_VOWELS',
    'BACK_VOWELS',
    'HIGH_VOWELS',
    'LOW_VOWELS',
    
    # Features
    'ConsonantFeatures',
    'VowelFeatures',
    
    # Enums (Iteración 1)
    'PlaceOfArticulation',
    'MannerOfArticulation',
    'Voicing',
    'VowelQuality',
    'VowelLength',
    'VowelHeight',
    'VowelBackness',
    'AccentType',
    'TextStatus',
    'ConsonantClass',
    'HistoricalOrigin',
    
    # Enums (Iteración 2)
    'WeakPosition',
    'SyllablePosition',
    'WordPosition',
    'PreservationStatus',
    'EvidenceType',
    'ReconstructMode',
    'ContractionMode',
    'WeakVerbClass',
    'HistoricalChange',
    'SpecialSpelling',
    
    # Context y Morfología
    'PhonologicalContext',
    'MorphologicalInfo',
    'create_context_from_sequence',
    'create_broken_spelling_context',
    
    # Weak Consonants
    'WeakConsonantBehavior',
    'WeakConsonantExample',
    'PhonologicalRule',
    'get_behavior',
    'get_applicable_rules',
    'WEAK_BEHAVIORS',
    
    # Syllable (Iteración 5)
    'SyllableWeight',
    'SyllablePos',  # SyllablePosition de syllable (evita conflicto)
    'SyllableType',
    'ClusterType',
    'EpenthesisContext',
    'EpentheticVowel',
    'Syllable',
    'SyllableStructure',
    'syllabify',
    'validate_syllable_structure',
    'syllabify_with_geminate_split',
    'needs_epenthesis',
    'apply_epenthesis',
    'assign_stress',
    'get_stressed_syllable',
    'predict_stress_position',
    'get_stress_pattern',
    
    # Nominal (Iteración 6)
    'Gender',
    'NominalNumber',
    'State',
    'PatternType',
    'NominalFunction',
    'NominalRoot',
    'NominalPattern',
    'DerivedNominal',
    'PARS',
    'PIRS',
    'PURS',
    'PARAS',
    'PARRAAS',
    'create_root_from_string',
    'apply_pattern_to_root',
    'derive_from_string',
]

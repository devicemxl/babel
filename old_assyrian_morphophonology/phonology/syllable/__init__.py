"""
Módulo de estructura silábica del Old Assyrian.

Basado en Kouwenberg (2017) § 3.2.2, § 3.2.3, § 3.5.
"""

from .enums import (
    SyllableWeight,
    SyllablePosition,
    SyllableType,
    ClusterType,
    EpenthesisContext,
    EpentheticVowel,
)

from .syllable import (
    Syllable,
    SyllableStructure,
)

from .syllabification import (
    syllabify,
    validate_syllable_structure,
    syllabify_with_geminate_split,
)

from .epenthesis import (
    EpenthesisRule,
    needs_epenthesis,
    apply_epenthesis,
    ALL_EPENTHESIS_RULES,
    EP_1_LIQUID_R,
    EP_2_LIQUID_L,
    EP_3_H_PLUS_C,
    EP_4_IMPERATIVE,
)

from .stress import (
    assign_stress,
    get_stressed_syllable,
    predict_stress_position,
    get_stress_pattern,
)

__all__ = [
    # Enums
    'SyllableWeight',
    'SyllablePosition',
    'SyllableType',
    'ClusterType',
    'EpenthesisContext',
    'EpentheticVowel',
    
    # Core classes
    'Syllable',
    'SyllableStructure',
    
    # Syllabification
    'syllabify',
    'validate_syllable_structure',
    'syllabify_with_geminate_split',
    
    # Epenthesis
    'EpenthesisRule',
    'needs_epenthesis',
    'apply_epenthesis',
    'ALL_EPENTHESIS_RULES',
    'EP_1_LIQUID_R',
    'EP_2_LIQUID_L',
    'EP_3_H_PLUS_C',
    'EP_4_IMPERATIVE',
    
    # Stress
    'assign_stress',
    'get_stressed_syllable',
    'predict_stress_position',
    'get_stress_pattern',
]

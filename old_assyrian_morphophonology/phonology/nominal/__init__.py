"""
Módulo de morfología nominal del Old Assyrian.

ITERACIÓN 6 + 7: Patrones nominales e inflexión completa.

Componentes principales:
- Enums: Gender, Number, State, PatternType, Case, etc.
- Pattern: NominalRoot, NominalPattern, DerivedNominal
- Templates: PARS, PIRS, PURS, PARAS, PARRAAS, etc.
- Derivation: apply_pattern_to_root(), derive_feminine(), etc.
- Inflection: Sistema completo de casos, número, constructo, posesivos
- Paradigm: Generación de paradigmas completos

Basado en Kouwenberg (2017) Capítulos 4-5, § 9.5.

Uso básico:
    >>> from old_assyrian_morphophonology.phonology.nominal import (
    ...     create_root_from_string,
    ...     PARS,
    ...     apply_pattern_to_root,
    ...     generate_paradigm
    ... )
    >>> 
    >>> # Derivar sustantivo desde raíz
    >>> root = create_root_from_string("mlk")
    >>> derived = apply_pattern_to_root(root, PARS)
    >>> 
    >>> # Generar paradigma completo
    >>> paradigm = generate_paradigm(derived)
    >>> print(paradigm.to_table())
"""

from .enums import (
    Gender,
    Number,
    State,
    PatternType,
    NominalFunction,
    RootType,
    VowelPatternType,
    Mimation,
)

from .pattern import (
    NominalExample,
    NominalRoot,
    NominalPattern,
    DerivedNominal,
    create_root_from_string,
    get_pattern_statistics,
)

from .templates import (
    # Patrones monovocálicos cortos
    PARS,
    PIRS,
    PURS,
    # Patrones monovocálicos largos
    PAARS,
    PIIRS,
    # Patrones bivocálicos
    PARAS,
    PIRIIS,
    # Patrones con geminación
    PARRAAS,
    PURRUS,
    # Patrones con prefijos
    MAPRAS,
    # Patrones femeninos
    PARS_T,
    # Colecciones
    ALL_PATTERNS,
    PATTERNS_BY_NAME,
    PATTERNS_BY_CODE,
    # Funciones de búsqueda
    get_pattern_by_name,
    get_pattern_by_code,
    get_patterns_by_function,
    get_patterns_by_gender,
    get_patterns_with_gemination,
    get_primary_patterns,
)

from .derivation import (
    apply_pattern_to_root,
    build_base_form,
    add_mimation,
    apply_construct_state,
    derive_feminine,
    derive_from_string,
    get_all_forms,
)

# ===== ITERACIÓN 7: INFLEXIÓN NOMINAL =====

from .inflection_enums import (
    Case,
    PossessivePerson,
    PossessiveNumber,
    ConstructType,
    ConstructContext,
    WeakConsonantType,
    AbsoluteStateFunction,
)

from .inflection import (
    CaseMarker,
    NumberMarker,
    PossessiveSuffix,
    InflectedNominal,
    InflectionContext,
)

from .case_system import (
    apply_case_marker,
    remove_mimation,
    is_oblique,
    get_case_vowel,
)

from .number_system import (
    form_dual,
    form_plural,
    form_plural_masculine,
    form_plural_feminine,
    get_number_marker,
)

from .construct_state import (
    to_construct_state,
)

from .possessive_system import (
    add_possessive,
    get_possessive_suffix,
    generate_possessive_paradigm,
)

from .paradigm import (
    NominalParadigm,
    generate_paradigm,
)

__all__ = [
    # ===== ITERACIÓN 6: PATRONES NOMINALES =====
    
    # Enums
    'Gender',
    'Number',
    'State',
    'PatternType',
    'NominalFunction',
    'RootType',
    'VowelPatternType',
    'Mimation',
    
    # Pattern classes
    'NominalExample',
    'NominalRoot',
    'NominalPattern',
    'DerivedNominal',
    
    # Pattern utilities
    'create_root_from_string',
    'get_pattern_statistics',
    
    # Templates - Monovocálicos cortos
    'PARS',
    'PIRS',
    'PURS',
    
    # Templates - Monovocálicos largos
    'PAARS',
    'PIIRS',
    
    # Templates - Bivocálicos
    'PARAS',
    'PIRIIS',
    
    # Templates - Con geminación
    'PARRAAS',
    'PURRUS',
    
    # Templates - Con prefijos
    'MAPRAS',
    
    # Templates - Femeninos
    'PARS_T',
    
    # Template collections
    'ALL_PATTERNS',
    'PATTERNS_BY_NAME',
    'PATTERNS_BY_CODE',
    
    # Template search functions
    'get_pattern_by_name',
    'get_pattern_by_code',
    'get_patterns_by_function',
    'get_patterns_by_gender',
    'get_patterns_with_gemination',
    'get_primary_patterns',
    
    # Derivation functions
    'apply_pattern_to_root',
    'build_base_form',
    'add_mimation',
    'apply_construct_state',
    'derive_feminine',
    'derive_from_string',
    'get_all_forms',
    
    # ===== ITERACIÓN 7: INFLEXIÓN NOMINAL =====
    
    # Enums de inflexión
    'Case',
    'PossessivePerson',
    'PossessiveNumber',
    'ConstructType',
    'ConstructContext',
    'WeakConsonantType',
    'AbsoluteStateFunction',
    
    # Clases de inflexión
    'CaseMarker',
    'NumberMarker',
    'PossessiveSuffix',
    'InflectedNominal',
    'InflectionContext',
    
    # Sistema de casos
    'apply_case_marker',
    'remove_mimation',
    'is_oblique',
    'get_case_vowel',
    
    # Sistema de número
    'form_dual',
    'form_plural',
    'get_number_marker',
    
    # Estado constructo
    'to_construct_state',
    
    # Sufijos posesivos
    'add_possessive',
    'get_possessive_suffix',
    'generate_possessive_paradigm',
    
    # Paradigmas
    'NominalParadigm',
    'generate_paradigm',
]

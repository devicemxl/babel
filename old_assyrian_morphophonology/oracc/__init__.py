"""
Módulo ORACC para parseo y conversión de transliteraciones.

ORACC (Open Richly Annotated Cuneiform Corpus) es el estándar
para transliteración de textos acadios cuneiformes.

Este módulo proporciona:
- Parseo de transliteraciones ORACC a fonemas
- Conversión de fonemas de vuelta a ORACC
- Manejo de metadata ortográfica y textual
- Reconstrucción de consonantes débiles (NUEVO Iteración 2)
"""

from .types import OraccToken, OraccWord, OraccLine
from .parser import (
    OraccParser,
    parse_oracc,
    oracc_to_phonemes,
    phonemes_to_oracc,
)
from .mappings import (
    ORACC_TO_PHONEME_MAP,
    ORACC_SUBSCRIPTS,
    ORACC_TEXT_MARKERS,
    ORACC_SEPARATORS,
    phoneme_to_oracc,
    get_phoneme_from_oracc,
)

# NUEVO en Iteración 2
from .reconstruction import (
    WeakConsonantReconstructor,
    ReconstructedWeak,
    reconstruct_weak_consonants,
    identify_weak_verb_class,
)
from .decision_tables import (
    ReconstructionDecision,
    lookup_decision,
    lookup_special_case,
    get_default_decision,
    get_table_statistics,
    BROKEN_SPELLING_DECISIONS,
    SPECIAL_CASES,
)

__all__ = [
    # Tipos
    'OraccToken',
    'OraccWord',
    'OraccLine',
    
    # Parser
    'OraccParser',
    'parse_oracc',
    'oracc_to_phonemes',
    'phonemes_to_oracc',
    
    # Mapeos
    'ORACC_TO_PHONEME_MAP',
    'ORACC_SUBSCRIPTS',
    'ORACC_TEXT_MARKERS',
    'ORACC_SEPARATORS',
    'phoneme_to_oracc',
    'get_phoneme_from_oracc',
    
    # Reconstrucción (Iteración 2)
    'WeakConsonantReconstructor',
    'ReconstructedWeak',
    'reconstruct_weak_consonants',
    'identify_weak_verb_class',
    
    # Tablas de decisión
    'ReconstructionDecision',
    'lookup_decision',
    'lookup_special_case',
    'get_default_decision',
    'get_table_statistics',
    'BROKEN_SPELLING_DECISIONS',
    'SPECIAL_CASES',
]

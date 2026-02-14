"""
Sistema de stems verbales del Old Assyrian.

ITERACIÓN 8 - Stems verbales derivados.

Este módulo implementa el sistema completo de derivación verbal
del Old Assyrian, incluyendo:
- G-stem (base)
- Derivados con infijo -t- (Gt, Gtn)
- Derivados con geminación (D, Dt, Dtn)
- Derivados causativos (Š, Št, Štn)
- Derivados con nasal (N, Ntn)

Basado en Kouwenberg (2017) Capítulo 17.

Autor: Claude
Fecha: 2026-02-10
"""

from .enums import (
    StemType,
    VoiceType,
    SemanticFunction,
    VowelClass,
    MorphologicalMarker,
    Productivity,
    STEM_PRODUCTIVITY,
    STEM_MARKERS,
    STEM_DEFAULT_FUNCTION,
    STEM_DEFAULT_VOICE
)

from .stem import (
    VerbalRoot,
    VerbalStem,
    create_root,
    is_derived_from
)

__all__ = [
    # Enumeraciones
    'StemType',
    'VoiceType',
    'SemanticFunction',
    'VowelClass',
    'MorphologicalMarker',
    'Productivity',
    
    # Mappings
    'STEM_PRODUCTIVITY',
    'STEM_MARKERS',
    'STEM_DEFAULT_FUNCTION',
    'STEM_DEFAULT_VOICE',
    
    # Clases
    'VerbalRoot',
    'VerbalStem',
    
    # Funciones
    'create_root',
    'is_derived_from',
]

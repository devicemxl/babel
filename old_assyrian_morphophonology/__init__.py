"""
Old Assyrian Morphophonology System

Sistema completo de reglas morfofonológicas del Old Assyrian basado en:
Kouwenberg, N. J. C. (2017). "A Grammar of Old Assyrian"

Este paquete proporciona:
- Representación fonológica completa del Old Assyrian
- Parser para transliteraciones ORACC
- Reglas morfofonológicas en cascada
- Generación de formas morfológicas

Iteración 1: Fundamentos Fonológicos Básicos
- Inventario consonántico (20 fonemas)
- Inventario vocálico (4 cualidades × 2 cantidades)
- Mapeo ORACC ↔ Fonológico
- Clases base: Phoneme, Consonant, Vowel
"""

__version__ = '0.1.0'
__author__ = 'Old Assyrian Morphophonology Project'

# Importar componentes principales para fácil acceso
from .phonology import (
    Phoneme,
    Consonant,
    Vowel,
    CONSONANT_INVENTORY,
    VOWEL_INVENTORY,
    get_consonant,
    get_vowel,
)

from .oracc import (
    OraccParser,
    parse_oracc,
    oracc_to_phonemes,
    phonemes_to_oracc,
)

__all__ = [
    # Clases fonológicas
    'Phoneme',
    'Consonant',
    'Vowel',
    
    # Inventarios
    'CONSONANT_INVENTORY',
    'VOWEL_INVENTORY',
    
    # Acceso a fonemas
    'get_consonant',
    'get_vowel',
    
    # ORACC
    'OraccParser',
    'parse_oracc',
    'oracc_to_phonemes',
    'phonemes_to_oracc',
]

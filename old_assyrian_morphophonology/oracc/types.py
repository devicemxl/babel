"""
Tipos y clases para representación de transliteraciones ORACC.

ORACC (Open Richly Annotated Cuneiform Corpus) es el estándar
para transliteración de textos cuneiformes acadios.
"""

from dataclasses import dataclass
from typing import List, Optional

import sys
import os
# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phonology import Phoneme, AccentType, TextStatus


@dataclass
class OraccToken:
    """
    Representación de un token ORACC con múltiples capas de información.
    
    ORACC incluye:
    - Contenido fonológico (lista de fonemas)
    - Metadata ortográfica (variante de signo cuneiforme)
    - Metadata textual (estado de preservación)
    - Metadata prosódica (acento, en algunos casos)
    - Reconstrucción de débiles (NUEVO en Iteración 2)
    
    Ejemplo:
        "li₂" → OraccToken(
            phonemes=[Consonant(l), Vowel(i)],
            cuneiform_variant=2,
            text_status=TextStatus.CLEAR
        )
        
        "ša-a-lum" (con reconstrucción) → OraccToken(
            phonemes=[š, a, ʾ, ā, l, u, m],
            reconstructed_weak=[ReconstructedWeak(ʾ, pos=2)]
        )
    """
    
    phonemes: List[Phoneme]
    cuneiform_variant: Optional[int] = None  # Subíndice ₁, ₂, ₃, etc.
    text_status: TextStatus = TextStatus.CLEAR
    original_spelling: Optional[str] = None  # Spelling ORACC original
    
    # NUEVO en Iteración 2
    reconstructed_weak: Optional[List['ReconstructedWeak']] = None  # Débiles reconstruidas
    
    def to_phonological_string(self) -> str:
        """Convierte solo la parte fonológica a string."""
        return ''.join(p.symbol for p in self.phonemes)
    
    def to_oracc(self) -> str:
        """
        Reconstruye la representación ORACC completa.
        
        Incluye:
        - Fonemas con diacríticos apropiados
        - Subíndice numérico si existe
        - Marcadores de daño/restauración
        """
        base = ''.join(p.to_oracc() for p in self.phonemes)
        
        # Añadir subíndice si existe
        if self.cuneiform_variant is not None:
            subscript_map = {
                0: '₀', 1: '₁', 2: '₂', 3: '₃', 4: '₄',
                5: '₅', 6: '₆', 7: '₇', 8: '₈', 9: '₉',
            }
            if self.cuneiform_variant in subscript_map:
                base += subscript_map[self.cuneiform_variant]
        
        # Añadir marcadores textuales
        if self.text_status == TextStatus.DAMAGED:
            base = f'⸢{base}⸣'
        elif self.text_status == TextStatus.RESTORED:
            base = f'⸤{base}⸥'
        elif self.text_status == TextStatus.BROKEN:
            return 'u'  # Palabra rota
        elif self.text_status == TextStatus.UNCERTAIN:
            return 'X'  # Lectura incierta
        
        return base
    
    def __str__(self) -> str:
        return self.to_oracc()
    
    def __repr__(self) -> str:
        return f"OraccToken({self.to_oracc()})"


@dataclass
class OraccWord:
    """
    Representación de una palabra completa en ORACC.
    
    Una palabra puede consistir de múltiples tokens (sílabas)
    separados por guiones en la transliteración.
    
    Ejemplo:
        "i-ṣa-ba-at" → OraccWord([
            OraccToken([i]),
            OraccToken([ṣ, a]),
            OraccToken([b, a]),
            OraccToken([a, t])
        ])
    """
    
    tokens: List[OraccToken]
    word_divider: str = '-'  # Separador entre sílabas
    
    def to_phonemes(self) -> List[Phoneme]:
        """Extrae todos los fonemas de todos los tokens."""
        phonemes = []
        for token in self.tokens:
            phonemes.extend(token.phonemes)
        return phonemes
    
    def to_oracc(self) -> str:
        """Reconstruye la transliteración ORACC completa."""
        return self.word_divider.join(token.to_oracc() for token in self.tokens)
    
    def to_phonological_string(self) -> str:
        """Solo la secuencia fonológica sin separadores."""
        return ''.join(p.symbol for p in self.to_phonemes())
    
    def __str__(self) -> str:
        return self.to_oracc()
    
    def __repr__(self) -> str:
        return f"OraccWord({self.to_oracc()})"


@dataclass
class OraccLine:
    """
    Representación de una línea de texto ORACC.
    
    Puede contener múltiples palabras.
    """
    
    words: List[OraccWord]
    
    def to_oracc(self) -> str:
        """Reconstruye la línea ORACC completa."""
        return ' '.join(word.to_oracc() for word in self.words)
    
    def __str__(self) -> str:
        return self.to_oracc()
    
    def __repr__(self) -> str:
        return f"OraccLine({self.to_oracc()})"

"""
Parser para transliteraciones ORACC del Old Assyrian.

Este módulo convierte strings ORACC a representación fonológica interna.
"""

import re
from typing import List, Optional, Tuple
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .types import OraccToken, OraccWord, OraccLine
from .mappings import (
    ORACC_TO_PHONEME_MAP,
    ORACC_SUBSCRIPTS,
    ORACC_TEXT_MARKERS,
    ORACC_SEPARATORS,
    get_phoneme_from_oracc,
)
from phonology import Phoneme, TextStatus


class OraccParser:
    """
    Parser para transliteraciones ORACC.
    
    Maneja:
    - Conversión de caracteres Unicode ORACC a fonemas
    - Subíndices numéricos (variantes cuneiformes)
    - Marcadores de preservación textual (⸢⸣, ⸤⸥)
    - Separadores de sílabas y palabras
    - Reconstrucción de consonantes débiles (NUEVO en Iteración 2)
    """
    
    @staticmethod
    def parse_token(
        text: str,
        reconstruct_weak: bool = False,
        morphological_hint: 'Optional[MorphologicalInfo]' = None,
    ) -> OraccToken:
        """
        Parsea un token ORACC individual (típicamente una sílaba).
        
        Args:
            text: String ORACC (ej: "ba", "li₂", "⸢ab⸣")
            reconstruct_weak: Si True, intenta reconstruir consonantes débiles
            morphological_hint: Información morfológica para ayudar en reconstrucción
        
        Returns:
            OraccToken con fonemas y metadata
        
        Examples:
            >>> parse_token("ba")
            OraccToken([Consonant(b), Vowel(a)])
            
            >>> parse_token("li₂")
            OraccToken([Consonant(l), Vowel(i)], cuneiform_variant=2)
            
            >>> parse_token("⸢ab⸣")
            OraccToken([Vowel(a), Consonant(b)], text_status=DAMAGED)
            
            >>> parse_token("ša-a-lum", reconstruct_weak=True)  # Reconstruye ʾ
            OraccToken([...], reconstructed_weak=[...])
        """
        if not text:
            raise ValueError("Token vacío")
        
        # Casos especiales: palabras rotas/inciertas
        if text == 'u':
            return OraccToken([], text_status=TextStatus.BROKEN, original_spelling=text)
        if text == 'X':
            return OraccToken([], text_status=TextStatus.UNCERTAIN, original_spelling=text)
        
        # Detectar marcadores de preservación
        text_status = TextStatus.CLEAR
        if text.startswith('⸢') and text.endswith('⸣'):
            text_status = TextStatus.DAMAGED
            text = text[1:-1]  # Remover marcadores
        elif text.startswith('⸤') and text.endswith('⸥'):
            text_status = TextStatus.RESTORED
            text = text[1:-1]
        
        # Separar subíndice numérico si existe
        cuneiform_variant = None
        for subscript, number in ORACC_SUBSCRIPTS.items():
            if text.endswith(subscript):
                if isinstance(number, int):
                    cuneiform_variant = number
                text = text[:-1]  # Remover subíndice
                break
        
        # Parsear caracteres fonológicos
        phonemes = OraccParser._parse_phonological_content(text)
        
        # NUEVO: Reconstruir consonantes débiles si se solicita
        reconstructed_weak = None
        if reconstruct_weak:
            try:
                from .reconstruction import reconstruct_weak_consonants
                from phonology.weak_enums import ReconstructMode
                
                phonemes_with_weak, reconstructions = reconstruct_weak_consonants(
                    phonemes,
                    mode=ReconstructMode.AUTO,
                    morphology=morphological_hint,
                    original_spelling=text,
                )
                
                if reconstructions:
                    phonemes = phonemes_with_weak
                    reconstructed_weak = reconstructions
            except ImportError:
                pass  # Módulo de reconstrucción no disponible
        
        return OraccToken(
            phonemes=phonemes,
            cuneiform_variant=cuneiform_variant,
            text_status=text_status,
            original_spelling=text,
            reconstructed_weak=reconstructed_weak,
        )
    
    @staticmethod
    def _parse_phonological_content(text: str) -> List[Phoneme]:
        """
        Parsea el contenido fonológico puro de un token.
        
        Convierte cada carácter ORACC a su fonema correspondiente.
        Maneja caracteres multi-byte (ā, š, ṣ, etc.)
        """
        phonemes = []
        i = 0
        
        while i < len(text):
            # Los caracteres Unicode de ORACC son siempre de 1 carácter
            # (ā, š, ṣ, etc. son single code points)
            char = text[i]
            try:
                phoneme = get_phoneme_from_oracc(char)
                phonemes.append(phoneme)
                i += 1
            except KeyError:
                raise ValueError(
                    f"Carácter desconocido en posición {i}: '{char}' "
                    f"(U+{ord(char):04X}) en token '{text}'"
                )
        
        return phonemes
    
    @staticmethod
    def parse_word(text: str, divider: str = '-') -> OraccWord:
        """
        Parsea una palabra ORACC completa.
        
        Args:
            text: Palabra ORACC (ej: "i-ṣa-ba-at")
            divider: Separador de sílabas (default: '-')
        
        Returns:
            OraccWord con todos sus tokens
        
        Examples:
            >>> parse_word("i-ṣa-ba-at")
            OraccWord([
                OraccToken([i]),
                OraccToken([ṣ, a]),
                OraccToken([b, a]),
                OraccToken([a, t])
            ])
        """
        if not text:
            raise ValueError("Palabra vacía")
        
        # Dividir por separador
        syllables = text.split(divider)
        
        # Parsear cada sílaba
        tokens = [OraccParser.parse_token(syl) for syl in syllables]
        
        return OraccWord(tokens=tokens, word_divider=divider)
    
    @staticmethod
    def parse_line(text: str) -> OraccLine:
        """
        Parsea una línea completa de texto ORACC.
        
        Args:
            text: Línea ORACC (ej: "i-na a-lim")
        
        Returns:
            OraccLine con todas sus palabras
        
        Examples:
            >>> parse_line("i-na a-lim")
            OraccLine([OraccWord(...), OraccWord(...)])
        """
        if not text:
            raise ValueError("Línea vacía")
        
        # Dividir por espacios (palabras)
        word_strings = text.split()
        
        # Parsear cada palabra
        words = [OraccParser.parse_word(w) for w in word_strings]
        
        return OraccLine(words=words)
    
    @staticmethod
    def to_phonemes(text: str) -> List[Phoneme]:
        """
        Conversión directa de texto ORACC a lista de fonemas.
        
        Ignora metadata ortográfica y textual.
        Útil para procesamiento fonológico puro.
        
        Args:
            text: Cualquier string ORACC
        
        Returns:
            Lista plana de fonemas
        
        Examples:
            >>> to_phonemes("i-ṣa-ba-at")
            [Vowel(i), Consonant(ṣ), Vowel(a), Consonant(b), Vowel(a), Consonant(t)]
        """
        # Remover separadores
        cleaned = text.replace('-', '').replace('.', '').replace(' ', '')
        
        # Remover marcadores de preservación
        cleaned = cleaned.replace('⸢', '').replace('⸣', '')
        cleaned = cleaned.replace('⸤', '').replace('⸥', '')
        
        # Remover subíndices
        for subscript in ORACC_SUBSCRIPTS:
            cleaned = cleaned.replace(subscript, '')
        
        # Parsear contenido fonológico
        return OraccParser._parse_phonological_content(cleaned)
    
    @staticmethod
    def validate_oracc(text: str) -> Tuple[bool, Optional[str]]:
        """
        Valida si un string es ORACC válido.
        
        Returns:
            (is_valid, error_message)
        """
        try:
            OraccParser.parse_line(text)
            return (True, None)
        except Exception as e:
            return (False, str(e))


# ============================================================================
# FUNCIONES DE CONVENIENCIA
# ============================================================================

def parse_oracc(text: str) -> OraccWord:
    """
    Función de conveniencia para parsear ORACC.
    
    Automáticamente detecta si es palabra o línea.
    """
    if ' ' in text:
        # Es una línea con múltiples palabras
        return OraccParser.parse_line(text)
    else:
        # Es una palabra simple
        return OraccParser.parse_word(text)


def oracc_to_phonemes(text: str) -> List[Phoneme]:
    """Función de conveniencia para conversión directa a fonemas."""
    return OraccParser.to_phonemes(text)


def phonemes_to_oracc(phonemes: List[Phoneme], 
                      add_syllable_breaks: bool = False) -> str:
    """
    Convierte lista de fonemas de vuelta a ORACC.
    
    Args:
        phonemes: Lista de fonemas
        add_syllable_breaks: Si True, intenta añadir guiones entre sílabas
    
    Returns:
        String ORACC
    
    Note:
        La silabificación automática es compleja y se implementará
        en iteraciones posteriores. Por ahora, solo concatena.
    """
    oracc_chars = [p.to_oracc() for p in phonemes]
    
    if add_syllable_breaks:
        # Silabificación simple (a mejorar en Iteración 5)
        # Por ahora, solo separa cada CV
        result = []
        for i, char in enumerate(oracc_chars):
            result.append(char)
            # Heurística básica: añadir guion después de vocal si sigue consonante
            if i < len(oracc_chars) - 1:
                # Esto es muy simplificado
                pass  # TODO: implementar en Iteración 5
        return ''.join(result)
    else:
        return ''.join(oracc_chars)

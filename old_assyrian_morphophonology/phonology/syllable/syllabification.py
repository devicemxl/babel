"""
Algoritmo de silabificación y validación para Old Assyrian.

Basado en Kouwenberg (2017) § 3.5.1.
"""

from typing import List, Tuple, Optional
from .. import Phoneme, Consonant, Vowel
from .syllable import Syllable, SyllableStructure
from .enums import SyllablePosition, SyllableWeight


def syllabify(phonemes: List[Phoneme]) -> SyllableStructure:
    """
    Divide secuencia de fonemas en sílabas.
    
    Algoritmo de silabificación OA:
      1. Clusters siempre divididos por frontera silábica
      2. Geminadas divididas (C₁.C₂)
      3. No onset clusters (prohibidos)
      4. VV separado por frontera silábica (con glide ʾ/w/y)
    
    Args:
        phonemes: Secuencia de fonemas
    
    Returns:
        SyllableStructure con división completa
    """
    if not phonemes:
        return SyllableStructure(syllables=[])
    
    syllables = []
    current_onset = []
    current_nucleus = None
    current_coda = []
    
    i = 0
    while i < len(phonemes):
        phoneme = phonemes[i]
        
        if isinstance(phoneme, Vowel):
            # Vocal = núcleo
            if current_nucleus is None:
                # Primera vocal → núcleo de sílaba actual
                current_nucleus = phoneme
            else:
                # Segunda vocal → nueva sílaba
                # Completar sílaba actual
                syl = Syllable(
                    onset=current_onset if current_onset else None,
                    nucleus=current_nucleus,
                    coda=current_coda if current_coda else None
                )
                syllables.append(syl)
                
                # Iniciar nueva sílaba
                current_onset = []  # VV separado por frontera
                current_nucleus = phoneme
                current_coda = []
        
        elif isinstance(phoneme, Consonant):
            # Consonante
            if current_nucleus is None:
                # Antes de vocal → onset
                current_onset.append(phoneme)
            else:
                # Después de vocal → potencial coda
                # Verificar si hay más fonemas
                if i + 1 < len(phonemes):
                    next_phoneme = phonemes[i + 1]
                    
                    if isinstance(next_phoneme, Vowel):
                        # C seguida de V → onset de próxima sílaba
                        # Completar sílaba actual
                        syl = Syllable(
                            onset=current_onset if current_onset else None,
                            nucleus=current_nucleus,
                            coda=current_coda if current_coda else None
                        )
                        syllables.append(syl)
                        
                        # Iniciar nueva
                        current_onset = [phoneme]
                        current_nucleus = None
                        current_coda = []
                    else:
                        # C seguida de C → primera va a coda
                        current_coda.append(phoneme)
                        
                        # Completar sílaba (clusters divididos)
                        syl = Syllable(
                            onset=current_onset if current_onset else None,
                            nucleus=current_nucleus,
                            coda=current_coda if current_coda else None
                        )
                        syllables.append(syl)
                        
                        # Siguiente C será onset
                        current_onset = []
                        current_nucleus = None
                        current_coda = []
                else:
                    # Última consonante → coda
                    current_coda.append(phoneme)
        
        i += 1
    
    # Completar última sílaba si hay núcleo
    if current_nucleus is not None:
        syl = Syllable(
            onset=current_onset if current_onset else None,
            nucleus=current_nucleus,
            coda=current_coda if current_coda else None
        )
        syllables.append(syl)
    
    # Asignar posiciones
    for i, syl in enumerate(syllables):
        if i == 0:
            syl.position = SyllablePosition.INITIAL
        elif i == len(syllables) - 1:
            syl.position = SyllablePosition.FINAL
        elif i == len(syllables) - 2:
            syl.position = SyllablePosition.PENULTIMATE
        elif i == len(syllables) - 3:
            syl.position = SyllablePosition.ANTEPENULTIMATE
        else:
            syl.position = SyllablePosition.MEDIAL
    
    return SyllableStructure(syllables=syllables)


def validate_syllable_structure(
    structure: SyllableStructure
) -> Tuple[bool, List[str]]:
    """
    Valida que estructura silábica sea legal en OA.
    
    Verifica:
      - No clusters en onset/coda (máximo 1 consonante)
      - CV̄C solo en posición final (o condiciones específicas)
      - Todas sílabas tienen núcleo
      - Geminadas divididas correctamente (si detectables)
    
    Args:
        structure: Estructura a validar
    
    Returns:
        (is_valid, list_of_violations)
    """
    violations = []
    
    for i, syl in enumerate(structure.syllables):
        # Onset: máximo 1 consonante
        if syl.onset and len(syl.onset) > 1:
            violations.append(
                f"Sílaba {i} ({syl.to_string()}): "
                f"onset cluster prohibido ({len(syl.onset)} consonantes)"
            )
        
        # Coda: máximo 1 consonante (generalmente)
        if syl.coda and len(syl.coda) > 1:
            violations.append(
                f"Sílaba {i} ({syl.to_string()}): "
                f"coda cluster prohibido ({len(syl.coda)} consonantes)"
            )
        
        # CV̄C solo en final (regla estricta)
        # O en medial bajo condiciones (vocal larga original + sufijo)
        if syl.weight == SyllableWeight.SUPERHEAVY:
            if syl.position != SyllablePosition.FINAL:
                # Permitir en medial bajo ciertas condiciones
                # Por ahora, advertencia no violación
                violations.append(
                    f"Sílaba {i} ({syl.to_string()}): "
                    f"CV̄C en posición no-final (permitido bajo condiciones)"
                )
        
        # Núcleo obligatorio
        if syl.nucleus is None:
            violations.append(
                f"Sílaba {i}: falta núcleo (obligatorio)"
            )
    
    return (len(violations) == 0, violations)


def split_at_geminate(phonemes: List[Phoneme]) -> List[List[Phoneme]]:
    """
    Divide secuencia en geminadas detectadas.
    
    Geminadas siempre divididas por frontera silábica.
    
    Args:
        phonemes: Secuencia de fonemas
    
    Returns:
        Lista de segmentos (cada uno sin geminadas internas)
    """
    segments = []
    current = []
    
    i = 0
    while i < len(phonemes):
        phoneme = phonemes[i]
        current.append(phoneme)
        
        # Verificar geminada
        if (isinstance(phoneme, Consonant) and
            i + 1 < len(phonemes) and
            isinstance(phonemes[i + 1], Consonant) and
            phoneme.symbol == phonemes[i + 1].symbol):
            
            # Geminada detectada → dividir
            segments.append(current)
            current = []
        
        i += 1
    
    if current:
        segments.append(current)
    
    return segments


def syllabify_with_geminate_split(phonemes: List[Phoneme]) -> SyllableStructure:
    """
    Silabifica con división explícita de geminadas.
    
    Args:
        phonemes: Secuencia de fonemas
    
    Returns:
        SyllableStructure
    """
    # Primero dividir en geminadas
    segments = split_at_geminate(phonemes)
    
    # Silabificar cada segmento
    all_syllables = []
    for segment in segments:
        structure = syllabify(segment)
        all_syllables.extend(structure.syllables)
    
    # Crear estructura completa
    result = SyllableStructure(syllables=all_syllables)
    
    # Re-asignar posiciones
    for i, syl in enumerate(result.syllables):
        if i == 0:
            syl.position = SyllablePosition.INITIAL
        elif i == len(result.syllables) - 1:
            syl.position = SyllablePosition.FINAL
        elif i == len(result.syllables) - 2:
            syl.position = SyllablePosition.PENULTIMATE
        else:
            syl.position = SyllablePosition.MEDIAL
    
    return result

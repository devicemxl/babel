"""
Sistema de asignación de estrés para Old Assyrian.

Basado en Kouwenberg (2017) § 3.5.2.
ADVERTENCIA: Evidencia limitada en OA.
"""

from typing import Optional
from .syllable import Syllable, SyllableStructure
from .enums import SyllableWeight, SyllablePosition


def assign_stress(structure: SyllableStructure) -> SyllableStructure:
    """
    Asigna estrés a sílaba apropiada.
    
    Regla (basada en comparación con otras lenguas semíticas):
      1. Última sílaba pesada → estrés
      2. Si no hay pesada → penúltima
      3. Default → penúltima
    
    ADVERTENCIA: Especulativo. Evidencia directa limitada en OA.
    
    Args:
        structure: Estructura silábica
    
    Returns:
        Estructura con estrés asignado
    """
    if not structure.syllables:
        return structure
    
    # Limpiar estrés previo
    for syl in structure.syllables:
        syl.is_stressed = False
    
    # Buscar última sílaba pesada
    for i in range(len(structure.syllables) - 1, -1, -1):
        syl = structure.syllables[i]
        if syl.weight in [SyllableWeight.HEAVY, SyllableWeight.SUPERHEAVY]:
            syl.is_stressed = True
            return structure
    
    # Si no hay pesada, penúltima
    if len(structure.syllables) >= 2:
        structure.syllables[-2].is_stressed = True
    elif len(structure.syllables) == 1:
        # Palabra monosilábica → lleva estrés
        structure.syllables[0].is_stressed = True
    
    return structure


def get_stressed_syllable(structure: SyllableStructure) -> Optional[Syllable]:
    """
    Retorna sílaba con estrés.
    
    Args:
        structure: Estructura silábica
    
    Returns:
        Syllable marcada como stressed, o None
    """
    return structure.get_stressed_syllable()


def predict_stress_position(structure: SyllableStructure) -> Optional[int]:
    """
    Predice índice de sílaba que debería llevar estrés.
    
    Args:
        structure: Estructura silábica
    
    Returns:
        Índice de sílaba (0-based), o None
    """
    if not structure.syllables:
        return None
    
    # Buscar última pesada
    for i in range(len(structure.syllables) - 1, -1, -1):
        syl = structure.syllables[i]
        if syl.weight in [SyllableWeight.HEAVY, SyllableWeight.SUPERHEAVY]:
            return i
    
    # Default: penúltima
    if len(structure.syllables) >= 2:
        return len(structure.syllables) - 2
    else:
        return 0


def has_stress_conditioned_contraction(structure: SyllableStructure) -> bool:
    """
    Detecta si contracción podría estar condicionada por estrés.
    
    Basado en evidencia diacrónica (MA, NA):
      Vocales ANTES de sílaba tónica → contraídas
      Vocales DESPUÉS de sílaba tónica → no contraídas
    
    Ya operativo en OA en grupo leʾāʾum (§ 3.5.2).
    
    Args:
        structure: Estructura silábica
    
    Returns:
        True si patrón sugiere condicionamiento por estrés
    """
    # Esto requeriría análisis más sofisticado
    # Por ahora, placeholder
    stressed_syl = get_stressed_syllable(structure)
    if not stressed_syl:
        return False
    
    # Verificar si hay vocales adyacentes antes/después de tónica
    # (Requiere análisis de fonemas completo)
    return False


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def get_stress_pattern(structure: SyllableStructure) -> str:
    """
    Retorna patrón de estrés tipo: σσ́σ (σ = sílaba átona, σ́ = tónica).
    
    Args:
        structure: Estructura silábica
    
    Returns:
        String con patrón
    """
    pattern = []
    for syl in structure.syllables:
        if syl.is_stressed:
            pattern.append('σ́')
        else:
            pattern.append('σ')
    return ''.join(pattern)


def is_ultima_stressed(structure: SyllableStructure) -> bool:
    """True si última sílaba lleva estrés."""
    if not structure.syllables:
        return False
    return structure.syllables[-1].is_stressed


def is_penult_stressed(structure: SyllableStructure) -> bool:
    """True si penúltima sílaba lleva estrés."""
    if len(structure.syllables) < 2:
        return False
    return structure.syllables[-2].is_stressed


def is_antepenult_stressed(structure: SyllableStructure) -> bool:
    """True si antepenúltima sílaba lleva estrés."""
    if len(structure.syllables) < 3:
        return False
    return structure.syllables[-3].is_stressed

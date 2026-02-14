"""
Tablas de decisión para reconstrucción de consonantes débiles en broken spellings.

Basado en análisis de § 3.3.1-3.3.3 de Kouwenberg (2017).
"""

from dataclasses import dataclass
from typing import Optional, Dict, Tuple

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phonology import Consonant, Vowel, get_consonant, VowelQuality
from phonology.weak_enums import (
    WeakPosition,
    EvidenceType,
    WeakVerbClass,
)


@dataclass
class ReconstructionDecision:
    """
    Decisión de reconstrucción para un broken spelling.
    
    Indica qué consonante débil reconstruir (si alguna) y con qué confianza.
    """
    consonant: Optional[Consonant]  # None si no reconstruir
    confidence: float  # 0.0-1.0
    reason: str
    evidence_type: EvidenceType
    alternative: Optional[Consonant] = None  # Interpretación alternativa
    alternative_confidence: float = 0.0


# ============================================================================
# TABLA DE DECISIÓN PRINCIPAL
# ============================================================================

# Clave: (vocal1_quality, vocal2_quality, posición, clase_verbal)
# Valor: ReconstructionDecision

BROKEN_SPELLING_DECISIONS: Dict[
    Tuple[str, str, Optional[WeakPosition], Optional[WeakVerbClass]],
    ReconstructionDecision
] = {
    
    # ========================================================================
    # VOCALES IDÉNTICAS → Probablemente ʾ
    # ========================================================================
    
    ('a', 'a', None, None): ReconstructionDecision(
        consonant=get_consonant('ʾ'),
        confidence=0.9,
        reason="ʾ typically preserved between identical vowels",
        evidence_type=EvidenceType.CONTEXTUAL,
    ),
    
    ('i', 'i', None, None): ReconstructionDecision(
        consonant=get_consonant('ʾ'),
        confidence=0.85,
        reason="ʾ likely between identical i vowels",
        evidence_type=EvidenceType.CONTEXTUAL,
    ),
    
    ('e', 'e', None, None): ReconstructionDecision(
        consonant=get_consonant('ʾ'),
        confidence=0.85,
        reason="ʾ likely between identical e vowels",
        evidence_type=EvidenceType.CONTEXTUAL,
    ),
    
    ('u', 'u', None, None): ReconstructionDecision(
        consonant=get_consonant('ʾ'),
        confidence=0.75,
        reason="ʾ possible between identical u vowels, but could be w",
        evidence_type=EvidenceType.CONTEXTUAL,
        alternative=get_consonant('w'),
        alternative_confidence=0.25,
    ),
    
    # ========================================================================
    # i-a → Probablemente y (contexto verbal)
    # ========================================================================
    
    ('i', 'a', WeakPosition.WORD_FINAL, WeakVerbClass.III_Y): ReconstructionDecision(
        consonant=get_consonant('y'),
        confidence=0.95,
        reason="III-y verbs have y before final -a",
        evidence_type=EvidenceType.MORPHOLOGICAL,
    ),
    
    ('i', 'a', WeakPosition.WORD_FINAL, WeakVerbClass.III_I_LONG): ReconstructionDecision(
        consonant=get_consonant('y'),
        confidence=0.9,
        reason="III-ī verbs often have y in some forms",
        evidence_type=EvidenceType.MORPHOLOGICAL,
    ),
    
    # i-a post-consonántico sin info morfológica
    ('i', 'a', WeakPosition.POST_CONSONANTAL, None): ReconstructionDecision(
        consonant=get_consonant('y'),
        confidence=0.7,
        reason="Post-consonantal i-a often represents y",
        evidence_type=EvidenceType.CONTEXTUAL,
        alternative=get_consonant('ʾ'),
        alternative_confidence=0.3,
    ),
    
    # ========================================================================
    # u-a → Probablemente w
    # ========================================================================
    
    ('u', 'a', None, WeakVerbClass.III_U_LONG): ReconstructionDecision(
        consonant=get_consonant('w'),
        confidence=0.85,
        reason="III-ū verbs may have w in some contexts",
        evidence_type=EvidenceType.MORPHOLOGICAL,
    ),
    
    ('u', 'a', WeakPosition.POST_CONSONANTAL, None): ReconstructionDecision(
        consonant=get_consonant('w'),
        confidence=0.7,
        reason="u-a after consonant may be w, but can contract to ū",
        evidence_type=EvidenceType.CONTEXTUAL,
        alternative=None,  # Podría ser simple secuencia sin w
        alternative_confidence=0.3,
    ),
    
    # ========================================================================
    # e-a → Probablemente ʾ (de *ʾ o *ʿ)
    # ========================================================================
    
    ('e', 'a', None, None): ReconstructionDecision(
        consonant=get_consonant('ʾ'),
        confidence=0.85,
        reason="e from *a/i by guttural, likely has ʾ",
        evidence_type=EvidenceType.ETYMOLOGICAL,
    ),
    
    # ========================================================================
    # a-i → Ambiguo
    # ========================================================================
    
    ('a', 'i', None, None): ReconstructionDecision(
        consonant=get_consonant('ʾ'),
        confidence=0.6,
        reason="Could be ʾ, but ambiguous",
        evidence_type=EvidenceType.CONTEXTUAL,
        alternative=get_consonant('y'),
        alternative_confidence=0.4,
    ),
    
    # ========================================================================
    # a-e → Probablemente ʾ
    # ========================================================================
    
    ('a', 'e', None, None): ReconstructionDecision(
        consonant=get_consonant('ʾ'),
        confidence=0.8,
        reason="ʾ affects adjacent vowels, a_e suggests ʾ",
        evidence_type=EvidenceType.CONTEXTUAL,
    ),
    
    # ========================================================================
    # i-e / e-i → Probablemente y o ʾ
    # ========================================================================
    
    ('i', 'e', None, None): ReconstructionDecision(
        consonant=get_consonant('y'),
        confidence=0.65,
        reason="i-e may represent y glide",
        evidence_type=EvidenceType.CONTEXTUAL,
        alternative=get_consonant('ʾ'),
        alternative_confidence=0.35,
    ),
    
    # ========================================================================
    # Verbos específicos
    # ========================================================================
    
    # Verbos II/aleph
    ('a', 'a', None, WeakVerbClass.II_ALEPH): ReconstructionDecision(
        consonant=get_consonant('ʾ'),
        confidence=0.98,
        reason="Verb classified as II/aleph",
        evidence_type=EvidenceType.MORPHOLOGICAL,
    ),
    
    # Verbos III/aleph
    ('a', 'a', WeakPosition.WORD_FINAL, WeakVerbClass.III_ALEPH): ReconstructionDecision(
        consonant=get_consonant('ʾ'),
        confidence=0.98,
        reason="Verb classified as III/aleph",
        evidence_type=EvidenceType.MORPHOLOGICAL,
    ),
    
}


# ============================================================================
# FUNCIONES DE BÚSQUEDA EN TABLA
# ============================================================================

def lookup_decision(
    vowel1_quality: str,
    vowel2_quality: str,
    position: Optional[WeakPosition] = None,
    verb_class: Optional[WeakVerbClass] = None,
) -> Optional[ReconstructionDecision]:
    """
    Busca decisión de reconstrucción en la tabla.
    
    Implementa búsqueda jerárquica: primero intenta con toda la info,
    luego va generalizando.
    
    Args:
        vowel1_quality: Cualidad de primera vocal ('a', 'e', 'i', 'u')
        vowel2_quality: Cualidad de segunda vocal
        position: Posición de la débil (opcional)
        verb_class: Clase de verbo (opcional)
    
    Returns:
        ReconstructionDecision si se encuentra, None si no
    """
    # Nivel 1: Búsqueda con toda la información
    key = (vowel1_quality, vowel2_quality, position, verb_class)
    if key in BROKEN_SPELLING_DECISIONS:
        return BROKEN_SPELLING_DECISIONS[key]
    
    # Nivel 2: Sin posición específica
    key = (vowel1_quality, vowel2_quality, None, verb_class)
    if key in BROKEN_SPELLING_DECISIONS:
        return BROKEN_SPELLING_DECISIONS[key]
    
    # Nivel 3: Sin clase verbal
    key = (vowel1_quality, vowel2_quality, position, None)
    if key in BROKEN_SPELLING_DECISIONS:
        return BROKEN_SPELLING_DECISIONS[key]
    
    # Nivel 4: Solo vocales
    key = (vowel1_quality, vowel2_quality, None, None)
    if key in BROKEN_SPELLING_DECISIONS:
        return BROKEN_SPELLING_DECISIONS[key]
    
    # No se encontró decisión
    return None


def get_default_decision(
    vowel1: Vowel,
    vowel2: Vowel,
) -> ReconstructionDecision:
    """
    Retorna decisión por defecto cuando no hay regla específica.
    
    Default: No reconstruir débil, asumir glide predecible.
    """
    return ReconstructionDecision(
        consonant=None,
        confidence=0.5,
        reason=f"No specific rule for {vowel1.quality.value}-{vowel2.quality.value}, assuming predictable glide",
        evidence_type=EvidenceType.CONTEXTUAL,
    )


# ============================================================================
# CASOS ESPECIALES
# ============================================================================

SPECIAL_CASES = {
    # Palabras específicas con comportamiento conocido
    "ša-a-lum": ReconstructionDecision(
        consonant=get_consonant('ʾ'),
        confidence=1.0,
        reason="šaʾālum 'to ask' is well-documented II/aleph verb",
        evidence_type=EvidenceType.ETYMOLOGICAL,
    ),
    
    "be-a-lum": ReconstructionDecision(
        consonant=get_consonant('ʾ'),
        confidence=1.0,
        reason="beʾālum 'to possess' < *baʿālum",
        evidence_type=EvidenceType.ETYMOLOGICAL,
    ),
    
    "i-tù-ar": ReconstructionDecision(
        consonant=None,  # Kouwenberg: sin w
        confidence=0.8,
        reason="Kouwenberg transcribes without w when not written",
        evidence_type=EvidenceType.SPELLING_VARIANT,
    ),
    
    "i-tù-wa-ar": ReconstructionDecision(
        consonant=get_consonant('w'),
        confidence=1.0,
        reason="w explicitly written",
        evidence_type=EvidenceType.SPELLING_VARIANT,
    ),
}


def lookup_special_case(oracc_spelling: str) -> Optional[ReconstructionDecision]:
    """
    Busca casos especiales documentados.
    
    Args:
        oracc_spelling: Spelling ORACC exacto
    
    Returns:
        ReconstructionDecision si es caso especial, None si no
    """
    return SPECIAL_CASES.get(oracc_spelling)


# ============================================================================
# ESTADÍSTICAS DE LA TABLA
# ============================================================================

def get_table_statistics() -> dict:
    """Retorna estadísticas sobre la tabla de decisión."""
    total_entries = len(BROKEN_SPELLING_DECISIONS)
    
    by_consonant = {
        'ʾ': 0,
        'w': 0,
        'y': 0,
        None: 0,
    }
    
    by_evidence = {et: 0 for et in EvidenceType}
    
    high_confidence = 0  # >= 0.9
    medium_confidence = 0  # 0.7-0.89
    low_confidence = 0  # < 0.7
    
    for decision in BROKEN_SPELLING_DECISIONS.values():
        # Por consonante
        symbol = decision.consonant.symbol if decision.consonant else None
        by_consonant[symbol] = by_consonant.get(symbol, 0) + 1
        
        # Por tipo de evidencia
        by_evidence[decision.evidence_type] += 1
        
        # Por confianza
        if decision.confidence >= 0.9:
            high_confidence += 1
        elif decision.confidence >= 0.7:
            medium_confidence += 1
        else:
            low_confidence += 1
    
    return {
        'total_entries': total_entries,
        'by_consonant': by_consonant,
        'by_evidence': {et.value: count for et, count in by_evidence.items()},
        'confidence_distribution': {
            'high (≥0.9)': high_confidence,
            'medium (0.7-0.89)': medium_confidence,
            'low (<0.7)': low_confidence,
        },
        'special_cases': len(SPECIAL_CASES),
    }

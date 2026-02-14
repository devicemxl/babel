"""
Módulo de procesos vocálicos del Old Assyrian.

Basado en Kouwenberg (2017) § 3.4.
"""

from .enums import (
    VowelRuleType,
    VowelChangeDirection,
    ConditioningPosition,
    AlternationType,
    VowelAssimilationType,
    ContractionType,
    VowelMorphologicalContext,
    RuleObligatoriness,
    VowelEvidenceLevel,
)

__all__ = [
    # Enums
    'VowelRuleType',
    'VowelChangeDirection',
    'ConditioningPosition',
    'AlternationType',
    'VowelAssimilationType',
    'ContractionType',
    'VowelMorphologicalContext',
    'RuleObligatoriness',
    'VowelEvidenceLevel',
]

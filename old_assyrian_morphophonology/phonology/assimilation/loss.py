"""
Reglas de pérdida consonántica del Old Assyrian.

Basado en extracción de Kouwenberg (2017).
Requiere análisis silábico (Iteración 5).
"""

from dataclasses import dataclass, field
from typing import Optional, List, Callable, Tuple
from .. import Consonant, get_consonant
from .enums import (
    AssimilationDirection,
    AssimilationType,
    AssimilationStatus,
    EvidenceLevel,
)


@dataclass
class ConsonantLossExample:
    """Ejemplo de pérdida consonántica."""
    underlying: str
    surface: str
    gloss: str
    reference: Optional[str] = None
    section: str = ""


@dataclass
class ConsonantLossRule:
    """
    Regla de pérdida consonántica.
    
    Define cuándo una consonante se pierde (→ ∅).
    """
    name: str
    code: str
    description: str
    
    # Consonante que se pierde
    target_consonant: str
    
    # Contexto de pérdida
    syllable_position: str  # 'syllable_final', 'word_final', etc.
    
    # Condiciones
    condition: Callable[[Consonant, dict], bool]
    
    # Aplicación
    status: AssimilationStatus
    evidence_level: EvidenceLevel
    
    # Documentación
    source_section: str = ""
    examples: List[ConsonantLossExample] = field(default_factory=list)
    notes: str = ""
    
    def applies(self, consonant: Consonant, context: dict) -> bool:
        """Verifica si regla aplica."""
        if consonant.symbol != self.target_consonant:
            return False
        return self.condition(consonant, context)
    
    def apply(self, consonant: Consonant) -> Optional[Consonant]:
        """Aplica pérdida → retorna None (consonante eliminada)."""
        return None


# ============================================================================
# CONDICIONES DE PÉRDIDA
# ============================================================================

def condition_r_syllable_final(consonant: Consonant, context: dict) -> bool:
    """
    r → ∅ / _C (final de sílaba).
    
    Requiere:
      - r en coda de sílaba
      - Seguida por consonante
      - Contexto esporádico
    
    Args:
        consonant: Consonante r
        context: Debe incluir:
                   - 'is_syllable_final': bool
                   - 'followed_by_consonant': bool
    
    Returns:
        True si debe perderse
    """
    return (
        consonant.symbol == 'r' and
        context.get('is_syllable_final', False) and
        context.get('followed_by_consonant', False)
    )


def condition_s_syllable_final(consonant: Consonant, context: dict) -> bool:
    """
    s → ∅ / _C (final de sílaba).
    
    Similar a r pero aún más raro.
    
    Args:
        consonant: Consonante s
        context: Contexto silábico
    
    Returns:
        True si debe perderse
    """
    return (
        consonant.symbol == 's' and
        context.get('is_syllable_final', False) and
        context.get('followed_by_consonant', False)
    )


def condition_m_word_final_grammatical(consonant: Consonant, context: dict) -> bool:
    """
    -m# → ∅ / [+grammatical] (final de palabra).
    
    Solo m GRAMATICAL (mimación, ventivo).
    m de raíz NO se pierde.
    
    Args:
        consonant: Consonante m
        context: Debe incluir:
                   - 'is_word_final': bool
                   - 'is_grammatical': bool
    
    Returns:
        True si debe perderse
    """
    return (
        consonant.symbol == 'm' and
        context.get('is_word_final', False) and
        context.get('is_grammatical', False)  # Solo gramatical
    )


def condition_n_word_final_grammatical(consonant: Consonant, context: dict) -> bool:
    """
    -n# → ∅ / [+grammatical] (final de palabra).
    
    Similar a -m#.
    
    Args:
        consonant: Consonante n
        context: Contexto morfológico
    
    Returns:
        True si debe perderse
    """
    return (
        consonant.symbol == 'n' and
        context.get('is_word_final', False) and
        context.get('is_grammatical', False)  # Solo gramatical
    )


# ============================================================================
# REGLAS DE PÉRDIDA CONSONÁNTICA
# ============================================================================

PER_3_R_LOSS_SYLLABLE_FINAL = ConsonantLossRule(
    name="R_LOSS_SYLLABLE_FINAL",
    code="PER-3",
    description="r → ∅ / _C (final de sílaba, esporádico)",
    target_consonant='r',
    syllable_position='syllable_final',
    condition=condition_r_syllable_final,
    status=AssimilationStatus.SPORADIC,
    evidence_level=EvidenceLevel.EXPLICIT,
    source_section="Extracción Iter 3",
    examples=[
        ConsonantLossExample(
            "*warke", "wake", "(algún) después",
            section="Extracción Iter 3"
        ),
    ],
    notes=(
        "ESPORÁDICO. r en coda silábica antes de consonante puede perderse. "
        "Ejemplo: warke → wake. "
        "Requiere análisis silábico para determinar 'final de sílaba'."
    )
)

PER_4_S_LOSS_SYLLABLE_FINAL = ConsonantLossRule(
    name="S_LOSS_SYLLABLE_FINAL",
    code="PER-4",
    description="s → ∅ / _C (final de sílaba, esporádico)",
    target_consonant='s',
    syllable_position='syllable_final',
    condition=condition_s_syllable_final,
    status=AssimilationStatus.SPORADIC,
    evidence_level=EvidenceLevel.COMPARATIVE,
    source_section="Extracción Iter 3",
    examples=[
        ConsonantLossExample(
            "*ištānakkan", "itānakkan", "sigue colocando",
            section="Extracción Iter 3"
        ),
    ],
    notes=(
        "ESPORÁDICO. s en coda silábica antes de consonante puede perderse. "
        "Ejemplo: ištānakkan → itānakkan. "
        "Más raro que pérdida de r."
    )
)

PER_1_M_LOSS_WORD_FINAL = ConsonantLossRule(
    name="M_LOSS_WORD_FINAL_GRAMMATICAL",
    code="PER-1",
    description="-m# → ∅ / [+grammatical] (mimación/ventivo)",
    target_consonant='m',
    syllable_position='word_final',
    condition=condition_m_word_final_grammatical,
    status=AssimilationStatus.OPTIONAL,
    evidence_level=EvidenceLevel.EXPLICIT,
    source_section="Extracción Iter 3",
    examples=[
        ConsonantLossExample(
            "ba-am", "ba", "verdaderamente",
            section="Extracción Iter 3"
        ),
    ],
    notes=(
        "OPCIONAL. -m gramatical (mimación, ventivo) puede perderse final de palabra. "
        "m DE RAÍZ NO se pierde. "
        "Requiere análisis morfológico para distinguir."
    )
)

PER_2_N_LOSS_WORD_FINAL = ConsonantLossRule(
    name="N_LOSS_WORD_FINAL_GRAMMATICAL",
    code="PER-2",
    description="-n# → ∅ / [+grammatical]",
    target_consonant='n',
    syllable_position='word_final',
    condition=condition_n_word_final_grammatical,
    status=AssimilationStatus.OPTIONAL,
    evidence_level=EvidenceLevel.COMPARATIVE,
    source_section="Extracción Iter 3",
    examples=[
        ConsonantLossExample(
            "ištēn", "ištē", "uno",
            section="Extracción Iter 3"
        ),
    ],
    notes=(
        "OPCIONAL. Similar a -m#. "
        "-n gramatical puede perderse final de palabra."
    )
)


# ============================================================================
# TODAS LAS REGLAS DE PÉRDIDA
# ============================================================================

ALL_LOSS_RULES = [
    PER_3_R_LOSS_SYLLABLE_FINAL,
    PER_4_S_LOSS_SYLLABLE_FINAL,
    PER_1_M_LOSS_WORD_FINAL,
    PER_2_N_LOSS_WORD_FINAL,
]


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def can_consonant_be_lost(
    consonant: Consonant,
    syllable_context: dict,
    morphological_context: dict
) -> bool:
    """
    Determina si consonante puede perderse.
    
    Args:
        consonant: Consonante a verificar
        syllable_context: Contexto silábico (posición, etc.)
        morphological_context: Contexto morfológico (gramatical vs. raíz)
    
    Returns:
        True si alguna regla de pérdida aplica
    """
    # Combinar contextos
    context = {**syllable_context, **morphological_context}
    
    for rule in ALL_LOSS_RULES:
        if rule.applies(consonant, context):
            return True
    
    return False


def apply_consonant_loss(
    consonant: Consonant,
    context: dict
) -> Optional[Consonant]:
    """
    Aplica pérdida consonántica si corresponde.
    
    Args:
        consonant: Consonante
        context: Contexto completo
    
    Returns:
        None si consonante se pierde, consonante original si no
    """
    for rule in ALL_LOSS_RULES:
        if rule.applies(consonant, context):
            return rule.apply(consonant)  # None
    
    return consonant  # Sin cambio


def get_applicable_loss_rules(
    consonant: Consonant,
    context: dict
) -> List[ConsonantLossRule]:
    """
    Retorna reglas de pérdida aplicables.
    
    Args:
        consonant: Consonante
        context: Contexto
    
    Returns:
        Lista de reglas aplicables
    """
    applicable = []
    for rule in ALL_LOSS_RULES:
        if rule.applies(consonant, context):
            applicable.append(rule)
    
    return applicable


# ============================================================================
# INTEGRACIÓN CON ESTRUCTURA SILÁBICA (Iter 5)
# ============================================================================

def create_syllable_context_for_loss(
    consonant: Consonant,
    syllable_structure  # De Iter 5
) -> dict:
    """
    Crea contexto silábico para reglas de pérdida.
    
    Usa SyllableStructure de Iteración 5 para determinar
    si consonante está en final de sílaba.
    
    Args:
        consonant: Consonante a analizar
        syllable_structure: SyllableStructure de Iter 5
    
    Returns:
        Diccionario con contexto silábico
    """
    context = {
        'is_syllable_final': False,
        'is_word_final': False,
        'followed_by_consonant': False,
    }
    
    # Buscar consonante en estructura
    for i, syl in enumerate(syllable_structure.syllables):
        # Verificar si está en coda
        if syl.coda and any(c.symbol == consonant.symbol for c in syl.coda):
            context['is_syllable_final'] = True
            
            # Verificar si es última sílaba
            if i == len(syllable_structure.syllables) - 1:
                context['is_word_final'] = True
            
            # Verificar si seguida por consonante
            if i + 1 < len(syllable_structure.syllables):
                next_syl = syllable_structure.syllables[i + 1]
                if next_syl.onset:
                    context['followed_by_consonant'] = True
    
    return context


# ============================================================================
# NOTAS DE IMPLEMENTACIÓN
# ============================================================================

LOSS_RULES_NOTES = {
    'general': (
        "Reglas de pérdida consonántica del OA. "
        "PER-3 y PER-4 requieren análisis silábico (Iter 5). "
        "PER-1 y PER-2 requieren análisis morfológico (Iter 6+)."
    ),
    
    'syllable_final': (
        "r y s pueden perderse en posición final de sílaba antes de consonante. "
        "ESPORÁDICO, no sistemático. "
        "Ejemplos: warke → wake, ištānakkan → itānakkan"
    ),
    
    'word_final_grammatical': (
        "-m y -n GRAMATICALES pueden perderse final de palabra. "
        "m/n DE RAÍZ NO se pierden. "
        "Requiere distinción morfológica. "
        "Ejemplos: ba-am → ba, ištēn → ištē"
    ),
    
    'implementation': (
        "PER-3 y PER-4: IMPLEMENTADAS (requieren Iter 5). "
        "PER-1 y PER-2: ESQUELETO (requieren Iter 6 para detección morfológica)."
    ),
}

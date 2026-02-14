"""
Reglas de epéntesis vocálica del Old Assyrian.

Basado en Kouwenberg (2017) § 3.2.2.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Callable, Tuple
from .. import Phoneme, Consonant, Vowel, get_vowel
from .enums import EpenthesisContext, EpentheticVowel, ClusterType


@dataclass
class EpenthesisExample:
    """Ejemplo de epéntesis documentado."""
    underlying: str
    surface: str
    gloss: str
    spelling: Optional[str] = None  # ORACC spelling
    reference: Optional[str] = None
    section: str = ""


@dataclass
class EpenthesisRule:
    """
    Regla de epéntesis vocálica.
    
    Define cuándo y dónde insertar vocal para romper cluster.
    """
    name: str
    code: str
    description: str
    
    # Cluster que dispara
    cluster_type: ClusterType
    
    # Vocal insertada
    epenthetic_vowel: EpentheticVowel
    
    # Posición de inserción
    position: str  # 'between', 'after', 'before'
    
    # Contexto
    context: EpenthesisContext
    
    # Condiciones
    condition: Callable[[List[Consonant]], bool]
    
    # Aplicación
    frequency: str  # 'common', 'rare', 'sporadic'
    
    # Documentación
    source_section: str = ""
    examples: List[EpenthesisExample] = field(default_factory=list)
    notes: str = ""
    
    def applies(self, cluster: List[Consonant]) -> bool:
        """Verifica si regla aplica a este cluster."""
        return self.condition(cluster)
    
    def get_epenthetic_vowel_phoneme(self) -> Vowel:
        """Retorna fonema de vocal epentética."""
        vowel_map = {
            EpentheticVowel.I: 'i',
            EpentheticVowel.U: 'u',
            EpentheticVowel.E: 'e',
            EpentheticVowel.A: 'a',
        }
        symbol = vowel_map[self.epenthetic_vowel]
        return get_vowel(symbol, length='short')


# ============================================================================
# CONDICIONES DE EPÉNTESIS
# ============================================================================

def condition_liquid_r_plus_c(cluster: List[Consonant]) -> bool:
    """r + C → epenthesis (más frecuente)."""
    return (
        len(cluster) >= 2 and
        cluster[0].symbol == 'r'
    )


def condition_liquid_l_plus_c(cluster: List[Consonant]) -> bool:
    """l + C → epenthesis."""
    return (
        len(cluster) >= 2 and
        cluster[0].symbol == 'l'
    )


def condition_c_plus_n(cluster: List[Consonant]) -> bool:
    """C + n → epenthesis (raro, algunos contextos)."""
    return (
        len(cluster) >= 2 and
        cluster[1].symbol == 'n'
    )


def condition_c_plus_m(cluster: List[Consonant]) -> bool:
    """C + m → epenthesis (muy raro)."""
    return (
        len(cluster) >= 2 and
        cluster[1].symbol == 'm'
    )


def condition_h_plus_c(cluster: List[Consonant]) -> bool:
    """h + C → epenthesis."""
    return (
        len(cluster) >= 2 and
        cluster[0].symbol == 'h'
    )


# ============================================================================
# REGLAS DE EPÉNTESIS
# ============================================================================

EP_1_LIQUID_R = EpenthesisRule(
    name="EPENTHESIS_R_PLUS_C",
    code="EP-1",
    description="r + C → reC (vocal e, más frecuente)",
    cluster_type=ClusterType.LIQUID_C,
    epenthetic_vowel=EpentheticVowel.E,
    position='between',
    context=EpenthesisContext.CLUSTER_RESOLUTION,
    condition=condition_liquid_r_plus_c,
    frequency='common',
    source_section="§ 3.2.2.1 (3)",
    examples=[
        EpenthesisExample(
            "*kabrū", "kāberu", "están gordos",
            section="§ 3.2.2.1"
        ),
        EpenthesisExample(
            "*puzrum", "puzurem", "refugio",
            spelling="pu-zú-re-em",
            section="§ 3.2.2.1"
        ),
        EpenthesisExample(
            "*šikrum", "šikerem", "cerveza",
            spelling="ší-ke-re-em",
            reference="a/k 478b: 31",
            section="§ 3.2.2.1"
        ),
    ],
    notes="MÁS FRECUENTE. Previene síncope vocálica. e < i / _r (§ 3.4.5.2)"
)

EP_2_LIQUID_L = EpenthesisRule(
    name="EPENTHESIS_L_PLUS_C",
    code="EP-2",
    description="l + C → liC (vocal i/u)",
    cluster_type=ClusterType.LIQUID_C,
    epenthetic_vowel=EpentheticVowel.U,  # Más común u
    position='between',
    context=EpenthesisContext.CLUSTER_RESOLUTION,
    condition=condition_liquid_l_plus_c,
    frequency='common',
    source_section="§ 3.2.2.1 (2)",
    examples=[
        EpenthesisExample(
            "*šuqlum", "šuqulum", "paquete",
            spelling="šu-qú-lu-um",
            reference="TC 3, 81: 19",
            section="§ 3.2.2.1"
        ),
        EpenthesisExample(
            "*lublūnem", "lubulūnem", "que traigan",
            spelling="lu-bu-lu-nem",
            reference="TC 2, 25: 21",
            section="§ 3.2.2.1"
        ),
    ],
    notes="Típicamente vocal u insertada."
)

EP_3_H_PLUS_C = EpenthesisRule(
    name="EPENTHESIS_H_PLUS_C",
    code="EP-3",
    description="h + C → hiC (vocal i, común en verbos)",
    cluster_type=ClusterType.H_C,
    epenthetic_vowel=EpentheticVowel.I,
    position='between',
    context=EpenthesisContext.CLUSTER_RESOLUTION,
    condition=condition_h_plus_c,
    frequency='common',
    source_section="§ 3.2.2.3",
    examples=[
        EpenthesisExample(
            "*ihdā", "ihidā", "¡tengan cuidado!",
            spelling="i-hi-da(-ma)",
            reference="Prag I 709: 32+",
            section="§ 3.2.2.3"
        ),
        EpenthesisExample(
            "*iḫliqu", "iḫiliqu", "se perdieron",
            spelling="i-hi-li-qu(-ma)",
            reference="AKT 3, 33: 1",
            section="§ 3.2.2.3"
        ),
        EpenthesisExample(
            "*miḫram", "miḫiram", "copia, lista",
            spelling="mi-hi-ra-am",
            reference="BIN 6, 98: 4",
            section="§ 3.2.2.3"
        ),
    ],
    notes="Común en formas verbales. Puede ser ortográfico (HI para /iḫ/)."
)

EP_4_IMPERATIVE = EpenthesisRule(
    name="EPENTHESIS_IMPERATIVE",
    code="EP-4",
    description="Imperativos con terminación → CuCVnam",
    cluster_type=ClusterType.HETEROGENEOUS,
    epenthetic_vowel=EpentheticVowel.U,
    position='between',
    context=EpenthesisContext.IMPERATIVE,
    condition=lambda c: True,  # Específico a imperativo
    frequency='common',
    source_section="§ 3.2.2.2",
    examples=[
        EpenthesisExample(
            "*šuknam", "šukunam", "¡coloca para mí!",
            spelling="šu-ku-nam",
            reference="TC 3, 1: 29",
            section="§ 3.2.2.2"
        ),
        EpenthesisExample(
            "*kunkī(ma)", "kunukī(ma)", "¡sella! (Fem)",
            spelling="ku-nu-ki(-ma)",
            reference="BIN 6, 20: 31",
            section="§ 3.2.2.2"
        ),
    ],
    notes="Caso especial. Puede ser analógico no puramente fonológico."
)


# ============================================================================
# TODAS LAS REGLAS
# ============================================================================

ALL_EPENTHESIS_RULES = [
    EP_1_LIQUID_R,
    EP_2_LIQUID_L,
    EP_3_H_PLUS_C,
    EP_4_IMPERATIVE,
]


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def needs_epenthesis(cluster: List[Consonant]) -> bool:
    """
    Determina si cluster necesita epéntesis.
    
    Args:
        cluster: Lista de consonantes en cluster
    
    Returns:
        True si alguna regla aplica
    """
    for rule in ALL_EPENTHESIS_RULES:
        if rule.applies(cluster):
            return True
    return False


def apply_epenthesis(
    cluster: List[Consonant],
    context: Optional[EpenthesisContext] = None
) -> List[Phoneme]:
    """
    Aplica epéntesis a cluster.
    
    Args:
        cluster: Cluster consonántico
        context: Contexto opcional (ej: IMPERATIVE)
    
    Returns:
        Lista de fonemas con vocal epentética insertada
    """
    # Buscar regla apropiada
    applicable_rules = [r for r in ALL_EPENTHESIS_RULES if r.applies(cluster)]
    
    if not applicable_rules:
        # No epéntesis, retornar cluster original
        return cluster
    
    # Filtrar por contexto si proporcionado
    if context:
        context_rules = [r for r in applicable_rules if r.context == context]
        if context_rules:
            applicable_rules = context_rules
    
    # Usar primera regla aplicable
    rule = applicable_rules[0]
    
    # Obtener vocal epentética
    epenthetic_v = rule.get_epenthetic_vowel_phoneme()
    
    # Insertar según posición
    if rule.position == 'between':
        # Entre consonantes
        if len(cluster) >= 2:
            return [cluster[0], epenthetic_v] + cluster[1:]
        else:
            return cluster
    elif rule.position == 'after':
        # Después de cluster
        return cluster + [epenthetic_v]
    elif rule.position == 'before':
        # Antes de cluster
        return [epenthetic_v] + cluster
    
    return cluster

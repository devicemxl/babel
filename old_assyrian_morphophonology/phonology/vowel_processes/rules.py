"""
Reglas vocálicas del Old Assyrian - VERSIÓN COMPACTA.

Implementa reglas de § 3.4 de Kouwenberg (2017).
Debido a limitaciones de espacio, esta es una implementación condensada.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Callable, Tuple
from ...phonology import Vowel, get_vowel
from .enums import *
from .context import VowelContext


@dataclass
class VowelExample:
    """Ejemplo de regla vocálica."""
    underlying: str
    surface: str
    gloss: str
    reference: Optional[str] = None
    section: str = ""


@dataclass
class VowelRule:
    """
    Regla base para cambios vocálicos.
    
    Sistema modular para alternancias, asimilación, contracción, etc.
    """
    name: str
    code: str
    description: str
    rule_type: VowelRuleType
    
    # Condiciones
    condition: Callable[[VowelContext], bool]
    transformation: Callable[[Vowel], Vowel]
    
    # Metadata
    obligatoriness: RuleObligatoriness = RuleObligatoriness.OBLIGATORY
    evidence_level: VowelEvidenceLevel = VowelEvidenceLevel.EXPLICIT
    source_section: str = ""
    examples: List[VowelExample] = field(default_factory=list)
    notes: str = ""
    
    def applies(self, context: VowelContext) -> bool:
        """Verifica si regla aplica en este contexto."""
        return self.condition(context)
    
    def apply(self, vowel: Vowel) -> Vowel:
        """Aplica transformación a vocal."""
        return self.transformation(vowel)


# ============================================================================
# REGLAS DE ALTERNANCIA: a → e
# ============================================================================

def condition_a_to_e_before_r(ctx: VowelContext) -> bool:
    """a → e / _r"""
    return (
        ctx.vowel.quality.value == 'a' and
        ctx.vowel.length.value == 'short' and
        ctx.following_consonant and
        ctx.following_consonant.symbol == 'r'
    )

def transform_a_to_e(vowel: Vowel) -> Vowel:
    """Transforma a → e."""
    return get_vowel('e', length='short')

VA_1_A_TO_E_BEFORE_R = VowelRule(
    name="A_TO_E_BEFORE_R",
    code="VA-1",
    description="a → e / _r (inconsistente)",
    rule_type=VowelRuleType.CONDITIONING,
    condition=condition_a_to_e_before_r,
    transformation=transform_a_to_e,
    obligatoriness=RuleObligatoriness.INCONSISTENT,
    source_section="§ 3.4.5.1",
    examples=[
        VowelExample("*šarrum", "šerrum", "niño", section="§ 3.4.5.1"),
        VowelExample("*qarbum", "qerbum", "interior", section="§ 3.4.5.1"),
        VowelExample("*wardum", "werdum/erdum", "esclavo", section="§ 3.4.5.1"),
    ],
    notes="Formas con a y e coexisten. Más común en sustantivos/adjetivos."
)


def condition_a_to_e_before_guttural(ctx: VowelContext) -> bool:
    """a → e cerca de gutural"""
    return (
        ctx.vowel.quality.value == 'a' and
        ctx.vowel.length.value == 'short' and
        ctx.has_guttural()
    )

VA_2_A_TO_E_GUTTURAL = VowelRule(
    name="A_TO_E_NEAR_GUTTURAL",
    code="VA-2",
    description="a → e por influencia gutural (esporádico)",
    rule_type=VowelRuleType.CONDITIONING,
    condition=condition_a_to_e_before_guttural,
    transformation=transform_a_to_e,
    obligatoriness=RuleObligatoriness.SPORADIC,
    source_section="§ 3.4.4.1",
    examples=[
        VowelExample("*rabʾum", "rebitum", "cuarto (Fem)", section="§ 3.4.4.1"),
        VowelExample("lamuttum", "lemuttum", "mal", section="§ 3.4.4.1"),
    ],
    notes="Sin patrón claro. Esporádico."
)


# ============================================================================
# REGLAS DE ALTERNANCIA: i → e
# ============================================================================

def condition_i_to_e_before_r(ctx: VowelContext) -> bool:
    """i → e / _r"""
    return (
        ctx.vowel.quality.value == 'i' and
        ctx.vowel.length.value == 'short' and
        ctx.following_consonant and
        ctx.following_consonant.symbol == 'r'
    )

def transform_i_to_e(vowel: Vowel) -> Vowel:
    """Transforma i → e."""
    return get_vowel('e', length='short')

VA_3_I_TO_E_BEFORE_R = VowelRule(
    name="I_TO_E_BEFORE_R",
    code="VA-3",
    description="i → e / _r",
    rule_type=VowelRuleType.CONDITIONING,
    condition=condition_i_to_e_before_r,
    transformation=transform_i_to_e,
    obligatoriness=RuleObligatoriness.INCONSISTENT,
    source_section="§ 3.4.5.2",
    examples=[
        VowelExample("*tuārum", "tùta-e-ram", "devolviste a mí", section="§ 3.4.5.2"),
        VowelExample("*ukāilu", "ú-kà-i-lu", "sostuvo", section="§ 3.4.5.2"),
    ],
    notes="Visible en verbos II/débil. i antes de r menos frecuente que e."
)


def condition_i_to_e_before_m_grammatical(ctx: VowelContext) -> bool:
    """i → e / _m# (morfema gramatical)"""
    return (
        ctx.vowel.quality.value == 'i' and
        ctx.vowel.length.value == 'short' and
        ctx.is_word_final and
        ctx.following_consonant and
        ctx.following_consonant.symbol == 'm' and
        ctx.is_in_grammatical_morpheme
    )

VA_4_I_TO_E_BEFORE_M_GRAM = VowelRule(
    name="I_TO_E_BEFORE_M_GRAMMATICAL",
    code="VA-4",
    description="i → e / _m# (morfema gramatical)",
    rule_type=VowelRuleType.CONDITIONING,
    condition=condition_i_to_e_before_m_grammatical,
    transformation=transform_i_to_e,
    obligatoriness=RuleObligatoriness.OBLIGATORY,
    source_section="§ 3.4.5.3",
    examples=[
        VowelExample("*waṣāʾim", "wa-ṣā-e(-ma)", "para dejar", section="§ 3.4.5.3"),
        VowelExample("*rādīem", "ra-di-e-em", "para escolta", section="§ 3.4.5.3"),
    ],
    notes="Solo afecta m de morfema gramatical (Gen -im, ventivo -nim, etc.)"
)


# ============================================================================
# REGLA DE ASIMILACIÓN VOCÁLICA ASIRIA
# ============================================================================

def condition_assyrian_vowel_assimilation(ctx: VowelContext) -> bool:
    """
    Asimilación vocálica asiria: penúltima a → vocal final.
    
    Regla distintiva del asirio.
    """
    return ctx.requires_assimilation()

def transform_assimilate_to_final(vowel: Vowel, final_vowel: Vowel) -> Vowel:
    """Asimila vocal penúltima a vocal final."""
    return get_vowel(final_vowel.quality.value, length='short')

@dataclass  
class VowelAssimilationRule(VowelRule):
    """Regla especializada para asimilación vocálica."""
    target_vowel_getter: Optional[Callable[[VowelContext], Vowel]] = None
    
    def apply_with_context(self, context: VowelContext) -> Vowel:
        """Aplica asimilación usando contexto completo."""
        if not self.target_vowel_getter or not context.following_vowel:
            return context.vowel
        
        target = self.target_vowel_getter(context)
        return transform_assimilate_to_final(context.vowel, target)

VAS_1_ASSYRIAN_ASSIMILATION = VowelAssimilationRule(
    name="ASSYRIAN_VOWEL_ASSIMILATION",
    code="VAS-1",
    description="a penúltima → vocal final (3+ sílabas)",
    rule_type=VowelRuleType.ASSIMILATION,
    condition=condition_assyrian_vowel_assimilation,
    transformation=lambda v: v,  # Usa apply_with_context
    target_vowel_getter=lambda ctx: ctx.following_vowel,
    obligatoriness=RuleObligatoriness.OBLIGATORY,
    source_section="§ 3.4.9.1",
    examples=[
        VowelExample("*aššātum", "aššutum", "esposa (Nom)", section="§ 3.4.9.1"),
        VowelExample("*aššātem", "aššetem", "esposa (Gen)", section="§ 3.4.9.1"),
        VowelExample("*išakkan", "išakkan", "coloca", section="§ 3.4.9.1"),
        VowelExample("*išakkanū", "išakkunū", "colocan", section="§ 3.4.9.1"),
    ],
    notes="Distingue asirio de todos otros dialectos acadios."
)


# ============================================================================
# REGLAS DE CONTRACCIÓN VOCÁLICA
# ============================================================================

def condition_identical_vowel_contraction(ctx: VowelContext) -> bool:
    """VV → V̂ (vocales idénticas)"""
    return (
        ctx.following_vowel is not None and
        ctx.vowels_are_adjacent() and
        ctx.vowels_match_quality()
    )

def transform_contract_identical(vowel: Vowel, following: Vowel) -> Vowel:
    """Contrae vocales idénticas → larga."""
    return get_vowel(vowel.quality.value, length='long')

@dataclass
class VowelContractionRule(VowelRule):
    """Regla especializada para contracción vocálica."""
    v1_quality: Optional[str] = None
    v2_quality: Optional[str] = None
    result_quality: Optional[str] = None
    
    def get_contraction_result(self, v1: Vowel, v2: Vowel) -> Vowel:
        """Obtiene resultado de contracción."""
        if self.result_quality:
            return get_vowel(self.result_quality, length='long')
        # Default: primera vocal larga
        return get_vowel(v1.quality.value, length='long')

VC_1_IDENTICAL_CONTRACTION = VowelContractionRule(
    name="IDENTICAL_VOWEL_CONTRACTION",
    code="VC-1",
    description="VV → V̂ (idénticas)",
    rule_type=VowelRuleType.CONTRACTION,
    condition=condition_identical_vowel_contraction,
    transformation=lambda v: v,  # Usa get_contraction_result
    obligatoriness=RuleObligatoriness.OPTIONAL,
    source_section="§ 3.4.11",
    examples=[
        VowelExample("*banaʾan", "banān", "construyó", section="§ 3.4.11.1"),
        VowelExample("*išuʾūni", "i-šu-ni", "tiene (Subj)", section="§ 3.4.11.3"),
    ],
    notes="Incidental. Preferencia por formas no-contraídas."
)


# ============================================================================
# REGLA DE SÍNCOPE VOCÁLICA
# ============================================================================

def condition_vowel_syncope(ctx: VowelContext) -> bool:
    """
    Síncope vocálica: secuencia 2+ sílabas cortas.
    
    Última vocal de secuencia se sincopa.
    """
    # Esta regla necesita contexto de secuencia completa
    # Implementación simplificada aquí
    return (
        ctx.total_syllables >= 3 and
        ctx.vowel.length.value == 'short' and
        not ctx.is_word_final
    )

def transform_syncope(vowel: Vowel) -> Optional[Vowel]:
    """Síncope: elimina vocal."""
    return None  # Vocal eliminada

VS_1_VOWEL_SYNCOPE = VowelRule(
    name="VOWEL_SYNCOPE",
    code="VS-1",
    description="Síncope de última vocal en secuencia cortas",
    rule_type=VowelRuleType.DELETION,
    condition=condition_vowel_syncope,
    transformation=transform_syncope,
    obligatoriness=RuleObligatoriness.OBLIGATORY,
    source_section="§ 3.4.8",
    examples=[
        VowelExample("*dāmīqum", "damqum", "bueno", section="§ 3.4.8"),
        VowelExample("*šākinū", "šaknū", "colocados", section="§ 3.4.8"),
        VowelExample("*mitāgar", "mitgar", "ponte de acuerdo", section="§ 3.4.8"),
    ],
    notes="Pan-acadio. Aplica consistentemente en raíces fuertes."
)


# ============================================================================
# TABLA DE TODAS LAS REGLAS
# ============================================================================

ALL_VOWEL_RULES = [
    VA_1_A_TO_E_BEFORE_R,
    VA_2_A_TO_E_GUTTURAL,
    VA_3_I_TO_E_BEFORE_R,
    VA_4_I_TO_E_BEFORE_M_GRAM,
    VAS_1_ASSYRIAN_ASSIMILATION,
    VC_1_IDENTICAL_CONTRACTION,
    VS_1_VOWEL_SYNCOPE,
]


# ============================================================================
# TABLA DE CONDICIONAMIENTO CONSONÁNTICO
# ============================================================================

CONSONANT_VOWEL_CONDITIONING = {
    # Formato: (consonante, posición, vocal_input) → vocal_output
    
    # Gutural + a → e
    ('ʾ', 'preceding', 'a'): 'e',
    ('ḫ', 'preceding', 'a'): 'e',
    ('ʿ', 'preceding', 'a'): 'e',
    ('h', 'preceding', 'a'): 'e',
    ('ḥ', 'preceding', 'a'): 'e',
    
    ('ʾ', 'following', 'a'): 'e',
    ('ḫ', 'following', 'a'): 'e',
    ('ʿ', 'following', 'a'): 'e',
    ('h', 'following', 'a'): 'e',
    ('ḥ', 'following', 'a'): 'e',
    
    # r + a → e
    ('r', 'following', 'a'): 'e',
    
    # r + i → e  
    ('r', 'following', 'i'): 'e',
    
    # m# gramatical + i → e
    ('m', 'following', 'i'): 'e',  # Solo si gramatical
    
    # ʾ + ī → ē (después de ʾ)
    ('ʾ', 'preceding', 'ī'): 'ē',
}


# ============================================================================
# TABLA DE CONTRACCIONES
# ============================================================================

VOWEL_CONTRACTION_TABLE = {
    # Formato: (v1, v2) → (resultado, longitud, obligatorio)
    
    # Idénticas
    ('a', 'a'): ('ā', 'long', False),
    ('i', 'i'): ('ī', 'long', False),
    ('u', 'u'): ('ū', 'long', False),
    ('e', 'e'): ('ē', 'long', False),
    
    # Diferentes (muy raras)
    ('a', 'i'): ('ē', 'long', False),
    ('i', 'a'): ('ē', 'long', False),
    ('a', 'u'): ('ū', 'long', False),
    ('i', 'u'): ('î', 'long', False),
    ('u', 'i'): ('û', 'long', False),
}

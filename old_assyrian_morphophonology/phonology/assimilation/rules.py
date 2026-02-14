"""
Reglas de asimilación consonántica del Old Assyrian.

Implementa todas las reglas documentadas en § 3.2.4 de Kouwenberg (2017).
"""

from dataclasses import dataclass, field
from typing import Optional, List, Callable, Tuple
from ...phonology import Phoneme, Consonant, Vowel, get_consonant
from ...phonology import ConsonantClass
from .enums import (
    AssimilationDirection,
    AssimilationType,
    AssimilationStatus,
    EvidenceLevel,
    RulePrecedence,
)
from .contexts import AssimilationEnvironment, MorphologicalContext


@dataclass
class AssimilationExample:
    """Ejemplo de asimilación documentado en Kouwenberg."""
    underlying: str      # Forma subyacente
    surface: str        # Forma superficial
    gloss: str         # Traducción
    spelling: Optional[str] = None  # Spelling ORACC
    reference: Optional[str] = None  # Referencia de tablilla
    section: str = ""   # Sección del libro
    
    def __repr__(self) -> str:
        return f"{self.underlying} → {self.surface} '{self.gloss}'"


@dataclass
class AssimilationRule:
    """
    Regla de asimilación consonántica.
    
    Define condiciones de aplicación y transformación resultante.
    """
    # Identificación
    name: str
    code: str  # Código corto (ej: 'AN-1')
    description: str
    
    # Segmentos involucrados
    trigger_class: ConsonantClass      # Clase que dispara asimilación
    target_class: ConsonantClass       # Clase objetivo
    
    # Tipo de asimilación
    direction: AssimilationDirection
    assimilation_type: AssimilationType
    
    # Aplicación
    status: AssimilationStatus
    condition: Callable[[AssimilationEnvironment], bool]
    transformation: Callable[[Consonant, Consonant], Tuple[Consonant, Consonant]]
    
    # Ordenamiento
    precedence: int = RulePrecedence.OBLIGATORY_ASSIM.value
    feeds: List[str] = field(default_factory=list)    # Reglas que alimenta
    bleeds: List[str] = field(default_factory=list)   # Reglas que sangra
    
    # Evidencia
    evidence_level: EvidenceLevel = EvidenceLevel.EXPLICIT
    
    # Documentación
    source_section: str = ""
    examples: List[AssimilationExample] = field(default_factory=list)
    notes: str = ""
    
    def applies(self, env: AssimilationEnvironment) -> bool:
        """
        Determina si regla aplica en este ambiente.
        
        Args:
            env: Ambiente fonológico y morfológico
        
        Returns:
            True si regla debe aplicarse
        """
        # Verificar bloqueo morfológico
        if env.morphological_context.should_block_assimilation():
            return False
        
        # Aplicar condición específica
        return self.condition(env)
    
    def apply(
        self,
        c1: Consonant,
        c2: Consonant
    ) -> Tuple[Consonant, Consonant]:
        """
        Aplica transformación de asimilación.
        
        Args:
            c1: Primera consonante
            c2: Segunda consonante
        
        Returns:
            (c1_resultado, c2_resultado) después de asimilación
        """
        return self.transformation(c1, c2)
    
    def __repr__(self) -> str:
        return f"Rule({self.code}: {self.name})"


# ============================================================================
# CONDICIONES DE ASIMILACIÓN
# ============================================================================

def condition_nasal_plus_any(env: AssimilationEnvironment) -> bool:
    """Condición: nasal + cualquier consonante."""
    return (env.consonant1.is_nasal and 
            env.forms_cluster())


def condition_nasal_plus_obstruent(env: AssimilationEnvironment) -> bool:
    """Condición: nasal + obstruente."""
    return (env.consonant1.is_nasal and 
            env.consonant2.is_obstruent and
            env.forms_cluster())


def condition_nasal_plus_fricative(env: AssimilationEnvironment) -> bool:
    """Condición: nasal + fricativa."""
    return (env.consonant1.is_nasal and 
            env.consonant2.is_fricative and
            env.forms_cluster())


def condition_nasal_plus_nasal(env: AssimilationEnvironment) -> bool:
    """Condición: nasal + nasal."""
    return (env.consonant1.is_nasal and 
            env.consonant2.is_nasal and
            env.forms_cluster())


def condition_nasal_plus_weak(env: AssimilationEnvironment) -> bool:
    """Condición: nasal + débil (w, y)."""
    return (env.consonant1.is_nasal and 
            env.consonant2.is_weak and
            env.consonant2.symbol in ['w', 'y'] and
            env.forms_cluster())


def condition_nasal_plus_aleph(env: AssimilationEnvironment) -> bool:
    """Condición: nasal + ʾ."""
    return (env.consonant1.is_nasal and 
            env.consonant2.symbol == 'ʾ' and
            env.forms_cluster())


def condition_grammatical_m_plus_consonant(env: AssimilationEnvironment) -> bool:
    """Condición: m gramatical + consonante."""
    from .enums import MorphemeType
    
    if not env.consonant1.symbol == 'm':
        return False
    
    if not env.forms_cluster():
        return False
    
    # m debe ser de morfema gramatical
    grammatical_types = {
        MorphemeType.CASE_ENDING,
        MorphemeType.PRONOMINAL_SUFFIX,
    }
    
    return env.morphological_context.left_morpheme_type in grammatical_types


def condition_dental_plus_fem_t(env: AssimilationEnvironment) -> bool:
    """Condición: dental + sufijo femenino -t."""
    from .enums import MorphemeType
    
    return (env.consonant1.is_dental and
            env.consonant2.symbol == 't' and
            env.morphological_context.right_morpheme_type == MorphemeType.FEMININE_SUFFIX and
            env.forms_cluster())


def condition_dental_plus_sh_pronoun(env: AssimilationEnvironment) -> bool:
    """Condición: dental + pronombre 3ª persona con š."""
    from .enums import MorphemeType
    
    return (env.consonant1.is_dental and
            env.consonant2.symbol == 'š' and
            env.morphological_context.right_morpheme_type == MorphemeType.PRONOMINAL_SUFFIX and
            env.forms_cluster())


def condition_sibilant_plus_t_infix(env: AssimilationEnvironment) -> bool:
    """Condición: sibilante + infijo -t-."""
    from .enums import MorphemeType
    
    return (env.consonant1.is_sibilant and
            env.consonant2.symbol == 't' and
            env.morphological_context.has_t_infix and
            env.forms_cluster())


# ============================================================================
# TRANSFORMACIONES DE ASIMILACIÓN
# ============================================================================

def transform_to_geminate_c2(c1: Consonant, c2: Consonant) -> Tuple[Consonant, Consonant]:
    """
    Transformación: C₁C₂ → C₂C₂ (asimilación progresiva total).
    
    Ejemplos: n + p → pp, n + š → šš
    """
    return (c2, c2)


def transform_to_geminate_c1(c1: Consonant, c2: Consonant) -> Tuple[Consonant, Consonant]:
    """
    Transformación: C₁C₂ → C₁C₁ (asimilación regresiva total).
    
    Ejemplos: t + t → tt
    """
    return (c1, c1)


def transform_dental_sh_to_ss(c1: Consonant, c2: Consonant) -> Tuple[Consonant, Consonant]:
    """
    Transformación: dental + š → ss.
    
    Refleja pronunciación africada: [qāt-su] → /qāˢˢsu/
    """
    s = get_consonant('s')
    return (s, s)


def transform_sibilant_sh_to_sibilant_geminate(
    c1: Consonant,
    c2: Consonant
) -> Tuple[Consonant, Consonant]:
    """
    Transformación: sibilante + š → sibilante geminada.
    
    Ejemplos: s + š → ss, z + š → zz (pero escrito con serie-S)
    """
    # Preserva la sibilante original
    s_variant = get_consonant('s')  # Representado con serie-S
    return (s_variant, s_variant)


def transform_sibilant_t_to_sibilant_geminate(
    c1: Consonant,
    c2: Consonant
) -> Tuple[Consonant, Consonant]:
    """
    Transformación: sibilante + t_infix → sibilante geminada.
    
    Preserva radical original para transparencia.
    Ejemplos: s + t → ss, z + t → zz, ṣ + t → ṣṣ
    """
    return (c1, c1)


# ============================================================================
# REGLAS DE ASIMILACIÓN DE NASALES (AN-1 a AN-7)
# ============================================================================

AN_1_NASAL_OBSTRUENT = AssimilationRule(
    name="NASAL_ASSIMILATION_OBSTRUENT",
    code="AN-1",
    description="n/m + obstruent → obstruent geminate",
    trigger_class=ConsonantClass.NASAL,
    target_class=ConsonantClass.OBSTRUENT,
    direction=AssimilationDirection.PROGRESSIVE,
    assimilation_type=AssimilationType.TOTAL,
    status=AssimilationStatus.OBLIGATORY,
    condition=condition_nasal_plus_obstruent,
    transformation=transform_to_geminate_c2,
    precedence=RulePrecedence.OBLIGATORY_ASSIM.value,
    evidence_level=EvidenceLevel.EXPLICIT,
    source_section="§ 3.2.4.1",
    examples=[
        AssimilationExample(
            "*tanṣur", "/taṣṣur/", "guardaste",
            spelling="ta-ṣú-ur",
            reference="TC 3, 93: 30 (= OAA 1, 14)",
            section="§ 3.2.4.1"
        ),
        AssimilationExample(
            "*intakrū", "/ittakrū/", "negaron",
            spelling="i-ta-ak-ru-ú",
            reference="BIN 4, 151: 16",
            section="§ 3.2.4.1"
        ),
        AssimilationExample(
            "in-paras", "/ipparas/", "él separó",
            section="§ 3.2.4.1"
        ),
    ],
    notes="Pan-acádico. n asimila a siguiente consonante obstruente."
)

AN_2_NASAL_FRICATIVE = AssimilationRule(
    name="NASAL_ASSIMILATION_FRICATIVE",
    code="AN-2",
    description="n + fricative → fricative geminate",
    trigger_class=ConsonantClass.NASAL,
    target_class=ConsonantClass.FRICATIVE,
    direction=AssimilationDirection.PROGRESSIVE,
    assimilation_type=AssimilationType.TOTAL,
    status=AssimilationStatus.OBLIGATORY,
    condition=condition_nasal_plus_fricative,
    transformation=transform_to_geminate_c2,
    precedence=RulePrecedence.OBLIGATORY_ASSIM.value,
    evidence_level=EvidenceLevel.EXPLICIT,
    source_section="§ 3.2.4.1",
    examples=[
        AssimilationExample(
            "in-šakkan", "/iššakkan/", "él pone",
            section="§ 3.2.4.1"
        ),
    ],
)

AN_3_NASAL_NASAL = AssimilationRule(
    name="NASAL_ASSIMILATION_NASAL",
    code="AN-3",
    description="n + nasal → nasal geminate",
    trigger_class=ConsonantClass.NASAL,
    target_class=ConsonantClass.NASAL,
    direction=AssimilationDirection.PROGRESSIVE,
    assimilation_type=AssimilationType.TOTAL,
    status=AssimilationStatus.OBLIGATORY,
    condition=condition_nasal_plus_nasal,
    transformation=transform_to_geminate_c2,
    precedence=RulePrecedence.OBLIGATORY_ASSIM.value,
    evidence_level=EvidenceLevel.EXPLICIT,
    source_section="§ 3.2.4.1",
    examples=[
        AssimilationExample(
            "in-maqut", "/immaqut/", "él cayó",
            section="§ 3.2.4.1"
        ),
    ],
)

AN_4_NASAL_WAW = AssimilationRule(
    name="NASAL_ASSIMILATION_WAW",
    code="AN-4",
    description="n + w → ww",
    trigger_class=ConsonantClass.NASAL,
    target_class=ConsonantClass.WEAK,
    direction=AssimilationDirection.PROGRESSIVE,
    assimilation_type=AssimilationType.TOTAL,
    status=AssimilationStatus.OBLIGATORY,
    condition=condition_nasal_plus_weak,
    transformation=transform_to_geminate_c2,
    precedence=RulePrecedence.OBLIGATORY_ASSIM.value,
    evidence_level=EvidenceLevel.EXPLICIT,
    source_section="§ 3.2.4.1 + § 3.3.2.3",
    examples=[
        AssimilationExample(
            "in-warḫim", "/iwwarḫim/", "en el mes",
            section="§ 3.2.4.1"
        ),
        AssimilationExample(
            "an(a) wabrem", "/awwabrem/", "al residente extranjero",
            spelling="a-wa-áb-re-em",
            reference="CCT 5, 1b: 30",
            section="§ 3.2.4.1"
        ),
    ],
    notes="Interacción con débiles (Iteración 2)."
)

AN_5_NASAL_ALEPH = AssimilationRule(
    name="NASAL_ASSIMILATION_ALEPH",
    code="AN-5",
    description="n + ʾ → ʾʾ",
    trigger_class=ConsonantClass.NASAL,
    target_class=ConsonantClass.WEAK,  # ʾ es débil
    direction=AssimilationDirection.PROGRESSIVE,
    assimilation_type=AssimilationType.TOTAL,
    status=AssimilationStatus.OBLIGATORY,
    condition=condition_nasal_plus_aleph,
    transformation=transform_to_geminate_c2,
    precedence=RulePrecedence.OBLIGATORY_ASSIM.value,
    evidence_level=EvidenceLevel.EXPLICIT,
    source_section="§ 3.2.4.1",
    examples=[
        AssimilationExample(
            "an-ʾamtim", "/aʾʾamtim/", "en la esclava",
            section="§ 3.2.4.1"
        ),
    ],
    notes="n asimila a ʾ igual que a otras consonantes."
)

AN_6_GRAMMATICAL_M = AssimilationRule(
    name="GRAMMATICAL_M_ASSIMILATION",
    code="AN-6",
    description="m grammatical + C → CC",
    trigger_class=ConsonantClass.NASAL,
    target_class=ConsonantClass.ANY,
    direction=AssimilationDirection.PROGRESSIVE,
    assimilation_type=AssimilationType.TOTAL,
    status=AssimilationStatus.OBLIGATORY,
    condition=condition_grammatical_m_plus_consonant,
    transformation=transform_to_geminate_c2,
    precedence=RulePrecedence.OBLIGATORY_ASSIM.value,
    evidence_level=EvidenceLevel.EXPLICIT,
    source_section="§ 3.2.4.2",
    examples=[
        AssimilationExample(
            "naš(i)ʾ-am-kum-šu", "/našʾakkuššu/", "te lo está trayendo",
            spelling="na-áš-a-ku-šu",
            reference="BIN 6, 21: 13",
            section="§ 3.2.4.2"
        ),
        AssimilationExample(
            "qātātum-ni", "/qātātunni/", "fue garante",
            spelling="qá-ta-tù-ni",
            reference="VS 26, 97B: 4",
            section="§ 3.2.4.2"
        ),
    ],
    notes="SOLO m de morfema gramatical. m de raíz NO asimila."
)

# Continuará en siguiente archivo...

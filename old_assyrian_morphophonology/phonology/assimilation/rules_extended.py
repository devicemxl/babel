"""
Reglas de asimilación consonántica - Continuación.

Reglas de dentales, sibilantes, y otras asimilaciones.
"""

from ...phonology import get_consonant
from .rules import (
    AssimilationRule,
    AssimilationExample,
    condition_dental_plus_fem_t,
    condition_dental_plus_sh_pronoun,
    condition_sibilant_plus_t_infix,
    transform_to_geminate_c1,
    transform_dental_sh_to_ss,
    transform_sibilant_t_to_sibilant_geminate,
    transform_sibilant_sh_to_sibilant_geminate,
)
from ...phonology import ConsonantClass
from .enums import (
    AssimilationDirection,
    AssimilationType,
    AssimilationStatus,
    EvidenceLevel,
    RulePrecedence,
)


# ============================================================================
# REGLAS DE ASIMILACIÓN DE DENTALES (AD-1 a AD-4)
# ============================================================================

AD_1_DENTAL_FEM_T = AssimilationRule(
    name="DENTAL_FEMININE_T_ASSIMILATION",
    code="AD-1",
    description="dental + feminine -t → tt (presumably)",
    trigger_class=ConsonantClass.DENTAL,
    target_class=ConsonantClass.DENTAL,
    direction=AssimilationDirection.REGRESSIVE,  # Probable
    assimilation_type=AssimilationType.TOTAL,
    status=AssimilationStatus.OBLIGATORY,
    condition=condition_dental_plus_fem_t,
    transformation=transform_to_geminate_c1,  # Probable -tt-
    precedence=RulePrecedence.OBLIGATORY_ASSIM.value,
    evidence_level=EvidenceLevel.COMPARATIVE,
    source_section="§ 3.2.4.4",
    examples=[
        AssimilationExample(
            "pirid-tum", "pirittum", "miedo",
            section="§ 3.2.4.4",
        ),
        AssimilationExample(
            "šalīṭ-tum", "šalittum", "disponible" (Fem),
            section="§ 3.2.4.4",
        ),
    ],
    notes="Comparación con otros dialectos sugiere -tt-. Spelling no muestra cuál consonante prevalece."
)

AD_2_DENTAL_SH_PRONOUN = AssimilationRule(
    name="DENTAL_SH_PRONOUN_ASSIMILATION",
    code="AD-2",
    description="dental + 3rd person š → ss (affricate [ˢˢs])",
    trigger_class=ConsonantClass.DENTAL,
    target_class=ConsonantClass.SIBILANT,
    direction=AssimilationDirection.COALESCENCE,  # Fusión especial
    assimilation_type=AssimilationType.COALESCENCE,
    status=AssimilationStatus.OBLIGATORY,
    condition=condition_dental_plus_sh_pronoun,
    transformation=transform_dental_sh_to_ss,
    precedence=RulePrecedence.OBLIGATORY_ASSIM.value,
    evidence_level=EvidenceLevel.EXPLICIT,
    source_section="§ 3.2.4.4",
    examples=[
        AssimilationExample(
            "qāt-šu", "/qāssu/", "su mano",
            spelling="qá-sú",
            reference="CTMMA 1, 71: 41+",
            section="§ 3.2.4.4"
        ),
        AssimilationExample(
            "iṭarrad-ši", "/iṭarrassi/", "no la enviará",
            spelling="la i-tá-ra-sí",
            reference="a/k 1255: 15",
            section="§ 3.2.4.4"
        ),
        AssimilationExample(
            "uballiṭ-šunu", "/uballissunu/", "los mantuvo vivos",
            spelling="ú-ba-li-sú-nu",
            reference="AHw 1, 107: 11",
            section="§ 3.2.4.4"
        ),
    ],
    notes="Refleja pronunciación africada [ˢˢs]. Serie-S en spelling."
)

AD_3_DENTAL_N = AssimilationRule(
    name="DENTAL_N_ASSIMILATION",
    code="AD-3",
    description="t + n → nn (?)",
    trigger_class=ConsonantClass.DENTAL,
    target_class=ConsonantClass.NASAL,
    direction=AssimilationDirection.REGRESSIVE,
    assimilation_type=AssimilationType.TOTAL,
    status=AssimilationStatus.OBLIGATORY,  # Dudoso
    condition=lambda env: (
        env.consonant1.symbol == 't' and
        env.consonant2.symbol == 'n' and
        env.forms_cluster()
    ),
    transformation=transform_to_geminate_c1,  # → nn
    precedence=RulePrecedence.OBLIGATORY_ASSIM.value,
    evidence_level=EvidenceLevel.SPORADIC,
    source_section="§ 3.2.4.4",
    examples=[
        AssimilationExample(
            "bēt-ni", "/bēnni/", "nuestra casa",
            spelling="bê-(et)-ni",
            reference="87/k 39: 3",
            section="§ 3.2.4.4"
        ),
        AssimilationExample(
            "aḫāt-ni", "/aḫānni/", "nuestra hermana",
            spelling="a-ba-(at)-ni",
            reference="88/k 71: 61",
            section="§ 3.2.4.4"
        ),
    ],
    notes="Pocas instancias. Necesita más evidencia."
)

AD_4_DSH_TO_SSH = AssimilationRule(
    name="DSH_TO_SSH_ROOT_RADICALS",
    code="AD-4",
    description="-dš- → -šš- cuando son dos radicales finales",
    trigger_class=ConsonantClass.DENTAL,
    target_class=ConsonantClass.SIBILANT,
    direction=AssimilationDirection.REGRESSIVE,
    assimilation_type=AssimilationType.TOTAL,
    status=AssimilationStatus.OBLIGATORY,
    condition=lambda env: (
        env.consonant1.symbol == 'd' and
        env.consonant2.symbol == 'š' and
        env.morphological_context.left_consonant_is_radical and
        env.morphological_context.right_consonant_is_radical and
        env.forms_cluster()
    ),
    transformation=lambda c1, c2: (c2, c2),  # → šš
    precedence=RulePrecedence.OBLIGATORY_ASSIM.value,
    evidence_level=EvidenceLevel.EXPLICIT,
    source_section="§ 3.2.4.4",
    examples=[
        AssimilationExample(
            "*edšum", "eššum", "nuevo",
            section="§ 3.2.4.4",
            notes="< Sem ḥdθ"
        ),
        AssimilationExample(
            "*šedš-", "šešši-", "seis",
            section="§ 3.2.4.4",
            notes="< Sem šdθ, adi šeššišu 'seis veces'"
        ),
    ],
    notes="Diferente de regla normal dental + š. Solo cuando ambos son radicales de raíz."
)


# ============================================================================
# REGLAS DE ASIMILACIÓN DE SIBILANTES (AS-1 a AS-4)
# ============================================================================

def condition_sibilant_plus_sh_pronoun(env):
    """Condición: sibilante + pronombre 3ª con š."""
    from .enums import MorphemeType
    
    return (env.consonant1.is_sibilant and
            env.consonant1.symbol != 'š' and  # NO š
            env.consonant2.symbol == 'š' and
            env.morphological_context.right_morpheme_type == MorphemeType.PRONOMINAL_SUFFIX and
            env.forms_cluster())


AS_1_Z_DEVOICING = AssimilationRule(
    name="Z_DEVOICING",
    code="AS-1",
    description="z → s / _[voiceless]",
    trigger_class=ConsonantClass.SIBILANT,
    target_class=ConsonantClass.ANY,
    direction=AssimilationDirection.PROGRESSIVE,
    assimilation_type=AssimilationType.DEVOICING,
    status=AssimilationStatus.OBLIGATORY,
    condition=lambda env: (
        env.consonant1.symbol == 'z' and
        env.consonant2.features.voicing.value == 'voiceless' and
        env.forms_cluster()
    ),
    transformation=lambda c1, c2: (get_consonant('s'), c2),
    precedence=RulePrecedence.PHONETIC.value,
    evidence_level=EvidenceLevel.THEORETICAL,
    source_section="§ 3.2.4.6",
    examples=[
        AssimilationExample(
            "ēḫuz-ki", "[ēḫuski]", "te casó" (Fem),
            spelling="e-hu-uz-ki",
            section="§ 3.2.4.6"
        ),
    ],
    notes="Probable pero spelling no lo muestra."
)

AS_2_SIBILANT_SH_PRONOUN = AssimilationRule(
    name="SIBILANT_SH_PRONOUN_ASSIMILATION",
    code="AS-2",
    description="sibilant + 3rd person š → sibilant geminate (S-series)",
    trigger_class=ConsonantClass.SIBILANT,
    target_class=ConsonantClass.SIBILANT,
    direction=AssimilationDirection.REGRESSIVE,  # Preserva radical
    assimilation_type=AssimilationType.TOTAL,
    status=AssimilationStatus.OBLIGATORY,
    condition=condition_sibilant_plus_sh_pronoun,
    transformation=transform_sibilant_sh_to_sibilant_geminate,
    precedence=RulePrecedence.OBLIGATORY_ASSIM.value,
    evidence_level=EvidenceLevel.EXPLICIT,
    source_section="§ 3.2.4.6",
    examples=[
        AssimilationExample(
            "rakkis-šu", "/rakkissu/", "¡átalo!",
            spelling="ra-ki-sú",
            reference="AKT 3, 96: 36+",
            section="§ 3.2.4.6"
        ),
        AssimilationExample(
            "ēḫuz-ši", "/ēḫussi/", "se casó con ella",
            spelling="e-hu-sí",
            reference="CCT 5, 16a: 3",
            section="§ 3.2.4.6"
        ),
        AssimilationExample(
            "rābiš-šunu", "/rābissunu/", "su abogado",
            spelling="ra-bi₄-sú-nu",
            reference="TC 2, 38: 10",
            section="§ 3.2.4.6"
        ),
    ],
    notes="Igual que dental final. Refleja naturaleza africada."
)

AS_3_SIBILANT_T_INFIX = AssimilationRule(
    name="SIBILANT_T_INFIX_ASSIMILATION",
    code="AS-3",
    description="sibilant + t_infix → sibilant geminate",
    trigger_class=ConsonantClass.SIBILANT,
    target_class=ConsonantClass.DENTAL,
    direction=AssimilationDirection.REGRESSIVE,  # Preserva radical
    assimilation_type=AssimilationType.TOTAL,
    status=AssimilationStatus.OBLIGATORY,
    condition=condition_sibilant_plus_t_infix,
    transformation=transform_sibilant_t_to_sibilant_geminate,
    precedence=RulePrecedence.OBLIGATORY_ASSIM.value,
    evidence_level=EvidenceLevel.EXPLICIT,
    source_section="§ 3.2.4.8",
    examples=[
        AssimilationExample(
            "*astahur", "/assuhur/", "he sido retrasado",
            spelling="a-sú-hu-ur",
            reference="CCT 4, 3a: 16 (= OAA 1, 118)",
            section="§ 3.2.4.8",
            notes="saḫārum"
        ),
        AssimilationExample(
            "*iztuaz", "/izzuaz/", "ha dividido",
            spelling="i-zu-a-áz",
            reference="AKT 1, 15: 19 (= OAA 1, 73)",
            section="§ 3.2.4.8",
            notes="zuāzum"
        ),
        AssimilationExample(
            "*taṣtabtā", "/taṣṣabtā/", "agarraron" (Pl),
            spelling="ta-ṣa-áb-ta",
            reference="ATHE 44: 42",
            section="§ 3.2.4.8",
            notes="ṣabātum"
        ),
    ],
    notes="Preserva radical para transparencia. Infijo era originalmente prefijo."
)

AS_4_SH_DISTANT_ASSIM = AssimilationRule(
    name="SH_DISTANT_ASSIMILATION",
    code="AS-4",
    description="š → s / distant sibilant in word",
    trigger_class=ConsonantClass.SIBILANT,
    target_class=ConsonantClass.SIBILANT,
    direction=AssimilationDirection.REGRESSIVE,  # A distancia
    assimilation_type=AssimilationType.TOTAL,
    status=AssimilationStatus.OPTIONAL,
    condition=lambda env: (
        env.consonant1.symbol == 'š' and
        env.consonant2.is_sibilant and
        env.is_distant_assimilation()
    ),
    transformation=lambda c1, c2: (get_consonant('s'), c2),
    precedence=RulePrecedence.OPTIONAL_ASSIM.value,
    evidence_level=EvidenceLevel.EXPLICIT,
    source_section="§ 3.2.4.7",
    examples=[
        AssimilationExample(
            "ušašḫar", "usasḫar", "hará retrasar",
            spelling="la tu-sa-as-ha-ra-šu-nu",
            reference="Prag I 492: 21+",
            section="§ 3.2.4.7",
            notes="saḫārum Š"
        ),
        AssimilationExample(
            "ušazkar", "usaskar", "hará jurar",
            spelling="nu-sá-[a]z-kà-ar",
            reference="BIN 6, 101: 28",
            section="§ 3.2.4.7",
            notes="zakārum Š, realizado como /usaskar/"
        ),
    ],
    notes="Asimilación a distancia. š de prefijo → s cuando raíz tiene sibilante."
)


# ============================================================================
# REGLAS DE ASIMILACIÓN DE š (ASH-1)
# ============================================================================

def condition_sh_plus_sh_pronoun(env):
    """Condición: š + pronombre 3ª con š."""
    from .enums import MorphemeType
    
    return (env.consonant1.symbol == 'š' and
            env.consonant2.symbol == 'š' and
            env.morphological_context.right_morpheme_type == MorphemeType.PRONOMINAL_SUFFIX and
            env.forms_cluster())


ASH_1_SH_SH_PRONOUN = AssimilationRule(
    name="SH_SH_PRONOUN_ASSIMILATION",
    code="AŠ-1",
    description="š + 3rd person š → šš (S-series spelling)",
    trigger_class=ConsonantClass.SIBILANT,
    target_class=ConsonantClass.SIBILANT,
    direction=AssimilationDirection.PROGRESSIVE,
    assimilation_type=AssimilationType.TOTAL,
    status=AssimilationStatus.OBLIGATORY,
    condition=condition_sh_plus_sh_pronoun,
    transformation=lambda c1, c2: (c1, c1),  # šš
    precedence=RulePrecedence.OBLIGATORY_ASSIM.value,
    evidence_level=EvidenceLevel.EXPLICIT,
    source_section="§ 3.2.4.7",
    examples=[
        AssimilationExample(
            "lubūš-šunu", "/lubūššunu/", "su ropa",
            spelling="lu-bu-šu-nu",
            reference="TC 3, 36: 43",
            section="§ 3.2.4.7"
        ),
        AssimilationExample(
            "nērīš-šu", "/nēriššu/", "le preguntamos",
            spelling="né-ri-šu",
            reference="TPAK 1, 35: 11",
            section="§ 3.2.4.7"
        ),
    ],
    notes="Diferente de dentales/sibilantes africadas. Usa S-series."
)


# ============================================================================
# REGLAS DE INFIJO -t- VERBAL (AV-1 a AV-3)
# ============================================================================

def condition_g_plus_t_infix(env):
    """Condición: g + infijo -t-."""
    from .enums import MorphemeType
    
    return (env.consonant1.symbol == 'g' and
            env.consonant2.symbol == 't' and
            env.morphological_context.has_t_infix and
            env.forms_cluster())


AV_1_G_T_INFIX = AssimilationRule(
    name="G_T_INFIX_ASSIMILATION",
    code="AV-1",
    description="g + t_infix → gd (probable)",
    trigger_class=ConsonantClass.VELAR,
    target_class=ConsonantClass.DENTAL,
    direction=AssimilationDirection.REGRESSIVE,
    assimilation_type=AssimilationType.PARTIAL_VOICING,  # Asimilación de sonoridad
    status=AssimilationStatus.OBLIGATORY,
    condition=condition_g_plus_t_infix,
    transformation=lambda c1, c2: (c1, get_consonant('d')),  # g + d
    precedence=RulePrecedence.OBLIGATORY_ASSIM.value,
    evidence_level=EvidenceLevel.COMPARATIVE,
    source_section="§ 3.2.4.8",
    examples=[
        AssimilationExample(
            "ig-t-amar", "igdamar", "ha gastado",
            spelling="ag-da-ma-ar // ag-TA-ma-ar",
            reference="CCT 3, 24: 22+ // Sadberk No. 10: 18",
            section="§ 3.2.4.8",
            notes="gamārum. Spellings fluctúan."
        ),
    ],
    notes="Como otros dialectos. Spellings fluctúan. Leer TA como ⟨dá⟩."
)

AV_2_D_T_INFIX = AssimilationRule(
    name="D_T_INFIX_ASSIMILATION",
    code="AV-2",
    description="d/ṭ + t_infix → dd/ṭṭ (probable)",
    trigger_class=ConsonantClass.DENTAL,
    target_class=ConsonantClass.DENTAL,
    direction=AssimilationDirection.REGRESSIVE,
    assimilation_type=AssimilationType.TOTAL,
    status=AssimilationStatus.OBLIGATORY,
    condition=lambda env: (
        env.consonant1.is_dental and
        env.consonant1.symbol in ['d', 'ṭ'] and
        env.consonant2.symbol == 't' and
        env.morphological_context.has_t_infix and
        env.forms_cluster()
    ),
    transformation=lambda c1, c2: (c1, c1),  # → dd o ṭṭ
    precedence=RulePrecedence.OBLIGATORY_ASSIM.value,
    evidence_level=EvidenceLevel.COMPARATIVE,
    source_section="§ 3.2.4.8",
    examples=[
        AssimilationExample(
            "i-d-t-amqā", "/iddamqā/", "se volvieron buenas" (Fem),
            spelling="i-da-am-qá",
            reference="CCT 5, 1b: 11",
            section="§ 3.2.4.8"
        ),
        AssimilationExample(
            "ta-ṭ-t-ardam", "/taṭṭardam/", "me enviaste",
            spelling="ta-ṭá-ar-dam",
            reference="BIN 6, 74: 32",
            section="§ 3.2.4.8"
        ),
    ],
    notes="Basado en otros dialectos. Resultado idéntico al radical original."
)


# ============================================================================
# REGISTRO DE TODAS LAS REGLAS
# ============================================================================

ALL_ASSIMILATION_RULES = [
    # Nasales (AN-1 a AN-6) - del archivo anterior
    # Se importarán después
    
    # Dentales
    AD_1_DENTAL_FEM_T,
    AD_2_DENTAL_SH_PRONOUN,
    AD_3_DENTAL_N,
    AD_4_DSH_TO_SSH,
    
    # Sibilantes
    AS_1_Z_DEVOICING,
    AS_2_SIBILANT_SH_PRONOUN,
    AS_3_SIBILANT_T_INFIX,
    AS_4_SH_DISTANT_ASSIM,
    
    # š
    ASH_1_SH_SH_PRONOUN,
    
    # Infijo -t-
    AV_1_G_T_INFIX,
    AV_2_D_T_INFIX,
]

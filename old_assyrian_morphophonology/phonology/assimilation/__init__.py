"""
Módulo de asimilación consonántica del Old Assyrian.

Basado en Kouwenberg (2017) § 3.2.4-3.2.7.
"""

from .enums import (
    AssimilationDirection,
    AssimilationType,
    MorphologicalBoundary,
    MorphemeType,
    AssimilationStatus,
    EvidenceLevel,
    RulePrecedence,
)

from .contexts import (
    MorphologicalContext,
    AssimilationEnvironment,
    create_prefix_root_context,
    create_root_suffix_context,
    create_t_infix_context,
    create_compound_context,
)

from .rules import (
    AssimilationRule,
    AssimilationExample,
    # Reglas específicas
    AN_1_NASAL_OBSTRUENT,
    AN_2_NASAL_FRICATIVE,
    AN_3_NASAL_NASAL,
    AN_4_NASAL_WAW,
    AN_5_NASAL_ALEPH,
    AN_6_GRAMMATICAL_M,
)

from .rules_extended import (
    AD_1_DENTAL_FEM_T,
    AD_2_DENTAL_SH_PRONOUN,
    AD_3_DENTAL_N,
    AD_4_DSH_TO_SSH,
    AS_1_Z_DEVOICING,
    AS_2_SIBILANT_SH_PRONOUN,
    AS_3_SIBILANT_T_INFIX,
    AS_4_SH_DISTANT_ASSIM,
    ASH_1_SH_SH_PRONOUN,
    AV_1_G_T_INFIX,
    AV_2_D_T_INFIX,
    ALL_ASSIMILATION_RULES,
)

from .loss import (
    ConsonantLossRule,
    ConsonantLossExample,
    # Reglas de pérdida consonántica
    PER_1_M_LOSS_WORD_FINAL,
    PER_2_N_LOSS_WORD_FINAL,
    PER_3_R_LOSS_SYLLABLE_FINAL,
    PER_4_S_LOSS_SYLLABLE_FINAL,
    # Funciones de utilidad
    can_consonant_be_lost,
    apply_consonant_loss,
    create_syllable_context_for_loss,
    ALL_LOSS_RULES,
)

__all__ = [
    # Enums
    'AssimilationDirection',
    'AssimilationType',
    'MorphologicalBoundary',
    'MorphemeType',
    'AssimilationStatus',
    'EvidenceLevel',
    'RulePrecedence',
    
    # Contexts
    'MorphologicalContext',
    'AssimilationEnvironment',
    'create_prefix_root_context',
    'create_root_suffix_context',
    'create_t_infix_context',
    'create_compound_context',
    
    # Rules
    'AssimilationRule',
    'AssimilationExample',
    
    # Reglas específicas (nasales)
    'AN_1_NASAL_OBSTRUENT',
    'AN_2_NASAL_FRICATIVE',
    'AN_3_NASAL_NASAL',
    'AN_4_NASAL_WAW',
    'AN_5_NASAL_ALEPH',
    'AN_6_GRAMMATICAL_M',
    
    # Reglas específicas (dentales)
    'AD_1_DENTAL_FEM_T',
    'AD_2_DENTAL_SH_PRONOUN',
    'AD_3_DENTAL_N',
    'AD_4_DSH_TO_SSH',
    
    # Reglas específicas (sibilantes)
    'AS_1_Z_DEVOICING',
    'AS_2_SIBILANT_SH_PRONOUN',
    'AS_3_SIBILANT_T_INFIX',
    'AS_4_SH_DISTANT_ASSIM',
    
    # Reglas específicas (š)
    'ASH_1_SH_SH_PRONOUN',
    
    # Reglas específicas (infijo)
    'AV_1_G_T_INFIX',
    'AV_2_D_T_INFIX',
    
    # Colección completa
    'ALL_ASSIMILATION_RULES',
    
    # Reglas de pérdida consonántica (PER) - NUEVAS
    'ConsonantLossRule',
    'ConsonantLossExample',
    'PER_1_M_LOSS_WORD_FINAL',
    'PER_2_N_LOSS_WORD_FINAL',
    'PER_3_R_LOSS_SYLLABLE_FINAL',
    'PER_4_S_LOSS_SYLLABLE_FINAL',
    'can_consonant_be_lost',
    'apply_consonant_loss',
    'create_syllable_context_for_loss',
    'ALL_LOSS_RULES',
]

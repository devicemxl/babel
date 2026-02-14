"""
Templates de patrones nominales del Old Assyrian.

Basado en Kouwenberg (2017) § 4.2.1 (Patrones Primarios).

Patrones implementados:
- PaRS, PiRS, PuRS (monovocálicos cortos)
- PāRS, PīRS, PūRS (monovocálicos largos)
- PaRāS, PiRīS (bivocálicos)
- PaRRāS, PuRRuS (con geminación)
"""

from typing import List
from .. import get_vowel
from .pattern import NominalPattern, NominalExample
from .enums import (
    Gender,
    PatternType,
    VowelPatternType,
    NominalFunction,
)


# ============================================================================
# PATRONES MONOVOCÁLICOS CORTOS
# ============================================================================

PARS = NominalPattern(
    name="PaRS",
    code="NOM-01",
    template="CACVC",
    vowels=[get_vowel('a')],
    has_mimation=True,
    gender=Gender.MASCULINE,
    pattern_type=PatternType.PRIMARY,
    vowel_pattern_type=VowelPatternType.SHORT,
    nominal_function=NominalFunction.AGENT,
    description=(
        "Patrón nominal primario monovocálico con vocal corta a. "
        "Típicamente denota agente, instrumento, o nombre concreto."
    ),
    examples=[
        NominalExample(
            root="√mlk",
            surface="malkum",
            gloss="consejo",
            section="§ 4.2.1"
        ),
        NominalExample(
            root="√nkr",
            surface="nakrum",
            gloss="enemigo",
            section="§ 4.2.1"
        ),
        NominalExample(
            root="√qrb",
            surface="qerbum",
            gloss="interior",
            section="§ 4.2.1"
        ),
    ],
    section="§ 4.2.1",
    notes="Uno de los patrones más productivos en OA."
)

PIRS = NominalPattern(
    name="PiRS",
    code="NOM-02",
    template="CICVC",
    vowels=[get_vowel('i')],
    has_mimation=True,
    gender=Gender.MASCULINE,
    pattern_type=PatternType.PRIMARY,
    vowel_pattern_type=VowelPatternType.SHORT,
    nominal_function=NominalFunction.ABSTRACT,
    description=(
        "Patrón nominal primario monovocálico con vocal corta i. "
        "Típicamente denota nombre abstracto o resultado de acción."
    ),
    examples=[
        NominalExample(
            root="√dyn",
            surface="dīnum",
            gloss="juicio",
            section="§ 4.2.1",
            notes="Vocal i se alarga por contracción: *diyn-um → dīnum"
        ),
        NominalExample(
            root="√špr",
            surface="šiprum",
            gloss="envío, mensaje",
            section="§ 4.2.1"
        ),
    ],
    section="§ 4.2.1",
    notes="Común para nombres abstractos y de acción."
)

PURS = NominalPattern(
    name="PuRS",
    code="NOM-03",
    template="CUCVC",
    vowels=[get_vowel('u')],
    has_mimation=True,
    gender=Gender.MASCULINE,
    pattern_type=PatternType.PRIMARY,
    vowel_pattern_type=VowelPatternType.SHORT,
    nominal_function=NominalFunction.ABSTRACT,
    description=(
        "Patrón nominal primario monovocálico con vocal corta u. "
        "Denota nombre abstracto, cualidad, o estado."
    ),
    examples=[
        NominalExample(
            root="√šlm",
            surface="šulmum",
            gloss="salud, bienestar",
            section="§ 4.2.1"
        ),
        NominalExample(
            root="√dmq",
            surface="dumqum",
            gloss="bondad",
            section="§ 4.2.1"
        ),
    ],
    section="§ 4.2.1",
    notes="Típicamente nombres abstractos de cualidad."
)


# ============================================================================
# PATRONES MONOVOCÁLICOS LARGOS
# ============================================================================

PAARS = NominalPattern(
    name="PāRS",
    code="NOM-04",
    template="CVVCVC",
    vowels=[get_vowel('ā')],
    has_mimation=True,
    gender=Gender.MASCULINE,
    pattern_type=PatternType.PRIMARY,
    vowel_pattern_type=VowelPatternType.LONG,
    nominal_function=NominalFunction.AGENT,
    description=(
        "Patrón nominal primario monovocálico con vocal larga ā. "
        "Denota agente o profesión."
    ),
    examples=[
        NominalExample(
            root="√kšd",
            surface="kāšidum",
            gloss="conquistador",
            section="§ 4.2.1"
        ),
    ],
    section="§ 4.2.1",
    notes="Menos frecuente que PaRS."
)

PIIRS = NominalPattern(
    name="PīRS",
    code="NOM-05",
    template="CVVCVC",
    vowels=[get_vowel('ī')],
    has_mimation=True,
    gender=Gender.MASCULINE,
    pattern_type=PatternType.PRIMARY,
    vowel_pattern_type=VowelPatternType.LONG,
    nominal_function=NominalFunction.RESULT,
    description=(
        "Patrón nominal primario monovocálico con vocal larga ī. "
        "Denota resultado o producto de acción."
    ),
    examples=[
        NominalExample(
            root="√bny",
            surface="bīnum",
            gloss="construcción",
            section="§ 4.2.1",
            notes="De raíz III-y: *biny-um → bīnum"
        ),
    ],
    section="§ 4.2.1",
    notes="Común con raíces débiles."
)


# ============================================================================
# PATRONES BIVOCÁLICOS
# ============================================================================

PARAS = NominalPattern(
    name="PaRāS",
    code="NOM-06",
    template="CACVVCVC",
    vowels=[get_vowel('a'), get_vowel('ā')],
    has_mimation=True,
    gender=Gender.MASCULINE,
    pattern_type=PatternType.PRIMARY,
    vowel_pattern_type=VowelPatternType.MIXED,
    nominal_function=NominalFunction.ABSTRACT,
    description=(
        "Patrón nominal primario bivocálico (a-ā). "
        "Denota nombre de acción o resultado verbal (infinitivo nominal)."
    ),
    examples=[
        NominalExample(
            root="√šrq",
            surface="šarāqum",
            gloss="robo",
            section="§ 4.2.1"
        ),
        NominalExample(
            root="√qtl",
            surface="qatālum",
            gloss="matanza, asesinato",
            section="§ 4.2.1"
        ),
    ],
    section="§ 4.2.1",
    notes="Infinitivo nominal del G-stem. Muy productivo."
)

PIRIIS = NominalPattern(
    name="PiRīS",
    code="NOM-07",
    template="CICVVCVC",
    vowels=[get_vowel('i'), get_vowel('ī')],
    has_mimation=True,
    gender=Gender.MASCULINE,
    pattern_type=PatternType.PRIMARY,
    vowel_pattern_type=VowelPatternType.MIXED,
    nominal_function=NominalFunction.ABSTRACT,
    description=(
        "Patrón nominal primario bivocálico (i-ī). "
        "Menos frecuente, variante de PiRS."
    ),
    examples=[],
    section="§ 4.2.1",
    notes="Relativamente raro en OA."
)


# ============================================================================
# PATRONES CON GEMINACIÓN
# ============================================================================

PARRAAS = NominalPattern(
    name="PaRRāS",
    code="NOM-08",
    template="CACGCVVCVC",
    vowels=[get_vowel('a'), get_vowel('ā')],
    has_mimation=True,
    gender=Gender.MASCULINE,
    pattern_type=PatternType.PRIMARY,
    vowel_pattern_type=VowelPatternType.MIXED,
    nominal_function=NominalFunction.AGENT,
    description=(
        "Patrón nominal con geminación de R2 (segunda consonante). "
        "Denota agente habitual o profesión."
    ),
    examples=[
        NominalExample(
            root="√šrq",
            surface="šarrāqum",
            gloss="ladrón (habitual)",
            section="§ 4.2.1"
        ),
        NominalExample(
            root="√dyn",
            surface="dayyānum",
            gloss="juez",
            section="§ 4.2.1"
        ),
    ],
    section="§ 4.2.1",
    notes=(
        "La geminación intensifica el sentido: "
        "šarāqum 'robar' → šarrāqum 'ladrón (habitual)'"
    )
)

PURRUS = NominalPattern(
    name="PuRRuS",
    code="NOM-09",
    template="CUCGCVCVC",
    vowels=[get_vowel('u'), get_vowel('u')],
    has_mimation=True,
    gender=Gender.MASCULINE,
    pattern_type=PatternType.PRIMARY,
    vowel_pattern_type=VowelPatternType.SHORT,
    nominal_function=NominalFunction.QUALITY,
    description=(
        "Patrón nominal con geminación y vocales u. "
        "Denota cualidad o estado."
    ),
    examples=[
        NominalExample(
            root="√qrb",
            surface="qurrubu",
            gloss="cercanía",
            section="§ 4.2.1"
        ),
    ],
    section="§ 4.2.1",
    notes="Menos frecuente que PaRRāS."
)


# ============================================================================
# PATRONES CON PREFIJOS
# ============================================================================

MAPRAS = NominalPattern(
    name="maPRaS",
    code="NOM-10",
    template="MACACVC",
    vowels=[get_vowel('a'), get_vowel('a')],
    has_mimation=True,
    gender=Gender.MASCULINE,
    pattern_type=PatternType.PRIMARY,
    vowel_pattern_type=VowelPatternType.SHORT,
    nominal_function=NominalFunction.PLACE,
    description=(
        "Patrón nominal con prefijo ma-. "
        "Típicamente denota lugar o instrumento."
    ),
    examples=[
        NominalExample(
            root="√nzz",
            surface="manzāzum",
            gloss="posición, lugar de estar",
            section="§ 4.2.1"
        ),
        NominalExample(
            root="√škn",
            surface="maškarum",
            gloss="lugar de molienda",
            section="§ 4.2.1"
        ),
    ],
    section="§ 4.2.1",
    notes="ma- es el prefijo de lugar/instrumento más común."
)


# ============================================================================
# PATRONES FEMENINOS
# ============================================================================

PARS_T = NominalPattern(
    name="PaRS-at",
    code="NOM-11",
    template="CACVCVC",
    vowels=[get_vowel('a'), get_vowel('a')],
    has_mimation=True,
    gender=Gender.FEMININE,
    pattern_type=PatternType.PRIMARY,
    vowel_pattern_type=VowelPatternType.SHORT,
    nominal_function=NominalFunction.ABSTRACT,
    description=(
        "Patrón femenino con sufijo -at (→ -atum con mimación). "
        "Forma femenino de PaRS, típicamente nombre abstracto."
    ),
    examples=[
        NominalExample(
            root="√mlk",
            surface="malkatum",
            gloss="consejo (fem.)",
            section="§ 4.2.1"
        ),
    ],
    section="§ 4.2.1",
    notes="El sufijo -at forma femenino de muchos patrones masculinos."
)


# ============================================================================
# COLECCIÓN DE TODOS LOS PATRONES
# ============================================================================

ALL_PATTERNS = [
    PARS,
    PIRS,
    PURS,
    PAARS,
    PIIRS,
    PARAS,
    PIRIIS,
    PARRAAS,
    PURRUS,
    MAPRAS,
    PARS_T,
]

# Índice por nombre
PATTERNS_BY_NAME = {p.name: p for p in ALL_PATTERNS}

# Índice por código
PATTERNS_BY_CODE = {p.code: p for p in ALL_PATTERNS}


# ============================================================================
# FUNCIONES DE BÚSQUEDA
# ============================================================================

def get_pattern_by_name(name: str) -> NominalPattern:
    """Obtiene patrón por nombre (PaRS, PiRS, etc.)."""
    if name not in PATTERNS_BY_NAME:
        raise ValueError(f"Patrón desconocido: {name}")
    return PATTERNS_BY_NAME[name]


def get_pattern_by_code(code: str) -> NominalPattern:
    """Obtiene patrón por código (NOM-01, NOM-02, etc.)."""
    if code not in PATTERNS_BY_CODE:
        raise ValueError(f"Código de patrón desconocido: {code}")
    return PATTERNS_BY_CODE[code]


def get_patterns_by_function(function: NominalFunction) -> List[NominalPattern]:
    """Obtiene patrones por función semántica."""
    return [p for p in ALL_PATTERNS if p.nominal_function == function]


def get_patterns_by_gender(gender: Gender) -> List[NominalPattern]:
    """Obtiene patrones por género."""
    return [p for p in ALL_PATTERNS if p.gender == gender]


def get_patterns_with_gemination() -> List[NominalPattern]:
    """Obtiene patrones que requieren geminación."""
    return [p for p in ALL_PATTERNS if p.requires_gemination()]


def get_primary_patterns() -> List[NominalPattern]:
    """Obtiene patrones primarios."""
    return [p for p in ALL_PATTERNS if p.pattern_type == PatternType.PRIMARY]

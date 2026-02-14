"""
Comportamiento de consonantes débiles y reglas fonológicas.

Este módulo implementa el sistema completo de reglas para ʾ, w, y
basado en Kouwenberg (2017) § 3.3.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Callable, Tuple
from .phoneme import Phoneme, Consonant, Vowel
from .inventory import get_consonant, get_vowel
from .phoneme import VowelLength, VowelFeatures, AccentType
from .weak_enums import (
    WeakPosition,
    PreservationStatus,
    EvidenceType,
    HistoricalChange,
    WeakVerbClass,
)
from .phonological_context import PhonologicalContext, MorphologicalInfo


@dataclass
class WeakConsonantExample:
    """
    Ejemplo de consonante débil del libro de Kouwenberg.
    
    Documenta casos atestiguados con toda su información.
    """
    # Información textual
    oracc_spelling: str
    transcription: str
    gloss: str
    
    # Información fonológica
    root: Optional[str] = None
    weak_consonant: Optional[Consonant] = None
    position: Optional[WeakPosition] = None
    
    # Comportamiento
    is_written: bool = False
    phonologically_preserved: bool = False
    
    # Metadata
    book_section: str = ""
    book_page: Optional[int] = None
    reference: Optional[str] = None  # Referencia de tablilla
    notes: str = ""  # Notas adicionales
    
    def __repr__(self) -> str:
        return f"Example({self.oracc_spelling} '{self.gloss}')"


@dataclass
class WeakConsonantBehavior:
    """
    Define el comportamiento de una consonante débil en un contexto específico.
    
    Basado en § 3.3.1-3.3.3 de Kouwenberg (2017).
    """
    consonant: Consonant  # ʾ, w, o y
    position: WeakPosition
    
    # Comportamiento ortográfico
    typically_written: bool
    alternative_spellings: List[str] = field(default_factory=list)
    
    # Comportamiento fonológico
    preservation_status: PreservationStatus = PreservationStatus.CONTEXT_DEPENDENT
    triggers_lengthening: bool = False
    can_fuse: bool = False  # Con consonante adyacente
    
    # Efectos sobre adyacentes
    contracts_with_vowels: bool = False
    assimilates_to_adjacent: bool = False
    
    # Ejemplos del libro
    examples: List[WeakConsonantExample] = field(default_factory=list)
    
    # Referencias
    book_section: str = ""
    notes: str = ""


# ============================================================================
# COMPORTAMIENTOS ESPECÍFICOS POR CONSONANTE Y POSICIÓN
# ============================================================================

# --- ʾ (GLOTTAL STOP) ---

ALEPH_INTERVOCALIC_IDENTICAL = WeakConsonantBehavior(
    consonant=get_consonant('ʾ'),
    position=WeakPosition.INTERVOCALIC_IDENTICAL,
    typically_written=False,
    preservation_status=PreservationStatus.ALWAYS_PRESERVED,
    triggers_lengthening=False,
    contracts_with_vowels=False,
    book_section="§ 3.3.1.3",
    notes="ʾ between identical vowels is preserved, represented by broken spelling",
    examples=[
        WeakConsonantExample(
            oracc_spelling="ša-a-lum",
            transcription="šaʾālum",
            gloss="to ask",
            root="√šʾl",
            weak_consonant=get_consonant('ʾ'),
            position=WeakPosition.INTERVOCALIC_IDENTICAL,
            is_written=False,
            phonologically_preserved=True,
            book_section="§ 3.3.1.3",
        ),
        WeakConsonantExample(
            oracc_spelling="be-a-lum",
            transcription="beʾālum",
            gloss="to possess",
            root="√bʿl",
            is_written=False,
            phonologically_preserved=True,
            book_section="§ 3.3.1.3",
        ),
    ]
)

ALEPH_SYLLABLE_FINAL = WeakConsonantBehavior(
    consonant=get_consonant('ʾ'),
    position=WeakPosition.SYLLABLE_FINAL,
    typically_written=False,
    preservation_status=PreservationStatus.COMPENSATORY_LENGTHENING,
    triggers_lengthening=True,
    contracts_with_vowels=False,
    book_section="§ 3.3.1.5",
    notes="ʾ after short vowel is dropped with compensatory lengthening",
    examples=[
        WeakConsonantExample(
            oracc_spelling="ši-mum",
            transcription="šīmum",
            gloss="purchase, price",
            root="√šʾm",
            is_written=False,
            phonologically_preserved=False,
            book_section="§ 3.3.1.5",
            notes="< *šiʾmum, PiRs of šaʾāmum"
        ),
        WeakConsonantExample(
            oracc_spelling="me-ra-šu",
            transcription="merāšu",
            gloss="his son",
            root="√mrʾ",
            is_written=False,
            phonologically_preserved=False,
            book_section="§ 3.3.1.5",
            notes="< *meraʾ-šu, compensatory lengthening proves long vowel"
        ),
    ]
)

ALEPH_POST_CONSONANTAL = WeakConsonantBehavior(
    consonant=get_consonant('ʾ'),
    position=WeakPosition.POST_CONSONANTAL,
    typically_written=False,
    preservation_status=PreservationStatus.VARIABLY_PRESERVED,
    triggers_lengthening=False,
    can_fuse=True,  # Con dental/glotálica
    book_section="§ 3.3.1.4",
    notes="Regularly preserved but can be lost; may fuse with dental → ṭ",
    examples=[
        WeakConsonantExample(
            oracc_spelling="ni-iš-um",
            transcription="nišʾum",
            gloss="present",
            root="√nšʾ",
            is_written=False,
            phonologically_preserved=True,
            book_section="§ 3.3.1.4",
        ),
        WeakConsonantExample(
            oracc_spelling="na-TA-ku",
            transcription="nadʾāku",
            gloss="I lay down",
            root="√ndʾ",
            is_written=False,  # Escrito como ṭ (fusión)
            phonologically_preserved=True,
            book_section="§ 3.3.1.4",
            notes="dental + ʾ written as TA (ṭ)"
        ),
    ]
)

# --- w (BILABIAL APPROXIMANT) ---

WAW_INITIAL = WeakConsonantBehavior(
    consonant=get_consonant('w'),
    position=WeakPosition.WORD_INITIAL,
    typically_written=True,
    preservation_status=PreservationStatus.VARIABLY_PRESERVED,
    triggers_lengthening=False,
    book_section="§ 3.3.2.2",
    notes="wa- → u- is ongoing change; forms alternate freely in OA",
    examples=[
        WeakConsonantExample(
            oracc_spelling="ur-du-um",
            transcription="urdum ~ wardum",
            gloss="slave",
            root="√wrd",
            is_written=False,  # En forma ur-
            phonologically_preserved=False,
            book_section="§ 3.3.2.2",
        ),
    ]
)

WAW_INTERVOCALIC_GEMINATE = WeakConsonantBehavior(
    consonant=get_consonant('w'),
    position=WeakPosition.INTERVOCALIC,
    typically_written=True,
    preservation_status=PreservationStatus.ALWAYS_PRESERVED,
    triggers_lengthening=False,
    book_section="§ 3.3.2.3",
    notes="Geminate -ww- in positions where strong verbs have geminates",
    examples=[
        WeakConsonantExample(
            oracc_spelling="a-la₁-we-e",
            transcription="alawwē",
            gloss="I will wrap",
            root="√lwʾ",
            is_written=True,
            phonologically_preserved=True,
            book_section="§ 3.3.2.3",
            notes="Pres 1s of lawāʾum, geminate /ww/"
        ),
    ]
)

WAW_GLIDE_AFTER_U = WeakConsonantBehavior(
    consonant=get_consonant('w'),
    position=WeakPosition.AFTER_U_BEFORE_VOWEL,
    typically_written=False,  # Puede omitirse
    preservation_status=PreservationStatus.CONTEXT_DEPENDENT,
    triggers_lengthening=False,
    book_section="§ 3.3.2.4",
    notes="w as glide after u may be written or omitted",
    examples=[
        WeakConsonantExample(
            oracc_spelling="i-tù-wa-ar",
            transcription="itūwar",
            gloss="he returns",
            is_written=True,
            phonologically_preserved=True,
            book_section="§ 3.3.2.4",
        ),
        WeakConsonantExample(
            oracc_spelling="i-tù-ar",
            transcription="itūar",
            gloss="he returns",
            is_written=False,
            phonologically_preserved=True,  # Kouwenberg: sin w
            book_section="§ 3.3.2.4",
        ),
    ]
)

# --- y (PALATAL APPROXIMANT) ---

YOD_INITIAL = WeakConsonantBehavior(
    consonant=get_consonant('y'),
    position=WeakPosition.WORD_INITIAL,
    typically_written=False,
    preservation_status=PreservationStatus.ALWAYS_LOST,
    triggers_lengthening=False,
    book_section="§ 3.3.3.2",
    notes="y initial completely lost in OA: *ya-, *yi- → i-, *yu- → u-",
    examples=[
        WeakConsonantExample(
            oracc_spelling="i-dum",
            transcription="idum",
            gloss="hand",
            root="√yd",
            is_written=False,
            phonologically_preserved=False,
            book_section="§ 3.3.3.2",
            notes="< *yad-"
        ),
    ]
)

YOD_POST_CONSONANTAL = WeakConsonantBehavior(
    consonant=get_consonant('y'),
    position=WeakPosition.POST_CONSONANTAL,
    typically_written=False,  # Generalmente glide o broken spelling
    preservation_status=PreservationStatus.CONTEXT_DEPENDENT,
    triggers_lengthening=False,
    book_section="§ 3.3.3.5",
    notes="Expressed by broken or glide spelling, alternating freely",
    examples=[
        WeakConsonantExample(
            oracc_spelling="qí-ib-a",
            transcription="qibya",
            gloss="speak! (Pl)",
            root="√qbʾ",
            is_written=False,  # Broken spelling
            phonologically_preserved=True,
            book_section="§ 3.3.3.5",
            notes="Kouwenberg: broken spelling transcribed with y"
        ),
        WeakConsonantExample(
            oracc_spelling="qí-bi-a",
            transcription="qibia",
            gloss="speak! (Pl)",
            root="√qbʾ",
            is_written=True,  # Glide spelling
            phonologically_preserved=True,
            book_section="§ 3.3.3.5",
        ),
    ]
)

YOD_BEFORE_HOMORGANIC = WeakConsonantBehavior(
    consonant=get_consonant('y'),
    position=WeakPosition.BEFORE_HOMORGANIC_VOWEL,
    typically_written=False,
    preservation_status=PreservationStatus.CONTRACTED,
    triggers_lengthening=False,
    contracts_with_vowels=True,
    book_section="§ 3.3.3.6",
    notes="-Cyi/e- → -Cī/ē- (contraction or elision of y)",
    examples=[
        WeakConsonantExample(
            oracc_spelling="ni-qí",
            transcription="niqī",
            gloss="my sacrifice",
            root="√nqʾ",
            is_written=False,
            phonologically_preserved=False,  # Contraído
            book_section="§ 3.3.3.6",
            notes="< *niq(y)ī, c.st. 1s of niqium"
        ),
    ]
)


# ============================================================================
# REGISTRO DE TODOS LOS COMPORTAMIENTOS
# ============================================================================

WEAK_BEHAVIORS = {
    # ʾ
    ('ʾ', WeakPosition.INTERVOCALIC_IDENTICAL): ALEPH_INTERVOCALIC_IDENTICAL,
    ('ʾ', WeakPosition.SYLLABLE_FINAL): ALEPH_SYLLABLE_FINAL,
    ('ʾ', WeakPosition.POST_CONSONANTAL): ALEPH_POST_CONSONANTAL,
    
    # w
    ('w', WeakPosition.WORD_INITIAL): WAW_INITIAL,
    ('w', WeakPosition.INTERVOCALIC): WAW_INTERVOCALIC_GEMINATE,
    ('w', WeakPosition.AFTER_U_BEFORE_VOWEL): WAW_GLIDE_AFTER_U,
    
    # y
    ('y', WeakPosition.WORD_INITIAL): YOD_INITIAL,
    ('y', WeakPosition.POST_CONSONANTAL): YOD_POST_CONSONANTAL,
    ('y', WeakPosition.BEFORE_HOMORGANIC_VOWEL): YOD_BEFORE_HOMORGANIC,
}


def get_behavior(consonant_symbol: str, position: WeakPosition) -> Optional[WeakConsonantBehavior]:
    """
    Obtiene el comportamiento documentado para una débil en una posición.
    
    Args:
        consonant_symbol: 'ʾ', 'w', o 'y'
        position: Posición de la débil
    
    Returns:
        WeakConsonantBehavior si está documentado, None si no
    """
    return WEAK_BEHAVIORS.get((consonant_symbol, position))


# ============================================================================
# REGLAS FONOLÓGICAS
# ============================================================================

@dataclass
class PhonologicalRule:
    """
    Regla fonológica para consonantes débiles.
    
    Define condición de aplicación y transformación.
    """
    name: str
    description: str
    consonant_symbol: str  # 'ʾ', 'w', o 'y'
    
    # Condición de aplicación
    condition: Callable[[PhonologicalContext], bool]
    
    # Transformación
    transformation: Callable[[List[Phoneme]], List[Phoneme]]
    
    # Metadata
    source_section: str
    examples: List[Tuple[str, str]] = field(default_factory=list)
    historical_change: Optional[HistoricalChange] = None
    
    def applies(self, context: PhonologicalContext) -> bool:
        """Determina si la regla aplica en este contexto."""
        return self.condition(context)
    
    def apply(self, phonemes: List[Phoneme]) -> List[Phoneme]:
        """Aplica la transformación."""
        return self.transformation(phonemes)
    
    def __repr__(self) -> str:
        return f"Rule({self.name})"


# ============================================================================
# REGLAS ESPECÍFICAS
# ============================================================================

def rule_aleph_compensatory_lengthening(phonemes: List[Phoneme]) -> List[Phoneme]:
    """
    Aplica alargamiento compensatorio por pérdida de ʾ.
    
    ʾ_C → V̄C
    """
    result = []
    i = 0
    while i < len(phonemes):
        if (i < len(phonemes) - 2 and
            isinstance(phonemes[i], Vowel) and
            phonemes[i].is_short and
            phonemes[i+1].symbol == 'ʾ' and
            isinstance(phonemes[i+2], Consonant)):
            
            # Alargar vocal, eliminar ʾ
            long_vowel = phonemes[i].lengthen()
            result.append(long_vowel)
            # Saltar ʾ
            i += 2
        else:
            result.append(phonemes[i])
            i += 1
    
    return result


RULE_ALEPH_COMPENSATORY = PhonologicalRule(
    name="ALEPH_COMPENSATORY_LENGTHENING",
    description="ʾ after short vowel is lost with compensatory lengthening",
    consonant_symbol='ʾ',
    condition=lambda ctx: (
        ctx.weak_position == WeakPosition.SYLLABLE_FINAL and
        ctx.preceding and isinstance(ctx.preceding, Vowel) and
        ctx.preceding.is_short
    ),
    transformation=rule_aleph_compensatory_lengthening,
    source_section="§ 3.3.1.5",
    examples=[
        ("*šiʾmum", "šīmum"),
        ("*meraʾ-šu", "merāšu"),
    ],
    historical_change=HistoricalChange.ALEPH_COMPENSATORY,
)


def rule_yod_contraction_before_i(phonemes: List[Phoneme]) -> List[Phoneme]:
    """
    Aplica contracción -Cyi- → -Cī-.
    """
    result = []
    i = 0
    while i < len(phonemes):
        if (i < len(phonemes) - 2 and
            isinstance(phonemes[i], Consonant) and
            phonemes[i+1].symbol == 'y' and
            isinstance(phonemes[i+2], Vowel) and
            phonemes[i+2].quality.value in ['i', 'e']):
            
            # Consonante + vocal larga (contracción)
            result.append(phonemes[i])
            contracted_vowel = phonemes[i+2].lengthen()
            result.append(contracted_vowel)
            i += 3
        else:
            result.append(phonemes[i])
            i += 1
    
    return result


RULE_YOD_CONTRACTION = PhonologicalRule(
    name="YOD_CONTRACTION_BEFORE_HOMORGANIC",
    description="-Cyi/e- → -Cī/ē- (contraction or elision)",
    consonant_symbol='y',
    condition=lambda ctx: (
        ctx.weak_position == WeakPosition.BEFORE_HOMORGANIC_VOWEL and
        isinstance(ctx.following, Vowel) and
        ctx.following.quality.value in ['i', 'e']
    ),
    transformation=rule_yod_contraction_before_i,
    source_section="§ 3.3.3.6",
    examples=[
        ("*niq(y)ī", "niqī"),
        ("*pit(y)ī", "pitī"),
    ],
    historical_change=HistoricalChange.Y_CONTRACTION,
)


# Registro de todas las reglas
ALL_RULES = [
    RULE_ALEPH_COMPENSATORY,
    RULE_YOD_CONTRACTION,
    # Más reglas a añadir...
]


def get_applicable_rules(context: PhonologicalContext) -> List[PhonologicalRule]:
    """
    Retorna todas las reglas aplicables a un contexto dado.
    
    Args:
        context: Contexto fonológico
    
    Returns:
        Lista de reglas que aplican
    """
    applicable = []
    for rule in ALL_RULES:
        if rule.applies(context):
            applicable.append(rule)
    
    return applicable

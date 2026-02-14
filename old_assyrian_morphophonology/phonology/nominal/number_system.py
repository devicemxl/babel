"""
Sistema de número nominal del Old Assyrian.

ITERACIÓN 7 - Formación de dual y plural.

Implementa las reglas de número extraídas de § 5.4:
- Dual: -ān (Nom), -ēn (Obl) - todos los géneros
- Plural masculino: -ū (Nom), -ī (Obl)
- Plural femenino: -ātum (todos los casos)

Incluye:
- Contracción vocálica en dual (āyi → ē)
- Distinción Nom/Obl en plural masculino
- Forma única plural femenino
- Reemplazo frecuente de dual/plural por singular

Basado en extracción Fase 1 de Kouwenberg (2017) § 5.4 (pp. 164-171).

Autor: Claude
Fecha: 2026-02-07
"""

from typing import List, Optional
from dataclasses import dataclass

from ..phoneme import Phoneme, Vowel, Consonant
from ..inventory import get_vowel, get_consonant
from .inflection import NumberMarker, InflectedNominal, InflectionContext
from .derivation import DerivedNominal
from .enums import Gender, Number, State
from .inflection_enums import Case, OBLIQUE_CASES


# ============================================================================
# DEFINICIÓN DE MARCADORES DE NÚMERO
# ============================================================================

# DUAL: Forma única para todos los géneros

DUAL_NOMINATIVE = NumberMarker(
    number=Number.DUAL,
    gender=Gender.COMMON,  # Aplica a todos
    case=Case.NOMINATIVE,
    phonemes=[get_vowel('ā'), get_consonant('n')]  # -ān
)

DUAL_OBLIQUE = NumberMarker(
    number=Number.DUAL,
    gender=Gender.COMMON,
    case=None,  # Sirve para Gen y Acc
    phonemes=[get_vowel('ē'), get_consonant('n')]  # -ēn
)
# Nota: -ēn < *-āyin con contracción (§ 3.4.11.1)


# PLURAL MASCULINO: Distinción Nom/Obl

PLURAL_MASC_NOM = NumberMarker(
    number=Number.PLURAL,
    gender=Gender.MASCULINE,
    case=Case.NOMINATIVE,
    phonemes=[get_vowel('ū')]  # -ū
)

PLURAL_MASC_OBL = NumberMarker(
    number=Number.PLURAL,
    gender=Gender.MASCULINE,
    case=None,  # Gen y Acc
    phonemes=[get_vowel('ī')]  # -ī
)


# PLURAL FEMENINO: Forma única para todos los casos

PLURAL_FEM = NumberMarker(
    number=Number.PLURAL,
    gender=Gender.FEMININE,
    case=None,  # Todos los casos
    phonemes=[  # -ātum
        get_vowel('ā'),
        get_consonant('t'),
        get_vowel('u'),
        get_consonant('m')
    ]
)


# ============================================================================
# FUNCIONES DE APLICACIÓN - DUAL
# ============================================================================

def form_dual(
    base: DerivedNominal,
    case: Case,
    preserve_mimation: bool = True
) -> InflectedNominal:
    """
    Forma dual de sustantivo.
    
    REGLAS DEL DUAL (§ 5.4.2):
    
    Nominativo:
        - Todos los géneros: -ān
        - šarrān "dos reyes"
        - mātān "dos tierras"
    
    Oblicuo (Gen/Acc):
        - Todos los géneros: -ēn (< *-āyin)
        - šarrēn "dos reyes" (Gen/Acc)
        - mātēn "dos tierras" (Gen/Acc)
    
    Contracción vocálica:
        - *šarr-āyin → šarrēn
        - āyi → ē (regla de contracción § 3.4.11.1)
    
    Pérdida de -n:
        - En constructo: -ān → -ā, -ēn → -ē
        - šarrā kārim "dos reyes del kārum"
    
    Args:
        base: Sustantivo derivado base
        case: Caso (Nom o Gen/Acc)
        preserve_mimation: Si mantener -n final (= mimación del dual)
        
    Returns:
        Sustantivo en dual
        
    Ejemplos:
        >>> # šarr- + dual.nom = šarrān
        >>> form_dual(sharr, Case.NOMINATIVE)
        InflectedNominal(šarrān [nominative.dual.absolute])
        
        >>> # šarr- + dual.obl = šarrēn
        >>> form_dual(sharr, Case.GENITIVE)
        InflectedNominal(šarrēn [genitive.dual.absolute])
    
    Ref: § 5.4.2 (pp. 165-166)
    """
    # Seleccionar marcador apropiado
    if case == Case.NOMINATIVE:
        marker = DUAL_NOMINATIVE
        phonemes = [get_vowel('ā'), get_consonant('n')]
    else:
        # Oblicuo (Gen/Acc)
        marker = DUAL_OBLIQUE
        phonemes = [get_vowel('ē'), get_consonant('n')]
    
    # Construir forma
    result_phonemes = list(base.phonemes)
    
    # Remover vocal final del stem si existe
    if result_phonemes and isinstance(result_phonemes[-1], Vowel):
        result_phonemes = result_phonemes[:-1]
    
    # Agregar marcador de dual
    result_phonemes.extend(phonemes)
    
    # En constructo, remover -n final
    if not preserve_mimation and result_phonemes[-1].value == 'n':
        result_phonemes = result_phonemes[:-1]
    
    return InflectedNominal(
        base=base,
        case=case,
        number=Number.DUAL,
        state=State.ABSOLUTE,
        phonemes=result_phonemes,
        number_marker=marker
    )


def dual_to_construct(dual: InflectedNominal) -> InflectedNominal:
    """
    Convierte dual a estado constructo.
    
    Regla: Dual pierde -n final en constructo
    - šarrān → šarrā
    - šarrēn → šarrē
    
    Args:
        dual: Forma dual en absoluto
        
    Returns:
        Forma dual en constructo
        
    Ejemplo:
        >>> dual_nom = form_dual(sharr, Case.NOMINATIVE)
        >>> construct = dual_to_construct(dual_nom)
        >>> print(construct.get_transcription())
        'šarrā'
    
    Ref: § 5.4.2 (p. 166)
    """
    phonemes = list(dual.phonemes)
    
    # Remover -n final
    if phonemes and phonemes[-1].value == 'n':
        phonemes = phonemes[:-1]
    
    return InflectedNominal(
        base=dual.base,
        case=dual.case,
        number=Number.DUAL,
        state=State.CONSTRUCT,
        phonemes=phonemes,
        number_marker=dual.number_marker
    )


# ============================================================================
# FUNCIONES DE APLICACIÓN - PLURAL
# ============================================================================

def form_plural_masculine(
    base: DerivedNominal,
    case: Case,
    preserve_mimation: bool = True
) -> InflectedNominal:
    """
    Forma plural masculino.
    
    REGLAS DEL PLURAL MASCULINO (§ 5.4.3):
    
    Nominativo:
        - Marcador: -ū
        - šarrū "reyes"
        - awīlū "hombres"
    
    Oblicuo (Gen/Acc):
        - Marcador: -ī
        - šarrī "reyes" (Gen/Acc)
        - awīlī "hombres" (Gen/Acc)
    
    Sin mimación:
        - Plural masculino nunca tiene mimación
        - (a diferencia del singular: šarrum vs. šarrū)
    
    Constructo:
        - Idéntico a absoluto
        - šarrū kārim "reyes del kārum"
    
    Args:
        base: Sustantivo derivado base
        case: Caso
        preserve_mimation: Ignorado (pl.masc nunca tiene mimación)
        
    Returns:
        Sustantivo en plural masculino
        
    Ejemplos:
        >>> # šarr- + pl.nom = šarrū
        >>> form_plural_masculine(sharr, Case.NOMINATIVE)
        InflectedNominal(šarrū [nominative.plural.absolute])
        
        >>> # šarr- + pl.obl = šarrī
        >>> form_plural_masculine(sharr, Case.GENITIVE)
        InflectedNominal(šarrī [genitive.plural.absolute])
    
    Ref: § 5.4.3 (pp. 166-168)
    """
    # Seleccionar marcador
    if case == Case.NOMINATIVE:
        marker = PLURAL_MASC_NOM
        vowel = get_vowel('ū')
    else:
        # Oblicuo
        marker = PLURAL_MASC_OBL
        vowel = get_vowel('ī')
    
    # Construir forma
    result_phonemes = list(base.phonemes)
    
    # Remover vocal final del stem
    if result_phonemes and isinstance(result_phonemes[-1], Vowel):
        result_phonemes = result_phonemes[:-1]
    
    # Agregar marcador de plural
    result_phonemes.append(vowel)
    
    return InflectedNominal(
        base=base,
        case=case,
        number=Number.PLURAL,
        state=State.ABSOLUTE,
        phonemes=result_phonemes,
        number_marker=marker
    )


def form_plural_feminine(
    base: DerivedNominal,
    case: Case,
    preserve_mimation: bool = True
) -> InflectedNominal:
    """
    Forma plural femenino.
    
    REGLAS DEL PLURAL FEMENINO (§ 5.4.4):
    
    Todos los casos:
        - Marcador único: -ātum
        - našperātum "mensajes" (Nom/Gen/Acc)
        - awīlātum "mujeres" (todos los casos)
    
    Sin distinción de caso:
        - A diferencia del masculino
        - Forma única sirve para Nom, Gen, Acc
    
    Constructo:
        - Pierde mimación: -ātum → -āt
        - našperāt kārim "mensajes del kārum"
    
    Base:
        - Típicamente de femeninos en -t(um)
        - našpertum → našperātum
        - awīltum → awīlātum
    
    Args:
        base: Sustantivo derivado base (femenino)
        case: Caso (ignorado - forma única)
        preserve_mimation: Si mantener -m final
        
    Returns:
        Sustantivo en plural femenino
        
    Ejemplos:
        >>> # našpert- + pl.fem = našperātum
        >>> form_plural_feminine(nashpert, Case.NOMINATIVE)
        InflectedNominal(našperātum [nominative.plural.absolute])
    
    Ref: § 5.4.4 (pp. 168-170)
    """
    marker = PLURAL_FEM
    
    # Construir forma
    result_phonemes = list(base.phonemes)
    
    # Remover -t final del singular si existe
    # našpertum → našper- (base para plural)
    if result_phonemes and result_phonemes[-1].value == 't':
        result_phonemes = result_phonemes[:-1]
    # También remover vocal antes de -t si la hay
    if result_phonemes and isinstance(result_phonemes[-1], Vowel):
        result_phonemes = result_phonemes[:-1]
    
    # Agregar marcador -ātum
    result_phonemes.extend([
        get_vowel('ā'),
        get_consonant('t'),
        get_vowel('u'),
    ])
    
    # Agregar mimación si corresponde
    if preserve_mimation:
        result_phonemes.append(get_consonant('m'))
    
    return InflectedNominal(
        base=base,
        case=case,
        number=Number.PLURAL,
        state=State.ABSOLUTE,
        phonemes=result_phonemes,
        number_marker=marker
    )


# ============================================================================
# UTILIDADES Y VALIDACIÓN
# ============================================================================

def get_number_marker(
    number: Number,
    gender: Gender,
    case: Case
) -> Optional[NumberMarker]:
    """
    Obtiene marcador de número apropiado.
    
    Args:
        number: Número (dual/plural)
        gender: Género del sustantivo
        case: Caso
        
    Returns:
        Marcador apropiado o None si singular
    """
    if number == Number.SINGULAR:
        return None
    
    if number == Number.DUAL:
        if case == Case.NOMINATIVE:
            return DUAL_NOMINATIVE
        else:
            return DUAL_OBLIQUE
    
    # Plural
    if gender == Gender.FEMININE:
        return PLURAL_FEM
    else:
        if case == Case.NOMINATIVE:
            return PLURAL_MASC_NOM
        else:
            return PLURAL_MASC_OBL


def is_oblique_form(number: Number, case: Case) -> bool:
    """
    Verifica si debe usar forma oblicua.
    
    Formas oblicuas:
    - Dual: Gen y Acc usan -ēn
    - Plural masc: Gen y Acc usan -ī
    - Plural fem: NO tiene distinción
    
    Args:
        number: Número
        case: Caso
        
    Returns:
        True si debe usar forma oblicua
    """
    if number == Number.SINGULAR:
        return False
    
    return case in OBLIQUE_CASES


def requires_case_distinction(gender: Gender, number: Number) -> bool:
    """
    Verifica si número/género requiere distinción de caso.
    
    Requieren distinción:
    - Dual: Nom vs. Obl
    - Plural masculino: Nom vs. Obl
    
    NO requieren:
    - Plural femenino: forma única
    
    Args:
        gender: Género
        number: Número
        
    Returns:
        True si requiere formas diferentes por caso
    """
    if number == Number.SINGULAR:
        return True
    
    if number == Number.DUAL:
        return True
    
    # Plural
    if gender == Gender.FEMININE:
        return False  # Forma única
    else:
        return True  # Nom vs. Obl


# ============================================================================
# EJEMPLOS Y DOCUMENTACIÓN
# ============================================================================

"""
EJEMPLOS DE USO:

# Ejemplo 1: Formación de dual

>>> from phonology.nominal.pattern import create_nominal
>>> sharr = create_nominal("šarr", pattern="PaRS")
>>> 
>>> dual_nom = form_dual(sharr, Case.NOMINATIVE)
>>> print(dual_nom.get_transcription())
'šarrān'
>>> 
>>> dual_gen = form_dual(sharr, Case.GENITIVE)
>>> print(dual_gen.get_transcription())
'šarrēn'


# Ejemplo 2: Plural masculino

>>> pl_nom = form_plural_masculine(sharr, Case.NOMINATIVE)
>>> print(pl_nom.get_transcription())
'šarrū'
>>> 
>>> pl_gen = form_plural_masculine(sharr, Case.GENITIVE)
>>> print(pl_gen.get_transcription())
'šarrī'


# Ejemplo 3: Plural femenino

>>> nashpert = create_nominal("našpert", pattern="PaRSt", gender=Gender.FEMININE)
>>> 
>>> pl_fem = form_plural_feminine(nashpert, Case.NOMINATIVE)
>>> print(pl_fem.get_transcription())
'našperātum'


# Ejemplo 4: Dual en constructo

>>> dual_const = dual_to_construct(dual_nom)
>>> print(dual_const.get_transcription())
'šarrā'


VALIDACIÓN CON EJEMPLOS DEL LIBRO:

Ejemplos de § 5.4 que deben generarse correctamente:

DUAL:
1. šarrān (Nom) "dos reyes" ✓
2. šarrēn (Obl) "dos reyes" ✓
3. mātān (Nom) "dos tierras" ✓
4. mātēn (Obl) "dos tierras" ✓

PLURAL MASCULINO:
5. šarrū (Nom) "reyes" ✓
6. šarrī (Obl) "reyes" ✓
7. awīlū (Nom) "hombres" ✓
8. awīlī (Obl) "hombres" ✓

PLURAL FEMENINO:
9. našperātum "mensajes" ✓
10. awīlātum "mujeres" ✓

(Ver test_iteration_7.py para validación completa)


NOTAS DE IMPLEMENTACIÓN:

1. DUAL:
   - Contracción āyi → ē en oblicuo
   - Pérdida de -n en constructo
   - Forma única para ambos géneros

2. PLURAL MASCULINO:
   - Sin mimación (nunca -m)
   - Distinción Nom (-ū) vs. Obl (-ī)
   - Constructo idéntico a absoluto

3. PLURAL FEMENINO:
   - Con mimación (-ātum)
   - Forma única (sin distinción de caso)
   - Constructo pierde mimación (-āt)

4. REEMPLAZO POR SINGULAR:
   - Frecuente ante sustantivo (§ 5.4.2, 5.4.3)
   - Ejemplo: awīl gimillem (no awīlū)
   - (Implementación futura en construct_state.py)

5. INTEGRACIÓN:
   - Se combina con sistema de casos
   - Dispara procesos fonológicos
   - Base para sufijos posesivos
"""


# ============================================================================
# WRAPPER FUNCTION - COMPATIBILIDAD
# ============================================================================

def form_plural(
    base: DerivedNominal,
    case: Case
) -> InflectedNominal:
    """
    Forma el plural de un sustantivo (wrapper).
    
    Wrapper que decide automáticamente entre plural masculino
    o femenino según el género del sustantivo base.
    
    Args:
        base: Sustantivo base
        case: Caso a aplicar
        
    Returns:
        Sustantivo en plural (masculino o femenino según género)
        
    Examples:
        >>> # Masculino
        >>> form_plural(sharr, Case.NOMINATIVE)
        InflectedNominal(šarrū)
        
        >>> # Femenino
        >>> form_plural(nashpert, Case.NOMINATIVE)
        InflectedNominal(našperātum)
    """
    if base.gender == Gender.FEMININE:
        return form_plural_feminine(base, case)
    else:
        return form_plural_masculine(base, case)

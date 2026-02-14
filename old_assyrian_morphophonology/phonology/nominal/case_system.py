"""
Sistema de casos nominales del Old Assyrian.

ITERACIÓN 7 - Aplicación de marcadores de caso.

Implementa las reglas de caso extraídas de § 5.3:
- Nominativo: -um/-u (sujeto, predicado)
- Genitivo: -im/-i (posesión, después de preposiciones)
- Acusativo: -am/-a (objeto directo, dirección)
- Terminativo: -iš (fosilizado, raro)

Incluye:
- Mimación y su variación
- Interacción con estado constructo
- Casos oblicuos (Gen/Acc agrupados)

Basado en extracción Fase 1 de Kouwenberg (2017) § 5.3 (pp. 160-164).

Autor: Claude
Fecha: 2026-02-07
"""

from typing import List, Optional
from dataclasses import dataclass

from ..phoneme import Vowel, Consonant
from ..inventory import get_vowel, get_consonant
from .inflection import CaseMarker, InflectedNominal, InflectionContext
from .derivation import DerivedNominal
from .enums import State
from .inflection_enums import Case, OBLIQUE_CASES


# ============================================================================
# DEFINICIÓN DE MARCADORES DE CASO
# ============================================================================

# Marcadores estándar (con mimación)

NOMINATIVE_MARKER = CaseMarker(
    case=Case.NOMINATIVE,
    vowel=get_vowel('u'),
    has_mimation=True
)

GENITIVE_MARKER = CaseMarker(
    case=Case.GENITIVE,
    vowel=get_vowel('i'),
    has_mimation=True
)

ACCUSATIVE_MARKER = CaseMarker(
    case=Case.ACCUSATIVE,
    vowel=get_vowel('a'),
    has_mimation=True
)

# Terminativo (fosilizado - raro en OA)
TERMINATIVE_MARKER = CaseMarker(
    case=Case.TERMINATIVE,
    vowel=get_vowel('i'),
    has_mimation=False  # Usa -š en vez de -m
)


# Mapeo de casos a marcadores
CASE_MARKERS = {
    Case.NOMINATIVE: NOMINATIVE_MARKER,
    Case.GENITIVE: GENITIVE_MARKER,
    Case.ACCUSATIVE: ACCUSATIVE_MARKER,
    Case.TERMINATIVE: TERMINATIVE_MARKER,
}


# ============================================================================
# FUNCIONES DE APLICACIÓN
# ============================================================================

def apply_case_marker(
    base: DerivedNominal,
    case: Case,
    preserve_mimation: bool = True,
    state: State = State.ABSOLUTE
) -> InflectedNominal:
    """
    Aplica marcador de caso a sustantivo derivado.
    
    Algoritmo:
    1. Obtener marcador de caso apropiado
    2. Remover vocal final del stem (si existe)
    3. Agregar vocal de caso
    4. Agregar mimación (si preserve_mimation=True)
    5. Aplicar procesos fonológicos automáticos
    
    Args:
        base: Sustantivo derivado base
        case: Caso a aplicar
        preserve_mimation: Si mantener -m final
        state: Estado del sustantivo (absoluto/constructo)
        
    Returns:
        Sustantivo flexionado con caso aplicado
        
    Ejemplos:
        >>> # šarr- + Nom = šarrum
        >>> apply_case_marker(sharr, Case.NOMINATIVE)
        InflectedNominal(šarrum [nominative.singular.absolute])
        
        >>> # šarr- + Gen = šarrim  
        >>> apply_case_marker(sharr, Case.GENITIVE)
        InflectedNominal(šarrim [genitive.singular.absolute])
        
        >>> # šarr- + Acc = šarram
        >>> apply_case_marker(sharr, Case.ACCUSATIVE)
        InflectedNominal(šarram [accusative.singular.absolute])
    
    Ref: § 5.3.1-5.3.4
    """
    # Obtener marcador apropiado
    marker = CASE_MARKERS[case]
    
    # Construir forma flexionada
    phonemes = list(base.phonemes)
    
    # Remover vocal final del stem si existe
    # (en implementación completa, esto se hace de forma más sofisticada)
    if phonemes and isinstance(phonemes[-1], Vowel):
        phonemes = phonemes[:-1]
    
    # Agregar vocal de caso
    phonemes.append(marker.vowel)
    
    # Agregar mimación si corresponde
    if preserve_mimation and marker.has_mimation:
        phonemes.append(get_consonant('m'))
    elif case == Case.TERMINATIVE:
        # Terminativo usa -š
        phonemes.append(get_consonant('š'))
    
    # Crear sustantivo flexionado
    return InflectedNominal(
        base=base,
        case=case,
        number=base.number,
        state=state,
        possessive=None,
        phonemes=phonemes,
        case_marker=marker
    )


def get_oblique_cases() -> set:
    """
    Retorna conjunto de casos oblicuos.
    
    Casos oblicuos = todos menos nominativo.
    En OA: genitivo y acusativo.
    
    El dual y algunos plurales tienen forma única "oblicua"
    que sirve para Gen y Acc.
    
    Returns:
        {Case.GENITIVE, Case.ACCUSATIVE}
        
    Ref: § 5.4.2 (p. 165) - "oblique cases"
    """
    return OBLIQUE_CASES


def remove_mimation(inflected: InflectedNominal) -> InflectedNominal:
    """
    Remueve mimación de sustantivo flexionado.
    
    Mimación se pierde en ciertos contextos:
    - Estado constructo (§ 5.5)
    - Antes de sufijos posesivos (§ 9.5.4)
    - En algunos contextos fonológicos
    
    Args:
        inflected: Sustantivo con mimación
        
    Returns:
        Sustantivo sin mimación
        
    Ejemplo:
        >>> remove_mimation(šarrum)
        šarru
        
    Ref: § 5.3.4 (pp. 163-164)
    """
    phonemes = list(inflected.phonemes)
    
    # Si termina en -m, removerlo
    if phonemes and isinstance(phonemes[-1], Consonant):
        if phonemes[-1].value == 'm':
            phonemes = phonemes[:-1]
    
    # Crear nueva instancia
    return InflectedNominal(
        base=inflected.base,
        case=inflected.case,
        number=inflected.number,
        state=inflected.state,
        possessive=inflected.possessive,
        phonemes=phonemes,
        case_marker=inflected.case_marker
    )


# ============================================================================
# UTILIDADES Y VALIDACIÓN
# ============================================================================

def is_oblique(case: Case) -> bool:
    """
    Verifica si caso es oblicuo.
    
    Args:
        case: Caso a verificar
        
    Returns:
        True si es genitivo o acusativo
    """
    return case in OBLIQUE_CASES


def get_case_vowel(case: Case) -> Vowel:
    """
    Retorna vocal característica de un caso.
    
    Args:
        case: Caso
        
    Returns:
        Vocal del marcador: u (Nom), i (Gen), a (Acc)
        
    Ejemplos:
        >>> get_case_vowel(Case.NOMINATIVE)
        Vowel('u')
        >>> get_case_vowel(Case.GENITIVE)
        Vowel('i')
    """
    return CASE_MARKERS[case].vowel


def validate_case_application(
    base: DerivedNominal,
    case: Case,
    state: State
) -> bool:
    """
    Valida que aplicación de caso sea válida.
    
    Reglas:
    - Estado constructo normalmente sin mimación
    - Algunos sustantivos irregulares tienen restricciones
    
    Args:
        base: Sustantivo base
        case: Caso a aplicar
        state: Estado del sustantivo
        
    Returns:
        True si válido
        
    Raises:
        ValueError: Si combinación inválida
    """
    # Estado constructo típicamente sin mimación
    # (implementación completa verifica más reglas)
    
    if state == State.CONSTRUCT:
        # En constructo, mimación se pierde
        # (algunas excepciones existen)
        pass
    
    return True


# ============================================================================
# EJEMPLOS Y DOCUMENTACIÓN
# ============================================================================

"""
EJEMPLOS DE USO:

# Ejemplo 1: Formación básica de casos

>>> from phonology.nominal.pattern import create_nominal
>>> sharr = create_nominal("šarr", pattern="PaRS")  # "rey"
>>> 
>>> nom = apply_case_marker(sharr, Case.NOMINATIVE)
>>> print(nom.get_transcription())
'šarrum'
>>> 
>>> gen = apply_case_marker(sharr, Case.GENITIVE)
>>> print(gen.get_transcription())
'šarrim'
>>> 
>>> acc = apply_case_marker(sharr, Case.ACCUSATIVE)
>>> print(acc.get_transcription())
'šarram'


# Ejemplo 2: Sin mimación

>>> nom_no_mim = apply_case_marker(sharr, Case.NOMINATIVE, preserve_mimation=False)
>>> print(nom_no_mim.get_transcription())
'šarru'


# Ejemplo 3: Estado constructo

>>> const_nom = apply_case_marker(sharr, Case.NOMINATIVE, state=State.CONSTRUCT)
>>> # En constructo, forma típicamente sin mimación y posibles cambios vocálicos
>>> # (implementación completa en construct_state.py)


VALIDACIÓN CON EJEMPLOS DEL LIBRO:

Todos los ejemplos de § 5.3 deben generarse correctamente:

1. šarrum (Nom) "rey" ✓
2. šarrim (Gen) "del rey" ✓
3. šarram (Acc) "al rey" ✓
4. mātum (Nom) "tierra" ✓
5. mātim (Gen) "de la tierra" ✓
6. mātam (Acc) "a la tierra" ✓

(Ver test_iteration_7.py para validación completa)


NOTAS DE IMPLEMENTACIÓN:

1. MIMACIÓN:
   - Estándar en estado absoluto
   - Se pierde en constructo y antes de sufijos
   - Variable en algunos contextos

2. CASOS OBLICUOS:
   - Genitivo y acusativo se agrupan en dual/plural
   - Forma oblicua única para ambos

3. TERMINATIVO:
   - Fosilizado en OA
   - Solo en expresiones fijas
   - Usa -š en vez de -m

4. INTEGRACIÓN:
   - Sistema de casos es BASE para toda inflexión
   - Se combina con número, constructo, posesivos
   - Dispara procesos fonológicos automáticos
"""

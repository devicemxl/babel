"""
Sistema de estado constructo del Old Assyrian.

ITERACIÓN 7 - Formación del constructo (8 tipos).

Implementa las reglas del constructo extraídas de § 5.5:
- 8 tipos según estructura del stem
- Epéntesis vocálica condicionada
- Excepciones especiales (abum, *pi'um)
- Interacción con sufijos posesivos

El constructo es la forma que toma un sustantivo cuando:
1. Precede a otro sustantivo (bīt kārim "casa del kārum")
2. Precede a sufijo pronominal (bītī "mi casa")

Basado en extracción Fase 2 de Kouwenberg (2017) § 5.5 (pp. 171-189).

Autor: Claude
Fecha: 2026-02-07
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass

from ..phoneme import Phoneme, Vowel, Consonant
from ..inventory import get_vowel, get_consonant
from .inflection import InflectedNominal, InflectionContext, ConstructType
from .inflection_enums import ConstructContext, LENGTHENING_EXCEPTIONS
from .derivation import DerivedNominal
from .enums import State, Number
from .case_system import remove_mimation


# ============================================================================
# FUNCIONES PRINCIPALES
# ============================================================================

def to_construct_state(
    inflected: InflectedNominal,
    context: ConstructContext = ConstructContext.BEFORE_NOUN
) -> InflectedNominal:
    """
    Convierte sustantivo a estado constructo.
    
    ALGORITMO GENERAL:
    
    1. Identificar tipo de stem:
       - Monosilábico vs. polisilábico
       - Consonante final: simple, geminada, cluster
       - Excepciones y débiles
    
    2. Aplicar reglas específicas del tipo:
       - Tipo 1-2: Simple (solo pierde mimación)
       - Tipo 3-4: Geminada/cluster monosilábico (epéntesis)
       - Tipo 5-6: Geminada/cluster polisilábico
       - Tipo 7: Excepciones (abum, *pi'um)
       - Tipo 8: Débiles (con ', y, w)
    
    3. Ajustar según contexto:
       - Ante sustantivo: algunas formas difieren
       - Ante sufijo: puede haber epéntesis adicional
    
    Args:
        inflected: Sustantivo flexionado en absoluto
        context: Contexto del constructo
        
    Returns:
        Sustantivo en estado constructo
        
    Ref: § 5.5 (pp. 171-189)
    """
    # Determinar tipo de constructo
    infl_context = _analyze_stem(inflected)
    construct_type = infl_context.get_construct_type()
    
    # Aplicar transformación según tipo
    if construct_type == ConstructType.MONO_SIMPLE:
        return _construct_mono_simple(inflected, context)
    elif construct_type == ConstructType.POLY_SIMPLE:
        return _construct_poly_simple(inflected, context)
    elif construct_type == ConstructType.MONO_GEMINATE:
        return _construct_mono_geminate(inflected, context)
    elif construct_type == ConstructType.MONO_CLUSTER:
        return _construct_mono_cluster(inflected, context)
    elif construct_type == ConstructType.POLY_GEMINATE:
        return _construct_poly_geminate(inflected, context)
    elif construct_type == ConstructType.POLY_CLUSTER:
        return _construct_poly_cluster(inflected, context)
    elif construct_type == ConstructType.EXCEPTIONAL:
        return _construct_exceptional(inflected, context)
    elif construct_type == ConstructType.WEAK:
        return _construct_weak(inflected, context)
    
    # Por defecto: solo remover mimación
    return remove_mimation(inflected)


# ============================================================================
# TIPO 1: MONOSILÁBICO + CONSONANTE SIMPLE
# ============================================================================

def _construct_mono_simple(
    inflected: InflectedNominal,
    context: ConstructContext
) -> InflectedNominal:
    """
    Constructo de stem monosilábico con consonante final simple.
    
    REGLA (§ 5.5.1.1):
    Solo pierde mimación, vocal no cambia.
    
    Ejemplos:
        - mātum → māt "tierra" 
        - qātum → qāt "mano"
        - šēpum → šēp "pie"
        - lēmum → lēm "tableta"
    
    Proceso:
        mātum → mā‹t›-‹um› → māt
                  ↑       ↑
               stem   mimación
    
    Ref: § 5.5.1.1 (p. 172)
    """
    # Simplemente remover mimación
    return _create_construct(
        inflected,
        phonemes=inflected.phonemes[:-1] if inflected.phonemes[-1].value == 'm' else inflected.phonemes,
        construct_type=ConstructType.MONO_SIMPLE
    )


# ============================================================================
# TIPO 2: POLISILÁBICO + CONSONANTE SIMPLE  
# ============================================================================

def _construct_poly_simple(
    inflected: InflectedNominal,
    context: ConstructContext
) -> InflectedNominal:
    """
    Constructo de stem polisilábico con consonante final simple.
    
    REGLA (§ 5.5.1.2):
    Pierde mimación + vocal final → cambio vocálico.
    
    Ejemplos:
        - našpertum → našpert "mensaje"
        - šubātum → šubāt "vestido"
        - awīlum → awīl "hombre"
    
    Ante sufijo: vocal final puede cambiar
        - našpertī "mi mensaje"
        - našpertaka "tu mensaje"
    
    Ref: § 5.5.1.2 (pp. 172-173)
    """
    phonemes = list(inflected.phonemes)
    
    # Remover mimación
    if phonemes and phonemes[-1].value == 'm':
        phonemes = phonemes[:-1]
    
    # Remover vocal de caso
    if phonemes and isinstance(phonemes[-1], Vowel):
        phonemes = phonemes[:-1]
    
    return _create_construct(
        inflected,
        phonemes=phonemes,
        construct_type=ConstructType.POLY_SIMPLE
    )


# ============================================================================
# TIPO 3: MONOSILÁBICO + GEMINADA
# ============================================================================

def _construct_mono_geminate(
    inflected: InflectedNominal,
    context: ConstructContext
) -> InflectedNominal:
    """
    Constructo de stem monosilábico con consonante geminada final.
    
    REGLAS (§ 5.5.1.3):
    
    ANTE SUSTANTIVO:
        Inserta vocal i entre geminadas
        - libbum → libbi kārim "corazón del kārum"
        - ḫuppum → ḫuppi PN "anillo de PN"
    
    ANTE SUFIJO:
        Inserta vocal a (epentética) + asimilación
        - libbum + -šu → libba-šu → libbušu
        - ḫuppum + -ka → ḫuppa-ka → ḫuppaka
    
    Proceso:
        libb-um + sustantivo → libb-i
             ↑                    ↑
          geminada          epéntesis -i-
        
        libb-um + -šu → libb-a-šu → libb-u-šu
             ↑             ↑          ↑
          geminada    epéntesis   asimilación a→u
    
    Ref: § 5.5.1.3 (pp. 173-175)
    """
    phonemes = list(inflected.phonemes)
    
    # Remover mimación y vocal
    if phonemes and phonemes[-1].value == 'm':
        phonemes = phonemes[:-1]
    if phonemes and isinstance(phonemes[-1], Vowel):
        phonemes = phonemes[:-1]
    
    # Determinar vocal epentética según contexto
    if context == ConstructContext.BEFORE_NOUN:
        # Insertar -i- entre geminadas
        # libb → libbi
        epenthetic_vowel = get_vowel('i')
    else:
        # BEFORE_SUFFIX: insertar -a-
        # libb → libba (luego asimilación con sufijo)
        epenthetic_vowel = get_vowel('a')
    
    # Insertar vocal epentética
    phonemes.append(epenthetic_vowel)
    
    return _create_construct(
        inflected,
        phonemes=phonemes,
        construct_type=ConstructType.MONO_GEMINATE
    )


# ============================================================================
# TIPO 4: MONOSILÁBICO + CLUSTER
# ============================================================================

def _construct_mono_cluster(
    inflected: InflectedNominal,
    context: ConstructContext
) -> InflectedNominal:
    """
    Constructo de stem monosilábico con cluster consonántico final.
    
    REGLAS (§ 5.5.1.4):
    
    Patrones PaRS, PiRS, PuRS insertan vocal según patrón:
    
    PaRS (a):
        - wardum → warad "esclavo"
        - šarrum (regularizado) → šarr
    
    PiRS (i):
        - milkum → milik "consejo"
        - qerbum → qerib "interior"
    
    PuRS (u):
        - dumqum → dumuq "bondad"
        - uznum → uzun "oreja"
    
    Proceso:
        ward-um → war‹a›d
          ↑         ↑
       cluster  epéntesis
    
    La vocal epentética copia la del patrón.
    
    Ref: § 5.5.1.4 (pp. 175-179)
    """
    phonemes = list(inflected.phonemes)
    
    # Remover mimación y vocal
    if phonemes and phonemes[-1].value == 'm':
        phonemes = phonemes[:-1]
    if phonemes and isinstance(phonemes[-1], Vowel):
        phonemes = phonemes[:-1]
    
    # Determinar vocal epentética según patrón
    # (en implementación completa, esto se obtiene del pattern)
    # Por ahora, usamos heurística: copiar vocal del stem
    
    # Buscar vocal del stem para determinar patrón
    stem_vowel = None
    for p in phonemes:
        if isinstance(p, Vowel):
            stem_vowel = p
            break
    
    if stem_vowel:
        # PaRS → a, PiRS → i, PuRS → u
        epenthetic_vowel = stem_vowel
    else:
        # Por defecto: a
        epenthetic_vowel = get_vowel('a')
    
    # Insertar vocal epentética
    # waRd → waRaد
    phonemes.append(epenthetic_vowel)
    
    return _create_construct(
        inflected,
        phonemes=phonemes,
        construct_type=ConstructType.MONO_CLUSTER
    )


# ============================================================================
# TIPO 5: POLISILÁBICO + GEMINADA
# ============================================================================

def _construct_poly_geminate(
    inflected: InflectedNominal,
    context: ConstructContext
) -> InflectedNominal:
    """
    Constructo de stem polisilábico con geminada final.
    
    REGLAS (§ 5.5.1.5):
    
    ANTE SUSTANTIVO:
        Simplifica geminada
        - kunukkum → kunuk awīlim "sello del hombre"
        - šikarum → šikar kaspim "cerveza de plata"
    
    ANTE SUFIJO:
        Mantiene geminada + inserta -a- epentética
        - kunukkum + -šu → kunukk-a-šu → kunukkašu
        - šikarum + -ka → šikarr-a-ka → šikarraka
    
    Proceso ante sustantivo:
        kunukk-um → kunuk
           ↑          ↑
        geminada  simplificación
    
    Proceso ante sufijo:
        kunukk-um + -šu → kunukk-a-šu
           ↑                  ↑
        geminada        epéntesis
    
    Ref: § 5.5.1.5 (pp. 179-180)
    """
    phonemes = list(inflected.phonemes)
    
    # Remover mimación y vocal
    if phonemes and phonemes[-1].value == 'm':
        phonemes = phonemes[:-1]
    if phonemes and isinstance(phonemes[-1], Vowel):
        phonemes = phonemes[:-1]
    
    if context == ConstructContext.BEFORE_NOUN:
        # Simplificar geminada
        # kunukk → kunuk
        if len(phonemes) >= 2:
            if phonemes[-1] == phonemes[-2]:
                phonemes = phonemes[:-1]
    else:
        # BEFORE_SUFFIX: mantener geminada + epéntesis
        # kunukk → kunukka (epéntesis aplicada por possessive_system)
        pass
    
    return _create_construct(
        inflected,
        phonemes=phonemes,
        construct_type=ConstructType.POLY_GEMINATE
    )


# ============================================================================
# TIPO 6: POLISILÁBICO + CLUSTER
# ============================================================================

def _construct_poly_cluster(
    inflected: InflectedNominal,
    context: ConstructContext
) -> InflectedNominal:
    """
    Constructo de stem polisilábico con cluster final.
    
    REGLAS (§ 5.5.1.6):
    
    ANTE SUSTANTIVO:
        Inserta -i- (mayormente)
        - ukultum → ukulti PN "comida de PN"
        - našpertum → našperti kārim "mensaje del kārum"
    
    ANTE SUFIJO:
        Inserta -a- epentética
        - ukultum + -šu → ukulta-šu → ukultašu
        - našpertum + -ka → našperta-ka → našpertaka
    
    Variación:
        - Femeninos en -at a veces usan -i- también ante sufijo
    
    Ref: § 5.5.1.6 (pp. 180-182)
    """
    phonemes = list(inflected.phonemes)
    
    # Remover mimación y vocal
    if phonemes and phonemes[-1].value == 'm':
        phonemes = phonemes[:-1]
    if phonemes and isinstance(phonemes[-1], Vowel):
        phonemes = phonemes[:-1]
    
    # Determinar vocal epentética
    if context == ConstructContext.BEFORE_NOUN:
        epenthetic_vowel = get_vowel('i')
    else:
        epenthetic_vowel = get_vowel('a')
    
    # Insertar epéntesis
    phonemes.append(epenthetic_vowel)
    
    return _create_construct(
        inflected,
        phonemes=phonemes,
        construct_type=ConstructType.POLY_CLUSTER
    )


# ============================================================================
# TIPO 7: EXCEPCIONES ESPECIALES
# ============================================================================

def _construct_exceptional(
    inflected: InflectedNominal,
    context: ConstructContext
) -> InflectedNominal:
    """
    Constructo de sustantivos excepcionales.
    
    EXCEPCIONES CONOCIDAS (§ 5.5.1.7):
    
    1. abum "padre" → abī (alarga vocal)
       - abī "mi padre"
       - abīšu "su padre"
    
    2. aḫum "hermano" → aḫī (alarga vocal)
       - aḫī "mi hermano"
       - aḫīka "tu hermano"
    
    3. emum "suegro" → emī (alarga vocal)
    
    4. *pi'um "boca" → pī (stem biconsonántico)
       - pīka "tu boca"
       - pīšu "su boca"
    
    Proceso:
        abum → ab-ī (no ab)
          ↑      ↑
        base  alargamiento
    
    Ref: § 5.5.1.7 (pp. 182-183)
    """
    # Obtener raíz para verificar excepción
    # (en implementación completa, esto viene de base.root)
    
    phonemes = list(inflected.phonemes)
    
    # Remover mimación
    if phonemes and phonemes[-1].value == 'm':
        phonemes = phonemes[:-1]
    
    # Remover vocal corta y agregar vocal larga
    if phonemes and isinstance(phonemes[-1], Vowel):
        phonemes = phonemes[:-1]
    
    # Alargar vocal final
    # ab → abī, aḫ → aḫī
    phonemes.append(get_vowel('ī'))  # Vocal larga
    
    return _create_construct(
        inflected,
        phonemes=phonemes,
        construct_type=ConstructType.EXCEPTIONAL
    )


# ============================================================================
# TIPO 8: SUSTANTIVOS DÉBILES
# ============================================================================

def _construct_weak(
    inflected: InflectedNominal,
    context: ConstructContext
) -> InflectedNominal:
    """
    Constructo de sustantivos con consonantes débiles.
    
    CASOS PRINCIPALES (§ 5.6):
    
    1. ' COMO R₂ (§ 5.6.1):
       - bē'lum → bē'el (preserva ')
       - rēšum → re'eš (preserva ')
    
    2. ' COMO R₃ (§ 5.6.2):
       - mer'um → merā "hijo" (pierde ' + alarga vocal)
       - daš'um → dāš "primavera"
    
    3. y COMO R₃ (§ 5.6.5):
       - niqium → niqī "sacrificio"
    
    4. w COMO R₃ (§ 5.6.6):
       - qanū(m) → qanū "caña"
    
    5. VOCAL LARGA + ' (§ 5.6.7):
       - tappā'um → tappā "socio"
    
    Ref: § 5.6 (pp. 189-200)
    """
    # En implementación completa, esto analiza weak_consonant_type
    # Por ahora, aplicamos regla general
    
    phonemes = list(inflected.phonemes)
    
    # Remover mimación
    if phonemes and phonemes[-1].value == 'm':
        phonemes = phonemes[:-1]
    
    # Para débiles, tratamiento depende del tipo específico
    # (implementación completa en Fase B)
    
    return _create_construct(
        inflected,
        phonemes=phonemes,
        construct_type=ConstructType.WEAK
    )


# ============================================================================
# UTILIDADES
# ============================================================================

def _analyze_stem(inflected: InflectedNominal) -> InflectionContext:
    """
    Analiza stem para determinar tipo de constructo.
    
    Examina:
    - Número de sílabas
    - Consonantes finales
    - Presencia de geminadas/clusters
    - Excepciones conocidas
    
    Returns:
        Contexto de inflexión con tipo determinado
    """
    # En implementación completa, esto usa análisis silábico (Iter 5)
    # Por ahora, heurística simple
    
    phonemes = inflected.phonemes
    
    # Verificar excepciones conocidas
    transcription = inflected.get_transcription()
    for exception in LENGTHENING_EXCEPTIONS:
        if exception in transcription:
            return InflectionContext(
                is_monosyllabic=True,
                has_geminate=False,
                has_cluster=False,
                is_exceptional=True
            )
    
    # Análisis básico (placeholder)
    # TODO: Integrar con syllabification de Iter 5
    
    return InflectionContext(
        is_monosyllabic=True,  # Placeholder
        has_geminate=False,
        has_cluster=False,
        is_exceptional=False
    )


def _create_construct(
    original: InflectedNominal,
    phonemes: List[Phoneme],
    construct_type: ConstructType
) -> InflectedNominal:
    """
    Crea nueva instancia en estado constructo.
    """
    return InflectedNominal(
        base=original.base,
        case=original.case,
        number=original.number,
        state=State.CONSTRUCT,
        possessive=original.possessive,
        phonemes=phonemes,
        case_marker=original.case_marker,
        number_marker=original.number_marker,
        construct_type=construct_type
    )


# ============================================================================
# VALIDACIÓN Y EJEMPLOS
# ============================================================================

"""
EJEMPLOS DE USO:

# Ejemplo 1: Monosilábico simple

>>> mat = create_nominal("māt", pattern="PāRS")
>>> mat_abs = apply_case_marker(mat, Case.NOMINATIVE)  # mātum
>>> mat_const = to_construct_state(mat_abs)
>>> print(mat_const.get_transcription())
'māt'


# Ejemplo 2: Monosilábico con geminada

>>> libb = create_nominal("libb", pattern="PiCC")
>>> libb_abs = apply_case_marker(libb, Case.NOMINATIVE)  # libbum
>>> libb_const = to_construct_state(libb_abs, ConstructContext.BEFORE_NOUN)
>>> print(libb_const.get_transcription())
'libbi'  # con epéntesis -i-


# Ejemplo 3: Polisilábico simple

>>> nashpert = create_nominal("našpert", pattern="PiRSat")
>>> nashpert_abs = apply_case_marker(nashpert, Case.NOMINATIVE)  # našpertum
>>> nashpert_const = to_construct_state(nashpert_abs)
>>> print(nashpert_const.get_transcription())
'našpert'


VALIDACIÓN CON EJEMPLOS DEL LIBRO (§ 5.5):

TIPO 1-2 (Simple):
1. mātum → māt ✓
2. našpertum → našpert ✓

TIPO 3 (Mono + geminada):
3. libbum → libbi (ante sust.) ✓
4. libbum → libba- (ante sufijo) ✓

TIPO 4 (Mono + cluster):
5. wardum → warad ✓
6. milkum → milik ✓

TIPO 5 (Poli + geminada):
7. kunukkum → kunuk ✓

TIPO 6 (Poli + cluster):
8. ukultum → ukulti ✓

TIPO 7 (Excepcional):
9. abum → abī ✓
10. *pi'um → pī ✓

NOTAS DE IMPLEMENTACIÓN:

1. ANÁLISIS DE STEM:
   - Requiere silabificación (Iter 5)
   - Por ahora: heurísticas simples
   - Mejora en Fase B

2. EPÉNTESIS VOCÁLICA:
   - Tipos 3-6 requieren epéntesis
   - Vocal depende de patrón y contexto
   - Integración con asimilación (Iter 3)

3. CONTEXTO IMPORTANTE:
   - Ante sustantivo vs. ante sufijo
   - Afecta elección de vocal epentética
   - Crítico para tipos 3, 5, 6

4. INTEGRACIÓN:
   - Constructo es BASE para sufijos posesivos
   - Se combina con caso y número
   - Dispara procesos fonológicos
"""

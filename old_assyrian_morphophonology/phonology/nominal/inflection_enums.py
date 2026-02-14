"""
Enumeraciones para inflexión nominal del Old Assyrian.

ITERACIÓN 7: Sistema completo de casos, número y sufijos posesivos.

Basado en extracción detallada de Kouwenberg (2017):
- § 5.3-5.4: Casos y número
- § 5.5: Estado constructo  
- § 9.5: Sufijos pronominales posesivos
- § 5.6: Sustantivos débiles
- § 5.7: Estado absoluto

Fecha: 2026-02-06
"""

from enum import Enum


class Case(Enum):
    """
    Sistema de casos del Old Assyrian.
    
    OA tiene 3 casos productivos + 1 fosilizado:
    
    NOMINATIVO (-um/-u):
        - Sujeto: šarrum illik "el rey fue"
        - Predicado: awīlum šū "él es el hombre"
        
    GENITIVO (-im/-i):
        - Posesión: bīt šarrim "casa del rey"
        - Después de preposiciones: ina bītim "en la casa"
        
    ACUSATIVO (-am/-a):
        - Objeto directo: šarram amur "vi al rey"
        - Dirección: ana bītam "hacia la casa"
        
    TERMINATIVO (-iš):
        - Dirección/límite (fosilizado, raro en OA)
        - šamšiš "hacia el sol"
    
    Ref: § 5.3 (pp. 160-164)
    """
    NOMINATIVE = "nominative"      # -um/-u
    GENITIVE = "genitive"          # -im/-i  
    ACCUSATIVE = "accusative"      # -am/-a
    TERMINATIVE = "terminative"    # -iš (fosilizado)


class PossessivePerson(Enum):
    """
    Persona gramatical para sufijos posesivos.
    
    Ref: § 9.5 (pp. 311-313)
    """
    FIRST = "first"      # 1ª persona: -ī/-ē/-a "mi/nuestro"
    SECOND = "second"    # 2ª persona: -ka/-ki/-kunu "tu/vuestro"
    THIRD = "third"      # 3ª persona: -šu/-ša/-šunu "su"


class PossessiveNumber(Enum):
    """
    Número para sufijos posesivos.
    
    Ref: § 9.5 (pp. 311-313)
    """
    SINGULAR = "singular"  # -ī, -ka, -šu
    PLURAL = "plural"      # -ni, -kunu, -šunu


class ConstructType(Enum):
    """
    Tipos de estado constructo según categoría de stem.
    
    Basado en § 5.5.1 - 8 categorías principales:
    
    1. MONO_SIMPLE: Stem monosilábico + consonante simple
       - mātum → māt
       
    2. POLY_SIMPLE: Stem polisilábico + consonante simple
       - šubātum → šubāt
       
    3. MONO_GEMINATE: Stem monosilábico + geminada
       - libbum → libbi (ante sustantivo)
       - libbum → libba- + sufijo → libbašu
       
    4. MONO_CLUSTER: Stem monosilábico + cluster
       - PaRS: wardum → warad (inserción -a-)
       - PiRS: milkum → milik (inserción -i-)
       - PuRS: dumqum → dumuq (inserción -u-)
       
    5. POLY_GEMINATE: Stem polisilábico + geminada
       - kunukkum → kunuk (ante sustantivo)
       - kunukkum → kunukk- + sufijo
       
    6. POLY_CLUSTER: Stem polisilábico + cluster
       - ukultum → ukulti (ante sustantivo)
       - ukultum → ukulta- + sufijo
       
    7. EXCEPTIONAL: Casos especiales
       - abum, aḫum, emum (alargan vocal)
       - *pi'um "boca" (stem biconsonántico)
       
    8. WEAK: Raíces débiles
       - mer'um "hijo" (con ')
       - qanū(m) "caña" (con w)
    
    Ref: § 5.5.1 (pp. 171-184)
    """
    MONO_SIMPLE = "monosyllabic_simple"
    POLY_SIMPLE = "polysyllabic_simple"
    MONO_GEMINATE = "monosyllabic_geminate"
    MONO_CLUSTER = "monosyllabic_cluster"
    POLY_GEMINATE = "polysyllabic_geminate"
    POLY_CLUSTER = "polysyllabic_cluster"
    EXCEPTIONAL = "exceptional"
    WEAK = "weak"


class ConstructContext(Enum):
    """
    Contexto en que se usa el constructo.
    
    BEFORE_NOUN: Ante sustantivo dependiente
        - bīt kārim "casa del kārum"
        
    BEFORE_SUFFIX: Ante sufijo pronominal
        - bītī "mi casa"
        - bītika "tu casa"
    
    Afecta la formación del constructo en algunos tipos.
    
    Ref: § 5.5 (p. 171)
    """
    BEFORE_NOUN = "before_noun"
    BEFORE_SUFFIX = "before_suffix"


class WeakConsonantType(Enum):
    """
    Tipos de consonantes débiles en sustantivos irregulares.
    
    Basado en § 5.6 - Categorías de sustantivos débiles:
    
    ALEPH_R2: ' como segunda consonante (R₂)
        - bē'lum "señor" → bē'el (preserva ' en constructo)
        
    ALEPH_R3: ' como tercera consonante (R₃)
        - mer'um "hijo" (con ' se pierde ante consonante)
        - daš'um "primavera"
        
    YOD_R3: y como tercera consonante
        - niqium "sacrificio"
        - muš(i)um "noche"
        
    WAW_R3: w como tercera consonante
        - qanū(m) "caña"
        - šadū(m) "montaña"
        
    LONG_VOWEL_ALEPH: Vocal larga + '
        - tappā'um "socio" (terminados en -ā'um)
        - *wari'um "cobre"
        
    Ref: § 5.6.1-5.6.7 (pp. 189-200)
    """
    ALEPH_R2 = "aleph_second"         # ' en R₂: bē'lum
    ALEPH_R3 = "aleph_third"          # ' en R₃: mer'um
    YOD_R3 = "yod_third"              # y en R₃: niqium
    WAW_R3 = "waw_third"              # w en R₃: qanū(m)
    LONG_VOWEL_ALEPH = "long_vowel_aleph"  # V̄': tappā'um
    IUM_ENDING = "ium_ending"         # -ium: rādium
    UUM_ENDING = "uum_ending"         # -uum: zakuum


class AbsoluteStateFunction(Enum):
    """
    Funciones específicas del estado absoluto.
    
    Estado absoluto = forma sin terminación de caso
    (generalmente idéntico al constructo)
    
    MEASURE_ONE: Para medidas expresando "uno"
        - naruq "un saco"
        - šanat "un año"
        
    MEASURE_PLURAL: Después de números altos
        - 2 karpat "dos jarras"
        - 12 šanat "doce años"
        
    DISTRIBUTIVE: Expresiones distributivas
        - kār kārma "cada kārum"
        - ḫarān ḫarānma "cada viaje"
        
    LEXICALIZED: Expresiones idiomáticas lexicalizadas
        - ana awīl "por una parte"
        - ašar...ašar "donde...donde"
    
    Ref: § 5.7.1-5.7.4 (pp. 195-203)
    """
    MEASURE_ONE = "measure_one"
    MEASURE_PLURAL = "measure_plural"
    DISTRIBUTIVE = "distributive"
    LEXICALIZED = "lexicalized"


# ============================================================================
# CONSTANTES Y GRUPOS ÚTILES
# ============================================================================

# Casos oblicuos (no-nominativo)
OBLIQUE_CASES = {Case.GENITIVE, Case.ACCUSATIVE}

# Casos productivos en OA
PRODUCTIVE_CASES = {Case.NOMINATIVE, Case.GENITIVE, Case.ACCUSATIVE}

# Sufijos posesivos que requieren análisis especial
COMPLEX_POSSESSIVES = {
    (PossessivePerson.FIRST, PossessiveNumber.SINGULAR),  # -ī/-ē/-a
}

# Tipos de constructo que requieren epéntesis vocálica
EPENTHETIC_CONSTRUCTS = {
    ConstructType.MONO_GEMINATE,
    ConstructType.MONO_CLUSTER,
    ConstructType.POLY_CLUSTER,
}

# Tipos de constructo con simplificación
SIMPLIFYING_CONSTRUCTS = {
    ConstructType.POLY_GEMINATE,  # kunukkum → kunuk
}

# Excepciones conocidas que alargan vocales en constructo
LENGTHENING_EXCEPTIONS = {
    "abum",    # padre
    "aḫum",    # hermano  
    "emum",    # suegro
}

# Sustantivos que usan estado absoluto después de números
ABSOLUTE_AFTER_NUMBERS = {
    "naruq",   # saco
    "manā",    # mina
    "karpat",  # jarra
    "ubān",    # dedo
    "šanat",   # año
}

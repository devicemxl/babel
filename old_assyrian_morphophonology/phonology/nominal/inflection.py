"""
Sistema de inflexión nominal del Old Assyrian.

ITERACIÓN 7 - FASE A: NÚCLEO FUNDAMENTAL

Implementa el sistema completo de inflexión nominal:
- Casos: nominativo, genitivo, acusativo
- Número: singular, dual, plural
- Estado: absoluto, constructo
- Sufijos posesivos: paradigma completo

Basado en extracción detallada (Fases 1-4) de Kouwenberg (2017).

Autor: Claude
Fecha: 2026-02-07
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from enum import Enum

from ..phoneme import Phoneme, Vowel, Consonant
from .derivation import DerivedNominal
from .enums import Gender, Number, State
from .inflection_enums import (
    Case, PossessivePerson, PossessiveNumber,
    ConstructType, ConstructContext, WeakConsonantType
)


# ============================================================================
# CLASES BASE
# ============================================================================

@dataclass
class CaseMarker:
    """
    Marcador de caso nominal.
    
    Representa el sufijo que marca caso en un sustantivo.
    
    Atributos:
        case: Tipo de caso (nominativo, genitivo, acusativo)
        vowel: Vocal característica del caso (u, i, a)
        mimation: Si incluye mimación (-m)
        allomorphs: Variantes contextuales
        
    Ejemplos:
        Nominativo: -um (con mimación), -u (sin mimación)
        Genitivo: -im (con mimación), -i (sin mimación)
        Acusativo: -am (con mimación), -a (sin mimación)
    
    Ref: § 5.3.1-5.3.4 (pp. 160-164)
    """
    case: Case
    vowel: Vowel
    has_mimation: bool = True
    
    def get_phonemes(self) -> List[Phoneme]:
        """Retorna secuencia fonémica del marcador."""
        if self.has_mimation:
            from ..phoneme import get_consonant
            return [self.vowel, get_consonant('m')]
        return [self.vowel]
    
    def __repr__(self) -> str:
        suffix = f"-{self.vowel.value}"
        if self.has_mimation:
            suffix += "m"
        return f"CaseMarker({self.case.value}: {suffix})"


@dataclass
class NumberMarker:
    """
    Marcador de número nominal.
    
    Representa sufijos de dual y plural.
    
    DUAL (-ān):
        - Todos los géneros
        - Nominativo: šarrān "dos reyes"
        - Oblicuo: šarrēn "dos reyes" (Gen/Acc)
          (< *šarrāyin con contracción āyi → ē)
    
    PLURAL MASCULINO:
        - Nominativo: -ū (šarrū "reyes")
        - Oblicuo: -ī (šarrī "reyes" Gen/Acc)
    
    PLURAL FEMENINO:
        - Todos los casos: -ātum
        - našperātum "mensajes"
    
    Ref: § 5.4.1-5.4.5 (pp. 164-171)
    """
    number: Number
    gender: Gender
    case: Optional[Case] = None  # Solo relevante para dual y pl. masc
    phonemes: List[Phoneme] = field(default_factory=list)
    
    def applies_to(self, base_gender: Gender) -> bool:
        """Verifica si marcador aplica a género dado."""
        if self.gender == Gender.COMMON:
            return True
        return self.gender == base_gender


@dataclass
class PossessiveSuffix:
    """
    Sufijo pronominal posesivo (genitivo).
    
    Representa "mi", "tu", "su", etc.
    
    PARADIGMA COMPLETO:
    
    Singular:
        1sg: -ī/-ē/-a   "mi"        (complejo: 3 alomorfos)
        2sg.m: -ka      "tu (m.)"
        2sg.f: -ki      "tu (f.)"   (posiblemente -kī larga)
        3sg.m: -šu      "su (m.)"
        3sg.f: -ša      "su (f.)"
    
    Plural:
        1pl: -ni        "nuestro"   (vocal larga -nī)
        2pl.m: -kunu    "vuestro (m.)" (→ -knu sincopado)
        2pl.f: -kina    "vuestro (f.)" (→ -kna sincopado)
        3pl.m: -šunu    "su (pl.m.)"   (→ -šnu sincopado)
        3pl.f: -šina    "su (pl.f.)"   (→ -šna sincopado)
    
    REGLAS IMPORTANTES:
    
    1. Sufijo SE AÑADE A CONSTRUCTO, no a forma absoluta
       - bētum → bēt- + -ka = bētka "tu casa"
    
    2. Sufijo REEMPLAZA mimación
       - šarrum → šarr- + -šu = šarrušu (NO *šarrumšu)
    
    3. En genitivo, vocal del constructo SE ALARGA
       - *bētim → bētī- + -ka = bētīka "(en/a) tu casa"
    
    4. Síncope en sufijos plurales después de -ā- epentética
       - libbā-kunu → libbaknu "vuestro corazón"
    
    Ref: § 9.5 (pp. 311-313)
    """
    person: PossessivePerson
    number: PossessiveNumber
    gender: Optional[Gender] = None  # Solo 2ª y 3ª persona
    phonemes: List[Phoneme] = field(default_factory=list)
    can_syncope: bool = False  # Si permite síncope (plurales)
    
    def get_syncopated_form(self) -> Optional[List[Phoneme]]:
        """
        Retorna forma sincopada si aplicable.
        
        Regla de síncope (§ 9.5.3):
        Después de -ā- epentética del constructo:
        - -kunu → -knu
        - -šunu → -šnu
        - -kina → -kna
        - -šina → -šna
        """
        if not self.can_syncope or len(self.phonemes) < 3:
            return None
        
        # Sufijos bisilábicos: CVCu/inu → Cnu/na
        # Ejemplo: [k, u, n, u] → [k, n, u]
        if len(self.phonemes) == 4:
            return [self.phonemes[0], self.phonemes[2], self.phonemes[3]]
        
        return None
    
    def __repr__(self) -> str:
        gender_str = f".{self.gender.value[0]}" if self.gender else ""
        return f"Poss({self.person.value[0]}{self.number.value[0]}{gender_str})"


@dataclass
class InflectedNominal:
    """
    Sustantivo completamente flexionado.
    
    Representa una forma nominal completa con:
    - Caso
    - Número
    - Estado (absoluto/constructo)
    - Sufijo posesivo (opcional)
    
    Atributos:
        base: Sustantivo derivado base
        case: Caso gramatical
        number: Número gramatical
        state: Estado (absoluto/constructo)
        possessive: Sufijo posesivo (si aplica)
        phonemes: Secuencia fonémica completa
        
    Ejemplos:
        šarrum "rey" (Nom.Sg.Abs)
        šarrim "rey" (Gen.Sg.Abs)
        šarr "rey" (Nom.Sg.Const)
        šarrušu "su rey" (Nom.Sg + Poss.3sm)
        šarrū "reyes" (Nom.Pl.Abs)
    
    Ref: Integración de § 5.3-5.5, § 9.5
    """
    base: DerivedNominal
    case: Case
    number: Number
    state: State
    possessive: Optional[PossessiveSuffix] = None
    phonemes: List[Phoneme] = field(default_factory=list)
    
    # Metadatos de derivación
    case_marker: Optional[CaseMarker] = None
    number_marker: Optional[NumberMarker] = None
    construct_type: Optional[ConstructType] = None
    
    def get_transcription(self) -> str:
        """Retorna transcripción fonológica."""
        return ''.join(p.value for p in self.phonemes)
    
    def get_cuneiform_hints(self) -> str:
        """
        Retorna pistas para escritura cuneiforme.
        
        NOTA: Implementación completa requiere integración con ORACC.
        """
        # Placeholder - requiere análisis silábico completo
        return self.get_transcription()
    
    def __repr__(self) -> str:
        poss_str = f"+{self.possessive}" if self.possessive else ""
        return (f"InflectedNominal({self.get_transcription()} "
                f"[{self.case.value}.{self.number.value}.{self.state.value}]"
                f"{poss_str})")


# ============================================================================
# CONTEXTOS PARA REGLAS CONDICIONALES
# ============================================================================

@dataclass
class InflectionContext:
    """
    Contexto para aplicación de reglas de inflexión.
    
    Captura información necesaria para decidir qué reglas aplicar:
    - Tipo de stem (monosilábico, polisilábico)
    - Estructura consonántica final (simple, geminada, cluster)
    - Contexto del constructo (ante sustantivo vs. sufijo)
    - Presencia de consonantes débiles
    
    Usado para determinar:
    - Qué tipo de constructo aplicar (§ 5.5.1)
    - Si aplicar epéntesis vocálica
    - Si aplicar síncope en sufijos
    - Tratamiento de consonantes débiles
    """
    # Propiedades del stem
    is_monosyllabic: bool
    has_geminate: bool
    has_cluster: bool
    cluster_pattern: Optional[str] = None  # "PaRS", "PiRS", "PuRS"
    
    # Contexto de uso
    construct_context: Optional[ConstructContext] = None
    before_vowel: bool = False  # Si siguiente elemento empieza con vocal
    
    # Irregularidades
    weak_consonant: Optional[WeakConsonantType] = None
    is_exceptional: bool = False  # abum, aḫum, emum, *pi'um
    
    # Fonología
    final_consonant: Optional[Consonant] = None
    penultimate_consonant: Optional[Consonant] = None
    
    def get_construct_type(self) -> ConstructType:
        """
        Determina tipo de constructo apropiado.
        
        Basado en clasificación de § 5.5.1:
        1. Monosilábico + simple
        2. Polisilábico + simple
        3. Monosilábico + geminada
        4. Monosilábico + cluster
        5. Polisilábico + geminada
        6. Polisilábico + cluster
        7. Excepcional
        8. Débil
        """
        # Casos especiales primero
        if self.is_exceptional:
            return ConstructType.EXCEPTIONAL
        
        if self.weak_consonant:
            return ConstructType.WEAK
        
        # Casos regulares
        if self.is_monosyllabic:
            if self.has_geminate:
                return ConstructType.MONO_GEMINATE
            elif self.has_cluster:
                return ConstructType.MONO_CLUSTER
            else:
                return ConstructType.MONO_SIMPLE
        else:  # Polisilábico
            if self.has_geminate:
                return ConstructType.POLY_GEMINATE
            elif self.has_cluster:
                return ConstructType.POLY_CLUSTER
            else:
                return ConstructType.POLY_SIMPLE


# ============================================================================
# EXCEPCIONES Y CASOS ESPECIALES
# ============================================================================

class InflectionException(Exception):
    """Excepción base para errores de inflexión."""
    pass


class UnknownConstructTypeError(InflectionException):
    """Error cuando no se puede determinar tipo de constructo."""
    pass


class InvalidPossessiveCombinationError(InflectionException):
    """Error cuando combinación de sufijo posesivo es inválida."""
    pass


# ============================================================================
# NOTAS DE IMPLEMENTACIÓN
# ============================================================================

"""
ARQUITECTURA MODULAR:

Este archivo define las CLASES BASE del sistema de inflexión.
Los algoritmos específicos están en módulos separados:

1. case_system.py: Aplicación de marcadores de caso
2. number_system.py: Formación de dual y plural
3. construct_state.py: Formación del constructo (8 tipos)
4. possessive_system.py: Aplicación de sufijos posesivos
5. paradigm.py: Generación de paradigmas completos

FLUJO DE INFLEXIÓN:

DerivedNominal 
    → apply_case() 
    → apply_number() 
    → to_construct() 
    → add_possessive() 
    → InflectedNominal

PROCESOS FONOLÓGICOS:

La inflexión dispara varios procesos fonológicos de iteraciones previas:
- Asimilación consonántica (Iter 3)
- Asimilación vocálica (Iter 4)
- Síncope (Iter 4)
- Epéntesis (Iter 5)

Estos se aplican automáticamente a través del sistema fonológico existente.

VALIDACIÓN:

Cada transformación se valida contra ejemplos extraídos del libro.
Ver test_iteration_7.py para >30 casos de prueba.
"""

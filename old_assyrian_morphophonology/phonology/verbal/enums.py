"""
Enumeraciones para el sistema de stems verbales del Old Assyrian.

ITERACIÓN 8 - Sistema de stems verbales derivados.

Define los tipos de stems, funciones semánticas, y categorías
relacionadas con la derivación verbal.

Basado en Kouwenberg (2017) Capítulo 17.

Autor: Claude
Fecha: 2026-02-10
"""

from enum import Enum


# ============================================================================
# TIPOS DE STEM
# ============================================================================

class StemType(Enum):
    """
    Tipos de stem verbal en Old Assyrian.
    
    Basado en § 17.1-17.5 de Kouwenberg (2017).
    
    El sistema de stems verbales del OA consiste en:
    - Un stem base (G)
    - Stems derivados mediante afijos (Gt, D, Š, N)
    - Stems pluraccionales (Gtn, Dtn, Štn, Ntn)
    - Stems secundarios (Dt, Št₁, Št₂)
    
    Cada stem tiene funciones semánticas específicas.
    """
    
    # Stem base
    G = "g_stem"              # Grundstamm (base, no marcado)
    
    # Derivados de G con infijo -t-
    GT = "gt_stem"            # G + infijo -t- (reciprocal/reflexivo)
    GTN = "gtn_stem"          # G + -t- + geminación (pluraccional)
    
    # Stem con geminación de R₂ (doubled)
    D = "d_stem"              # Doubled (intensivo/factitivo)
    DT = "dt_stem"            # D + infijo -t- (detransitivo)
    DTN = "dtn_stem"          # D + -tan- (pluraccional)
    
    # Stem causativo con prefijo š-
    SH = "sh_stem"            # Š-causativo
    SHT1 = "sht1_stem"        # Št₁ (pasivo/reflexivo de Š)
    SHT2 = "sht2_stem"        # Št₂ (léxico/impredecible)
    SHTN = "shtn_stem"        # Štn (pluraccional de Š)
    
    # Stem con prefijo nasal
    N = "n_stem"              # N-medio/pasivo
    NTN = "ntn_stem"          # Ntn (pluraccional de N)
    
    def __str__(self) -> str:
        """Representación legible del stem."""
        labels = {
            StemType.G: "G",
            StemType.GT: "Gt",
            StemType.GTN: "Gtn",
            StemType.D: "D",
            StemType.DT: "Dt",
            StemType.DTN: "Dtn",
            StemType.SH: "Š",
            StemType.SHT1: "Št₁",
            StemType.SHT2: "Št₂",
            StemType.SHTN: "Štn",
            StemType.N: "N",
            StemType.NTN: "Ntn"
        }
        return labels[self]
    
    @property
    def is_pluractional(self) -> bool:
        """Verifica si el stem es pluraccional (tan-stem)."""
        return self in {
            StemType.GTN,
            StemType.DTN,
            StemType.SHTN,
            StemType.NTN
        }
    
    @property
    def has_t_infix(self) -> bool:
        """Verifica si el stem tiene infijo -t-."""
        return self in {
            StemType.GT,
            StemType.GTN,
            StemType.DT,
            StemType.DTN,
            StemType.SHT1,
            StemType.SHT2,
            StemType.SHTN
        }
    
    @property
    def base_stem(self) -> 'StemType':
        """Retorna el stem base del cual deriva este stem."""
        base_map = {
            StemType.G: StemType.G,
            StemType.GT: StemType.G,
            StemType.GTN: StemType.GT,
            StemType.D: StemType.D,
            StemType.DT: StemType.D,
            StemType.DTN: StemType.D,
            StemType.SH: StemType.SH,
            StemType.SHT1: StemType.SH,
            StemType.SHT2: StemType.SH,
            StemType.SHTN: StemType.SH,
            StemType.N: StemType.N,
            StemType.NTN: StemType.N
        }
        return base_map[self]


# ============================================================================
# VOZ GRAMATICAL
# ============================================================================

class VoiceType(Enum):
    """
    Voz gramatical en stems verbales.
    
    Indica la relación entre el sujeto y la acción verbal.
    
    Referencias:
    - § 17.2.2: Gt reciprocal/reflexivo
    - § 17.3.4: Dt detransitivo
    - § 17.4.2: Š causativo
    - § 17.5.2: N (medio)pasivo
    """
    
    ACTIVE = "active"         # Acción realizada por sujeto
    MIDDLE = "middle"         # Acción con efecto en sujeto
    PASSIVE = "passive"       # Acción recibida por sujeto
    RECIPROCAL = "reciprocal" # Acción mutua entre participantes
    REFLEXIVE = "reflexive"   # Acción sobre sí mismo
    CAUSATIVE = "causative"   # Sujeto causa que otro haga acción
    
    def __str__(self) -> str:
        return self.value


# ============================================================================
# FUNCIÓN SEMÁNTICA
# ============================================================================

class SemanticFunction(Enum):
    """
    Funciones semánticas de los stems verbales.
    
    Basado en las funciones documentadas en § 17.2-17.5.
    """
    
    # Funciones básicas
    BASE = "base"                      # G-stem (acción simple)
    
    # Funciones de Gt (§ 17.2.2)
    RECIPROCAL = "reciprocal"          # Acción mutua
    REFLEXIVE = "reflexive"            # Acción sobre sí mismo
    LEXICALIZED = "lexicalized"        # Sin función predecible
    
    # Funciones de D (§ 17.3.2)
    FACTITIVE = "factitive"            # Hacer que X sea Y
    INTENSIVE = "intensive"            # Hacer intensamente
    PLURACTIONAL = "pluractional"      # Acción múltiple/repetida
    CAUSATIVE = "causative"            # Causar que alguien haga
    
    # Funciones de Dt (§ 17.3.4)
    MEDIOPASSIVE = "mediopassive"      # Pasivo/medio
    DETRANSITIVE = "detransitive"      # Reducir transitividad
    
    # Funciones de Š (§ 17.4.2)
    CAUSATIVE_SH = "causative_sh"      # Š-causativo
    
    # Funciones de Št (§ 17.4.4)
    PASSIVE_SH = "passive_sh"          # Pasivo de Š
    LEXICAL_SHT = "lexical_sht"        # Št₂ léxico
    
    # Funciones de N (§ 17.5.2)
    PASSIVE_N = "passive_n"            # N-pasivo
    MIDDLE_N = "middle_n"              # N-medio
    INGRESSIVE = "ingressive"          # Comienzo de acción
    
    # Funciones pluraccionales (§ 17.2.4, etc.)
    FREQUENTATIVE = "frequentative"    # Acción frecuente
    HABITUAL = "habitual"              # Acción habitual
    CONTINUOUS = "continuous"          # Acción continua
    DISTRIBUTIVE = "distributive"      # Acción distributiva
    
    def __str__(self) -> str:
        return self.value.replace('_', ' ')


# ============================================================================
# CLASES VOCÁLICAS
# ============================================================================

class VowelClass(Enum):
    """
    Clases vocálicas del G-stem.
    
    Determinan el patrón vocálico del verbo en diferentes formas.
    
    Referencias:
    - § 17.2.1: Gt distingue clases vocálicas
    - § 17.3.1: D NO distingue clases vocálicas
    - § 17.5.1: N distingue clases vocálicas
    
    Formato: PRESENTE/PRETÉRITO
    """
    
    A_U = "a/u"    # PaRaS (presente) / PaRuS (pretérito)
    A_A = "a/a"    # PaRaS (presente) / PaRaS (pretérito)
    A_I = "a/i"    # PaRaS (presente) / PaRiS (pretérito)
    I_I = "i/i"    # PaRiS (presente) / PaRiS (pretérito)
    U_U = "u/u"    # PaRuS (presente) / PaRuS (pretérito)
    
    @property
    def present_vowel(self) -> str:
        """Vocal del presente."""
        return self.value.split('/')[0]
    
    @property
    def preterite_vowel(self) -> str:
        """Vocal del pretérito."""
        return self.value.split('/')[1]
    
    def __str__(self) -> str:
        return self.value


# ============================================================================
# MARCADORES MORFOLÓGICOS
# ============================================================================

class MorphologicalMarker(Enum):
    """
    Marcadores morfológicos que caracterizan cada stem.
    
    Referencias:
    - § 17.2.1: Gt tiene infijo -t-
    - § 17.3.1: D tiene geminación de R₂
    - § 17.4.1: Š tiene prefijo š-
    - § 17.5.1: N tiene prefijo nasal
    """
    
    # Infijos
    T_INFIX = "t_infix"           # Infijo -t- (Gt, Dt, Št)
    TAN_INFIX = "tan_infix"       # Infijo -tan- (Gtn, Dtn, Štn, Ntn)
    
    # Geminación
    R2_GEMINATION = "r2_gemination"  # Geminación de R₂ (D, Dt, Dtn)
    R1_GEMINATION = "r1_gemination"  # Geminación de R₁ (N por asimilación)
    
    # Prefijos
    SH_PREFIX = "sh_prefix"       # Prefijo š- (Š, Št, Štn)
    N_PREFIX = "n_prefix"         # Prefijo nasal n- (N, Ntn)
    U_PREFIX = "u_prefix"         # Vocal u en prefijos (D, Š)
    
    def __str__(self) -> str:
        return self.value.replace('_', '-')


# ============================================================================
# PRODUCTIVIDAD
# ============================================================================

class Productivity(Enum):
    """
    Nivel de productividad de cada stem.
    
    Basado en frecuencia y regularidad de uso documentada
    en el Capítulo 17.
    """
    
    VERY_HIGH = "very_high"    # Muy productivo (D factitivo, Š causativo)
    HIGH = "high"              # Productivo (N pasivo, tan-stems)
    MEDIUM = "medium"          # Medianamente productivo (Gt, Dt)
    LOW = "low"                # Poco productivo (Št₂)
    VERY_LOW = "very_low"      # Muy poco productivo (Št₁)
    RARE = "rare"              # Raro/atestiguado esporádicamente
    
    def __str__(self) -> str:
        return self.value.replace('_', ' ')


# ============================================================================
# TIPOS DE FORMAS VERBALES
# ============================================================================

class VerbFormType(Enum):
    """
    Tipos de formas verbales que se pueden generar.
    
    Used by: form_*() methods to determine which form to generate.
    
    Referencias:
    - Cap 16 § 16.3: Las ocho categorías inflexionales
    - Cap 16 § 16.9: Conjugación del G-stem
    """
    PRESENT = "present"           # iPaRRaS (prefix conjugation con geminación)
    PRETERITE = "preterite"       # iPRuS (prefix conjugation sin geminación)
    PERFECT = "perfect"           # iPTaRaS (prefix conjugation con infijo -t-)
    IMPERATIVE = "imperative"     # PuRuS (no prefix, solo sufijos)
    STATIVE = "stative"           # PaRiS (conjugación especial)
    INFINITIVE = "infinitive"     # PaRāSum (forma nominal)
    PARTICIPLE = "participle"     # PāRiSum (forma adjetival)
    VERBAL_ADJECTIVE = "verbal_adjective"  # PaRiSum (forma adjetival)
    
    def __str__(self) -> str:
        return self.value


# ============================================================================
# MAPPING: STEM → CARACTERÍSTICAS
# ============================================================================

# Productividad por stem (basado en documentación)
STEM_PRODUCTIVITY = {
    StemType.G: Productivity.VERY_HIGH,
    StemType.GT: Productivity.MEDIUM,
    StemType.GTN: Productivity.HIGH,
    StemType.D: Productivity.VERY_HIGH,
    StemType.DT: Productivity.MEDIUM,
    StemType.DTN: Productivity.LOW,
    StemType.SH: Productivity.VERY_HIGH,
    StemType.SHT1: Productivity.VERY_LOW,
    StemType.SHT2: Productivity.LOW,
    StemType.SHTN: Productivity.VERY_LOW,
    StemType.N: Productivity.HIGH,
    StemType.NTN: Productivity.LOW
}

# Marcadores morfológicos por stem
STEM_MARKERS = {
    StemType.G: set(),
    StemType.GT: {MorphologicalMarker.T_INFIX},
    StemType.GTN: {MorphologicalMarker.TAN_INFIX, MorphologicalMarker.R2_GEMINATION},
    StemType.D: {MorphologicalMarker.R2_GEMINATION, MorphologicalMarker.U_PREFIX},
    StemType.DT: {MorphologicalMarker.T_INFIX, MorphologicalMarker.R2_GEMINATION, 
                  MorphologicalMarker.U_PREFIX},
    StemType.DTN: {MorphologicalMarker.TAN_INFIX, MorphologicalMarker.R2_GEMINATION, 
                   MorphologicalMarker.U_PREFIX},
    StemType.SH: {MorphologicalMarker.SH_PREFIX, MorphologicalMarker.U_PREFIX},
    StemType.SHT1: {MorphologicalMarker.SH_PREFIX, MorphologicalMarker.T_INFIX, 
                    MorphologicalMarker.U_PREFIX},
    StemType.SHT2: {MorphologicalMarker.SH_PREFIX, MorphologicalMarker.T_INFIX, 
                    MorphologicalMarker.U_PREFIX},
    StemType.SHTN: {MorphologicalMarker.SH_PREFIX, MorphologicalMarker.TAN_INFIX, 
                    MorphologicalMarker.U_PREFIX},
    StemType.N: {MorphologicalMarker.N_PREFIX, MorphologicalMarker.R1_GEMINATION},
    StemType.NTN: {MorphologicalMarker.N_PREFIX, MorphologicalMarker.TAN_INFIX, 
                   MorphologicalMarker.R1_GEMINATION}
}

# Función semántica típica por stem
STEM_DEFAULT_FUNCTION = {
    StemType.G: SemanticFunction.BASE,
    StemType.GT: SemanticFunction.RECIPROCAL,
    StemType.GTN: SemanticFunction.PLURACTIONAL,
    StemType.D: SemanticFunction.FACTITIVE,
    StemType.DT: SemanticFunction.DETRANSITIVE,
    StemType.DTN: SemanticFunction.PLURACTIONAL,
    StemType.SH: SemanticFunction.CAUSATIVE_SH,
    StemType.SHT1: SemanticFunction.PASSIVE_SH,
    StemType.SHT2: SemanticFunction.LEXICAL_SHT,
    StemType.SHTN: SemanticFunction.PLURACTIONAL,
    StemType.N: SemanticFunction.PASSIVE_N,
    StemType.NTN: SemanticFunction.PLURACTIONAL
}

# Voz típica por stem
STEM_DEFAULT_VOICE = {
    StemType.G: VoiceType.ACTIVE,
    StemType.GT: VoiceType.RECIPROCAL,
    StemType.GTN: VoiceType.RECIPROCAL,
    StemType.D: VoiceType.ACTIVE,
    StemType.DT: VoiceType.MIDDLE,
    StemType.DTN: VoiceType.MIDDLE,
    StemType.SH: VoiceType.CAUSATIVE,
    StemType.SHT1: VoiceType.PASSIVE,
    StemType.SHT2: VoiceType.ACTIVE,
    StemType.SHTN: VoiceType.CAUSATIVE,
    StemType.N: VoiceType.PASSIVE,
    StemType.NTN: VoiceType.PASSIVE
}


# ============================================================================
# ITERATION 9: WEAK VERBS - NEW ENUMERATIONS
# ============================================================================

class WeakVerbType(Enum):
    """
    Tipos de verbos débiles según posición y naturaleza de la debilidad.
    
    Clasificación basada en Kouwenberg (2017), Capítulo 18.
    
    Los verbos débiles tienen una o más consonantes "débiles" que son
    susceptibles a cambios fonológicos en ciertos contextos.
    
    Referencias:
    - § 18.1: Introducción a verbos débiles
    - § 18.2: I/w e I/*y verbs
    - § 18.3: I/voc verbs
    - § 18.4: I/n verbs
    """
    
    # I-débil (Iteration 9)
    I_W_FIENTIVE = "I/w_fientive"      # wasābum tipo - verbos de acción
    I_W_ADJECTIVAL = "I/w_adjectival"  # watārum, waqārum tipo - adjetivales
    I_VOC_A = "I/voc_a"                # ahāzum tipo (< *ʔ, *h)
    I_VOC_E = "I/voc_e"                # epāšum tipo (< *ʕ, *ḥ)
    I_N = "I/n"                        # nadā'um, naṣārum tipo
    
    # Casos especiales I-débil
    I_ATAWWUM = "I/atawwum"            # atawwum - doblemente débil (I/voc + II/gem)
    I_N_NASAUM = "I/n_nasaum"          # našā'um - asimilación variable en N-stem
    
    # II-débil (Iteration 10 - FUTURO)
    II_VOC = "II/voc"                  # šūmum tipo
    II_ALEPH = "II/aleph"              # ša'ālum tipo
    II_GEM = "II/gem"                  # madādum tipo
    
    # III-débil (Iteration 11 - FUTURO)
    III_W = "III/w"                    # banūm tipo
    III_Y = "III/y"                    # našûm tipo
    III_ALEPH = "III/aleph"            # malā'um tipo
    
    # Fuerte (referencia)
    STRONG = "strong"                  # parāsum tipo
    
    def __str__(self) -> str:
        """Representación legible del tipo."""
        return self.value


class WeakPosition(Enum):
    """
    Posición de la debilidad en la raíz triconsonántica.
    
    Indica qué radical (R₁, R₂, R₃) es débil.
    
    Usado para:
    - Determinar qué reglas fonológicas aplicar
    - Clasificar verbos doblemente débiles
    - Validar consistencia de WeakRoot
    """
    R1 = "R1"          # Primera radical débil (I/w, I/voc, I/n)
    R2 = "R2"          # Segunda radical débil (II/voc, II/gem)
    R3 = "R3"          # Tercera radical débil (III/w, III/y)
    MULTIPLE = "multiple"  # Múltiples posiciones débiles (ej: atawwum)
    
    def __str__(self) -> str:
        return self.value


class ContractionType(Enum):
    """
    Tipos de contracción vocálica en verbos débiles.
    
    Especifica qué regla fonológica aplicar según el contexto.
    
    Referencias:
    - § 18.2.1: Contracciones w+i en I/w fientivo
    - § 18.2.2: Contracciones w+i en I/w adjetival
    - § 18.3.1: Asimilación vocálica en I/voc
    - § 18.4: Asimilación y pérdida de n en I/n
    """
    W_I_TO_U = "w+i→u"           # I/w fientivo presente: *wi-šab → ušab
    W_I_TO_U_LONG = "w+i→ū"      # I/w fientivo pretérito: *wi-šib → ūšib
    W_I_TO_I_LONG = "w+i→ī"      # I/w adjetival: *wi-ter → īter
    V_I_ASSIMILATION = "V+i→i"   # I/voc asimilación: a+i → i
    N_ASSIMILATION = "n+C→CC"    # I/n asimilación: n+ṣ → ṣṣ
    N_LOSS = "n→Ø"               # I/n pérdida: #n+i → i
    
    def __str__(self) -> str:
        return self.value


class PhonologicalContext(Enum):
    """
    Contexto fonológico para determinar comportamiento de consonantes débiles.
    
    Usado en reglas condicionales para decidir:
    - Si aplicar contracción, asimilación o pérdida
    - Qué tipo de transformación aplicar
    - Si preservar o modificar la consonante débil
    
    Ejemplos de uso:
    - WORD_INITIAL + n + i → pérdida de n (imperativo I/n)
    - BEFORE_CONSONANT + n → asimilación (pretérito I/n)
    - WITH_INFIX_T + w → comportamiento especial (perfect I/w)
    """
    BEFORE_VOWEL = "before_vowel"          # Consonante débil + vocal
    BEFORE_CONSONANT = "before_consonant"  # Consonante débil + consonante
    WORD_INITIAL = "word_initial"          # Al inicio de palabra
    AFTER_PREFIX = "after_prefix"          # Después de prefijo personal
    WITH_INFIX_T = "with_infix_t"          # En presencia de infijo -t-
    WITH_ENDING = "with_ending"            # Con ending vocálico
    WITHOUT_ENDING = "without_ending"      # Sin ending
    
    def __str__(self) -> str:
        return self.value.replace('_', ' ')

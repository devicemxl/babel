"""
Enumeraciones para morfología nominal del Old Assyrian.

Basado en Kouwenberg (2017) § 4.1-4.2.
"""

from enum import Enum


class Gender(Enum):
    """
    Género gramatical del Old Assyrian.
    
    OA distingue masculino y femenino.
    Algunos sustantivos son comunes (ambos géneros).
    """
    MASCULINE = "masculine"
    FEMININE = "feminine"
    COMMON = "common"  # Puede ser ambos


class Number(Enum):
    """
    Número gramatical del Old Assyrian.
    
    OA mantiene distinción tripartita:
    - Singular: šarrum "rey"
    - Dual: šarrān "dos reyes"  
    - Plural: šarrū "reyes"
    """
    SINGULAR = "singular"
    DUAL = "dual"
    PLURAL = "plural"


class State(Enum):
    """
    Estado (status) del sustantivo.
    
    - Absoluto: forma independiente (šarrum "un rey")
    - Constructo: en construcción genitive (šar bābilim "rey de Babilonia")
    
    El estado constructo típicamente pierde mimación y/o acorta vocales finales.
    """
    ABSOLUTE = "absolute"
    CONSTRUCT = "construct"


class PatternType(Enum):
    """
    Tipo de patrón nominal según origen morfológico.
    
    - Primary: Derivado directamente de raíz verbal (PaRS, PiRS, PuRS)
    - Secondary: Derivado de otro nominal (PaRRāS de PaRS)
    - Compound: Sustantivo compuesto
    - Loanword: Préstamo de otro idioma
    """
    PRIMARY = "primary"
    SECONDARY = "secondary"
    COMPOUND = "compound"
    LOANWORD = "loanword"


class NominalFunction(Enum):
    """
    Función semántica del patrón nominal.
    
    Basado en § 4.2.1 de Kouwenberg.
    """
    AGENT = "agent"                    # Agente: šarrāqum "ladrón"
    INSTRUMENT = "instrument"          # Instrumento: maškarum "lugar de molienda"
    ABSTRACT = "abstract"              # Abstracto: dīnum "juicio"
    RESULT = "result"                  # Resultado: šiprum "envío"
    PLACE = "place"                    # Lugar: manzāzum "posición"
    TIME = "time"                      # Tiempo
    PROFESSION = "profession"          # Profesión: dannānum "juez"
    QUALITY = "quality"                # Cualidad: dumqum "bondad"
    COLLECTIVE = "collective"          # Colectivo
    GENTILICS = "gentilics"           # Gentilicio: aššurāyum "asirio"


class RootType(Enum):
    """
    Tipo de raíz consonántica.
    
    OA mayormente triconsonántico, pero también hay biconsonánticas.
    """
    BICONSONANTAL = "biconsonantal"    # √CC (menos común)
    TRICONSONANTAL = "triconsonantal"  # √CCC (más común)
    QUADRICONSONANTAL = "quadriconsonantal"  # √CCCC (raro)


class VowelPatternType(Enum):
    """
    Tipo de patrón vocálico en el template.
    
    - Short: Solo vocales cortas (PaRS)
    - Long: Incluye vocal larga (PīRS, PāRS)
    - Mixed: Mezcla de cortas y largas (PaRāS)
    """
    SHORT = "short"
    LONG = "long"
    MIXED = "mixed"


class Mimation(Enum):
    """
    Presencia de mimación (-m final).
    
    OA típicamente tiene mimación, pero puede perderse en:
    - Estado constructo
    - Antes de sufijos
    - En algunos contextos fonológicos
    """
    PRESENT = "present"      # -um/-im/-am
    ABSENT = "absent"        # Sin -m
    VARIABLE = "variable"    # Opcional


# ============================================================================
# CONSTANTES ÚTILES
# ============================================================================

# Géneros que pueden formar femenino con -t
GENDERED_PATTERNS = {Gender.MASCULINE, Gender.COMMON}

# Números que tienen formas distintas
PRODUCTIVE_NUMBERS = {Number.SINGULAR, Number.PLURAL, Number.DUAL}

# Estados productivos
PRODUCTIVE_STATES = {State.ABSOLUTE, State.CONSTRUCT}

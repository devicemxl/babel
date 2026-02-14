"""
Clases principales para patrones nominales del Old Assyrian.

Basado en Kouwenberg (2017) § 4.1-4.2.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from .. import Consonant, Vowel, Phoneme
from .enums import (
    Gender,
    Number,
    State,
    PatternType,
    NominalFunction,
    RootType,
    VowelPatternType,
    Mimation,
)


@dataclass
class NominalExample:
    """
    Ejemplo documentado de patrón nominal.
    
    Attributes:
        root: Raíz consonántica (√mlk, √šrq, etc.)
        surface: Forma superficial (malkum, šarrāqum)
        gloss: Traducción
        oracc_spelling: Spelling ORACC si disponible
        section: Referencia a Kouwenberg
        notes: Notas adicionales
    """
    root: str
    surface: str
    gloss: str
    oracc_spelling: Optional[str] = None
    section: str = ""
    notes: str = ""


@dataclass
class NominalRoot:
    """
    Raíz consonántica nominal.
    
    OA típicamente usa raíces triconsonánticas (√CCC),
    pero también hay biconsonánticas (√CC).
    
    Ejemplos:
        √mlk → malkum "consejo"
        √šrq → šarrāqum "ladrón"
        √dn → dīnum "juicio" (biconsonántica)
    
    Attributes:
        C1: Primera consonante (obligatoria)
        C2: Segunda consonante (obligatoria)
        C3: Tercera consonante (opcional para raíces biconsonánticas)
        root_type: Tipo de raíz
    """
    C1: Consonant
    C2: Consonant
    C3: Optional[Consonant] = None
    root_type: Optional[RootType] = None
    
    def __post_init__(self):
        """Determina tipo de raíz automáticamente si no se especifica."""
        if self.root_type is None:
            if self.C3 is None:
                self.root_type = RootType.BICONSONANTAL
            else:
                self.root_type = RootType.TRICONSONANTAL
    
    def is_biconsonantal(self) -> bool:
        """Verifica si raíz es biconsonántica."""
        return self.C3 is None
    
    def is_triconsonantal(self) -> bool:
        """Verifica si raíz es triconsonántica."""
        return self.C3 is not None
    
    def get_consonants(self) -> List[Consonant]:
        """Retorna lista de consonantes de la raíz."""
        if self.C3:
            return [self.C1, self.C2, self.C3]
        return [self.C1, self.C2]
    
    def to_string(self) -> str:
        """Representación en string de la raíz."""
        consonants = ''.join(c.symbol for c in self.get_consonants())
        return f"√{consonants}"
    
    def __str__(self) -> str:
        return self.to_string()
    
    def __repr__(self) -> str:
        return f"NominalRoot({self.to_string()})"


@dataclass
class NominalPattern:
    """
    Template morfológico nominal.
    
    Define el patrón abstracto de un sustantivo OA.
    
    Template notation:
        C = slot para consonante de raíz
        V = slot para vocal del patrón
        G = geminación de consonante
    
    Ejemplos:
        PaRS: template="CACVC", vowels=[a]
            √mlk + PaRS → malkum
        
        PiRS: template="CICVC", vowels=[i]
            √dn + PiRS → dīnum
        
        PaRRāS: template="CACGCVVC", vowels=[a, ā]
            √šrq + PaRRāS → šarrāqum
    
    Attributes:
        name: Nombre del patrón (PaRS, PiRS, etc.)
        code: Código único (NOM-1, NOM-2, etc.)
        template: String de template (CACVC)
        vowels: Lista de vocales del patrón
        has_mimation: ¿Tiene mimación -um/-im/-am?
        gender: Género por defecto
        pattern_type: Tipo de patrón
        vowel_pattern_type: Tipo de patrón vocálico
        nominal_function: Función semántica
        description: Descripción del patrón
        examples: Ejemplos documentados
        section: Referencia a Kouwenberg
        notes: Notas adicionales
    """
    name: str
    code: str
    template: str
    vowels: List[Vowel]
    has_mimation: bool
    gender: Gender
    pattern_type: PatternType
    
    # Opcionales
    vowel_pattern_type: VowelPatternType = VowelPatternType.SHORT
    nominal_function: Optional[NominalFunction] = None
    
    # Documentación
    description: str = ""
    examples: List[NominalExample] = field(default_factory=list)
    section: str = ""
    notes: str = ""
    
    def get_consonant_slots(self) -> int:
        """Cuenta slots de consonante (C) en template."""
        return self.template.count('C')
    
    def get_vowel_slots(self) -> int:
        """Cuenta slots de vocal (V) en template."""
        return self.template.count('V')
    
    def requires_gemination(self) -> bool:
        """Verifica si patrón requiere geminación."""
        return 'G' in self.template
    
    def is_compatible_with_root(self, root: NominalRoot) -> bool:
        """
        Verifica si patrón es compatible con raíz.
        
        Un patrón es compatible si tiene suficientes slots C
        para las consonantes de la raíz.
        """
        consonant_slots = self.get_consonant_slots()
        root_consonants = len(root.get_consonants())
        
        # Si hay geminación, cuenta como slot adicional
        if self.requires_gemination():
            consonant_slots += 1
        
        return consonant_slots >= root_consonants
    
    def get_vowel_count(self) -> int:
        """Retorna número de vocales en el patrón."""
        return len(self.vowels)
    
    def __str__(self) -> str:
        return f"{self.name} ({self.code})"
    
    def __repr__(self) -> str:
        return f"NominalPattern({self.name}, template={self.template})"


@dataclass
class DerivedNominal:
    """
    Sustantivo derivado por aplicación de patrón a raíz.
    
    Representa el resultado de aplicar un patrón nominal
    a una raíz consonántica.
    
    Ejemplo:
        root = √mlk
        pattern = PaRS
        → malkum "consejo"
    
    Attributes:
        root: Raíz consonántica original
        pattern: Patrón aplicado
        phonemes: Secuencia fonémica resultante
        gender: Género del sustantivo
        number: Número (singular/dual/plural)
        state: Estado (absoluto/constructo)
        gloss: Traducción
    """
    root: NominalRoot
    pattern: NominalPattern
    phonemes: List[Phoneme]
    
    # Propiedades morfológicas
    gender: Gender
    number: Number = Number.SINGULAR
    state: State = State.ABSOLUTE
    
    # Opcional
    gloss: str = ""
    
    def to_string(self) -> str:
        """Representación en string de forma superficial."""
        return ''.join(p.symbol for p in self.phonemes)
    
    def to_phonemic(self) -> str:
        """Representación fonémica."""
        return f"/{self.to_string()}/"
    
    def get_syllable_structure(self):
        """
        Retorna estructura silábica (requiere Iteración 5).
        
        Usa el módulo de silabificación para analizar la palabra.
        """
        from ..syllable import syllabify
        return syllabify(self.phonemes)
    
    def to_oracc(self) -> str:
        """
        Convierte a formato ORACC aproximado.
        
        Nota: Aproximación, no garantiza spelling exacto.
        """
        from ...oracc import phonemes_to_oracc
        return phonemes_to_oracc(self.phonemes)
    
    def __str__(self) -> str:
        return self.to_string()
    
    def __repr__(self) -> str:
        return (
            f"DerivedNominal("
            f"root={self.root.to_string()}, "
            f"pattern={self.pattern.name}, "
            f"surface={self.to_string()})"
        )


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def create_root_from_string(root_string: str) -> NominalRoot:
    """
    Crea NominalRoot desde string.
    
    Args:
        root_string: String como "√mlk", "mlk", o "m-l-k"
    
    Returns:
        NominalRoot creado
    
    Examples:
        >>> create_root_from_string("√mlk")
        NominalRoot(√mlk)
        
        >>> create_root_from_string("šrq")
        NominalRoot(√šrq)
    """
    from .. import get_consonant
    
    # Limpiar string
    clean = root_string.replace('√', '').replace('-', '')
    
    if len(clean) < 2:
        raise ValueError(f"Raíz debe tener al menos 2 consonantes: {root_string}")
    
    C1 = get_consonant(clean[0])
    C2 = get_consonant(clean[1])
    C3 = get_consonant(clean[2]) if len(clean) >= 3 else None
    
    return NominalRoot(C1=C1, C2=C2, C3=C3)


def get_pattern_statistics(pattern: NominalPattern) -> Dict[str, any]:
    """
    Retorna estadísticas de un patrón.
    
    Returns:
        Dict con:
            - consonant_slots
            - vowel_slots
            - has_gemination
            - has_long_vowel
            - template_length
    """
    has_long = any(v.is_long for v in pattern.vowels)
    
    return {
        'consonant_slots': pattern.get_consonant_slots(),
        'vowel_slots': pattern.get_vowel_slots(),
        'has_gemination': pattern.requires_gemination(),
        'has_long_vowel': has_long,
        'template_length': len(pattern.template),
        'vowel_count': len(pattern.vowels),
    }

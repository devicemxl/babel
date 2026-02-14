"""
Š-stem y derivados del Old Assyrian.

ITERACIÓN 8 - Stems verbales derivados.

Implementa:
- Š-stem: Causativo con prefijo š-
- Št₁-stem: Pasivo/reflexivo de Š
- Št₂-stem: Št léxico (impredecible)
- Štn-stem: Š pluraccional

Basado en Kouwenberg (2017) § 17.4.

Autor: Claude
Fecha: 2026-02-10
"""

from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum

from ..phoneme import Phoneme, Vowel, Consonant
from ..inventory import get_vowel, get_consonant
from .stem import VerbalRoot, VerbalStem
from .enums import StemType, VoiceType, SemanticFunction, VowelClass, VerbFormType


# ============================================================================
# FUNCIONES ESPECÍFICAS DEL Š-STEM
# ============================================================================

class Sh_Function(Enum):
    """
    Funciones específicas del Š-stem.
    
    Basado en § 17.4.2.
    """
    
    CAUSATIVE_MOTION = "caus_motion"      # Causativo de verbo de movimiento
    CAUSATIVE_PROCESS = "caus_process"    # Causativo de verbo de proceso
    CAUSATIVE_TRANS = "caus_trans"        # Causativo de verbo transitivo
    UNPREDICTABLE = "unpredictable"       # Significado impredecible
    SH_TANTUM = "sh_tantum"               # Solo Š, no G


# ============================================================================
# Š-STEM (CAUSATIVO)
# ============================================================================

@dataclass
class Sh_Stem(VerbalStem):
    """Š-stem del Old Assyrian. Stem causativo con prefijo š-."""
    
    stem_type: StemType = field(default=StemType.SH)
    
    sh_function: Optional[Sh_Function] = None
    
    def __post_init__(self):
        """Inicializa Sh_Stem con valores por defecto."""
        super().__post_init__()
    
    @property
    def pattern_template(self) -> str:
        """Patrón del Š-stem."""
        return "šaPRuS"
    
    @property
    def is_causative_of_motion(self) -> bool:
        """Verifica si es causativo de verbo de movimiento."""
        return self.sh_function == Sh_Function.CAUSATIVE_MOTION
    
    @property
    def is_causative_of_process(self) -> bool:
        """Verifica si es causativo de verbo de proceso."""
        return self.sh_function == Sh_Function.CAUSATIVE_PROCESS
    
    # ========================================================================
    # PHONOLOGICAL FORMATION METHODS
    # ========================================================================
    
    def form_present(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma el presente del Š-stem.
        
        Pattern: ušaPRaS
        - Double prefix: u- + š-
        - NO gemination of R₂ (unlike D-stem)
        - Fixed vowels: a...a
        
        Example:
            >>> # √PRS Š 'hacer separar'
            >>> sh.form_present(3, 'sg', 'm')
            [u, š, a, p, r, a, s]  # ušapras
        """
        from .phonological_formation import (
            get_prefix, get_suffix, apply_vowel_assimilation
        )
        
        # 1. Get prefix with u-
        prefix = get_prefix(person, number, gender, use_u_prefix=True)
        
        # 2. Build stem with š- prefix: š + a + R₁ + R₂ + a + R₃
        stem = [
            get_consonant('š'),
            get_vowel('a'),  # Fixed vowel
            self.root.R1,
            self.root.R2,  # NOT geminated
            get_vowel('a'),  # Fixed vowel
            self.root.R3
        ]
        
        # 3. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 4. Apply vowel assimilation if suffix
        if suffix:
            suffix_vowel = str(suffix[0])
            stem = apply_vowel_assimilation(stem, suffix_vowel)
        
        # 5. Combine: u-prefix + š-stem + suffix
        result = prefix + stem + suffix
        
        return result
    
    def form_preterite(self, person: int = 3, number: str = 'sg',
                       gender: str = 'm') -> List[Phoneme]:
        """
        Forma el pretérito del Š-stem.
        
        Pattern: ušaPRiS
        - Double prefix: u- + š-
        - NO gemination
        - Fixed vowels: a...i (like D-stem)
        
        Example:
            >>> # √PRS Š
            >>> sh.form_preterite(3, 'sg', 'm')
            [u, š, a, p, r, i, s]  # ušapris
        """
        from .phonological_formation import get_prefix, get_suffix
        
        # 1. Get prefix with u-
        prefix = get_prefix(person, number, gender, use_u_prefix=True)
        
        # 2. Build stem: š + a + R₁ + R₂ + i + R₃
        stem = [
            get_consonant('š'),
            get_vowel('a'),  # Fixed
            self.root.R1,
            self.root.R2,  # NOT geminated
            get_vowel('i'),  # Fixed (different from present)
            self.root.R3
        ]
        
        # 3. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 4. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_perfect(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> Optional[List[Phoneme]]:
        """
        Forma el perfecto del Š-stem.
        
        Pattern: uštaPRiS (SPECIAL!)
        - Double prefix: u- + št- (š + t combined)
        - Fixed vowels: a...i
        
        Example:
            >>> # √PRS Š
            >>> sh.form_perfect(3, 'sg', 'm')
            [u, š, t, a, p, r, i, s]  # uštapris
        """
        from .phonological_formation import get_prefix, get_suffix
        
        # 1. Get prefix with u-
        prefix = get_prefix(person, number, gender, use_u_prefix=True)
        
        # 2. Build stem with št- (special combination)
        # NOT š + i + t, but št directly
        stem = [
            get_consonant('š'),
            get_consonant('t'),  # št combined
            get_vowel('a'),  # Fixed
            self.root.R1,
            self.root.R2,  # NOT geminated
            get_vowel('i'),  # Fixed
            self.root.R3
        ]
        
        # 3. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 4. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_imperative(self, number: str = 'sg',
                        gender: str = 'm') -> List[Phoneme]:
        """
        Forma el imperativo del Š-stem.
        
        Pattern: šaPRiS
        - Only š- prefix (no u-)
        - Fixed vowels: a...i (like preterite)
        
        Example:
            >>> # √PRS Š
            >>> sh.form_imperative('sg', 'm')
            [š, a, p, r, i, s]  # šapris
        """
        from .phonological_formation import get_suffix
        
        # 1. Build stem: š + a + R₁ + R₂ + i + R₃
        stem = [
            get_consonant('š'),
            get_vowel('a'),
            self.root.R1,
            self.root.R2,
            get_vowel('i'),
            self.root.R3
        ]
        
        # 2. Get suffix (no u-prefix for imperative)
        suffix = get_suffix(2, number, gender)
        
        # 3. Combine
        result = stem + suffix
        
        return result
    
    def form_stative(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """Š-stem stative - not commonly used."""
        raise NotImplementedError("Š-stem stative not commonly attested")
    
    def get_stem_vowel(self, form_type: VerbFormType) -> str:
        """
        Š-stem uses FIXED vowels (like D-stem).
        
        Present: a...a
        Preterite/Perfect/Imperative: a...i
        """
        if form_type == VerbFormType.PRESENT:
            return 'a'  # Second vowel in present
        else:
            return 'i'  # Second vowel in other forms


# ============================================================================
# ŠT₁-STEM (PASIVO/REFLEXIVO DE Š)
# ============================================================================

@dataclass
class Sht1_Stem(VerbalStem):
    """Št₁-stem del Old Assyrian. Pasivo/reflexivo de Š."""
    
    stem_type: StemType = field(default=StemType.SHT1)
    
    def __post_init__(self):
        """Inicializa Sht1_Stem con valores por defecto."""
        super().__post_init__()
    
    # ========================================================================
    # PHONOLOGICAL FORMATION METHODS
    # ========================================================================
    
    def form_present(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma el presente del Št₁-stem.
        
        Pattern: uštaPRaS
        - Same as Št₂ (phonologically identical)
        - Different function: passive of Š
        
        Example:
            >>> # √ABL Št₁ 'ser traído'
            >>> sht1.form_present(3, 'sg', 'm')
            [u, š, t, a, b, l, a, s]  # uštabalas (simplified)
        """
        from .phonological_formation import get_prefix, get_suffix
        
        # 1. Get prefix with u-
        prefix = get_prefix(person, number, gender, use_u_prefix=True)
        
        # 2. Build stem: št + a + R₁ + R₂ + a + R₃
        stem = [
            get_consonant('š'),
            get_consonant('t'),
            get_vowel('a'),
            self.root.R1,
            self.root.R2,
            get_vowel('a'),
            self.root.R3
        ]
        
        # 3. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 4. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_preterite(self, person: int = 3, number: str = 'sg',
                       gender: str = 'm') -> List[Phoneme]:
        """
        Forma el pretérito del Št₁-stem.
        
        Pattern: uštaPRiS
        - IDENTICAL to Š-stem perfect!
        
        Example:
            >>> sht1.form_preterite(3, 'sg', 'm')
            [u, š, t, a, p, r, i, s]  # uštapris
        """
        from .phonological_formation import get_prefix, get_suffix
        
        # 1. Get prefix with u-
        prefix = get_prefix(person, number, gender, use_u_prefix=True)
        
        # 2. Build stem: št + a + R₁ + R₂ + i + R₃
        stem = [
            get_consonant('š'),
            get_consonant('t'),
            get_vowel('a'),
            self.root.R1,
            self.root.R2,
            get_vowel('i'),
            self.root.R3
        ]
        
        # 3. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 4. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_perfect(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> Optional[List[Phoneme]]:
        """Št₁ NO tiene perfecto (evita doble -t-)."""
        return None
    
    def form_imperative(self, number: str = 'sg',
                        gender: str = 'm') -> List[Phoneme]:
        """Št₁ imperative - rare."""
        raise NotImplementedError("Št₁ imperative not commonly attested")
    
    def get_stem_vowel(self, form_type: VerbFormType) -> str:
        """Št₁ usa 'a' o 'i'."""
        if form_type == VerbFormType.PRESENT:
            return 'a'
        else:
            return 'i'


# ============================================================================
# ŠT₂-STEM (ŠT LÉXICO)
# ============================================================================

@dataclass
class Sht2_Stem(VerbalStem):
    """Št₂-stem del Old Assyrian. Št léxico."""
    
    stem_type: StemType = field(default=StemType.SHT2)
    
    def __post_init__(self):
        """Inicializa Sht2_Stem con valores por defecto."""
        super().__post_init__()
    
    # ========================================================================
    # PHONOLOGICAL FORMATION METHODS
    # ========================================================================
    # NOTE: Št₂ is PHONOLOGICALLY IDENTICAL to Št₁
    # Only differs in semantic function (lexical vs passive)
    
    def form_present(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma el presente del Št₂-stem.
        
        Pattern: uštaPRaS
        - Same as Št₁ (phonologically identical)
        - Different function: lexical/unpredictable
        
        Example:
            >>> # √ABL Št₂ 'traer' (lexical)
            >>> sht2.form_present(3, 'sg', 'm')
            [u, š, t, a, b, a, l]  # uštabal (simplified)
        """
        from .phonological_formation import get_prefix, get_suffix
        
        # 1. Get prefix with u-
        prefix = get_prefix(person, number, gender, use_u_prefix=True)
        
        # 2. Build stem: št + a + R₁ + R₂ + a + R₃
        stem = [
            get_consonant('š'),
            get_consonant('t'),
            get_vowel('a'),
            self.root.R1,
            self.root.R2,
            get_vowel('a'),
            self.root.R3
        ]
        
        # 3. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 4. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_preterite(self, person: int = 3, number: str = 'sg',
                       gender: str = 'm') -> List[Phoneme]:
        """
        Forma el pretérito del Št₂-stem.
        
        Pattern: uštaPRiS
        - Identical to Št₁ and Š-perfect
        """
        from .phonological_formation import get_prefix, get_suffix
        
        # 1. Get prefix with u-
        prefix = get_prefix(person, number, gender, use_u_prefix=True)
        
        # 2. Build stem: št + a + R₁ + R₂ + i + R₃
        stem = [
            get_consonant('š'),
            get_consonant('t'),
            get_vowel('a'),
            self.root.R1,
            self.root.R2,
            get_vowel('i'),
            self.root.R3
        ]
        
        # 3. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 4. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_perfect(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> Optional[List[Phoneme]]:
        """Št₂ NO tiene perfecto."""
        return None
    
    def form_imperative(self, number: str = 'sg',
                        gender: str = 'm') -> List[Phoneme]:
        """Št₂ imperative - rare."""
        raise NotImplementedError("Št₂ imperative not commonly attested")
    
    def get_stem_vowel(self, form_type: VerbFormType) -> str:
        """Št₂ usa 'a' o 'i'."""
        if form_type == VerbFormType.PRESENT:
            return 'a'
        else:
            return 'i'


# ============================================================================
# ŠTN-STEM (PLURACCIONAL DE Š)
# ============================================================================

@dataclass
class Shtn_Stem(VerbalStem):
    """Štn-stem del Old Assyrian. Š pluraccional."""
    
    stem_type: StemType = field(default=StemType.SHTN)
    
    def __post_init__(self):
        """Inicializa Shtn_Stem con valores por defecto."""
        super().__post_init__()
        object.__setattr__(self, 'semantic_function', SemanticFunction.PLURACTIONAL)
    
    # ========================================================================
    # PHONOLOGICAL FORMATION METHODS
    # ========================================================================
    
    def form_present(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma el presente del Štn-stem.
        
        Pattern: ušTanaPRaS
        - Double prefix: u- + š-
        - Infix: -tan-
        - NO gemination of R₂
        - Fixed vowels: a...a
        
        Example:
            >>> # √PRS Štn
            >>> shtn.form_present(3, 'sg', 'm')
            [u, š, t, a, n, a, p, r, a, s]  # uštanapras
        """
        from .phonological_formation import get_prefix, get_suffix
        
        # 1. Get prefix with u-
        prefix = get_prefix(person, number, gender, use_u_prefix=True)
        
        # 2. Build stem: š + t + a + n + a + R₁ + R₂ + a + R₃
        stem = [
            get_consonant('š'),
            get_consonant('t'),
            get_vowel('a'),
            get_consonant('n'),  # -tan- infix
            get_vowel('a'),
            self.root.R1,
            self.root.R2,  # NOT geminated (like Š)
            get_vowel('a'),  # Fixed
            self.root.R3
        ]
        
        # 3. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 4. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_preterite(self, person: int = 3, number: str = 'sg',
                       gender: str = 'm') -> List[Phoneme]:
        """
        Forma el pretérito del Štn-stem.
        
        Pattern: ušTaPRaS
        - Only -t- (no -n-)
        - R₂ NOT geminated
        
        Example:
            >>> # √PRS Štn
            >>> shtn.form_preterite(3, 'sg', 'm')
            [u, š, t, a, p, r, a, s]  # uštapras
        """
        from .phonological_formation import get_prefix, get_suffix
        
        # 1. Get prefix with u-
        prefix = get_prefix(person, number, gender, use_u_prefix=True)
        
        # 2. Build stem: š + t + a + R₁ + R₂ + a + R₃ (no -n-)
        stem = [
            get_consonant('š'),
            get_consonant('t'),
            get_vowel('a'),
            self.root.R1,
            self.root.R2,  # NOT geminated
            get_vowel('a'),  # Fixed
            self.root.R3
        ]
        
        # 3. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 4. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_perfect(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> Optional[List[Phoneme]]:
        """Štn-stem NO tiene perfecto."""
        return None
    
    def form_imperative(self, number: str = 'sg',
                        gender: str = 'm') -> List[Phoneme]:
        """Štn-stem imperative - not commonly attested."""
        raise NotImplementedError("Štn imperative not commonly attested")
    
    def get_stem_vowel(self, form_type: VerbFormType) -> str:
        """Štn-stem uses FIXED vowel 'a'."""
        return 'a'


# ============================================================================
# FUNCIONES DE FORMACIÓN
# ============================================================================

def form_sh_stem(root: VerbalRoot,
                 sh_function: Optional[Sh_Function] = None,
                 semantic_function: Optional[SemanticFunction] = None,
                 meaning: Optional[str] = None) -> Sh_Stem:
    """
    Forma el Š-stem de una raíz verbal.
    
    Args:
        root: Raíz verbal base
        sh_function: Función específica del Š
        semantic_function: Función semántica general
        meaning: Significado derivado
        
    Returns:
        Sh_Stem formado
        
    Example:
        >>> root = create_root('r', 'b', 'm', VowelClass.A_U, 'entrar')
        >>> sh = form_sh_stem(
        ...     root,
        ...     Sh_Function.CAUSATIVE_MOTION,
        ...     SemanticFunction.CAUSATIVE_SH,
        ...     'traer adentro'
        ... )
    """
    return Sh_Stem(
        root=root,
        sh_function=sh_function,
        semantic_function=semantic_function,
        meaning=meaning
    )


def form_sht1_stem(root: VerbalRoot,
                   semantic_function: Optional[SemanticFunction] = None,
                   voice: Optional[VoiceType] = None,
                   meaning: Optional[str] = None) -> Sht1_Stem:
    """
    Forma el Št₁-stem de una raíz verbal.
    
    Args:
        root: Raíz verbal base
        semantic_function: Función semántica
        voice: Voz gramatical
        meaning: Significado derivado
        
    Returns:
        Sht1_Stem formado
    """
    return Sht1_Stem(
        root=root,
        semantic_function=semantic_function,
        voice=voice,
        meaning=meaning
    )


def form_sht2_stem(root: VerbalRoot,
                   meaning: Optional[str] = None) -> Sht2_Stem:
    """
    Forma el Št₂-stem (léxico) de una raíz verbal.
    
    Args:
        root: Raíz verbal base
        meaning: Significado derivado
        
    Returns:
        Sht2_Stem formado
    """
    return Sht2_Stem(
        root=root,
        meaning=meaning
    )


def form_shtn_stem(root: VerbalRoot,
                   meaning: Optional[str] = None) -> Shtn_Stem:
    """
    Forma el Štn-stem (pluraccional) de una raíz verbal.
    
    Args:
        root: Raíz verbal base
        meaning: Significado derivado
        
    Returns:
        Shtn_Stem formado
    """
    return Shtn_Stem(
        root=root,
        meaning=meaning
    )


# ============================================================================
# EJEMPLOS DEL LIBRO
# ============================================================================

# Š-stem causativos de movimiento (§ 17.4.2)
SH_MOTION_EXAMPLES = {
    'waṣāʾum': ('salir', 'sacar, producir'),
    'erābum': ('entrar', 'traer adentro'),
    'sahārum': ('dar vueltas', 'retrasar a alguien')
}

# Š-stem causativos de proceso (§ 17.4.2)
SH_PROCESS_EXAMPLES = {
    'išārum': ('ser recto', 'hacer normal, poner en orden'),
    'marāšum': ('enfermarse', 'hacer enojar'),
    'muātum': ('morir', 'matar')
}

# Š-stem causativos de transitivos (§ 17.4.2)
SH_TRANSITIVE_EXAMPLES = {
    'šaqālum': 'hacer pagar',
    'šamāʾum': 'hacer oír',
    'gamārum': 'hacer gastar'
}

# Š tantum (§ 17.4.2)
SH_TANTUM_EXAMPLES = {
    'šamDuum': 'advertir, amenazar',
    'šaklulum': 'terminar',
    'šamšuum': 'pasar la noche'
}

# Št₁-stem ejemplos (§ 17.4.4) - MUY RAROS
SHT1_EXAMPLES = {
    'wabālum': 'ser enviado',
    'erābum': 'ser traído'
}

# Št₂-stem ejemplos (§ 17.4.4)
SHT2_EXAMPLES = {
    'amārum': 'encontrarse con',
    'išārum': 'estar en orden(?)',
    'lamānum': 'tener malas relaciones con',
    'magārum': 'hacer estar de acuerdo mutuamente',
    'mahārūm': 'hacer iguales mutuamente',
    'malāʾum': 'suplementar',
    'marāṣum': 'hacer lo mejor posible',
    'ṣabātum': 'reunir, preparar',
    'šanāʾum': 'hacer segunda vez',
    'šutēbulum': 'hacer negocios, comerciar',
    'šutēṣuum': 'pelear'
}

# Štn-stem ejemplo (§ 17.4.5) - ÚNICO DE VERBO FUERTE
SHTN_EXAMPLES = {
    'bašālum': 'seguir fundiendo'
}

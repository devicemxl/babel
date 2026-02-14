"""
D-stem y derivados del Old Assyrian.

ITERACIÓN 8 - Stems verbales derivados.

Implementa:
- D-stem: Doubled (geminación R₂, factitivo/intensivo)
- Dt-stem: D + infijo -t- (detransitivo)
- Dtn-stem: D + -tan- (pluraccional)

Basado en Kouwenberg (2017) § 17.3.

Autor: Claude
Fecha: 2026-02-10
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

from ..phoneme import Phoneme, Vowel, Consonant
from ..inventory import get_vowel, get_consonant
from .stem import VerbalRoot, VerbalStem
from .enums import StemType, VoiceType, SemanticFunction, VowelClass, VerbFormType


# ============================================================================
# FUNCIONES ESPECÍFICAS DEL D-STEM
# ============================================================================

class D_Function(Enum):
    """
    Funciones específicas del D-stem según tipo de G-stem base.
    
    Basado en § 17.3.2.
    """
    
    # De G intransitivo (§ 17.3.2 sub (1))
    FACTITIVE = "factitive"              # G intrans. → D trans. factitivo
    
    # De G transitivo de estado/proceso (§ 17.3.2 sub (2))
    TRANSITIVE_AGENTIVE = "trans_agent"  # G trans. → D trans. agentivo
    
    # De G transitivo de acción (§ 17.3.2 sub (3))
    VERBAL_PLURALITY = "verbal_plural"   # Objeto plural/masa
    SPECIALIZED = "specialized"          # Significado especializado
    INTERCHANGEABLE = "interchangeable"  # Intercambiable con G
    
    # Sin G-stem (§ 17.3.2 sub (4))
    D_TANTUM = "d_tantum"                # Solo D, no G


# ============================================================================
# D-STEM (FACTITIVO/INTENSIVO)
# ============================================================================

@dataclass
class D_Stem(VerbalStem):
    """D-stem del Old Assyrian. Doubled stem con geminación de R₂."""
    
    stem_type: StemType = field(default=StemType.D)
    
    d_function: Optional[D_Function] = None
    
    def __post_init__(self):
        """Inicializa D_Stem con valores por defecto."""
        super().__post_init__()
    
    @property
    def pattern_template(self) -> str:
        """Patrón del D-stem."""
        return "PaRRuS"
    
    @property
    def is_factitive(self) -> bool:
        """Verifica si es D factitivo."""
        return (self.d_function == D_Function.FACTITIVE or
                self.semantic_function == SemanticFunction.FACTITIVE)
    
    @property
    def is_intensive(self) -> bool:
        """Verifica si expresa intensidad/pluralidad."""
        return (self.d_function == D_Function.VERBAL_PLURALITY or
                self.semantic_function == SemanticFunction.INTENSIVE)
    
    # ========================================================================
    # PHONOLOGICAL FORMATION METHODS
    # ========================================================================
    
    def form_present(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma el presente del D-stem.
        
        Pattern: uPaRRaS
        - u-prefix (not i-)
        - R₂ ALWAYS geminated
        - Fixed vowels: a...a
        
        Example:
            >>> # √PRS D 'hacer separar'
            >>> d.form_present(3, 'sg', 'm')
            [u, p, a, r, r, a, s]  # uparras
        """
        from .phonological_formation import (
            get_prefix, get_suffix, geminate_consonant,
            apply_vowel_assimilation
        )
        
        # 1. Get prefix with u-
        prefix = get_prefix(person, number, gender, use_u_prefix=True)
        
        # 2. Build stem: R₁ + a + R₂ + R₂ + a + R₃
        stem = [
            self.root.R1,
            get_vowel('a'),  # Fixed vowel
            self.root.R2,
            # R₂ will be geminated
            get_vowel('a'),  # Fixed vowel
            self.root.R3
        ]
        
        # 3. Geminate R₂ (index 2 in stem)
        stem = geminate_consonant(stem, 2)
        
        # 4. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 5. Apply vowel assimilation if suffix
        if suffix:
            suffix_vowel = str(suffix[0])
            stem = apply_vowel_assimilation(stem, suffix_vowel)
        
        # 6. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_preterite(self, person: int = 3, number: str = 'sg',
                       gender: str = 'm') -> List[Phoneme]:
        """
        Forma el pretérito del D-stem.
        
        Pattern: uPaRRiS
        - u-prefix
        - R₂ ALWAYS geminated
        - Fixed vowels: a...i
        
        Example:
            >>> # √PRS D
            >>> d.form_preterite(3, 'sg', 'm')
            [u, p, a, r, r, i, s]  # uparris
        """
        from .phonological_formation import (
            get_prefix, get_suffix, geminate_consonant
        )
        
        # 1. Get prefix with u-
        prefix = get_prefix(person, number, gender, use_u_prefix=True)
        
        # 2. Build stem: R₁ + a + R₂ + R₂ + i + R₃
        stem = [
            self.root.R1,
            get_vowel('a'),  # Fixed
            self.root.R2,
            # R₂ will be geminated
            get_vowel('i'),  # Fixed (different from present)
            self.root.R3
        ]
        
        # 3. Geminate R₂
        stem = geminate_consonant(stem, 2)
        
        # 4. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 5. Combine (no assimilation, already 'i')
        result = prefix + stem + suffix
        
        return result
    
    def form_perfect(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> Optional[List[Phoneme]]:
        """
        Forma el perfecto del D-stem.
        
        Pattern: uPTaRRiS
        - u-prefix
        - Infix -t- after R₁
        - R₂ ALWAYS geminated
        - Fixed vowels: a...i
        
        Example:
            >>> # √PRS D
            >>> d.form_perfect(3, 'sg', 'm')
            [u, p, t, a, r, r, i, s]  # uptarris
        """
        from .phonological_formation import (
            get_prefix, get_suffix, geminate_consonant,
            apply_t_assimilation
        )
        
        # 1. Get prefix with u-
        prefix = get_prefix(person, number, gender, use_u_prefix=True)
        
        # 2. Insert -t- and build stem
        t = get_consonant('t')
        t_assim = apply_t_assimilation(t, self.root.R1)
        
        stem = [
            self.root.R1,
            t_assim,
            get_vowel('a'),  # Fixed
            self.root.R2,
            # R₂ will be geminated
            get_vowel('i'),  # Fixed
            self.root.R3
        ]
        
        # 3. Geminate R₂
        stem = geminate_consonant(stem, 3)
        
        # 4. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 5. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_imperative(self, number: str = 'sg',
                        gender: str = 'm') -> List[Phoneme]:
        """
        Forma el imperativo del D-stem.
        
        Pattern: PaRRiS
        - No prefix
        - R₂ ALWAYS geminated
        - Fixed vowels: a...i (like preterite)
        
        Example:
            >>> # √PRS D
            >>> d.form_imperative('sg', 'm')
            [p, a, r, r, i, s]  # parris
        """
        from .phonological_formation import (
            get_suffix, geminate_consonant
        )
        
        # 1. Build stem: R₁ + a + R₂ + R₂ + i + R₃
        stem = [
            self.root.R1,
            get_vowel('a'),
            self.root.R2,
            # R₂ will be geminated
            get_vowel('i'),
            self.root.R3
        ]
        
        # 2. Geminate R₂
        stem = geminate_consonant(stem, 2)
        
        # 3. Get suffix (no prefix for imperative)
        suffix = get_suffix(2, number, gender)
        
        # 4. Combine
        result = stem + suffix
        
        return result
    
    def form_stative(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """D-stem stative - not commonly used."""
        raise NotImplementedError("D-stem stative not commonly attested")
    
    def get_stem_vowel(self, form_type: VerbFormType) -> str:
        """
        D-stem uses FIXED vowels (not from vowel class).
        
        Present: a...a
        Preterite/Perfect/Imperative: a...i
        """
        if form_type == VerbFormType.PRESENT:
            return 'a'  # Second vowel in present
        else:
            return 'i'  # Second vowel in other forms


# ============================================================================
# DT-STEM (DETRANSITIVO)
# ============================================================================

@dataclass
class Dt_Stem(VerbalStem):
    """Dt-stem del Old Assyrian. D-stem con infijo -t-."""
    
    stem_type: StemType = field(default=StemType.DT)
    
    def __post_init__(self):
        """Inicializa Dt_Stem con valores por defecto."""
        super().__post_init__()
    
    @property
    def pattern_template(self) -> str:
        """Patrón del Dt-stem."""
        return "PutaRRiS"
    
    # ========================================================================
    # PHONOLOGICAL FORMATION METHODS
    # ========================================================================
    
    def form_present(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma el presente del Dt-stem.
        
        Pattern: uPTaRRiS
        - SPECIAL: Present = Preterite (same pattern)
        - u-prefix + -t- infix + R₂R₂
        - Fixed vowels: a...i
        
        Example:
            >>> # √PRS Dt
            >>> dt.form_present(3, 'sg', 'm')
            [u, p, t, a, r, r, i, s]  # uptarris
        """
        from .phonological_formation import (
            get_prefix, get_suffix, geminate_consonant,
            apply_t_assimilation
        )
        
        # 1. Get prefix with u-
        prefix = get_prefix(person, number, gender, use_u_prefix=True)
        
        # 2. Build stem with -t- infix
        t = get_consonant('t')
        t_assim = apply_t_assimilation(t, self.root.R1)
        
        stem = [
            self.root.R1,
            t_assim,
            get_vowel('a'),  # Fixed
            self.root.R2,
            # R₂ will be geminated
            get_vowel('i'),  # Fixed
            self.root.R3
        ]
        
        # 3. Geminate R₂
        stem = geminate_consonant(stem, 3)
        
        # 4. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 5. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_preterite(self, person: int = 3, number: str = 'sg',
                       gender: str = 'm') -> List[Phoneme]:
        """
        Forma el pretérito del Dt-stem.
        
        Pattern: uPTaRRiS (IDENTICAL to present!)
        - This is a SPECIAL feature of Dt-stem
        - Present and Preterite have the same form
        
        Example:
            >>> # √PRS Dt
            >>> dt.form_preterite(3, 'sg', 'm')
            [u, p, t, a, r, r, i, s]  # uptarris (same as present)
        """
        # Dt-stem SPECIAL: preterite = present
        return self.form_present(person, number, gender)
    
    def form_perfect(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> Optional[List[Phoneme]]:
        """
        Dt-stem NO tiene perfecto (evita doble -t-).
        
        Returns:
            None
        """
        return None
    
    def form_imperative(self, number: str = 'sg',
                        gender: str = 'm') -> List[Phoneme]:
        """
        Forma el imperativo del Dt-stem.
        
        Pattern: PTaRRiS
        - No u-prefix
        - Has -t- infix
        - R₂ geminated
        
        Example:
            >>> # √PRS Dt
            >>> dt.form_imperative('sg', 'm')
            [p, t, a, r, r, i, s]  # ptarris
        """
        from .phonological_formation import (
            get_suffix, geminate_consonant, apply_t_assimilation
        )
        
        # 1. Build stem
        t = get_consonant('t')
        t_assim = apply_t_assimilation(t, self.root.R1)
        
        stem = [
            self.root.R1,
            t_assim,
            get_vowel('a'),
            self.root.R2,
            # R₂ will be geminated
            get_vowel('i'),
            self.root.R3
        ]
        
        # 2. Geminate R₂
        stem = geminate_consonant(stem, 3)
        
        # 3. Get suffix (no prefix for imperative)
        suffix = get_suffix(2, number, gender)
        
        # 4. Combine
        result = stem + suffix
        
        return result
    
    def form_stative(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """Dt-stem stative - not commonly used."""
        raise NotImplementedError("Dt-stem stative not commonly attested")
    
    def get_stem_vowel(self, form_type: VerbFormType) -> str:
        """Dt-stem uses FIXED vowel 'i' (second vowel)."""
        return 'i'


# ============================================================================
# DTN-STEM (PLURACCIONAL DE D)
# ============================================================================

@dataclass
class Dtn_Stem(VerbalStem):
    """Dtn-stem del Old Assyrian. D-stem pluraccional."""
    
    stem_type: StemType = field(default=StemType.DTN)
    
    def __post_init__(self):
        """Inicializa Dtn_Stem con valores por defecto."""
        super().__post_init__()
        object.__setattr__(self, 'semantic_function', SemanticFunction.PLURACTIONAL)
    
    @property
    def pattern_template(self) -> str:
        """Patrón del Dtn-stem."""
        return "uPtanaRRaS"
    
    # ========================================================================
    # PHONOLOGICAL FORMATION METHODS
    # ========================================================================
    
    def form_present(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma el presente del Dtn-stem.
        
        Pattern: uPTanaRRaS
        - u-prefix + -tan- infix + R₂R₂
        - Fixed vowels: a...a
        
        Example:
            >>> # √PRS Dtn
            >>> dtn.form_present(3, 'sg', 'm')
            [u, p, t, a, n, a, r, r, a, s]  # uptanarras
        """
        from .phonological_formation import (
            get_prefix, get_suffix, geminate_consonant
        )
        
        # 1. Get prefix with u-
        prefix = get_prefix(person, number, gender, use_u_prefix=True)
        
        # 2. Build stem: R₁ + t + a + n + a + R₂ + R₂ + a + R₃
        stem = [
            self.root.R1,
            get_consonant('t'),
            get_vowel('a'),
            get_consonant('n'),  # -tan- infix
            get_vowel('a'),
            self.root.R2,
            # R₂ will be geminated
            get_vowel('a'),  # Fixed
            self.root.R3
        ]
        
        # 3. Geminate R₂
        stem = geminate_consonant(stem, 5)
        
        # 4. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 5. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_preterite(self, person: int = 3, number: str = 'sg',
                       gender: str = 'm') -> List[Phoneme]:
        """
        Forma el pretérito del Dtn-stem.
        
        Pattern: uPTaRRaS
        - Only -t- (no -n-)
        - R₂ still geminated
        
        Example:
            >>> # √PRS Dtn
            >>> dtn.form_preterite(3, 'sg', 'm')
            [u, p, t, a, r, r, a, s]  # uptarras
        """
        from .phonological_formation import (
            get_prefix, get_suffix, geminate_consonant
        )
        
        # 1. Get prefix with u-
        prefix = get_prefix(person, number, gender, use_u_prefix=True)
        
        # 2. Build stem: R₁ + t + a + R₂ + R₂ + a + R₃ (no -n-)
        stem = [
            self.root.R1,
            get_consonant('t'),
            get_vowel('a'),
            self.root.R2,
            # R₂ will be geminated
            get_vowel('a'),  # Fixed
            self.root.R3
        ]
        
        # 3. Geminate R₂
        stem = geminate_consonant(stem, 3)
        
        # 4. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 5. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_perfect(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> Optional[List[Phoneme]]:
        """Dtn-stem NO tiene perfecto."""
        return None
    
    def form_imperative(self, number: str = 'sg',
                        gender: str = 'm') -> List[Phoneme]:
        """Dtn-stem imperative - not commonly attested."""
        raise NotImplementedError("Dtn imperative not commonly attested")
    
    def get_stem_vowel(self, form_type: VerbFormType) -> str:
        """Dtn-stem uses FIXED vowel 'a'."""
        return 'a'


# ============================================================================
# FUNCIONES DE FORMACIÓN
# ============================================================================

def form_d_stem(root: VerbalRoot,
                d_function: Optional[D_Function] = None,
                semantic_function: Optional[SemanticFunction] = None,
                meaning: Optional[str] = None) -> D_Stem:
    """
    Forma el D-stem de una raíz verbal.
    
    Args:
        root: Raíz verbal base
        d_function: Función específica del D
        semantic_function: Función semántica general
        meaning: Significado derivado
        
    Returns:
        D_Stem formado
        
    Example:
        >>> root = create_root('ḥ', 'd', 'ʾ', VowelClass.A_U, 'alegrarse')
        >>> d = form_d_stem(
        ...     root,
        ...     D_Function.FACTITIVE,
        ...     SemanticFunction.FACTITIVE,
        ...     'hacer feliz'
        ... )
    """
    return D_Stem(
        root=root,
        d_function=d_function,
        semantic_function=semantic_function,
        meaning=meaning
    )


def form_dt_stem(root: VerbalRoot,
                 semantic_function: Optional[SemanticFunction] = None,
                 voice: Optional[VoiceType] = None,
                 meaning: Optional[str] = None) -> Dt_Stem:
    """
    Forma el Dt-stem de una raíz verbal.
    
    Args:
        root: Raíz verbal base
        semantic_function: Función semántica
        voice: Voz gramatical
        meaning: Significado derivado
        
    Returns:
        Dt_Stem formado
    """
    return Dt_Stem(
        root=root,
        semantic_function=semantic_function,
        voice=voice,
        meaning=meaning
    )


def form_dtn_stem(root: VerbalRoot,
                  meaning: Optional[str] = None) -> Dtn_Stem:
    """
    Forma el Dtn-stem (pluraccional) de una raíz verbal.
    
    Args:
        root: Raíz verbal base
        meaning: Significado derivado
        
    Returns:
        Dtn_Stem formado
    """
    return Dtn_Stem(
        root=root,
        meaning=meaning
    )


# ============================================================================
# EJEMPLOS DEL LIBRO
# ============================================================================

# D-stem factitivos (§ 17.3.2 sub (1))
D_FACTITIVE_EXAMPLES = {
    'malāʾum': ('ser lleno', 'llenar'),
    'ḥadāʾum': ('alegrarse', 'hacer feliz'),
    'baʾāšum': ('venir a vergüenza', 'avergonzar'),
    'naḥādum': ('cuidar', 'informar')
}

# D-stem transitivo agentivo (§ 17.3.2 sub (2))
D_TRANSITIVE_EXAMPLES = {
    'lamādum': ('conocer', 'informar'),
    'magārum': ('estar de acuerdo', 'hacer estar de acuerdo'),
    'labāšum': ('llevar puesto', 'vestir a otro')
}

# D-stem con pluralidad verbal (§ 17.3.2 sub (3a))
D_PLURAL_EXAMPLES = {
    'barāʾum': 'inspeccionar (tablillas)',
    'epāšum': 'hacer, arreglar',
    'gamārum': 'resolver (disputas)',
    'ḥarāmum': 'certificar (tablillas)',
    'šaqālum': 'pagar (múltiples veces)'
}

# D tantum (§ 17.3.2 sub (4))
D_TANTUM_EXAMPLES = {
    'ahhurum': 'estar retrasado',
    'dappurum': 'irse, ausentarse',
    'kallumum': 'mostrar',
    'kaššuum': 'obtener ganancia',
    'kaʾūlum': 'sostener',
    'massūḫum': 'despreciar',
    'naddūdum': 'buscar',
    'qaʾuum': 'esperar',
    'waššūrum': 'liberar'
}

# Dt-stem ejemplos (§ 17.3.4)
DT_EXAMPLES = {
    'kaʾulum': ('medio/pasivo', 'ser sostenido'),
    'šabāʾum': ('medio/pasivo', 'ser satisfecho'),
    'waššūrum': ('medio/pasivo', 'ser liberado'),
    'kabāsum': ('reciprocal', 'remitirse mutuamente'),
    'kuānum': ('reciprocal', 'confirmar responsabilidad mutua'),
    'zakāʾum': ('reflexivo', 'librarse'),
    'rakāsum': ('reflexivo', 'obligarse')
}

"""
N-stem y Ntn-stem del Old Assyrian.

ITERACIÓN 8 - Stems verbales derivados.

Implementa:
- N-stem: Medio/pasivo con prefijo nasal
- Ntn-stem: N pluraccional

Basado en Kouwenberg (2017) § 17.5.

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
# FUNCIONES ESPECÍFICAS DEL N-STEM
# ============================================================================

class N_Function(Enum):
    """
    Funciones específicas del N-stem.
    
    Basado en § 17.5.2.
    """
    
    MEDIOPASSIVE = "mediopassive"      # (Medio)pasivo (mayoría)
    RECIPROCAL = "reciprocal"          # Reciprocal
    REFLEXIVE = "reflexive"            # Reflexivo (dudoso)
    ATYPICAL_ACTIVE = "atyp_active"    # Activo atípico (našāʾum)
    INGRESSIVE = "ingressive"          # Ingresivo (de intransitivos)
    N_TANTUM = "n_tantum"              # Solo N, no G


# ============================================================================
# N-STEM (MEDIO/PASIVO)
# ============================================================================

@dataclass
class N_Stem(VerbalStem):
    """N-stem del Old Assyrian. Stem medio/pasivo con prefijo nasal."""
    
    stem_type: StemType = field(default=StemType.N)
    
    n_function: Optional[N_Function] = None
    
    def __post_init__(self):
        """Inicializa N_Stem con valores por defecto."""
        super().__post_init__()
    
    @property
    def pattern_template(self) -> str:
        """Patrón del N-stem."""
        return "iPPaRaS"
    
    @property
    def present_vowel(self) -> str:
        """Vocal del presente según clase vocálica."""
        return self.root.vowel_class.present_vowel
    
    @property
    def is_passive(self) -> bool:
        """Verifica si es N pasivo."""
        return (self.n_function == N_Function.MEDIOPASSIVE or
                self.semantic_function == SemanticFunction.PASSIVE_N)
    
    @property
    def is_reciprocal(self) -> bool:
        """Verifica si es N reciprocal."""
        return (self.n_function == N_Function.RECIPROCAL or
                self.semantic_function == SemanticFunction.RECIPROCAL)
    
    @property
    def is_ingressive(self) -> bool:
        """Verifica si es N ingresivo."""
        return (self.n_function == N_Function.INGRESSIVE or
                self.semantic_function == SemanticFunction.INGRESSIVE)
    
    # ========================================================================
    # PHONOLOGICAL FORMATION METHODS
    # ========================================================================
    
    def form_present(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma el presente del N-stem.
        
        Pattern: iPPaRaS
        - Nasal assimilation: n + R₁ → R₁R₁
        - Vowel same as G present
        
        Example:
            >>> # √PRS N 'ser separado'
            >>> n.form_present(3, 'sg', 'm')
            [i, p, p, a, r, a, s]  # ipparas (< *inparas)
        """
        from .phonological_formation import (
            get_prefix, get_suffix, apply_nasal_assimilation,
            geminate_consonant, apply_vowel_assimilation
        )
        
        # 1. Get prefix
        prefix = get_prefix(person, number, gender, use_u_prefix=False)
        
        # 2. Apply nasal assimilation: n + R₁ → R₁
        # The result will be geminated R₁
        # Build stem: R₁ + R₁ + a + R₂ + vowel + R₃
        present_vowel = self.present_vowel
        
        stem = [
            self.root.R1,
            self.root.R1,  # Geminated from nasal assimilation
            get_vowel('a'),
            self.root.R2,
            get_vowel(present_vowel),
            self.root.R3
        ]
        
        # 3. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 4. Apply vowel assimilation if needed (like G-stem)
        if suffix and self.root.vowel_class in [
            VowelClass.A_A, VowelClass.A_U, VowelClass.A_I
        ]:
            suffix_vowel = str(suffix[0])
            stem = apply_vowel_assimilation(stem, suffix_vowel)
        
        # 5. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_preterite(self, person: int = 3, number: str = 'sg',
                       gender: str = 'm') -> List[Phoneme]:
        """
        Forma el pretérito del N-stem.
        
        Pattern: iPPeRiS
        - Nasal assimilation: n + R₁ → R₁R₁
        - Special vowel assimilation: a → e (when followed by i/u)
        
        Example:
            >>> # √PRS N
            >>> n.form_preterite(3, 'sg', 'm')
            [i, p, p, e, r, i, s]  # ipperis (< *ipparis)
        """
        from .phonological_formation import (
            get_prefix, get_suffix
        )
        
        # 1. Get prefix
        prefix = get_prefix(person, number, gender, use_u_prefix=False)
        
        # 2. Build stem with R₁R₁ (nasal assimilation)
        # N-stem preterite ALWAYS uses 'i' regardless of vowel class
        # Pattern: iPPeRiS (with special a→e assimilation)
        
        stem = [
            self.root.R1,
            self.root.R1,  # Geminated
            get_vowel('e'),  # Special N-stem: a → e
            self.root.R2,
            get_vowel('i'),  # N-stem always 'i' in preterite
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
        Forma el perfecto del N-stem.
        
        Pattern: iTTaPRaS
        - Complex interaction between nasal and -t-
        - The exact pattern varies, simplified here
        
        Example:
            >>> # √PRS N
            >>> n.form_perfect(3, 'sg', 'm')
            [i, t, t, a, p, r, a, s]  # ittapras (simplified)
        """
        from .phonological_formation import get_prefix, get_suffix
        
        # 1. Get prefix
        prefix = get_prefix(person, number, gender, use_u_prefix=False)
        
        # 2. Build stem: t + t + a + R₁ + R₂ + a + R₃
        # (Simplified - n + t → tt at beginning)
        stem = [
            get_consonant('t'),
            get_consonant('t'),  # Assimilation result
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
    
    def form_imperative(self, number: str = 'sg',
                        gender: str = 'm') -> List[Phoneme]:
        """
        Forma el imperativo del N-stem.
        
        Pattern: PPaRiS
        - R₁ geminated (from nasal assimilation)
        - No prefix
        
        Example:
            >>> # √PRS N
            >>> n.form_imperative('sg', 'm')
            [p, p, a, r, i, s]  # pparis
        """
        from .phonological_formation import get_suffix
        
        # 1. Build stem: R₁ + R₁ + a + R₂ + i + R₃
        stem = [
            self.root.R1,
            self.root.R1,  # Geminated
            get_vowel('a'),
            self.root.R2,
            get_vowel('i'),
            self.root.R3
        ]
        
        # 2. Get suffix (no prefix)
        suffix = get_suffix(2, number, gender)
        
        # 3. Combine
        result = stem + suffix
        
        return result
    
    def form_stative(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """N-stem stative - not commonly used."""
        raise NotImplementedError("N-stem stative not commonly attested")
    
    def get_stem_vowel(self, form_type: VerbFormType) -> str:
        """
        Obtiene la vocal del stem según el tipo de forma.
        
        N-stem usa las mismas vocales que G-stem.
        """
        if form_type == VerbFormType.PRESENT:
            return self.present_vowel
        elif form_type == VerbFormType.PRETERITE:
            # Special: check if assimilation applies
            pret_vowel = self.root.vowel_class.preterite_vowel
            if pret_vowel in ['i', 'u']:
                return 'e'  # First vowel becomes 'e'
            return 'a'
        else:
            return 'a'


# ============================================================================
# NTN-STEM (PLURACCIONAL DE N)
# ============================================================================

@dataclass
class Ntn_Stem(VerbalStem):
    """Ntn-stem del Old Assyrian. N pluraccional."""
    
    stem_type: StemType = field(default=StemType.NTN)
    
    def __post_init__(self):
        """Inicializa Ntn_Stem con valores por defecto."""
        super().__post_init__()
        object.__setattr__(self, 'semantic_function', SemanticFunction.PLURACTIONAL)
    
    @property
    def pattern_template(self) -> str:
        """Patrón del Ntn-stem."""
        return "iTTanaPRaS"
    
    @property
    def present_vowel(self) -> str:
        """Vocal del presente según clase vocálica."""
        return self.root.vowel_class.present_vowel
    
    # ========================================================================
    # PHONOLOGICAL FORMATION METHODS
    # ========================================================================
    
    def form_present(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma el presente del Ntn-stem.
        
        Pattern: iTTanaPRaS
        - Nasal assimilation + -tan- infix
        
        Example:
            >>> # √PRS Ntn
            >>> ntn.form_present(3, 'sg', 'm')
            [i, t, t, a, n, a, p, r, a, s]  # ittanaparas
        """
        from .phonological_formation import get_prefix, get_suffix
        
        # 1. Get prefix
        prefix = get_prefix(person, number, gender, use_u_prefix=False)
        
        # 2. Build stem: R₁ + t + t + a + n + a + R₂ + a + R₃
        present_vowel = self.present_vowel
        
        stem = [
            self.root.R1,
            get_consonant('t'),
            get_consonant('t'),
            get_vowel('a'),
            get_consonant('n'),
            get_vowel('a'),
            self.root.R2,
            get_vowel(present_vowel),
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
        Forma el pretérito del Ntn-stem.
        
        Pattern: iTTaPRaS
        - Like Ntn present but without -n-
        
        Example:
            >>> # √PRS Ntn
            >>> ntn.form_preterite(3, 'sg', 'm')
            [i, t, t, a, p, r, a, s]  # ittaparas
        """
        from .phonological_formation import get_prefix, get_suffix
        
        # 1. Get prefix
        prefix = get_prefix(person, number, gender, use_u_prefix=False)
        
        # 2. Build stem: R₁ + t + t + a + R₂ + a + R₃
        stem = [
            self.root.R1,
            get_consonant('t'),
            get_consonant('t'),
            get_vowel('a'),
            self.root.R2,
            get_vowel('a'),
            self.root.R3
        ]
        
        # 3. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 4. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_perfect(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> Optional[List[Phoneme]]:
        """Ntn-stem NO tiene perfecto."""
        return None
    
    def form_imperative(self, number: str = 'sg',
                        gender: str = 'm') -> List[Phoneme]:
        """Ntn-stem NO tiene imperativo común."""
        raise NotImplementedError("Ntn imperative not attested")
    
    def get_stem_vowel(self, form_type: VerbFormType) -> str:
        """Ntn usa 'a' principalmente."""
        return 'a'


# ============================================================================
# FUNCIONES DE FORMACIÓN
# ============================================================================

def form_n_stem(root: VerbalRoot,
                n_function: Optional[N_Function] = None,
                semantic_function: Optional[SemanticFunction] = None,
                voice: Optional[VoiceType] = None,
                meaning: Optional[str] = None) -> N_Stem:
    """
    Forma el N-stem de una raíz verbal.
    
    Args:
        root: Raíz verbal base
        n_function: Función específica del N
        semantic_function: Función semántica general
        voice: Voz gramatical
        meaning: Significado derivado
        
    Returns:
        N_Stem formado
        
    Example:
        >>> root = create_root('p', 't', 'ʾ', VowelClass.A_U, 'abrir')
        >>> n = form_n_stem(
        ...     root,
        ...     N_Function.MEDIOPASSIVE,
        ...     SemanticFunction.PASSIVE_N,
        ...     VoiceType.PASSIVE,
        ...     'ser abierto'
        ... )
    """
    return N_Stem(
        root=root,
        n_function=n_function,
        semantic_function=semantic_function,
        voice=voice,
        meaning=meaning
    )


def form_ntn_stem(root: VerbalRoot,
                  voice: Optional[VoiceType] = None,
                  meaning: Optional[str] = None) -> Ntn_Stem:
    """
    Forma el Ntn-stem (pluraccional) de una raíz verbal.
    
    Args:
        root: Raíz verbal base
        voice: Voz gramatical
        meaning: Significado derivado
        
    Returns:
        Ntn_Stem formado
    """
    return Ntn_Stem(
        root=root,
        voice=voice,
        meaning=meaning
    )


# ============================================================================
# EJEMPLOS DEL LIBRO
# ============================================================================

# N-stem (medio)pasivos (§ 17.5.2 sub (1))
N_PASSIVE_EXAMPLES = {
    'laqāʾum': 'ser tomado, recibido',
    'patāʾum': 'ser abierto',
    'šaqālum': 'ser pagado'
}

# N-stem reciprocales (§ 17.5.2 sub (2))
N_RECIPROCAL_EXAMPLES = {
    'awāʾum': 'hablar (mutuamente)',
    'ezābum': 'divorciarse',
    'garāʾum': 'pelear',
    'lawāʾum': '?',
    'magārum': 'llegar a acuerdo',
    'mahārum': 'encontrarse',
    'parāsum': 'divorciarse',
    'ṣabātum': 'agarrarse mutuamente; pelear'
}

# N-stem reflexivos (§ 17.5.2 sub (3)) - DUDOSOS
N_REFLEXIVE_EXAMPLES = {
    'lapātum': 'registrarse (como garante)',
    'šakānum': 'colocarse (al juramento del río)'
}

# N-stem activo atípico (§ 17.5.2 sub (4))
N_ATYPICAL_EXAMPLES = {
    'našāʾum': 'transportar (mercancía)',
    'aDāmum': 'invertir'
}

# N-stem ingresivos (§ 17.5.2 sub (5))
N_INGRESSIVE_EXAMPLES = {
    'bašāʾum': 'llegar a existir, hacerse disponible',
    'ḥabālum': 'endeudarse',
    'takālum': 'poner confianza en',
    'ḥamātum': 'empezar a arder',
    'marāʾum': 'engordar',
    'saḥārum': 'cambiar de opinión'
}

# N tantum (§ 17.5.2 sub (6))
N_TANTUM_EXAMPLES = {
    'nahdūrum': 'preocuparse',
    'nakṣūdum': 'ser retrasado',
    'naplusum': 'observar',
    'našlūlum': 'arrastrarse',
    'nābutum': 'huir'
}

# Ntn-stem ejemplos (§ 17.5.3)
NTN_EXAMPLES = {
    'nadāʾum': 'ser puesto constantemente',
    'šakānum': 'ser colocado siempre',
    'ṣabātum': 'ser agarrado constantemente',
    'magārum': 'hacer tratos constantemente',
    'ṣarāpum': 'estallar cada vez',
    'ekālum': 'oscurecerse constantemente',
    'naplusum': 'observar constantemente',
    'sahārum': 'ser zarandeado'
}


# ============================================================================
# PROCESO DE ASIMILACIÓN NASAL
# ============================================================================

def nasal_assimilation_pattern(r1_symbol: str) -> str:
    """
    Demuestra el proceso de asimilación nasal.
    
    El prefijo n- se asimila a R₁, resultando en geminación.
    
    Args:
        r1_symbol: Símbolo de la primera radical
        
    Returns:
        Patrón resultante mostrando asimilación
        
    Examples:
        >>> nasal_assimilation_pattern('p')
        'n + p → pp (ipparras)'
        >>> nasal_assimilation_pattern('ṣ')
        'n + ṣ → ṣṣ (iṣṣabbat)'
    """
    return f"n + {r1_symbol} → {r1_symbol}{r1_symbol}"


def vowel_assimilation_pattern() -> str:
    """
    Demuestra el proceso de asimilación vocálica en N pretérito.
    
    Returns:
        String mostrando el proceso de asimilación
        
    Example:
        >>> print(vowel_assimilation_pattern())
        'ipparis → *ippiris → ipperis'
    """
    return "ipparis → *ippiris → ipperis (§ 3.4.5.2)"

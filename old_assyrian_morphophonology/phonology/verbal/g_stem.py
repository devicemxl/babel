"""
G-stem y Gt-stem del Old Assyrian.

ITERACIÓN 8 - Stems verbales derivados.

Implementa:
- G-stem: Grundstamm (stem base, no marcado)
- Gt-stem: G + infijo -t- (reciprocal/reflexivo/lexicalizado)
- Gtn-stem: G + -t- + geminación R₂ (pluraccional)

Basado en Kouwenberg (2017) § 17.2.

Autor: Claude
Fecha: 2026-02-10
"""

from dataclasses import dataclass, field
from typing import List, Optional

from ..phoneme import Phoneme, Vowel, Consonant
from ..inventory import get_vowel, get_consonant
from .stem import VerbalRoot, VerbalStem
from .enums import StemType, VoiceType, SemanticFunction, VowelClass, VerbFormType


# ============================================================================
# G-STEM (BASE)
# ============================================================================

@dataclass
class G_Stem(VerbalStem):
    """
    G-stem (Grundstamm) del Old Assyrian.
    
    El stem base, no marcado, del cual derivan todos los demás stems.
    
    Características (basado en § 16-17):
    - Sin marcadores morfológicos adicionales
    - Distingue clases vocálicas (a/u, a/a, a/i, i/i, u/u)
    - Patrón base: PaRvS
    - Significado: acción simple/base
    
    Examples:
        >>> # parāsum (a/u) 'decidir, separar'
        >>> prs_root = create_root('p', 'r', 's', VowelClass.A_U, 'decidir')
        >>> g_stem = G_Stem(root=prs_root)
        >>> g_stem.pattern_template
        'PaRvS'
    """
    
    stem_type: StemType = field(default=StemType.G)
    
    def __post_init__(self):
        """Inicializa G-stem con valores por defecto."""
        super().__post_init__()
        object.__setattr__(self, 'semantic_function', SemanticFunction.BASE)
        object.__setattr__(self, 'voice', VoiceType.ACTIVE)
    
    @property
    def present_vowel(self) -> str:
        """
        Vocal del presente según clase vocálica.
        
        Returns:
            'a', 'i', o 'u' según la clase
        """
        return self.root.vowel_class.present_vowel
    
    @property
    def preterite_vowel(self) -> str:
        """
        Vocal del pretérito según clase vocálica.
        
        Returns:
            'a', 'i', o 'u' según la clase
        """
        return self.root.vowel_class.preterite_vowel
    
    # ========================================================================
    # PHONOLOGICAL FORMATION METHODS
    # ========================================================================
    
    def form_present(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma el presente del G-stem.
        
        Pattern: PaRRvS
        - Gemination of R₂
        - Vowel after R₂ depends on vowel class
        
        Example:
            >>> # √PRS (parāsum a/u)
            >>> root = create_root('p', 'r', 's', VowelClass.A_U, 'separar')
            >>> g = G_Stem(root=root)
            >>> g.form_present(3, 'sg', 'm')
            [i, p, a, r, r, a, s]  # iparras
        """
        from .phonological_formation import (
            get_prefix, get_suffix, geminate_consonant,
            apply_vowel_assimilation, phonemes_to_string
        )
        
        # 1. Get prefix
        prefix = get_prefix(person, number, gender, use_u_prefix=False)
        
        # 2. Build stem: R₁ + a + R₂ + R₂ + vowel + R₃
        present_vowel = self.present_vowel  # From vowel class
        
        stem = [
            self.root.R1,
            get_vowel('a'),
            self.root.R2,
            # R₂ will be geminated
            get_vowel(present_vowel),
            self.root.R3
        ]
        
        # 3. Geminate R₂ (index 2 in stem)
        stem = geminate_consonant(stem, 2)
        
        # 4. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 5. Apply vowel assimilation if needed
        if suffix and self.root.vowel_class in [
            VowelClass.A_A, VowelClass.A_U, VowelClass.A_I
        ]:
            # Extract suffix vowel
            suffix_vowel = str(suffix[0]) if suffix else None
            if suffix_vowel:
                stem = apply_vowel_assimilation(stem, suffix_vowel)
        
        # 6. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_preterite(self, person: int = 3, number: str = 'sg',
                       gender: str = 'm') -> List[Phoneme]:
        """
        Forma el pretérito del G-stem.
        
        Pattern: PRvS
        - No gemination
        - Vowel after R₂ depends on vowel class
        
        Example:
            >>> # √PRS (parāsum a/u)
            >>> g.form_preterite(3, 'sg', 'm')
            [i, p, r, u, s]  # iprus
        """
        from .phonological_formation import (
            get_prefix, get_suffix, apply_vowel_assimilation,
            apply_syncope
        )
        
        # 1. Get prefix
        prefix = get_prefix(person, number, gender, use_u_prefix=False)
        
        # 2. Build stem: R₁ + R₂ + vowel + R₃
        preterite_vowel = self.preterite_vowel  # From vowel class
        
        stem = [
            self.root.R1,
            self.root.R2,
            get_vowel(preterite_vowel),
            self.root.R3
        ]
        
        # 3. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 4. Apply syncope if a/i class with ending
        if suffix and self.root.vowel_class == VowelClass.A_I:
            stem = apply_syncope(stem, has_ending=True)
        
        # 5. Apply vowel assimilation if a/a class with ending
        if suffix and self.root.vowel_class == VowelClass.A_A:
            suffix_vowel = str(suffix[0])
            stem = apply_vowel_assimilation(stem, suffix_vowel)
        
        # 6. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_perfect(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> Optional[List[Phoneme]]:
        """
        Forma el perfecto del G-stem.
        
        Pattern: PtaRvS
        - Infix -t- after R₁
        - Vowel same as present
        - Syncope if ending present
        
        Example:
            >>> # √PRS (parāsum a/u)
            >>> g.form_perfect(3, 'sg', 'm')
            [i, p, t, a, r, a, s]  # iptaras
        """
        from .phonological_formation import (
            get_prefix, get_suffix, insert_t_infix,
            apply_t_assimilation, apply_syncope
        )
        
        # 1. Get prefix
        prefix = get_prefix(person, number, gender, use_u_prefix=False)
        
        # 2. Insert -t- infix
        t = get_consonant('t')
        t_assim = apply_t_assimilation(t, self.root.R1)
        
        # 3. Build stem: R₁ + t + vowel + R₂ + vowel + R₃
        present_vowel = self.present_vowel  # Perfect uses present vowel
        
        stem = [
            self.root.R1,
            t_assim,
            get_vowel(present_vowel),
            self.root.R2,
            get_vowel(present_vowel),
            self.root.R3
        ]
        
        # 4. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 5. Apply syncope if ending present
        if suffix:
            stem = apply_syncope(stem, has_ending=True)
        
        # 6. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_imperative(self, number: str = 'sg',
                        gender: str = 'm') -> List[Phoneme]:
        """
        Forma el imperativo del G-stem.
        
        Pattern: PRvS
        - Same as preterite (no prefix)
        - Vowel same as preterite
        - Syncope if ending present
        
        Example:
            >>> # √PRS (parāsum a/u)
            >>> g.form_imperative('sg', 'm')
            [p, u, r, u, s]  # purus
        """
        from .phonological_formation import get_suffix, apply_syncope
        
        # 1. Build stem: R₁ + vowel + R₂ + vowel + R₃ (sin ending)
        #    o R₁ + R₂ + vowel + R₃ (con ending, después de síncope)
        preterite_vowel = self.preterite_vowel
        
        stem = [
            self.root.R1,
            get_vowel(preterite_vowel),
            self.root.R2,
            get_vowel(preterite_vowel),
            self.root.R3
        ]
        
        # 2. Get suffix (no prefix for imperative)
        suffix = get_suffix(2, number, gender)  # Always 2nd person
        
        # 3. Apply syncope if ending present
        if suffix:
            stem = apply_syncope(stem, has_ending=True)
        
        # 4. Combine (no prefix)
        result = stem + suffix
        
        return result
    
    def form_stative(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma el estativo del G-stem.
        
        Pattern: PaRiS (most common for fientive verbs)
        
        Note: Only 3sm shows the stem vowel clearly.
        
        Example:
            >>> # √PRS (parāsum a/u)
            >>> g.form_stative(3, 'sg', 'm')
            [p, a, r, i, s]  # paris
        """
        # For now, only implement 3sm (simplest)
        # TODO: Implement full stative conjugation with endings
        
        if person == 3 and number == 'sg' and gender == 'm':
            # Pattern: R₁ + a + R₂ + i + R₃
            return [
                self.root.R1,
                get_vowel('a'),
                self.root.R2,
                get_vowel('i'),  # Standard PaRiS
                self.root.R3
            ]
        else:
            # TODO: Add endings for other persons
            raise NotImplementedError(
                "Stative forms with endings not yet implemented"
            )
    
    def get_stem_vowel(self, form_type: VerbFormType) -> str:
        """
        Obtiene la vocal del stem según el tipo de forma.
        
        Args:
            form_type: Tipo de forma verbal
            
        Returns:
            Vocal correspondiente
        """
        if form_type == VerbFormType.PRESENT:
            return self.present_vowel
        elif form_type == VerbFormType.PRETERITE:
            return self.preterite_vowel
        elif form_type == VerbFormType.PERFECT:
            return self.present_vowel  # Perfect uses present vowel
        elif form_type == VerbFormType.IMPERATIVE:
            return self.preterite_vowel  # Imperative uses preterite vowel
        else:
            return 'i'  # Default for other forms


# ============================================================================
# GT-STEM (RECIPROCAL/REFLEXIVO)
# ============================================================================

@dataclass
class Gt_Stem(VerbalStem):
    """
    Gt-stem del Old Assyrian.
    
    G-stem con infijo -t- después de R₁.
    
    Características (basado en § 17.2.1-17.2.2):
    - Marcador: infijo -t- después de R₁
    - Patrón: PitRaS
    - Distingue clases vocálicas (en formas finitas)
    - NO tiene formas perfectas (no doble -t-)
    - Metátesis š-t opcional
    
    Funciones semánticas (§ 17.2.2):
    1. Reciprocal (mayoría): acción mutua
    2. Reflexivo (pocos): acción sobre sí mismo
    3. Lexicalizado (sin función clara)
    
    Examples:
        >>> # šaʾālum Gt 'deliberar, tomar consejo' (reciprocal)
        >>> root = create_root('š', 'ʾ', 'l', VowelClass.A_A, 'preguntar')
        >>> gt_stem = Gt_Stem(
        ...     root=root,
        ...     semantic_function=SemanticFunction.RECIPROCAL,
        ...     meaning='deliberar'
        ... )
        
        >>> # pašāšum Gt 'ungirse' (reflexivo)
        >>> root2 = create_root('p', 'š', 'š', VowelClass.A_U, 'ungir')
        >>> gt_stem2 = Gt_Stem(
        ...     root=root2,
        ...     semantic_function=SemanticFunction.REFLEXIVE,
        ...     meaning='ungirse a sí mismo'
        ... )
    """
    
    stem_type: StemType = field(default=StemType.GT)
    
    def __post_init__(self):
        """Inicializa Gt-stem con valores por defecto."""
        super().__post_init__()
    
    @property
    def pattern_template(self) -> str:
        """
        Patrón del Gt-stem.
        
        Returns:
            "PitRaS" para formas sin ending
            
        Note:
            Vocal stem copia la del G presente
        """
        return "PitRaS"
    
    @property
    def stem_vowel(self) -> str:
        """
        Vocal del stem según clase vocálica del G.
        
        En formas finitas (excepto estativo):
        - Copia vocal del G presente
        
        En estativo, infinitivo, VA:
        - Siempre 'u'
        
        En participio:
        - Siempre 'i'
        
        Returns:
            Vocal correspondiente
        """
        return self.root.vowel_class.present_vowel
    
    # ========================================================================
    # PHONOLOGICAL FORMATION METHODS
    # ========================================================================
    
    def form_present(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma el presente del Gt-stem.
        
        Pattern: PitaRRaS
        - Infix -t- after R₁
        - Gemination of R₂
        - Vowel 'i' before -t-, 'a' throughout
        
        Example:
            >>> # √PRS Gt
            >>> gt.form_present(3, 'sg', 'm')
            [i, p, t, a, r, r, a, s]  # iptarras
        """
        from .phonological_formation import (
            get_prefix, get_suffix, geminate_consonant
        )
        
        # 1. Get prefix
        prefix = get_prefix(person, number, gender, use_u_prefix=False)
        
        # 2. Build stem: R₁ + t + a + R₂ + R₂ + a + R₃
        stem = [
            self.root.R1,
            get_consonant('t'),
            get_vowel('a'),
            self.root.R2,
            # R₂ will be geminated
            get_vowel('a'),
            self.root.R3
        ]
        
        # 3. Geminate R₂ (index 3 in stem after removing 'i')
        stem = geminate_consonant(stem, 3)
        
        # 4. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 5. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_preterite(self, person: int = 3, number: str = 'sg',
                       gender: str = 'm') -> List[Phoneme]:
        """
        Forma el pretérito del Gt-stem.
        
        Pattern: PitRiS
        - Infix -t- after R₁
        - Syncope: *PitaRiS → PitRiS
        - Vowel 'i' before -t- and after R₂
        
        Example:
            >>> # √PRS Gt
            >>> gt.form_preterite(3, 'sg', 'm')
            [i, p, t, r, i, s]  # iptris
        """
        from .phonological_formation import (
            get_prefix, get_suffix, apply_syncope
        )
        
        # 1. Get prefix
        prefix = get_prefix(person, number, gender, use_u_prefix=False)
        
        # 2. Build stem: R₁ + t + R₂ + i + R₃
        # (vowel after -t- is syncopated in base form)
        stem = [
            self.root.R1,
            get_consonant('t'),
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
        """
        Gt-stem NO tiene perfecto (double -t- no permitido).
        
        Returns:
            None
        """
        return None
    
    def form_imperative(self, number: str = 'sg',
                        gender: str = 'm') -> List[Phoneme]:
        """
        Forma el imperativo del Gt-stem.
        
        Pattern: PitRaS
        - Similar al presente pero sin prefix/suffix
        
        Example:
            >>> # √PRS Gt
            >>> gt.form_imperative('sg', 'm')
            [p, i, t, r, a, s]  # pitras
        """
        from .phonological_formation import get_suffix
        
        # 1. Build stem: R₁ + t + R₂ + a + R₃
        stem = [
            self.root.R1,
            get_consonant('t'),
            self.root.R2,
            get_vowel('a'),
            self.root.R3
        ]
        
        # 2. Get suffix (no prefix for imperative)
        suffix = get_suffix(2, number, gender)
        
        # 3. Combine
        result = stem + suffix
        
        return result
    
    def get_stem_vowel(self, form_type: VerbFormType) -> str:
        """
        Obtiene la vocal del stem según el tipo de forma.
        
        Gt usa vocales fijas: 'i' y 'a'
        """
        if form_type == VerbFormType.PRESENT:
            return 'a'
        elif form_type == VerbFormType.PRETERITE:
            return 'i'
        else:
            return 'a'  # Default


# ============================================================================
# GTN-STEM (PLURACCIONAL)
# ============================================================================

@dataclass
class Gtn_Stem(VerbalStem):
    """
    Gtn-stem del Old Assyrian.
    
    G-stem pluraccional con infijo -tan-/-t- y geminación de R₂.
    
    Características (basado en § 17.2.3-17.2.4):
    - Marcador: -tan- (Pres) / -t- (otros) + geminación R₂
    - Patrón Presente: PitanaRRaS
    - Patrón Pretérito: PitaRRaS
    - Distingue clases vocálicas
    - NO tiene perfecto, estativo, ni VA
    
    Función (§ 17.2.4): PLURACCIONAL
    - Frecuentativo/habitual/continuo
    - Distributivo
    - Pluralidad de constituyente
    - Intensidad/cuidado
    
    Examples:
        >>> # šamāʾum Gtn 'leer cuidadosamente' (intensidad)
        >>> root = create_root('š', 'm', 'ʾ', VowelClass.A_A, 'oír')
        >>> gtn_stem = Gtn_Stem(
        ...     root=root,
        ...     semantic_function=SemanticFunction.FREQUENTATIVE,
        ...     meaning='leer cuidadosamente/repetidamente'
        ... )
    """
    
    stem_type: StemType = field(default=StemType.GTN)
    
    def __post_init__(self):
        """Inicializa Gtn-stem con valores por defecto."""
        super().__post_init__()
        object.__setattr__(self, 'semantic_function', SemanticFunction.PLURACTIONAL)
    
    @property
    def pattern_template(self) -> str:
        """
        Patrón del Gtn-stem.
        
        Returns:
            "PitanaRRaS" para presente
            "PitaRRaS" para pretérito/imperativo
        """
        return "PitanaRRaS"  # Presente
    
    @property
    def stem_vowel(self) -> str:
        """
        Vocal del stem según clase vocálica.
        
        Igual que Gt: copia vocal del G presente.
        
        Returns:
            Vocal correspondiente
        """
        return self.root.vowel_class.present_vowel
    
    # ========================================================================
    # PHONOLOGICAL FORMATION METHODS
    # ========================================================================
    
    def form_present(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma el presente del Gtn-stem.
        
        Pattern: PitanaRRaS
        - Infix -tan- after R₁
        - Gemination of R₂
        
        Example:
            >>> # √PRS Gtn
            >>> gtn.form_present(3, 'sg', 'm')
            [i, p, t, a, n, a, r, r, a, s]  # iptanarras
        """
        from .phonological_formation import (
            get_prefix, get_suffix, geminate_consonant
        )
        
        # 1. Get prefix
        prefix = get_prefix(person, number, gender, use_u_prefix=False)
        
        # 2. Build stem: R₁ + t + a + n + a + R₂ + R₂ + a + R₃
        stem = [
            self.root.R1,
            get_consonant('t'),
            get_vowel('a'),
            get_consonant('n'),
            get_vowel('a'),
            self.root.R2,
            # R₂ will be geminated
            get_vowel('a'),
            self.root.R3
        ]
        
        # 3. Geminate R₂ (index 5 in stem)
        stem = geminate_consonant(stem, 5)
        
        # 4. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 5. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_preterite(self, person: int = 3, number: str = 'sg',
                       gender: str = 'm') -> List[Phoneme]:
        """
        Forma el pretérito del Gtn-stem.
        
        Pattern: PitaRRaS
        - Infix -t- (not -tan-)
        - Gemination of R₂
        
        Example:
            >>> # √PRS Gtn
            >>> gtn.form_preterite(3, 'sg', 'm')
            [i, p, t, a, r, r, a, s]  # iptarras (same as Gt present)
        """
        from .phonological_formation import (
            get_prefix, get_suffix, geminate_consonant
        )
        
        # 1. Get prefix
        prefix = get_prefix(person, number, gender, use_u_prefix=False)
        
        # 2. Build stem: R₁ + t + a + R₂ + R₂ + a + R₃
        stem = [
            self.root.R1,
            get_consonant('t'),
            get_vowel('a'),
            self.root.R2,
            # R₂ will be geminated
            get_vowel('a'),
            self.root.R3
        ]
        
        # 3. Geminate R₂ (index 3 in stem)
        stem = geminate_consonant(stem, 3)
        
        # 4. Get suffix
        suffix = get_suffix(person, number, gender)
        
        # 5. Combine
        result = prefix + stem + suffix
        
        return result
    
    def form_perfect(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> Optional[List[Phoneme]]:
        """Gtn-stem NO tiene perfecto."""
        return None
    
    def form_imperative(self, number: str = 'sg',
                        gender: str = 'm') -> List[Phoneme]:
        """Gtn-stem NO tiene imperativo común."""
        raise NotImplementedError("Gtn imperative not attested")
    
    def get_stem_vowel(self, form_type: VerbFormType) -> str:
        """Gtn usa 'a' para todas las formas."""
        return 'a'


# ============================================================================
# FUNCIONES DE FORMACIÓN
# ============================================================================

def form_gt_stem(root: VerbalRoot,
                 semantic_function: Optional[SemanticFunction] = None,
                 meaning: Optional[str] = None) -> Gt_Stem:
    """
    Forma el Gt-stem de una raíz verbal.
    
    Args:
        root: Raíz verbal base
        semantic_function: Función semántica (reciprocal/reflexivo/lexicalizado)
        meaning: Significado derivado
        
    Returns:
        Gt_Stem formado
        
    Example:
        >>> root = create_root('m', 'š', 'l', VowelClass.I_I, 'parecerse')
        >>> gt = form_gt_stem(
        ...     root,
        ...     SemanticFunction.RECIPROCAL,
        ...     'parecerse mutuamente'
        ... )
    """
    return Gt_Stem(
        root=root,
        semantic_function=semantic_function,
        meaning=meaning
    )


def form_gtn_stem(root: VerbalRoot,
                  meaning: Optional[str] = None) -> Gtn_Stem:
    """
    Forma el Gtn-stem (pluraccional) de una raíz verbal.
    
    Args:
        root: Raíz verbal base
        meaning: Significado derivado
        
    Returns:
        Gtn_Stem formado
        
    Example:
        >>> root = create_root('l', 'q', 'ʾ', VowelClass.A_I, 'tomar')
        >>> gtn = form_gtn_stem(root, 'tomar repetidamente')
    """
    return Gtn_Stem(
        root=root,
        meaning=meaning
    )


# ============================================================================
# EJEMPLOS DEL LIBRO
# ============================================================================

# Gt-stems reciprocales (§ 17.2.2 sub (1))
GT_RECIPROCAL_EXAMPLES = {
    'šaʾālum': 'deliberar, tomar consejo',
    'šapākum': 'depositar conjuntamente',
    'naṭālum': 'mirarse mutuamente',
    'baʾārum': 'pelearse mutuamente',
    'emādum': 'estar en contacto',
    'enāʾum': 'intercambiar',
    'magārum': 'ponerse de acuerdo',
    'mahāṣum': 'hacer lo máximo',
    'malākum': 'deliberar',
    'mašālum': 'parecerse mutuamente',
    'nakārum': 'hacerse hostil mutuamente',
    'ragāmum': 'demandarse mutuamente'
}

# Gt-stems reflexivos (§ 17.2.2 sub (2))
GT_REFLEXIVE_EXAMPLES = {
    'pašāšum': 'ungirse',
    'labāšum': 'ponerse (ropa)',
    'šakānum': 'proveerse de',
    'lapātum': 'registrarse (como garante)'
}

# Gt-stems lexicalizados (§ 17.2.2 sub (3))
GT_LEXICALIZED_EXAMPLES = {
    'alākum': 'empezar a ir, partir',
    'šapāʾum': 'quedar en silencio',
    'leʾāʾum': 'estar perdido',
    'reʾāʾum': 'pastar'
}

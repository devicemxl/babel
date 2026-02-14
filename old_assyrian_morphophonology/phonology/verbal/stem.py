"""
Clase base para stems verbales del Old Assyrian.

ITERACIÓN 8 - Sistema de stems verbales derivados.

Define la estructura base para todos los stems verbales,
incluyendo raíz, tipo de stem, y características fonológicas.

Basado en Kouwenberg (2017) Capítulo 17.

Autor: Claude
Fecha: 2026-02-10
"""

from dataclasses import dataclass, field
from typing import List, Optional, Set

from ..phoneme import Phoneme, Vowel, Consonant
from .enums import (
    StemType, VoiceType, SemanticFunction, VowelClass,
    MorphologicalMarker, Productivity, VerbFormType,
    STEM_PRODUCTIVITY, STEM_MARKERS,
    STEM_DEFAULT_FUNCTION, STEM_DEFAULT_VOICE
)


# ============================================================================
# RAÍZ VERBAL
# ============================================================================

@dataclass
class VerbalRoot:
    """
    Raíz verbal triconsonántica del Old Assyrian.
    
    Representa la raíz abstracta de un verbo (√PRS),
    compuesta típicamente por 3 consonantes radicales.
    
    Attributes:
        radicals: Lista de consonantes radicales (R₁, R₂, R₃)
        vowel_class: Clase vocálica del G-stem
        gloss: Significado base de la raíz
        
    Examples:
        >>> # √PRS (parāsum 'decidir, separar')
        >>> root = VerbalRoot(
        ...     radicals=[get_consonant('p'), get_consonant('r'), get_consonant('s')],
        ...     vowel_class=VowelClass.A_U,
        ...     gloss='decidir'
        ... )
    """
    
    radicals: List[Consonant]
    vowel_class: VowelClass
    gloss: str = ""
    
    def __post_init__(self):
        """Valida que la raíz tenga 3 radicales."""
        if len(self.radicals) != 3:
            raise ValueError(
                f"Raíz verbal debe tener 3 radicales, tiene {len(self.radicals)}"
            )
    
    @property
    def R1(self) -> Consonant:
        """Primera consonante radical."""
        return self.radicals[0]
    
    @property
    def R2(self) -> Consonant:
        """Segunda consonante radical."""
        return self.radicals[1]
    
    @property
    def R3(self) -> Consonant:
        """Tercera consonante radical."""
        return self.radicals[2]
    
    @property
    def pattern(self) -> str:
        """
        Patrón consonántico de la raíz.
        
        Returns:
            String en formato "C₁C₂C₃"
            
        Example:
            >>> root.pattern
            'PRS'
        """
        return ''.join(r.symbol for r in self.radicals).upper()
    
    def __str__(self) -> str:
        """Representación de la raíz como √PRS."""
        return f"√{self.pattern}"
    
    def __repr__(self) -> str:
        return (
            f"VerbalRoot(pattern={self.pattern}, "
            f"class={self.vowel_class}, gloss='{self.gloss}')"
        )


# ============================================================================
# STEM VERBAL BASE
# ============================================================================

@dataclass
class VerbalStem:
    """
    Stem verbal del Old Assyrian.
    
    Representa un stem derivado de una raíz verbal con marcadores
    morfológicos específicos y función semántica.
    
    Basado en § 17.1-17.5 de Kouwenberg (2017).
    
    Attributes:
        root: Raíz verbal base
        stem_type: Tipo de stem (G, D, Š, N, etc.)
        phonemes: Secuencia fonémica del stem
        semantic_function: Función semántica del stem
        voice: Voz gramatical
        meaning: Significado derivado (si difiere de raíz)
        
    Examples:
        >>> # Gt-stem de √PRS (parāsum 'decidir')
        >>> # Significado reciprocal: 'separarse mutuamente'
        >>> gt_stem = VerbalStem(
        ...     root=prs_root,
        ...     stem_type=StemType.GT,
        ...     phonemes=[...],  # pitRaS
        ...     semantic_function=SemanticFunction.RECIPROCAL,
        ...     meaning='separarse mutuamente'
        ... )
    """
    
    root: VerbalRoot
    stem_type: StemType
    phonemes: List[Phoneme] = field(default_factory=list)
    semantic_function: Optional[SemanticFunction] = None
    voice: Optional[VoiceType] = None
    meaning: Optional[str] = None
    
    def __post_init__(self):
        """Inicializa valores por defecto basados en tipo de stem."""
        # Si no se especificó función semántica, usar la por defecto
        if self.semantic_function is None:
            self.semantic_function = STEM_DEFAULT_FUNCTION[self.stem_type]
        
        # Si no se especificó voz, usar la por defecto
        if self.voice is None:
            self.voice = STEM_DEFAULT_VOICE[self.stem_type]
    
    @property
    def markers(self) -> Set[MorphologicalMarker]:
        """
        Marcadores morfológicos del stem.
        
        Returns:
            Conjunto de marcadores que caracterizan este stem
            
        Example:
            >>> gt_stem.markers
            {MorphologicalMarker.T_INFIX}
        """
        return STEM_MARKERS[self.stem_type]
    
    @property
    def productivity(self) -> Productivity:
        """
        Nivel de productividad del stem.
        
        Returns:
            Productividad basada en tipo de stem
        """
        return STEM_PRODUCTIVITY[self.stem_type]
    
    @property
    def has_t_infix(self) -> bool:
        """Verifica si el stem tiene infijo -t-."""
        return MorphologicalMarker.T_INFIX in self.markers
    
    @property
    def has_tan_infix(self) -> bool:
        """Verifica si el stem tiene infijo -tan- (pluraccional)."""
        return MorphologicalMarker.TAN_INFIX in self.markers
    
    @property
    def has_r2_gemination(self) -> bool:
        """Verifica si el stem geminada R₂."""
        return MorphologicalMarker.R2_GEMINATION in self.markers
    
    @property
    def has_r1_gemination(self) -> bool:
        """Verifica si el stem geminada R₁ (N-stem por asimilación)."""
        return MorphologicalMarker.R1_GEMINATION in self.markers
    
    @property
    def is_pluractional(self) -> bool:
        """Verifica si el stem es pluraccional (tan-stem)."""
        return self.stem_type.is_pluractional
    
    @property
    def base_stem_type(self) -> StemType:
        """
        Retorna el stem base del cual deriva este stem.
        
        Example:
            >>> gt_stem.base_stem_type
            StemType.G
            >>> dt_stem.base_stem_type
            StemType.D
        """
        return self.stem_type.base_stem
    
    @property
    def pattern_template(self) -> str:
        """
        Plantilla del patrón del stem.
        
        Returns:
            Patrón abstracto del stem (ej. "PitRaS", "PaRRuS")
            
        Note:
            Las subclases deben implementar patrones específicos
        """
        # Patrón básico por tipo de stem
        patterns = {
            StemType.G: "PaRvS",
            StemType.GT: "PitRaS",
            StemType.GTN: "PitaRRaS",
            StemType.D: "PaRRvS",
            StemType.DT: "PutaRRiS",
            StemType.DTN: "PutanaRRaS",
            StemType.SH: "ŠaPRvS",
            StemType.SHT1: "ŠuTaPRaS",
            StemType.SHT2: "ŠuTaPaRRaS",
            StemType.SHTN: "ŠuTanaPRaS",
            StemType.N: "iPPaRaS",
            StemType.NTN: "iTTanaPRaS"
        }
        return patterns.get(self.stem_type, "PaRvS")
    
    def get_transcription(self) -> str:
        """
        Transcripción fonológica del stem.
        
        Returns:
            String con transcripción en símbolos fonológicos
            
        Example:
            >>> gt_stem.get_transcription()
            'pitras'
        """
        if not self.phonemes:
            return ""
        return ''.join(p.symbol for p in self.phonemes)
    
    def distinguishes_vowel_classes(self) -> bool:
        """
        Verifica si este stem distingue clases vocálicas.
        
        Basado en § 17.2.1, § 17.3.1, § 17.4.1, § 17.5.1:
        - Gt, Gtn, N, Ntn: SÍ distinguen
        - D, Dt, Dtn, Š, Št, Štn: NO distinguen
        
        Returns:
            True si distingue clases vocálicas
        """
        distinguishing_stems = {
            StemType.G,
            StemType.GT,
            StemType.GTN,
            StemType.N,
            StemType.NTN
        }
        return self.stem_type in distinguishing_stems
    
    def allows_perfect(self) -> bool:
        """
        Verifica si este stem permite formas perfectas.
        
        Basado en § 17.2.1, § 17.3.3:
        OA no permite doble infijo -t-, por lo tanto:
        - Stems con -t-: NO tienen perfecto
        - Otros: SÍ tienen perfecto
        
        Returns:
            True si permite perfecto
        """
        return not self.has_t_infix
    
    # ========================================================================
    # HELPER METHODS FOR WEAK VERBS (ITERATION 9)
    # ========================================================================
    
    def _get_R1_for_present(self) -> Optional[Consonant]:
        """
        Retorna R₁ para presente.
        
        Override en verbos débiles para modificar o eliminar R₁.
        
        Returns:
            R₁ para presente (puede ser None si se elimina)
            
        Example (strong verb):
            >>> stem._get_R1_for_present()
            Consonant('p')
            
        Example (I/w verb):
            >>> # R₁ no aparece en presente (se contrae w+i→u)
            >>> stem._get_R1_for_present()
            None
        """
        return self.root.R1
    
    def _get_R1_for_preterite(self, assimilate_n: bool = False) -> List[Consonant]:
        """
        Retorna R₁ para pretérito.
        
        Override en verbos débiles para asimilación o pérdida de R₁.
        
        Args:
            assimilate_n: Si True y R₁=n, asimilar a R₂ (geminación)
        
        Returns:
            Lista de consonantes (puede estar vacía o geminada)
            
        Example (strong verb):
            >>> stem._get_R1_for_preterite()
            [Consonant('p')]
            
        Example (I/n verb with assimilation):
            >>> stem._get_R1_for_preterite(assimilate_n=True)
            [Consonant('ṣ'), Consonant('ṣ')]  # n+ṣ → ṣṣ
        """
        if assimilate_n and hasattr(self.root.R1, 'symbol') and self.root.R1.symbol == 'n':
            # Asimilación n + R₂ → R₂R₂
            return [self.root.R2, self.root.R2]
        else:
            return [self.root.R1] if self.root.R1 else []
    
    def _get_R1_for_perfect(self, assimilate_n: bool = False) -> List[Consonant]:
        """
        Retorna R₁ para perfect.
        
        Similar a pretérito pero puede tener comportamiento diferente.
        
        Args:
            assimilate_n: Si True y R₁=n, asimilar a infix-t o R₂
        
        Returns:
            Lista de consonantes
        """
        # Por defecto, mismo comportamiento que pretérito
        return self._get_R1_for_preterite(assimilate_n=assimilate_n)
    
    def _get_R1_for_imperative(self) -> Optional[Consonant]:
        """
        Retorna R₁ para imperativo.
        
        Override en verbos débiles para pérdida de R₁.
        
        Returns:
            R₁ para imperativo (puede ser None)
            
        Example (I/w verb):
            >>> # w desaparece en imperativo
            >>> stem._get_R1_for_imperative()
            None
        """
        return self.root.R1
    
    def _adjust_prefix_for_weak_verb(self, base_prefix: str, 
                                       form_type: VerbFormType) -> str:
        """
        Ajusta prefijo para verbos débiles.
        
        Override en verbos débiles para aplicar contracciones.
        
        Args:
            base_prefix: Prefijo base (ej: 'i' para presente)
            form_type: Tipo de forma verbal
        
        Returns:
            Prefijo ajustado
            
        Example (I/w fientive):
            >>> stem._adjust_prefix_for_weak_verb('i', VerbFormType.PRESENT)
            'u'  # w + i → u
            
        Example (strong):
            >>> stem._adjust_prefix_for_weak_verb('i', VerbFormType.PRESENT)
            'i'  # sin cambio
        """
        # Verbos fuertes: sin cambio
        return base_prefix
    
    def _should_geminate_R2_in_present(self) -> bool:
        """
        Determina si R₂ debe geminarse en presente.
        
        Override en verbos débiles con comportamiento especial.
        
        Returns:
            True si R₂ debe geminarse
            
        Example (strong):
            >>> stem._should_geminate_R2_in_present()
            True
            
        Example (I/w adjectival):
            >>> # NO geminación en adjetivales
            >>> stem._should_geminate_R2_in_present()
            False
        """
        # Verbos fuertes: siempre geminan R₂ en presente
        return True
    
    def _should_geminate_infix_t_in_perfect(self) -> bool:
        """
        Determina si infix-t debe geminarse en perfect.
        
        Override en verbos débiles con comportamiento especial.
        
        Returns:
            True si -t- debe geminarse
            
        Example (strong):
            >>> stem._should_geminate_infix_t_in_perfect()
            False  # i-ptaras (no geminación por defecto)
            
        Example (I/w fientive):
            >>> # Geminación -tt- en perfect
            >>> stem._should_geminate_infix_t_in_perfect()
            True  # ut-tašib
        """
        # Verbos fuertes: NO geminación de infix-t por defecto
        return False
    
    def _has_vocalic_ending(self, number: str, gender: str) -> bool:
        """
        Determina si la forma tiene ending vocálico.
        
        Útil para determinar síncope en verbos débiles.
        
        Args:
            number: 'sg', 'du', 'pl'
            gender: 'm', 'f'
        
        Returns:
            True si tiene ending vocálico
            
        Example:
            >>> stem._has_vocalic_ending('sg', 'm')
            False  # iparras (no ending)
            >>> stem._has_vocalic_ending('pl', 'm')
            True  # iparrasū (ending -ū)
        """
        # Endings vocálicos típicamente en:
        # - Plural masculino (-ū)
        # - Dual (-ā)
        # - Femenino singular 2da persona (-ī)
        if number == 'pl' and gender == 'm':
            return True
        if number == 'du':
            return True
        if number == 'sg' and gender == 'f':
            return True  # Algunas formas como 2fs
        return False
    
    # ========================================================================
    # PHONOLOGICAL FORMATION METHODS
    # ========================================================================
    
    def form_present(self, person: int = 3, number: str = 'sg', 
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma el presente del stem.
        
        Args:
            person: 1, 2, or 3
            number: 'sg', 'du', or 'pl'
            gender: 'm' or 'f'
            
        Returns:
            Secuencia de fonemas del presente
            
        Example:
            >>> root = create_root('p', 'r', 's', VowelClass.A_U, 'separar')
            >>> g = G_Stem(root=root)
            >>> g.form_present(3, 'sg', 'm')
            [i, p, a, r, r, a, s]  # iparras
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement form_present()"
        )
    
    def form_preterite(self, person: int = 3, number: str = 'sg',
                       gender: str = 'm') -> List[Phoneme]:
        """
        Forma el pretérito del stem.
        
        Args:
            person: 1, 2, or 3
            number: 'sg', 'du', or 'pl'
            gender: 'm' or 'f'
            
        Returns:
            Secuencia de fonemas del pretérito
            
        Example:
            >>> root = create_root('p', 'r', 's', VowelClass.A_U, 'separar')
            >>> g = G_Stem(root=root)
            >>> g.form_preterite(3, 'sg', 'm')
            [i, p, r, u, s]  # iprus
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement form_preterite()"
        )
    
    def form_perfect(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> Optional[List[Phoneme]]:
        """
        Forma el perfecto del stem (si existe).
        
        Args:
            person: 1, 2, or 3
            number: 'sg', 'du', or 'pl'
            gender: 'm' or 'f'
            
        Returns:
            Secuencia de fonemas del perfecto, o None si no tiene perfecto
            
        Example:
            >>> root = create_root('p', 'r', 's', VowelClass.A_U, 'separar')
            >>> g = G_Stem(root=root)
            >>> g.form_perfect(3, 'sg', 'm')
            [i, p, t, a, r, a, s]  # iptaras
            
            >>> gt = Gt_Stem(root=root)
            >>> gt.form_perfect(3, 'sg', 'm')
            None  # Gt no tiene perfecto
        """
        if not self.allows_perfect():
            return None
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement form_perfect()"
        )
    
    def form_imperative(self, number: str = 'sg',
                        gender: str = 'm') -> List[Phoneme]:
        """
        Forma el imperativo del stem.
        
        Args:
            number: 'sg' or 'pl' (no dual for imperative)
            gender: 'm' or 'f'
            
        Returns:
            Secuencia de fonemas del imperativo
            
        Example:
            >>> root = create_root('p', 'r', 's', VowelClass.A_U, 'separar')
            >>> g = G_Stem(root=root)
            >>> g.form_imperative('sg', 'm')
            [p, u, r, u, s]  # purus
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement form_imperative()"
        )
    
    def form_stative(self, person: int = 3, number: str = 'sg',
                     gender: str = 'm') -> List[Phoneme]:
        """
        Forma el estativo del stem.
        
        Args:
            person: 1, 2, or 3
            number: 'sg', 'du', or 'pl'
            gender: 'm' or 'f'
            
        Returns:
            Secuencia de fonemas del estativo
            
        Note:
            Solo la forma 3sm muestra la vocal del stem.
            Otras formas tienen endings que ocultan la vocal.
            
        Example:
            >>> root = create_root('p', 'r', 's', VowelClass.A_U, 'separar')
            >>> g = G_Stem(root=root)
            >>> g.form_stative(3, 'sg', 'm')
            [p, a, r, i, s]  # paris
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement form_stative()"
        )
    
    # Helper method para obtener vocal según forma
    def get_stem_vowel(self, form_type) -> str:
        """
        Obtiene la vocal del stem según el tipo de forma.
        
        Args:
            form_type: Tipo de forma verbal (VerbFormType)
            
        Returns:
            Vocal correspondiente ('a', 'i', 'u')
            
        Note:
            Subclases deben implementar esto según sus reglas.
            Por ejemplo, G-stem usa vowel_class, mientras que
            D-stem siempre usa 'a' en presente.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement get_stem_vowel()"
        )
    
    def __str__(self) -> str:
        """Representación legible del stem."""
        return f"{self.stem_type} of {self.root}"
    
    def __repr__(self) -> str:
        return (
            f"VerbalStem(root={self.root.pattern}, "
            f"type={self.stem_type}, "
            f"function={self.semantic_function})"
        )


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def create_root(r1: str, r2: str, r3: str, 
                vowel_class: VowelClass,
                gloss: str = "") -> VerbalRoot:
    """
    Crea una raíz verbal a partir de símbolos consonánticos.
    
    Args:
        r1: Primera radical (símbolo)
        r2: Segunda radical (símbolo)
        r3: Tercera radical (símbolo)
        vowel_class: Clase vocálica del verbo
        gloss: Significado base
        
    Returns:
        VerbalRoot inicializada
        
    Example:
        >>> prs = create_root('p', 'r', 's', VowelClass.A_U, 'decidir')
        >>> str(prs)
        '√PRS'
    """
    from ..inventory import get_consonant
    
    return VerbalRoot(
        radicals=[get_consonant(r1), get_consonant(r2), get_consonant(r3)],
        vowel_class=vowel_class,
        gloss=gloss
    )


def is_derived_from(stem: VerbalStem, base_type: StemType) -> bool:
    """
    Verifica si un stem deriva de cierto stem base.
    
    Args:
        stem: Stem verbal a verificar
        base_type: Tipo de stem base
        
    Returns:
        True si deriva del stem base especificado
        
    Example:
        >>> is_derived_from(gt_stem, StemType.G)
        True
        >>> is_derived_from(dt_stem, StemType.D)
        True
    """
    return stem.base_stem_type == base_type

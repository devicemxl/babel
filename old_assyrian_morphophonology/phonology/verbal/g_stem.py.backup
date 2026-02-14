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

from dataclasses import dataclass
from typing import List, Optional

from ..phoneme import Phoneme, Vowel, Consonant
from ..inventory import get_vowel, get_consonant
from .stem import VerbalRoot, VerbalStem
from .enums import StemType, VoiceType, SemanticFunction, VowelClass


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
    """Inicializa G-stem con valores por defecto."""
        # Inicializar valores base
        super().__post_init__()
        # Función semántica es siempre BASE
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
    """Inicializa Gt-stem con valores por defecto."""
        # Inicializar valores base
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
        # Para formas finitas: copia G presente
        return self.root.vowel_class.present_vowel


# ============================================================================
# GTN-STEM (PLURACCIONAL)
# ============================================================================

@dataclass
class Gtn_Stem(VerbalStem):
    """
    
    def __post_init__(self):
        """Inicializa Gtn-stem con valores por defecto."""
    
    # Sobrescribir stem_type con valor por defecto
    stem_type: StemType = StemType.GTN
        # Inicializar valores base
        super().__post_init__()
        # Función es pluraccional
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

"""
Representación de raíces débiles para el sistema verbal del Old Assyrian.

ITERACIÓN 9 - Verbos I-débil

Define:
- WeakConsonant: consonante débil con comportamiento especial
- WeakRoot: raíz verbal con una o más consonantes débiles
- Funciones helper para crear raíces débiles fácilmente

Basado en Kouwenberg (2017) Capítulo 18.

Autor: Claude
Fecha: 2026-02-12
"""

from dataclasses import dataclass
from typing import Union, Optional
import sys
import os

# Ajustar path para importar módulos del proyecto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from phonology import Phoneme, Consonant, Vowel
from phonology.verbal.enums import WeakVerbType, WeakPosition, VowelClass


# ============================================================================
# WEAK CONSONANT
# ============================================================================

@dataclass
class WeakConsonant:
    """
    Representa una consonante débil con comportamiento fonológico especial.
    
    Consonantes débiles en Old Assyrian:
    - w: bilabial approximant (I/w, III/w)
    - y: palatal approximant (I/*y histórico, III/y)
    - n: nasal con asimilación/pérdida (I/n)
    - ʔ: glottal stop (en II/aleph, III/aleph)
    - Ø: gutural perdida que causa alargamiento compensatorio (I/voc)
    
    Referencias:
    - § 3.3: Weak consonants en OA
    - § 18.1: Introducción a verbos débiles
    - § 18.2-18.4: Comportamiento específico por tipo
    
    Ejemplos:
        wasābum → R₁ = WeakConsonant('w', R1, 'contracts')
        ahāzum  → R₁ = WeakConsonant('Ø', R1, 'compensatory_lengthening')
        nadā'um → R₁ = WeakConsonant('n', R1, 'assimilates')
    """
    symbol: str  # 'w', 'y', 'n', 'ʔ', o 'Ø'
    position: WeakPosition
    behavior: str  # 'contracts', 'assimilates', 'lost', 'compensatory_lengthening'
    
    def __post_init__(self):
        """Validación de valores."""
        valid_symbols = {'w', 'y', 'n', 'ʔ', 'Ø'}
        if self.symbol not in valid_symbols:
            raise ValueError(f"Invalid weak consonant symbol: {self.symbol}. "
                           f"Must be one of {valid_symbols}")
        
        valid_behaviors = {'contracts', 'assimilates', 'lost', 'compensatory_lengthening'}
        if self.behavior not in valid_behaviors:
            raise ValueError(f"Invalid behavior: {self.behavior}. "
                           f"Must be one of {valid_behaviors}")
    
    def is_lost_guttural(self) -> bool:
        """
        Verifica si es gutural perdida que causa alargamiento compensatorio.
        
        Returns:
            True si es Ø con comportamiento compensatory_lengthening
        """
        return self.symbol == 'Ø' and self.behavior == 'compensatory_lengthening'
    
    def can_assimilate(self) -> bool:
        """
        Verifica si puede asimilar ante otra consonante.
        
        Returns:
            True si el behavior es 'assimilates' (típicamente n)
        """
        return self.behavior == 'assimilates'
    
    def contracts_with_i(self) -> bool:
        """
        Verifica si se contrae con vocal i del prefijo.
        
        Returns:
            True si w con behavior 'contracts'
        """
        return self.symbol == 'w' and self.behavior == 'contracts'
    
    def __str__(self) -> str:
        """Representación legible."""
        return f"{self.symbol} ({self.position.value}, {self.behavior})"
    
    def __repr__(self) -> str:
        return f"WeakConsonant('{self.symbol}', {self.position}, '{self.behavior}')"


# ============================================================================
# WEAK ROOT
# ============================================================================

@dataclass
class WeakRoot:
    """
    Raíz verbal con una o más consonantes débiles.
    
    A diferencia de Root (raíz fuerte), WeakRoot permite que R₁, R₂ o R₃
    sean WeakConsonant en vez de Consonant normal.
    
    Referencias:
    - § 18.1: Tipos de verbos débiles
    - § 18.2: I/w verbs
    - § 18.3: I/voc verbs
    - § 18.4: I/n verbs
    
    Attributes:
        R1: Primera radical (puede ser débil)
        R2: Segunda radical (puede ser débil)
        R3: Tercera radical (puede ser débil)
        vowel_class: Clase vocálica (a/u, i/i, etc.)
        meaning: Significado del verbo
        weak_type: Tipo específico de verbo débil
    
    Ejemplos:
        wasābum (I/w fientivo):
            R1 = WeakConsonant('w', R1, 'contracts')
            R2 = Consonant('s')
            R3 = Consonant('b')
            weak_type = I_W_FIENTIVE
        
        ahāzum (I/voc a):
            R1 = WeakConsonant('Ø', R1, 'compensatory_lengthening')
            R2 = Consonant('h')
            R3 = Consonant('z')
            weak_type = I_VOC_A
        
        nadā'um (I/n):
            R1 = WeakConsonant('n', R1, 'assimilates')
            R2 = Consonant('d')
            R3 = Consonant('ʔ')
            weak_type = I_N
        
        atawwum (doblemente débil - I/voc + II/gem):
            R1 = WeakConsonant('Ø', R1, 'compensatory_lengthening')
            R2 = Consonant('w')
            R3 = Consonant('w')  # R₂ = R₃ (geminado)
            weak_type = I_ATAWWUM
    """
    R1: Union[Consonant, WeakConsonant]
    R2: Union[Consonant, WeakConsonant]
    R3: Union[Consonant, WeakConsonant]
    vowel_class: VowelClass
    meaning: str
    weak_type: WeakVerbType
    
    def __post_init__(self):
        """Validación de consistencia entre weak_type y radicales."""
        # Validar que weak_type es consistente con R1/R2/R3
        if self.weak_type in [WeakVerbType.I_W_FIENTIVE, WeakVerbType.I_W_ADJECTIVAL]:
            if not isinstance(self.R1, WeakConsonant) or self.R1.symbol != 'w':
                raise ValueError(f"I/w verb debe tener R1 = WeakConsonant('w'), "
                               f"got R1 = {self.R1}")
        
        elif self.weak_type in [WeakVerbType.I_VOC_A, WeakVerbType.I_VOC_E, 
                                 WeakVerbType.I_ATAWWUM]:
            if not isinstance(self.R1, WeakConsonant) or not self.R1.is_lost_guttural():
                raise ValueError(f"I/voc verb debe tener R1 = WeakConsonant('Ø'), "
                               f"got R1 = {self.R1}")
        
        elif self.weak_type in [WeakVerbType.I_N, WeakVerbType.I_N_NASAUM]:
            if not isinstance(self.R1, WeakConsonant) or self.R1.symbol != 'n':
                raise ValueError(f"I/n verb debe tener R1 = WeakConsonant('n'), "
                               f"got R1 = {self.R1}")
        
        elif self.weak_type == WeakVerbType.STRONG:
            # Raíz fuerte no debería tener WeakConsonants
            if any(isinstance(r, WeakConsonant) for r in [self.R1, self.R2, self.R3]):
                raise ValueError(f"STRONG verb no debería tener WeakConsonants")
    
    def get_weak_positions(self) -> list[WeakPosition]:
        """
        Retorna lista de posiciones débiles en la raíz.
        
        Returns:
            Lista de WeakPosition indicando qué radicales son débiles
        
        Example:
            wasābum → [WeakPosition.R1]
            atawwum → [WeakPosition.R1] (R2/R3 son gem, no weak en sentido fonológico)
        """
        positions = []
        if isinstance(self.R1, WeakConsonant):
            positions.append(WeakPosition.R1)
        if isinstance(self.R2, WeakConsonant):
            positions.append(WeakPosition.R2)
        if isinstance(self.R3, WeakConsonant):
            positions.append(WeakPosition.R3)
        return positions
    
    def is_doubly_weak(self) -> bool:
        """
        Verifica si es doblemente débil (≥2 posiciones débiles).
        
        Returns:
            True si tiene 2 o más radicales débiles
        
        Example:
            atawwum → True (I/voc + II/gem)
            wasābum → False (solo R₁ débil)
        """
        return len(self.get_weak_positions()) >= 2
    
    def to_consonant_symbols(self) -> tuple[str, str, str]:
        """
        Extrae símbolos de consonantes para uso interno.
        
        Convierte WeakConsonant y Consonant a símbolos string.
        Útil para comparaciones y debugging.
        
        Returns:
            Tupla (R1_symbol, R2_symbol, R3_symbol)
        
        Example:
            wasābum → ('w', 's', 'b')
            ahāzum → ('Ø', 'h', 'z')
        """
        r1 = self.R1.symbol if isinstance(self.R1, WeakConsonant) else self.R1.symbol
        r2 = self.R2.symbol if isinstance(self.R2, WeakConsonant) else self.R2.symbol
        r3 = self.R3.symbol if isinstance(self.R3, WeakConsonant) else self.R3.symbol
        return (r1, r2, r3)
    
    def __str__(self) -> str:
        """Representación legible."""
        r1, r2, r3 = self.to_consonant_symbols()
        return f"√{r1}{r2}{r3} ({self.weak_type.value}, {self.vowel_class})"
    
    def __repr__(self) -> str:
        return (f"WeakRoot(R1={self.R1!r}, R2={self.R2!r}, R3={self.R3!r}, "
                f"vowel_class={self.vowel_class}, weak_type={self.weak_type})")


# ============================================================================
# HELPER FUNCTIONS - Crear raíces débiles fácilmente
# ============================================================================

def create_i_w_fientive_root(R2: str, R3: str, vowel_class: VowelClass, 
                              meaning: str) -> WeakRoot:
    """
    Crea raíz I/w fientivo.
    
    Verbos I/w fientivos son verbos de acción con w como R₁.
    Características:
    - Contracción w+i → u (presente)
    - Contracción w+i → ū (pretérito, vocal larga)
    - Perfect con geminación -tt-
    
    Referencias: § 18.2.1
    
    Args:
        R2: Segunda radical (símbolo string, ej: 's', 'b')
        R3: Tercera radical (símbolo string)
        vowel_class: Clase vocálica (VowelClass enum)
        meaning: Significado del verbo (string)
    
    Returns:
        WeakRoot configurado para I/w fientivo
    
    Examples:
        wasābum → create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
        wabālum → create_i_w_fientive_root('b', 'l', VowelClass.A_I, 'llevar')
        warādum → create_i_w_fientive_root('r', 'd', VowelClass.A_I, 'descender')
    """
    from phonology.inventory import get_consonant
    
    return WeakRoot(
        R1=WeakConsonant('w', WeakPosition.R1, 'contracts'),
        R2=get_consonant(R2),
        R3=get_consonant(R3),
        vowel_class=vowel_class,
        meaning=meaning,
        weak_type=WeakVerbType.I_W_FIENTIVE
    )


def create_i_w_adjectival_root(R2: str, R3: str, vowel_class: VowelClass,
                                 meaning: str) -> WeakRoot:
    """
    Crea raíz I/w adjetival.
    
    Verbos I/w adjetivales son verbos estativos con w como R₁.
    Características:
    - Contracción w+i → ī (vocal larga en TODOS los contextos)
    - NO geminación de R₂ en presente
    - Perfect con vocal larga (NO -tt-)
    
    Referencias: § 18.2.2
    
    Args:
        R2: Segunda radical
        R3: Tercera radical
        vowel_class: Clase vocálica (típicamente i/i para adjetivales)
        meaning: Significado
    
    Returns:
        WeakRoot configurado para I/w adjetival
    
    Examples:
        watārum → create_i_w_adjectival_root('t', 'r', VowelClass.I_I, 'exceder')
        waqārum → create_i_w_adjectival_root('q', 'r', VowelClass.I_I, 'ser caro')
    """
    from phonology.inventory import get_consonant
    
    return WeakRoot(
        R1=WeakConsonant('w', WeakPosition.R1, 'contracts'),
        R2=get_consonant(R2),
        R3=get_consonant(R3),
        vowel_class=vowel_class,
        meaning=meaning,
        weak_type=WeakVerbType.I_W_ADJECTIVAL
    )


def create_i_voc_a_root(R2: str, R3: str, vowel_class: VowelClass,
                         meaning: str) -> WeakRoot:
    """
    Crea raíz I/voc tipo a (< *ʔ, *h).
    
    Verbos I/voc a tienen vocal inicial 'a' por pérdida de gutural.
    Características:
    - Vocal larga compensatoria en prefijos (ā-, ē-)
    - Geminación de R₂ en presente (como verbos fuertes)
    - Infinitivo: ahāzum, akālum, etc.
    
    Referencias: § 18.3.1
    
    Args:
        R2: Segunda radical
        R3: Tercera radical
        vowel_class: Clase vocálica
        meaning: Significado
    
    Returns:
        WeakRoot configurado para I/voc a
    
    Examples:
        ahāzum → create_i_voc_a_root('h', 'z', VowelClass.A_U, 'tomar')
        amārum → create_i_voc_a_root('m', 'r', VowelClass.A_U, 'ver')
        akālum → create_i_voc_a_root('k', 'l', VowelClass.A_U, 'comer')
    """
    from phonology.inventory import get_consonant
    
    return WeakRoot(
        R1=WeakConsonant('Ø', WeakPosition.R1, 'compensatory_lengthening'),
        R2=get_consonant(R2),
        R3=get_consonant(R3),
        vowel_class=vowel_class,
        meaning=meaning,
        weak_type=WeakVerbType.I_VOC_A
    )


def create_i_voc_e_root(R2: str, R3: str, vowel_class: VowelClass,
                         meaning: str) -> WeakRoot:
    """
    Crea raíz I/voc tipo e (< *ʕ, *ḥ).
    
    Verbos I/voc e tienen vocal inicial 'e' por pérdida de gutural.
    Fonológicamente idénticos a I/voc a, solo difiere la vocal inicial.
    
    Referencias: § 18.3.1
    
    Args:
        R2: Segunda radical
        R3: Tercera radical
        vowel_class: Clase vocálica
        meaning: Significado
    
    Returns:
        WeakRoot configurado para I/voc e
    
    Examples:
        epāšum → create_i_voc_e_root('p', 'š', VowelClass.A_U, 'hacer')
        elā'um → create_i_voc_e_root('l', 'ʔ', VowelClass.I_I, 'subir')
        erābum → create_i_voc_e_root('r', 'b', VowelClass.A_U, 'entrar')
    """
    from phonology.inventory import get_consonant
    
    return WeakRoot(
        R1=WeakConsonant('Ø', WeakPosition.R1, 'compensatory_lengthening'),
        R2=get_consonant(R2),
        R3=get_consonant(R3),
        vowel_class=vowel_class,
        meaning=meaning,
        weak_type=WeakVerbType.I_VOC_E
    )


def create_i_n_root(R2: str, R3: str, vowel_class: VowelClass,
                     meaning: str, special_nasaum: bool = False) -> WeakRoot:
    """
    Crea raíz I/n.
    
    Verbos I/n tienen n como R₁ con comportamiento especial:
    - Asimilación n+C → CC en pretérito/perfect
    - Pérdida #n → Ø antes de i/u (imperativo, Gt/Gtn)
    
    Referencias: § 18.4
    
    Args:
        R2: Segunda radical
        R3: Tercera radical
        vowel_class: Clase vocálica
        meaning: Significado
        special_nasaum: True para našā'um (asimilación variable en N-stem)
    
    Returns:
        WeakRoot configurado para I/n
    
    Examples:
        naṣārum → create_i_n_root('ṣ', 'r', VowelClass.A_U, 'guardar')
        nadā'um → create_i_n_root('d', 'ʔ', VowelClass.I_I, 'depositar')
        našā'um → create_i_n_root('š', 'ʔ', VowelClass.I_I, 'transportar', 
                                   special_nasaum=True)
    """
    from phonology.inventory import get_consonant
    
    weak_type = WeakVerbType.I_N_NASAUM if special_nasaum else WeakVerbType.I_N
    
    return WeakRoot(
        R1=WeakConsonant('n', WeakPosition.R1, 'assimilates'),
        R2=get_consonant(R2),
        R3=get_consonant(R3),
        vowel_class=vowel_class,
        meaning=meaning,
        weak_type=weak_type
    )


def create_atawwum_root() -> WeakRoot:
    """
    Crea raíz de atawwum 'hablar'.
    
    Verbo especial doblemente débil:
    - I/voc (a- inicial < *ʔ)
    - II/gem (R₂ = R₃ = w)
    
    Solo atestiguado en Gt y N stems.
    Paradigma único muy complejo.
    
    Referencias: § 18.3.2.2
    
    Returns:
        WeakRoot configurado para atawwum
    
    Example:
        atawwum → create_atawwum_root()
    """
    from phonology.inventory import get_consonant
    
    return WeakRoot(
        R1=WeakConsonant('Ø', WeakPosition.R1, 'compensatory_lengthening'),
        R2=get_consonant('w'),
        R3=get_consonant('w'),  # II/gem: R₂ = R₃
        vowel_class=VowelClass.U_U,
        meaning='hablar',
        weak_type=WeakVerbType.I_ATAWWUM
    )


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def is_weak_root(root) -> bool:
    """
    Verifica si una raíz es débil.
    
    Args:
        root: Objeto Root o WeakRoot
    
    Returns:
        True si es WeakRoot o tiene al menos una consonante débil
    """
    if isinstance(root, WeakRoot):
        return True
    
    # Verificar si tiene WeakConsonants
    if hasattr(root, 'R1') and hasattr(root, 'R2') and hasattr(root, 'R3'):
        return any(isinstance(r, WeakConsonant) for r in [root.R1, root.R2, root.R3])
    
    return False


def get_weak_type_from_root(root) -> Optional[WeakVerbType]:
    """
    Extrae el tipo de verbo débil de una raíz.
    
    Args:
        root: WeakRoot o Root
    
    Returns:
        WeakVerbType si es débil, WeakVerbType.STRONG si es fuerte, None si inválido
    """
    if isinstance(root, WeakRoot):
        return root.weak_type
    
    if is_weak_root(root):
        # Intentar inferir tipo basado en R1
        if isinstance(root.R1, WeakConsonant):
            if root.R1.symbol == 'w':
                return WeakVerbType.I_W_FIENTIVE  # Default, podría ser adjetival
            elif root.R1.is_lost_guttural():
                return WeakVerbType.I_VOC_A  # Default, podría ser I_VOC_E
            elif root.R1.symbol == 'n':
                return WeakVerbType.I_N
    
    return WeakVerbType.STRONG

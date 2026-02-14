"""
Clases para representar sílabas y estructura silábica.

Basado en Kouwenberg (2017) § 3.5.1.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from .. import Phoneme, Consonant, Vowel
from .enums import (
    SyllableWeight,
    SyllablePosition,
    SyllableType,
    get_syllable_type_from_structure,
)


@dataclass
class Syllable:
    """
    Sílaba del Old Assyrian.
    
    Estructura: (onset) nucleus (coda)
    - Onset: opcional (pero asumido ʾ si no visible)
    - Nucleus: obligatorio (siempre una vocal)
    - Coda: opcional
    """
    # Componentes
    nucleus: Vowel                               # Núcleo (obligatorio)
    onset: Optional[List[Consonant]] = None      # Inicio (opcional)
    coda: Optional[List[Consonant]] = None       # Coda (opcional)
    
    # Propiedades derivadas (calculadas)
    weight: Optional[SyllableWeight] = None
    syllable_type: Optional[SyllableType] = None
    
    # Posición en palabra
    position: SyllablePosition = SyllablePosition.MEDIAL
    is_stressed: bool = False
    
    # Metadata
    original_spelling: Optional[str] = None
    
    def __post_init__(self):
        """Calcula propiedades derivadas si no proporcionadas."""
        if self.weight is None:
            self.weight = self.calculate_weight()
        if self.syllable_type is None:
            self.syllable_type = self.infer_type()
    
    def has_onset(self) -> bool:
        """True si tiene onset consonántico."""
        return self.onset is not None and len(self.onset) > 0
    
    def has_coda(self) -> bool:
        """True si tiene coda consonántica."""
        return self.coda is not None and len(self.coda) > 0
    
    def is_open(self) -> bool:
        """True si sílaba es abierta (sin coda)."""
        return not self.has_coda()
    
    def is_closed(self) -> bool:
        """True si sílaba es cerrada (con coda)."""
        return self.has_coda()
    
    def calculate_weight(self) -> SyllableWeight:
        """
        Calcula peso silábico en morae.
        
        CV = μ (ligera)
        CV̄, CVC = μμ (pesada)
        CV̄C = μμμ (super-pesada)
        
        Returns:
            SyllableWeight
        """
        morae = 1  # Núcleo siempre cuenta como 1 mora
        
        # Vocal larga = +1 mora
        if self.nucleus.length.value == 'long':
            morae += 1
        
        # Coda = +1 mora
        if self.has_coda():
            morae += 1
        
        if morae == 1:
            return SyllableWeight.LIGHT
        elif morae == 2:
            return SyllableWeight.HEAVY
        else:  # 3
            return SyllableWeight.SUPERHEAVY
    
    def infer_type(self) -> SyllableType:
        """
        Infiere tipo de sílaba desde componentes.
        
        Returns:
            SyllableType
        """
        return get_syllable_type_from_structure(
            has_onset=self.has_onset(),
            vowel_length=self.nucleus.length.value,
            has_coda=self.has_coda()
        )
    
    def get_phonemes(self) -> List[Phoneme]:
        """
        Retorna lista ordenada de fonemas.
        
        Returns:
            [onset..., nucleus, coda...]
        """
        phonemes = []
        
        if self.onset:
            phonemes.extend(self.onset)
        
        phonemes.append(self.nucleus)
        
        if self.coda:
            phonemes.extend(self.coda)
        
        return phonemes
    
    def to_string(self, show_length: bool = True) -> str:
        """
        Representación de sílaba.
        
        Args:
            show_length: Si True, muestra longitud vocálica con macron
        
        Returns:
            String tipo "CVC", "CV̄", etc.
        """
        onset_str = 'C' if self.has_onset() else '(ʾ)'
        
        if show_length:
            nucleus_str = 'V̄' if self.nucleus.length.value == 'long' else 'V'
        else:
            nucleus_str = 'V'
        
        coda_str = 'C' if self.has_coda() else ''
        
        return f"{onset_str}{nucleus_str}{coda_str}"
    
    def to_phonemic(self) -> str:
        """
        Representación fonémica tipo /dam/, /qum/.
        
        Returns:
            String fonémico
        """
        result = []
        
        if self.onset:
            result.extend([c.symbol for c in self.onset])
        
        # Vocal con longitud
        v_symbol = self.nucleus.symbol
        result.append(v_symbol)
        
        if self.coda:
            result.extend([c.symbol for c in self.coda])
        
        return ''.join(result)
    
    def __repr__(self) -> str:
        """Representación para debugging."""
        return f"Syl({self.to_string()}: /{self.to_phonemic()}/)"


@dataclass
class SyllableStructure:
    """
    Estructura silábica completa de una palabra.
    
    Representa división silábica y propiedades prosódicas.
    """
    syllables: List[Syllable] = field(default_factory=list)
    
    # Metadata
    word_form: Optional[str] = None
    
    def count_syllables(self) -> int:
        """Número total de sílabas."""
        return len(self.syllables)
    
    def get_stressed_syllable(self) -> Optional[Syllable]:
        """
        Retorna sílaba con estrés.
        
        Returns:
            Syllable marcada como stressed, o None
        """
        for syl in self.syllables:
            if syl.is_stressed:
                return syl
        return None
    
    def get_syllable_by_position(
        self,
        position: SyllablePosition
    ) -> Optional[Syllable]:
        """
        Retorna sílaba en posición específica.
        
        Args:
            position: Posición deseada
        
        Returns:
            Syllable en esa posición, o None
        """
        if position == SyllablePosition.INITIAL:
            return self.syllables[0] if self.syllables else None
        elif position == SyllablePosition.FINAL:
            return self.syllables[-1] if self.syllables else None
        elif position == SyllablePosition.PENULTIMATE:
            return self.syllables[-2] if len(self.syllables) >= 2 else None
        elif position == SyllablePosition.ANTEPENULTIMATE:
            return self.syllables[-3] if len(self.syllables) >= 3 else None
        return None
    
    def get_weight_pattern(self) -> List[SyllableWeight]:
        """
        Retorna patrón de pesos silábicos.
        
        Returns:
            [LIGHT, HEAVY, HEAVY, ...]
        """
        return [syl.weight for syl in self.syllables]
    
    def get_type_pattern(self) -> List[SyllableType]:
        """
        Retorna patrón de tipos silábicos.
        
        Returns:
            [CV, CVC, CV̄, ...]
        """
        return [syl.syllable_type for syl in self.syllables]
    
    def to_string(self, separator: str = '.') -> str:
        """
        Representación tipo: CV.CVC.CV̄
        
        Args:
            separator: Carácter entre sílabas (default: .)
        
        Returns:
            String con sílabas separadas
        """
        return separator.join(syl.to_string() for syl in self.syllables)
    
    def to_phonemic(self, separator: str = '.') -> str:
        """
        Representación fonémica tipo: /dam.qum/
        
        Args:
            separator: Carácter entre sílabas
        
        Returns:
            String fonémico
        """
        parts = [syl.to_phonemic() for syl in self.syllables]
        return f"/{separator.join(parts)}/"
    
    def has_superheavy_non_final(self) -> bool:
        """
        True si hay sílaba super-pesada en posición NO final.
        
        Esto es restringido en OA (solo permitido bajo condiciones).
        
        Returns:
            True si violación potencial
        """
        for i, syl in enumerate(self.syllables[:-1]):  # Excluir última
            if syl.weight == SyllableWeight.SUPERHEAVY:
                return True
        return False
    
    def count_light_syllables(self, exclude_final: bool = True) -> int:
        """
        Cuenta sílabas ligeras.
        
        Args:
            exclude_final: Si True, excluye sílaba final del conteo
        
        Returns:
            Número de sílabas ligeras
        """
        count = 0
        end_idx = len(self.syllables) - 1 if exclude_final else len(self.syllables)
        
        for i in range(end_idx):
            if self.syllables[i].weight == SyllableWeight.LIGHT:
                count += 1
        
        return count
    
    def __repr__(self) -> str:
        """Representación para debugging."""
        return f"SyllableStructure({self.to_string()})"

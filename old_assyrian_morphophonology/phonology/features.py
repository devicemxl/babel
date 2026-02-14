"""
Rasgos fonológicos para consonantes y vocales del Old Assyrian.

Este módulo define los rasgos distintivos que caracterizan cada fonema.
"""

from dataclasses import dataclass
from typing import Set
from .enums import (
    PlaceOfArticulation, MannerOfArticulation, Voicing,
    VowelQuality, VowelLength, VowelHeight, VowelBackness,
    ConsonantClass
)


@dataclass(frozen=True)
class ConsonantFeatures:
    """
    Rasgos fonológicos de una consonante.
    
    Basado en la Tabla 3.1 de Kouwenberg (2017).
    """
    place: PlaceOfArticulation
    manner: MannerOfArticulation
    voicing: Voicing
    
    # Rasgos binarios adicionales
    is_weak: bool = False       # ʾ, w, y
    is_sibilant: bool = False   # s, z, š, ṣ
    is_emphatic: bool = False   # ṭ, ṣ, q (glotálicas)
    is_guttural: bool = False   # ḫ, ʾ
    is_sonorant: bool = False   # m, n, l, r, w, y
    is_nasal: bool = False      # m, n
    is_liquid: bool = False     # l, r
    
    def get_natural_classes(self) -> Set[ConsonantClass]:
        """Devuelve el conjunto de clases naturales a las que pertenece."""
        classes = set()
        
        if self.is_weak:
            classes.add(ConsonantClass.WEAK)
        if self.is_sibilant:
            classes.add(ConsonantClass.SIBILANT)
        if self.is_emphatic:
            classes.add(ConsonantClass.EMPHATIC)
        if self.is_guttural:
            classes.add(ConsonantClass.GUTTURAL)
        if self.is_sonorant:
            classes.add(ConsonantClass.SONORANT)
        if self.is_nasal:
            classes.add(ConsonantClass.NASAL)
        if self.is_liquid:
            classes.add(ConsonantClass.LIQUID)
            
        return classes
    
    def can_assimilate_to(self, other: 'ConsonantFeatures') -> bool:
        """
        Determina si esta consonante puede asimilarse a otra.
        
        Reglas generales (a refinar en iteraciones posteriores):
        - Nasales asimilan a consonantes siguientes
        - Sibilantes asimilan ante dentales/sibilantes
        """
        # Nasales pueden asimilar
        if self.is_nasal:
            return True
        
        # Sibilantes pueden asimilar ante ciertas consonantes
        if self.is_sibilant:
            return True
            
        return False


@dataclass(frozen=True)
class VowelFeatures:
    """
    Rasgos fonológicos de una vocal.
    
    Basado en § 3.4.1 de Kouwenberg (2017).
    """
    quality: VowelQuality
    length: VowelLength
    
    # Rasgos derivados de quality
    @property
    def height(self) -> VowelHeight:
        """Altura vocálica."""
        mapping = {
            VowelQuality.I: VowelHeight.HIGH,
            VowelQuality.U: VowelHeight.HIGH,
            VowelQuality.E: VowelHeight.MID,
            VowelQuality.A: VowelHeight.LOW,
        }
        return mapping[self.quality]
    
    @property
    def backness(self) -> VowelBackness:
        """Posición anterior-posterior."""
        mapping = {
            VowelQuality.I: VowelBackness.FRONT,
            VowelQuality.E: VowelBackness.FRONT,
            VowelQuality.A: VowelBackness.CENTRAL,
            VowelQuality.U: VowelBackness.BACK,
        }
        return mapping[self.quality]
    
    @property
    def is_high(self) -> bool:
        """True si es vocal alta (i, u)."""
        return self.height == VowelHeight.HIGH
    
    @property
    def is_mid(self) -> bool:
        """True si es vocal media (e)."""
        return self.height == VowelHeight.MID
    
    @property
    def is_low(self) -> bool:
        """True si es vocal baja (a)."""
        return self.height == VowelHeight.LOW
    
    @property
    def is_front(self) -> bool:
        """True si es vocal frontal (i, e)."""
        return self.backness == VowelBackness.FRONT
    
    @property
    def is_back(self) -> bool:
        """True si es vocal posterior (u)."""
        return self.backness == VowelBackness.BACK
    
    @property
    def is_long(self) -> bool:
        """True si es vocal larga."""
        return self.length == VowelLength.LONG
    
    @property
    def is_short(self) -> bool:
        """True si es vocal corta."""
        return self.length == VowelLength.SHORT
    
    def can_contract_with(self, other: 'VowelFeatures') -> bool:
        """
        Determina si esta vocal puede contraerse con otra.
        
        Reglas básicas (a refinar en § 3.4.11):
        - Vocales idénticas pueden contraer
        - Algunas secuencias heterogéneas también
        """
        # Vocales idénticas siempre pueden contraer
        if self.quality == other.quality:
            return True
        
        # Otros casos requieren reglas específicas (Iteración 4)
        return False

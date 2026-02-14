"""
Clases base para representación fonológica del Old Assyrian.

Este módulo define las clases fundamentales Phoneme, Consonant y Vowel.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from .enums import VowelQuality, VowelLength, AccentType, HistoricalOrigin
from .features import ConsonantFeatures, VowelFeatures


class Phoneme(ABC):
    """
    Clase base abstracta para todos los fonemas del Old Assyrian.
    
    Un fonema es la unidad mínima distintiva del sistema fonológico.
    """
    
    @property
    @abstractmethod
    def symbol(self) -> str:
        """Representación interna del fonema (ej: 'ṣ', 'ā')."""
        pass
    
    @property
    @abstractmethod
    def oracc_representation(self) -> str:
        """Representación en formato ORACC."""
        pass
    
    @abstractmethod
    def to_oracc(self) -> str:
        """Convierte a formato ORACC."""
        pass
    
    def __str__(self) -> str:
        return self.symbol
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.symbol})"


@dataclass(frozen=True)
class Consonant(Phoneme):
    """
    Representación de una consonante del Old Assyrian.
    
    Basado en la Tabla 3.1 (§ 3.2.1) de Kouwenberg (2017).
    Las 20 consonantes: ʾ, b, d, g, ḫ, k, l, m, n, p, q, r, s, ṣ, š, t, ṭ, w, y, z
    """
    
    _symbol: str
    features: ConsonantFeatures
    unicode_codepoint: Optional[str] = None  # ej: 'U+1E63' para ṣ
    ipa: Optional[str] = None                # Notación IPA (opcional)
    historical_note: Optional[str] = None    # Notas sobre origen/desarrollo
    
    @property
    def symbol(self) -> str:
        return self._symbol
    
    @property
    def oracc_representation(self) -> str:
        """En consonantes, generalmente igual al símbolo."""
        return self._symbol
    
    def to_oracc(self) -> str:
        return self.oracc_representation
    
    # Propiedades de conveniencia (delegates a features)
    
    @property
    def is_weak(self) -> bool:
        """True si es consonante débil (ʾ, w, y)."""
        return self.features.is_weak
    
    @property
    def is_sibilant(self) -> bool:
        """True si es sibilante (s, z, š, ṣ)."""
        return self.features.is_sibilant
    
    @property
    def is_emphatic(self) -> bool:
        """True si es enfática/glotálica (ṭ, ṣ, q)."""
        return self.features.is_emphatic
    
    @property
    def is_guttural(self) -> bool:
        """True si es gutural (ḫ, ʾ)."""
        return self.features.is_guttural
    
    @property
    def is_sonorant(self) -> bool:
        """True si es sonorante (m, n, l, r, w, y)."""
        return self.features.is_sonorant
    
    @property
    def is_nasal(self) -> bool:
        """True si es nasal (m, n)."""
        return self.features.is_nasal
    
    @property
    def is_liquid(self) -> bool:
        """True si es líquida (l, r)."""
        return self.features.is_liquid
    
    def can_assimilate_to(self, other: 'Consonant') -> bool:
        """Determina si puede asimilarse a otra consonante."""
        return self.features.can_assimilate_to(other.features)
    
    def can_form_cluster_with(self, other: 'Consonant') -> bool:
        """
        Determina si puede formar cluster con otra consonante.
        
        OA solo permite clusters de 2 consonantes en posición medial.
        Algunos clusters requieren epéntesis (a refinar en iteraciones posteriores).
        """
        # Reglas básicas (a expandir)
        # Clusters con consonantes débiles son problemáticos
        if self.is_weak or other.is_weak:
            return False  # Simplificación; requiere análisis más detallado
        
        return True
    
    def geminate(self) -> 'Consonant':
        """
        Retorna la misma consonante (para representación de geminación).
        
        La geminación se representa típicamente como secuencia CC.
        """
        return self
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Consonant):
            return False
        return self.symbol == other.symbol
    
    def __hash__(self) -> int:
        return hash(self.symbol)


@dataclass(frozen=True)
class Vowel(Phoneme):
    """
    Representación de una vocal del Old Assyrian.
    
    Basado en § 3.4.1 de Kouwenberg (2017).
    4 cualidades vocálicas (a, e, i, u) × 2 cantidades (corta, larga).
    """
    
    features: VowelFeatures
    accent: AccentType = AccentType.NONE
    is_stressed: bool = False  # Derivado de accent en ORACC
    origin: Optional[HistoricalOrigin] = None
    
    @property
    def symbol(self) -> str:
        """Símbolo con macron si es larga."""
        base = self.features.quality.value
        if self.features.is_long:
            # Mapeo a vocales con macron
            macron_map = {'a': 'ā', 'e': 'ē', 'i': 'ī', 'u': 'ū'}
            return macron_map[base]
        return base
    
    @property
    def oracc_representation(self) -> str:
        """
        Representación ORACC con posibles diacríticos.
        
        ORACC puede añadir acento agudo para marcar estrés.
        """
        base = self.symbol
        
        if self.accent == AccentType.ACUTE:
            # Mapeo con agudo
            acute_map = {
                'a': 'á', 'ā': 'á',  # ORACC puede usar agudo en largas
                'e': 'é', 'ē': 'é',
                'i': 'í', 'ī': 'í',
                'u': 'ú', 'ū': 'ú',
            }
            return acute_map.get(base, base)
        elif self.accent == AccentType.CIRCUMFLEX:
            # Circumflex indica contracción
            circ_map = {
                'a': 'â', 'ā': 'â',
                'e': 'ê', 'ē': 'ê',
                'i': 'î', 'ī': 'î',
                'u': 'û', 'ū': 'û',
            }
            return circ_map.get(base, base)
        
        return base
    
    def to_oracc(self) -> str:
        return self.oracc_representation
    
    # Propiedades de conveniencia
    
    @property
    def quality(self) -> VowelQuality:
        """Cualidad vocálica (a, e, i, u)."""
        return self.features.quality
    
    @property
    def length(self) -> VowelLength:
        """Cantidad vocálica (corta, larga)."""
        return self.features.length
    
    @property
    def is_long(self) -> bool:
        """True si es vocal larga."""
        return self.features.is_long
    
    @property
    def is_short(self) -> bool:
        """True si es vocal corta."""
        return self.features.is_short
    
    @property
    def is_high(self) -> bool:
        """True si es vocal alta (i, u)."""
        return self.features.is_high
    
    @property
    def is_mid(self) -> bool:
        """True si es vocal media (e)."""
        return self.features.is_mid
    
    @property
    def is_low(self) -> bool:
        """True si es vocal baja (a)."""
        return self.features.is_low
    
    @property
    def is_front(self) -> bool:
        """True si es vocal frontal (i, e)."""
        return self.features.is_front
    
    @property
    def is_back(self) -> bool:
        """True si es vocal posterior (u)."""
        return self.features.is_back
    
    @property
    def is_e(self) -> bool:
        """
        True si es 'e' (vocal secundaria especial).
        
        'e' es marginal en OA y tiene origen histórico específico.
        """
        return self.quality == VowelQuality.E
    
    def lengthen(self) -> 'Vowel':
        """Retorna versión larga de esta vocal."""
        if self.is_long:
            return self
        long_features = VowelFeatures(
            quality=self.quality,
            length=VowelLength.LONG
        )
        return Vowel(
            features=long_features,
            accent=self.accent,
            is_stressed=self.is_stressed,
            origin=self.origin
        )
    
    def shorten(self) -> 'Vowel':
        """Retorna versión corta de esta vocal."""
        if self.is_short:
            return self
        short_features = VowelFeatures(
            quality=self.quality,
            length=VowelLength.SHORT
        )
        return Vowel(
            features=short_features,
            accent=self.accent,
            is_stressed=self.is_stressed,
            origin=self.origin
        )
    
    def can_contract_with(self, other: 'Vowel') -> bool:
        """Determina si puede contraerse con otra vocal."""
        return self.features.can_contract_with(other.features)
    
    def contract_with(self, other: 'Vowel') -> 'Vowel':
        """
        Retorna vocal resultante de contracción.
        
        Reglas básicas (a refinar en Iteración 4 § 3.4.11):
        - a + a → ā
        - i + i / e + e → ī/ē
        - u + u → ū
        - Secuencias heterogéneas: reglas específicas
        """
        # Por ahora, solo implementar casos idénticos
        if self.quality == other.quality:
            # Contracción produce vocal larga con circumflex
            result_features = VowelFeatures(
                quality=self.quality,
                length=VowelLength.LONG
            )
            return Vowel(
                features=result_features,
                accent=AccentType.CIRCUMFLEX,  # Marca contracción
                origin=HistoricalOrigin.FROM_CONTRACTION
            )
        
        # Casos heterogéneos requieren reglas específicas (pendiente)
        raise NotImplementedError(
            f"Contracción {self.quality.value} + {other.quality.value} "
            "no implementada aún (ver Iteración 4)"
        )
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Vowel):
            return False
        # Comparación básica por símbolo (ignora accent/stress para igualdad fonológica)
        return (self.quality == other.quality and 
                self.length == other.length)
    
    def __hash__(self) -> int:
        return hash((self.quality, self.length))


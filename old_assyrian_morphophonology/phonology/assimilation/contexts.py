"""
Contextos morfológicos para asimilación consonántica.

Define estructuras para capturar información morfológica necesaria
para aplicar reglas de asimilación correctamente.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from ...phonology import Phoneme, Consonant, Vowel
from .enums import (
    MorphologicalBoundary,
    MorphemeType,
    AssimilationStatus,
)


@dataclass
class MorphologicalContext:
    """
    Contexto morfológico para aplicación de reglas de asimilación.
    
    Captura información sobre fronteras morfológicas, tipos de morfemas,
    y restricciones de transparencia.
    """
    # Frontera morfológica
    boundary_type: Optional[MorphologicalBoundary] = None
    is_at_boundary: bool = False
    
    # Morfemas involucrados
    left_morpheme_type: Optional[MorphemeType] = None
    right_morpheme_type: Optional[MorphemeType] = None
    
    # Para bloqueo de asimilación
    left_consonant_is_radical: bool = False
    right_consonant_is_radical: bool = False
    
    # Información verbal específica
    is_verbal_stem: bool = False
    verbal_stem: Optional[str] = None  # 'G', 'D', 'Š', 'N', 'Gt', etc.
    has_t_infix: bool = False
    
    # Información nominal específica
    is_compound: bool = False
    is_proper_name: bool = False
    
    # Estatus de aplicación
    assimilation_status: AssimilationStatus = AssimilationStatus.OBLIGATORY
    
    def should_block_assimilation(self) -> bool:
        """
        Determina si asimilación debe bloquearse en este contexto.
        
        Returns:
            True si asimilación debe bloquearse por transparencia
        """
        # Bloquear si consonante es radical y contexto verbal específico
        if self.left_consonant_is_radical:
            # N-stem de verbos I/n
            if self.verbal_stem == 'N':
                return True
            # Š-stem de verbos I/n
            if self.verbal_stem == 'Š':
                return True
            # G-stem con n como R2
            if self.verbal_stem == 'G' and self.is_verbal_stem:
                return True
        
        return False
    
    def get_expected_status(self) -> AssimilationStatus:
        """
        Retorna estatus de asimilación esperado para este contexto.
        
        Returns:
            AssimilationStatus apropiado
        """
        if self.should_block_assimilation():
            return AssimilationStatus.BLOCKED
        
        # m/n gramatical siempre asimila
        if self.left_morpheme_type in {
            MorphemeType.CASE_ENDING,
            MorphemeType.VERBAL_PREFIX,
            MorphemeType.PRONOMINAL_SUFFIX,
        }:
            return AssimilationStatus.OBLIGATORY
        
        # b + -ma es opcional
        if (self.left_morpheme_type == MorphemeType.ROOT and
            self.right_morpheme_type == MorphemeType.ENCLITIC):
            return AssimilationStatus.OPTIONAL
        
        return self.assimilation_status


@dataclass
class AssimilationEnvironment:
    """
    Ambiente completo para asimilación: fonológico + morfológico.
    
    Combina PhonologicalContext (de Iteración 2) con MorphologicalContext.
    """
    # Contexto fonológico
    consonant1: Consonant
    consonant2: Consonant
    intervening: Optional[List[Phoneme]] = None  # Para asimilación a distancia
    
    # Contexto morfológico
    morphological_context: MorphologicalContext = field(
        default_factory=MorphologicalContext
    )
    
    # Metadata
    original_spelling: Optional[str] = None
    position_in_word: Optional[int] = None
    
    def forms_cluster(self) -> bool:
        """True si consonantes forman cluster directo."""
        return self.intervening is None or len(self.intervening) == 0
    
    def is_distant_assimilation(self) -> bool:
        """True si asimilación es a distancia."""
        return not self.forms_cluster()
    
    def __repr__(self) -> str:
        """Representación legible."""
        if self.forms_cluster():
            return f"Cluster({self.consonant1.symbol}-{self.consonant2.symbol})"
        else:
            return f"Distant({self.consonant1.symbol}...{self.consonant2.symbol})"


def create_prefix_root_context(
    prefix_consonant: Consonant,
    root_consonant: Consonant,
    prefix_type: MorphemeType = MorphemeType.VERBAL_PREFIX,
    verbal_stem: Optional[str] = None,
) -> AssimilationEnvironment:
    """
    Crea contexto para frontera prefijo-raíz.
    
    Args:
        prefix_consonant: Consonante final del prefijo
        root_consonant: Consonante inicial de raíz
        prefix_type: Tipo de prefijo
        verbal_stem: Stem verbal (G, N, Š, etc.)
    
    Returns:
        AssimilationEnvironment configurado
    """
    morph_ctx = MorphologicalContext(
        boundary_type=MorphologicalBoundary.PREFIX_ROOT,
        is_at_boundary=True,
        left_morpheme_type=prefix_type,
        right_morpheme_type=MorphemeType.ROOT,
        left_consonant_is_radical=False,
        right_consonant_is_radical=True,
        is_verbal_stem=True,
        verbal_stem=verbal_stem,
    )
    
    return AssimilationEnvironment(
        consonant1=prefix_consonant,
        consonant2=root_consonant,
        morphological_context=morph_ctx,
    )


def create_root_suffix_context(
    root_consonant: Consonant,
    suffix_consonant: Consonant,
    suffix_type: MorphemeType,
    root_consonant_is_radical: bool = True,
) -> AssimilationEnvironment:
    """
    Crea contexto para frontera raíz-sufijo.
    
    Args:
        root_consonant: Consonante final de raíz
        suffix_consonant: Consonante inicial de sufijo
        suffix_type: Tipo de sufijo
        root_consonant_is_radical: Si consonante es parte de raíz léxica
    
    Returns:
        AssimilationEnvironment configurado
    """
    morph_ctx = MorphologicalContext(
        boundary_type=MorphologicalBoundary.ROOT_SUFFIX,
        is_at_boundary=True,
        left_morpheme_type=MorphemeType.ROOT,
        right_morpheme_type=suffix_type,
        left_consonant_is_radical=root_consonant_is_radical,
        right_consonant_is_radical=False,
    )
    
    # m/n gramatical vs. m/n de raíz
    if not root_consonant_is_radical:
        morph_ctx.assimilation_status = AssimilationStatus.OBLIGATORY
    
    return AssimilationEnvironment(
        consonant1=root_consonant,
        consonant2=suffix_consonant,
        morphological_context=morph_ctx,
    )


def create_t_infix_context(
    root_consonant: Consonant,
    verbal_stem: str = 'Gt',
) -> AssimilationEnvironment:
    """
    Crea contexto para infijo -t- verbal.
    
    Args:
        root_consonant: Primer radical de raíz
        verbal_stem: Stem con infijo -t- (Gt, Gtn, Dt, Dtn)
    
    Returns:
        AssimilationEnvironment configurado
    """
    from ...phonology import get_consonant
    t = get_consonant('t')
    
    morph_ctx = MorphologicalContext(
        boundary_type=MorphologicalBoundary.INFIX,
        is_at_boundary=True,
        left_morpheme_type=MorphemeType.ROOT,
        right_morpheme_type=MorphemeType.VERBAL_INFIX,
        left_consonant_is_radical=True,
        right_consonant_is_radical=False,
        is_verbal_stem=True,
        verbal_stem=verbal_stem,
        has_t_infix=True,
    )
    
    return AssimilationEnvironment(
        consonant1=root_consonant,
        consonant2=t,
        morphological_context=morph_ctx,
    )


def create_compound_context(
    compound1_final: Consonant,
    compound2_initial: Consonant,
) -> AssimilationEnvironment:
    """
    Crea contexto para sustantivo compuesto.
    
    Args:
        compound1_final: Consonante final del primer elemento
        compound2_initial: Consonante inicial del segundo elemento
    
    Returns:
        AssimilationEnvironment configurado
    """
    morph_ctx = MorphologicalContext(
        boundary_type=MorphologicalBoundary.COMPOUND,
        is_at_boundary=True,
        is_compound=True,
        assimilation_status=AssimilationStatus.OBLIGATORY,
    )
    
    return AssimilationEnvironment(
        consonant1=compound1_final,
        consonant2=compound2_initial,
        morphological_context=morph_ctx,
    )

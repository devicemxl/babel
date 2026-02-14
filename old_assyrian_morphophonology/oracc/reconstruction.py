"""
Sistema de reconstrucción de consonantes débiles desde spellings ORACC.

Implementa el algoritmo completo para decidir qué débiles reconstruir
en broken spellings ambiguos.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phonology import Phoneme, Consonant, Vowel, get_consonant
from phonology.weak_enums import (
    ReconstructMode,
    ContractionMode,
    WeakPosition,
    WeakVerbClass,
)
from phonology.phonological_context import (
    PhonologicalContext,
    MorphologicalInfo,
    create_broken_spelling_context,
)
from .decision_tables import (
    lookup_decision,
    lookup_special_case,
    get_default_decision,
    ReconstructionDecision,
)


@dataclass
class ReconstructedWeak:
    """
    Información sobre una consonante débil reconstruida.
    
    Metadata completa para cada débil insertada.
    """
    position: int  # Posición en secuencia de fonemas (después de inserción)
    weak_consonant: Consonant  # Cuál débil (ʾ, w, y)
    confidence: float  # 0.0-1.0
    evidence_type: str  # Tipo de evidencia
    reason: str  # Explicación
    original_spelling: str  # Spelling ORACC que motivó reconstrucción
    alternative: Optional[Consonant] = None  # Interpretación alternativa
    
    def __repr__(self) -> str:
        return f"Reconstructed({self.weak_consonant.symbol} @{self.position}, conf={self.confidence:.2f})"


class WeakConsonantReconstructor:
    """
    Reconstruye consonantes débiles no escritas en ORACC.
    
    Usa tabla de decisión, información morfológica y contexto fonológico
    para decidir qué débiles insertar.
    """
    
    def __init__(
        self,
        mode: ReconstructMode = ReconstructMode.AUTO,
        contraction_mode: ContractionMode = ContractionMode.CONTEXT_DEPENDENT,
        min_confidence: float = 0.6,
    ):
        """
        Inicializa reconstructor.
        
        Args:
            mode: Modo de reconstrucción
            contraction_mode: Cómo manejar contracciones
            min_confidence: Confianza mínima para reconstruir (0.0-1.0)
        """
        self.mode = mode
        self.contraction_mode = contraction_mode
        self.min_confidence = min_confidence
        self.reconstructions: List[ReconstructedWeak] = []
    
    def reconstruct_from_phonemes(
        self,
        phonemes: List[Phoneme],
        morphology: Optional[MorphologicalInfo] = None,
        original_spelling: Optional[str] = None,
    ) -> Tuple[List[Phoneme], List[ReconstructedWeak]]:
        """
        Reconstruye débiles en una secuencia de fonemas.
        
        Busca broken spellings (V-V) y decide si insertar débil.
        
        Args:
            phonemes: Secuencia de fonemas parseada de ORACC
            morphology: Información morfológica opcional
            original_spelling: Spelling ORACC original
        
        Returns:
            (phonemes_con_debiles, lista_de_reconstrucciones)
        """
        if self.mode == ReconstructMode.NONE:
            return (phonemes, [])
        
        # Resetear reconstrucciones
        self.reconstructions = []
        
        # Procesar secuencia
        result = []
        i = 0
        
        while i < len(phonemes):
            # Detectar broken spelling: V + V
            if (i < len(phonemes) - 1 and
                isinstance(phonemes[i], Vowel) and
                isinstance(phonemes[i+1], Vowel)):
                
                # Crear contexto
                context = self._create_context(phonemes, i, i+1, morphology, original_spelling)
                
                # Decidir si reconstruir
                decision = self._make_decision(
                    phonemes[i],
                    phonemes[i+1],
                    context,
                    morphology,
                    original_spelling
                )
                
                # Insertar fonemas
                result.append(phonemes[i])
                
                if decision.consonant and decision.confidence >= self.min_confidence:
                    # Reconstruir débil
                    result.append(decision.consonant)
                    
                    # Registrar reconstrucción
                    reconstruction = ReconstructedWeak(
                        position=len(result) - 1,
                        weak_consonant=decision.consonant,
                        confidence=decision.confidence,
                        evidence_type=decision.evidence_type.value,
                        reason=decision.reason,
                        original_spelling=original_spelling or "",
                        alternative=decision.alternative,
                    )
                    self.reconstructions.append(reconstruction)
                
                result.append(phonemes[i+1])
                i += 2
            else:
                result.append(phonemes[i])
                i += 1
        
        return (result, self.reconstructions)
    
    def _create_context(
        self,
        phonemes: List[Phoneme],
        v1_index: int,
        v2_index: int,
        morphology: Optional[MorphologicalInfo],
        original_spelling: Optional[str],
    ) -> PhonologicalContext:
        """Crea contexto para broken spelling V1-V2."""
        preceding = phonemes[v1_index - 1] if v1_index > 0 else None
        following = phonemes[v2_index + 1] if v2_index < len(phonemes) - 1 else None
        
        context = PhonologicalContext(
            preceding=preceding,
            target=None,  # A reconstruir
            following=following,
            original_spelling=original_spelling,
            is_broken_spelling=True,
        )
        
        # Añadir info morfológica si disponible
        if morphology:
            context.verb_class = morphology.verb_class
            context.is_imperative = morphology.is_imperative
        
        return context
    
    def _make_decision(
        self,
        vowel1: Vowel,
        vowel2: Vowel,
        context: PhonologicalContext,
        morphology: Optional[MorphologicalInfo],
        original_spelling: Optional[str],
    ) -> ReconstructionDecision:
        """
        Decide qué débil reconstruir (si alguna).
        
        Jerarquía de decisión:
        1. Casos especiales conocidos
        2. Información morfológica
        3. Contexto fonológico
        4. Default (no reconstruir)
        """
        # Modo FORCE: forzar débil específica
        if self.mode == ReconstructMode.FORCE_ALEPH:
            return ReconstructionDecision(
                consonant=get_consonant('ʾ'),
                confidence=1.0,
                reason="Forced by FORCE_ALEPH mode",
                evidence_type=EvidenceType.CONTEXTUAL,
            )
        elif self.mode == ReconstructMode.FORCE_WAW:
            return ReconstructionDecision(
                consonant=get_consonant('w'),
                confidence=1.0,
                reason="Forced by FORCE_WAW mode",
                evidence_type=EvidenceType.CONTEXTUAL,
            )
        elif self.mode == ReconstructMode.FORCE_YOD:
            return ReconstructionDecision(
                consonant=get_consonant('y'),
                confidence=1.0,
                reason="Forced by FORCE_YOD mode",
                evidence_type=EvidenceType.CONTEXTUAL,
            )
        
        # 1. Casos especiales
        if original_spelling:
            special = lookup_special_case(original_spelling)
            if special:
                return special
        
        # 2. Consultar tabla de decisión
        v1_quality = vowel1.quality.value
        v2_quality = vowel2.quality.value
        position = context.weak_position
        verb_class = morphology.verb_class if morphology else None
        
        decision = lookup_decision(v1_quality, v2_quality, position, verb_class)
        
        if decision:
            return decision
        
        # 3. Default
        return get_default_decision(vowel1, vowel2)
    
    def get_reconstruction_report(self) -> str:
        """
        Genera reporte de reconstrucciones realizadas.
        
        Returns:
            String formateado con todas las reconstrucciones
        """
        if not self.reconstructions:
            return "No weak consonants reconstructed."
        
        report = f"Reconstructed {len(self.reconstructions)} weak consonant(s):\n\n"
        
        for i, recon in enumerate(self.reconstructions, 1):
            report += f"{i}. {recon.weak_consonant.symbol} at position {recon.position}\n"
            report += f"   Confidence: {recon.confidence:.2f}\n"
            report += f"   Evidence: {recon.evidence_type}\n"
            report += f"   Reason: {recon.reason}\n"
            if recon.alternative:
                report += f"   Alternative: {recon.alternative.symbol}\n"
            report += "\n"
        
        return report


# ============================================================================
# FUNCIONES DE CONVENIENCIA
# ============================================================================

def reconstruct_weak_consonants(
    phonemes: List[Phoneme],
    mode: ReconstructMode = ReconstructMode.AUTO,
    morphology: Optional[MorphologicalInfo] = None,
    original_spelling: Optional[str] = None,
    min_confidence: float = 0.6,
) -> Tuple[List[Phoneme], List[ReconstructedWeak]]:
    """
    Función de conveniencia para reconstruir débiles.
    
    Args:
        phonemes: Secuencia de fonemas
        mode: Modo de reconstrucción
        morphology: Información morfológica
        original_spelling: Spelling ORACC original
        min_confidence: Confianza mínima
    
    Returns:
        (fonemas_con_débiles, reconstrucciones)
    
    Example:
        >>> from old_assyrian_morphophonology import oracc_to_phonemes
        >>> phonemes = oracc_to_phonemes("ša-a-lum")
        >>> reconstructed, info = reconstruct_weak_consonants(phonemes)
        >>> print([p.symbol for p in reconstructed])
        ['š', 'a', 'ʾ', 'ā', 'l', 'u', 'm']
    """
    reconstructor = WeakConsonantReconstructor(
        mode=mode,
        min_confidence=min_confidence,
    )
    
    return reconstructor.reconstruct_from_phonemes(
        phonemes,
        morphology=morphology,
        original_spelling=original_spelling,
    )


def identify_weak_verb_class(
    root: str,
    attested_forms: List[str],
) -> Optional[WeakVerbClass]:
    """
    Identifica la clase de verbo débil basándose en formas atestiguadas.
    
    Args:
        root: Raíz triconsonántica (ej: "√šʾl")
        attested_forms: Lista de formas ORACC atestiguadas
    
    Returns:
        WeakVerbClass si se puede identificar, None si no
    
    Note:
        Implementación básica. Será expandida en iteraciones futuras
        con análisis morfológico completo.
    """
    # Análisis básico de la raíz
    if 'ʾ' in root:
        if root.index('ʾ') == 1:  # Primera posición (después de √)
            return WeakVerbClass.I_ALEPH
        elif root.index('ʾ') == 2:  # Segunda posición
            return WeakVerbClass.II_ALEPH
        else:  # Tercera posición
            return WeakVerbClass.III_ALEPH
    
    if 'w' in root:
        if root.index('w') == 1:
            return WeakVerbClass.I_W
        elif root.index('w') == 2:
            return WeakVerbClass.II_W
        else:
            return WeakVerbClass.III_W
    
    if 'y' in root:
        if root.index('y') == 1:
            return WeakVerbClass.I_Y
        elif root.index('y') == 2:
            return WeakVerbClass.II_Y
        else:
            return WeakVerbClass.III_Y
    
    # Buscar vocales largas que indiquen débiles
    if 'ū' in root:
        if root.index('ū') == 2:
            return WeakVerbClass.II_U_LONG
        else:
            return WeakVerbClass.III_U_LONG
    
    if 'ī' in root:
        if root.index('ī') == 2:
            return WeakVerbClass.II_I_LONG
        else:
            return WeakVerbClass.III_I_LONG
    
    return None


# Importar aquí para evitar circular imports
from phonology.weak_enums import EvidenceType

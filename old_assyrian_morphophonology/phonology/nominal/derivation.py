"""
Algoritmo de derivación nominal del Old Assyrian.

Aplica patrones nominales a raíces consonánticas.

Basado en Kouwenberg (2017) § 4.2.
"""

from typing import List, Optional
from .. import Consonant, Vowel, Phoneme, get_consonant, get_vowel
from .pattern import NominalRoot, NominalPattern, DerivedNominal
from .enums import Gender, Number, State


def apply_pattern_to_root(
    root: NominalRoot,
    pattern: NominalPattern,
    gender: Optional[Gender] = None,
    number: Number = Number.SINGULAR,
    state: State = State.ABSOLUTE,
    gloss: str = ""
) -> DerivedNominal:
    """
    Aplica patrón nominal a raíz consonántica.
    
    Algoritmo:
      1. Verificar compatibilidad raíz-patrón
      2. Mapear consonantes de raíz a slots C del template
      3. Insertar vocales del patrón en slots V
      4. Aplicar geminación si template incluye G
      5. Agregar mimación si corresponde
      6. [Futuro] Aplicar reglas fonológicas (Iter 3-5)
    
    Args:
        root: Raíz consonántica (√mlk, √šrq, etc.)
        pattern: Patrón nominal (PaRS, PiRS, etc.)
        gender: Género (usa default del patrón si None)
        number: Número (singular por defecto)
        state: Estado (absoluto por defecto)
        gloss: Traducción opcional
    
    Returns:
        DerivedNominal con forma fonológica completa
    
    Raises:
        ValueError: Si patrón no es compatible con raíz
    
    Examples:
        >>> root = NominalRoot(C1=get_consonant('m'), C2=get_consonant('l'), C3=get_consonant('k'))
        >>> from .templates import PARS
        >>> derived = apply_pattern_to_root(root, PARS)
        >>> derived.to_string()
        'malkum'
    """
    # 1. Verificar compatibilidad
    if not pattern.is_compatible_with_root(root):
        raise ValueError(
            f"Patrón {pattern.name} no es compatible con raíz {root.to_string()}. "
            f"Patrón requiere {pattern.get_consonant_slots()} consonantes, "
            f"raíz tiene {len(root.get_consonants())}."
        )
    
    # 2. Determinar género
    if gender is None:
        gender = pattern.gender
    
    # 3. Construir forma base
    phonemes = build_base_form(root, pattern)
    
    # 4. Agregar mimación si corresponde
    if pattern.has_mimation and state == State.ABSOLUTE and number == Number.SINGULAR:
        phonemes = add_mimation(phonemes, gender)
    
    # 5. [FUTURO] Aplicar reglas fonológicas
    # - Asimilación (Iter 3)
    # - Procesos vocálicos (Iter 4)
    # - Epéntesis (Iter 5)
    
    return DerivedNominal(
        root=root,
        pattern=pattern,
        phonemes=phonemes,
        gender=gender,
        number=number,
        state=state,
        gloss=gloss
    )


def build_base_form(root: NominalRoot, pattern: NominalPattern) -> List[Phoneme]:
    """
    Construye forma base aplicando template a raíz.
    
    Procesa template carácter por carácter:
      - 'C': Inserta siguiente consonante de raíz
      - 'V': Inserta siguiente vocal del patrón
      - 'G': Inserta geminación (repite última consonante)
      - 'M': Inserta prefijo ma-
    
    Args:
        root: Raíz consonántica
        pattern: Patrón nominal
    
    Returns:
        Lista de fonemas de forma base (sin mimación)
    """
    phonemes: List[Phoneme] = []
    consonants = root.get_consonants()
    vowels = pattern.vowels
    
    consonant_index = 0
    vowel_index = 0
    last_consonant = None
    
    template = pattern.template
    i = 0
    
    while i < len(template):
        char = template[i]
        
        if char == 'C':
            # Insertar consonante de raíz
            if consonant_index < len(consonants):
                consonant = consonants[consonant_index]
                phonemes.append(consonant)
                last_consonant = consonant
                consonant_index += 1
            else:
                raise ValueError(
                    f"Template requiere más consonantes de las disponibles en raíz. "
                    f"Template: {template}, Raíz: {root.to_string()}"
                )
        
        elif char == 'V':
            # Insertar vocal del patrón
            if vowel_index < len(vowels):
                vowel = vowels[vowel_index]
                phonemes.append(vowel)
                vowel_index += 1
            else:
                raise ValueError(
                    f"Template requiere más vocales de las especificadas en patrón. "
                    f"Template: {template}, Vocales: {len(vowels)}"
                )
        
        elif char == 'G':
            # Geminación: repetir última consonante
            if last_consonant is None:
                raise ValueError("Geminación requiere consonante previa")
            phonemes.append(last_consonant)
        
        elif char == 'M':
            # Prefijo ma-
            phonemes.append(get_consonant('m'))
            phonemes.append(get_vowel('a'))
        
        else:
            raise ValueError(f"Carácter desconocido en template: {char}")
        
        i += 1
    
    return phonemes


def add_mimation(phonemes: List[Phoneme], gender: Gender) -> List[Phoneme]:
    """
    Agrega mimación al final de palabra.
    
    Mimación en OA:
      - Masculino: -um
      - Femenino: -um (después de -at)
    
    Args:
        phonemes: Lista de fonemas base
        gender: Género del sustantivo
    
    Returns:
        Lista con mimación agregada
    """
    result = phonemes.copy()
    
    # Agregar -um
    result.append(get_vowel('u'))
    result.append(get_consonant('m'))
    
    return result


def apply_construct_state(derived: DerivedNominal) -> DerivedNominal:
    """
    Convierte sustantivo de estado absoluto a constructo.
    
    Cambios en estado constructo:
      - Pérdida de mimación: -um → ∅
      - Acortamiento de vocal final en algunos casos
    
    Args:
        derived: Sustantivo en estado absoluto
    
    Returns:
        Nuevo DerivedNominal en estado constructo
    
    Examples:
        >>> # šarrum "rey" → šar "rey de..."
        >>> # malkum "consejo" → malik "consejo de..."
    """
    if derived.state == State.CONSTRUCT:
        # Ya está en constructo
        return derived
    
    phonemes = derived.phonemes.copy()
    
    # Remover mimación (-um final)
    if len(phonemes) >= 2:
        # Verificar si termina en -um
        if (phonemes[-1].symbol == 'm' and 
            phonemes[-2].symbol == 'u'):
            # Remover -um
            phonemes = phonemes[:-2]
    
    # [FUTURO] Aplicar otras reglas de estado constructo
    # - Acortamiento vocálico
    # - Cambios de patrón específicos
    
    return DerivedNominal(
        root=derived.root,
        pattern=derived.pattern,
        phonemes=phonemes,
        gender=derived.gender,
        number=derived.number,
        state=State.CONSTRUCT,
        gloss=derived.gloss
    )


def derive_feminine(derived: DerivedNominal) -> DerivedNominal:
    """
    Deriva forma femenina de sustantivo masculino.
    
    Típicamente agrega sufijo -at:
      - malkum (masc.) → malkatum (fem.)
    
    Args:
        derived: Sustantivo masculino base
    
    Returns:
        Sustantivo femenino derivado
    
    Note:
        Implementación básica. En realidad, formación del
        femenino es más compleja y puede variar por patrón.
    """
    if derived.gender == Gender.FEMININE:
        # Ya es femenino
        return derived
    
    phonemes = derived.phonemes.copy()
    
    # Remover mimación masculina si presente
    if len(phonemes) >= 2 and phonemes[-1].symbol == 'm':
        phonemes = phonemes[:-2]  # Remover -um
    
    # Agregar -at
    phonemes.append(get_vowel('a'))
    phonemes.append(get_consonant('t'))
    
    # Agregar mimación femenina -um
    phonemes.append(get_vowel('u'))
    phonemes.append(get_consonant('m'))
    
    return DerivedNominal(
        root=derived.root,
        pattern=derived.pattern,
        phonemes=phonemes,
        gender=Gender.FEMININE,
        number=derived.number,
        state=derived.state,
        gloss=derived.gloss
    )


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def derive_from_string(
    root_string: str,
    pattern_name: str,
    **kwargs
) -> DerivedNominal:
    """
    Deriva sustantivo desde strings.
    
    Wrapper conveniente para derivación.
    
    Args:
        root_string: Raíz como string ("√mlk", "mlk")
        pattern_name: Nombre del patrón ("PaRS", "PiRS")
        **kwargs: Argumentos adicionales para apply_pattern_to_root
    
    Returns:
        DerivedNominal
    
    Examples:
        >>> derive_from_string("mlk", "PaRS")
        DerivedNominal(root=√mlk, pattern=PaRS, surface=malkum)
    """
    from .pattern import create_root_from_string
    from .templates import get_pattern_by_name
    
    root = create_root_from_string(root_string)
    pattern = get_pattern_by_name(pattern_name)
    
    return apply_pattern_to_root(root, pattern, **kwargs)


def get_all_forms(
    root: NominalRoot,
    pattern: NominalPattern
) -> dict:
    """
    Genera todas las formas de un sustantivo.
    
    Returns dict con:
        - abs_sg_m: Absoluto singular masculino
        - const_sg_m: Constructo singular masculino
        - abs_sg_f: Absoluto singular femenino
        - const_sg_f: Constructo singular femenino
    
    Args:
        root: Raíz consonántica
        pattern: Patrón nominal
    
    Returns:
        Dict con formas generadas
    """
    # Forma base: absoluto singular masculino
    abs_sg_m = apply_pattern_to_root(
        root, pattern,
        number=Number.SINGULAR,
        state=State.ABSOLUTE
    )
    
    # Constructo singular masculino
    const_sg_m = apply_construct_state(abs_sg_m)
    
    # Femenino singular absoluto
    abs_sg_f = derive_feminine(abs_sg_m)
    
    # Femenino singular constructo
    const_sg_f = apply_construct_state(abs_sg_f)
    
    return {
        'abs_sg_m': abs_sg_m,
        'const_sg_m': const_sg_m,
        'abs_sg_f': abs_sg_f,
        'const_sg_f': const_sg_f,
    }

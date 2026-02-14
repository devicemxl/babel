"""
Reglas fonológicas para verbos débiles del Old Assyrian.

ITERACIÓN 9 - Verbos I-débil

Implementa las transformaciones fonológicas específicas de verbos débiles:
- I/w: Contracciones w+i → u/ū/ī
- I/voc: Alargamiento compensatorio por gutural perdida
- I/n: Asimilación n+C → CC y pérdida #n → Ø

Basado en Kouwenberg (2017) Capítulo 18.

Autor: Claude
Fecha: 2026-02-12
"""

from typing import List, Optional, Callable
from functools import wraps
import sys
import os

# Ajustar path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from phonology import Phoneme, Vowel, Consonant
from phonology.inventory import get_consonant


# Helper function para crear vocales
def _make_vowel(symbol: str, length: str = 'short'):
    """Helper para crear Vowel con longitud."""
    from phonology.enums import VowelQuality, VowelLength
    from phonology.features import VowelFeatures
    
    quality_map = {'a': VowelQuality.A, 'e': VowelQuality.E, 
                   'i': VowelQuality.I, 'u': VowelQuality.U}
    length_enum = VowelLength.LONG if length == 'long' else VowelLength.SHORT
    
    return Vowel(features=VowelFeatures(quality=quality_map[symbol], length=length_enum))




# ============================================================================
# DECORADOR PARA REGLAS FONOLÓGICAS
# ============================================================================

def phonological_rule(func: Callable) -> Callable:
    """
    Decorador para marcar funciones como reglas fonológicas.
    
    Provee metadata útil para debugging y documentación.
    
    Usage:
        @phonological_rule
        def my_rule(phonemes: List[Phoneme]) -> List[Phoneme]:
            ...
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    wrapper._is_phonological_rule = True
    wrapper._rule_name = func.__name__
    return wrapper


# ============================================================================
# I/W RULES - Contracciones
# ============================================================================

@phonological_rule
def contract_w_i_to_u(phonemes: List[Phoneme], context: dict = None) -> List[Phoneme]:
    """
    Regla: w + i → u (I/w fientivo presente)
    
    Contexto: Prefijo i- del presente + w inicial
    
    Proceso:
        *wi-wšab → *w-i-šab → u-šab
    
    Referencias: § 18.2.1, Tabla 18.1
    
    Args:
        phonemes: Secuencia esperada [w, i, ...resto]
        context: Diccionario opcional con información contextual
    
    Returns:
        [u, ...resto] donde u es vocal CORTA
    
    Examples:
        wasābum Pres 3sm: [w, i, š, a, b] → [u, š, a, b]
        wabālum Pres 3sm: [w, i, b, a, l] → [u, b, a, l]
    """
    if len(phonemes) < 2:
        return phonemes
    
    # Detectar patrón w + i al inicio
    if (isinstance(phonemes[0], Consonant) and phonemes[0].symbol == 'w' and
        isinstance(phonemes[1], Vowel) and phonemes[1].symbol == 'i'):
        # Reemplazar w+i por u (corta)
        return [_make_vowel('u', 'short')] + phonemes[2:]
    
    return phonemes


@phonological_rule
def contract_w_i_to_u_long(phonemes: List[Phoneme], context: dict = None) -> List[Phoneme]:
    """
    Regla: w + i → ū (I/w fientivo pretérito - VOCAL LARGA)
    
    Contexto: Prefijo i- del pretérito + w inicial
    
    Proceso:
        *wi-wšib → ū-šib
    
    DIFERENCIA CRÍTICA con contract_w_i_to_u:
        - Presente: u (corta)
        - Pretérito: ū (LARGA)
    
    EXCEPCIÓN: Vocal corta si hay ending vocálico (síncope)
        ūšib (3sm, sin ending) vs ušbū (3pm, con ending -ū)
    
    Referencias: § 18.2.1, Tabla 18.1
    
    Args:
        phonemes: Secuencia esperada [w, i, ...resto]
        context: Debe contener 'has_ending': bool
    
    Returns:
        [ū, ...resto] si no hay ending
        [u, ...resto] si hay ending
    
    Examples:
        wasābum Pret 3sm: [w, i, š, i, b] → [ū, š, i, b]
        wasābum Pret 3pm: [w, i, š, (i), b, ū] → [u, š, b, ū] (síncope de i)
    """
    if len(phonemes) < 2:
        return phonemes
    
    # Detectar patrón w + i
    if (isinstance(phonemes[0], Consonant) and phonemes[0].symbol == 'w' and
        isinstance(phonemes[1], Vowel) and phonemes[1].symbol == 'i'):
        
        # Determinar si hay ending
        has_ending = context and context.get('has_ending', False)
        
        if has_ending:
            # Con ending: u corta (síncope previene vocal larga)
            return [_make_vowel('u', 'short')] + phonemes[2:]
        else:
            # Sin ending: ū larga
            return [_make_vowel('u', 'long')] + phonemes[2:]
    
    return phonemes


@phonological_rule
def contract_w_i_to_i_long(phonemes: List[Phoneme], context: dict = None) -> List[Phoneme]:
    """
    Regla: w + i → ī (I/w adjetival - SIEMPRE LARGA)
    
    Contexto: Prefijo i- + w inicial en verbos adjetivales
    
    Proceso:
        *wi-wter → ī-ter
    
    DIFERENCIA CLAVE con I/w fientivo:
        Fientivo:   Presente u-ššab (corta), Pretérito ū-šib (larga)
        Adjetival:  Presente ī-ter (larga), Pretérito ī-ter (larga)
    
    CARACTERÍSTICA: Vocal SIEMPRE larga independientemente de forma
    
    Referencias: § 18.2.2, Tabla 18.2
    
    Args:
        phonemes: Secuencia esperada [w, i, ...resto]
        context: No usado (siempre larga)
    
    Returns:
        [ī, ...resto] donde ī es vocal LARGA
    
    Examples:
        watārum Pres 3sm: [w, i, t, e, r] → [ī, t, e, r]
        watārum Pret 3sm: [w, i, t, e, r] → [ī, t, e, r]
        waqārum Pres 3sm: [w, i, q, e, r] → [ī, q, e, r]
    """
    if len(phonemes) < 2:
        return phonemes
    
    # Detectar patrón w + i
    if (isinstance(phonemes[0], Consonant) and phonemes[0].symbol == 'w' and
        isinstance(phonemes[1], Vowel) and phonemes[1].symbol == 'i'):
        # SIEMPRE reemplazar por ī larga
        return [_make_vowel('i', 'long')] + phonemes[2:]
    
    return phonemes


@phonological_rule
def drop_initial_w(phonemes: List[Phoneme], context: dict = None) -> List[Phoneme]:
    """
    Regla: w inicial → Ø (pérdida total de w)
    
    Contexto: Imperativo I/w, infinitivos con alternancia, algunos participios
    
    Proceso:
        *wšib → šib (imperativo)
    
    Referencias: § 18.2.1, Tabla 18.1
    
    Args:
        phonemes: Secuencia con w inicial
        context: Debe contener 'word_initial': True
    
    Returns:
        [...resto] sin w
    
    Examples:
        wasābum Imp sm: [w, š, i, b] → [š, i, b]
        wabālum Imp sm: [w, b, i, l] → [b, i, l]
        warādum Imp sm: [w, r, i, d] → [r, i, d]
    """
    if not phonemes:
        return phonemes
    
    # Verificar contexto word-initial
    if not (context and context.get('word_initial', False)):
        return phonemes
    
    # Si primer fonema es w, eliminar
    if isinstance(phonemes[0], Consonant) and phonemes[0].symbol == 'w':
        return phonemes[1:]
    
    return phonemes


# ============================================================================
# I/VOC RULES - Compensación vocálica
# ============================================================================

@phonological_rule
def apply_compensatory_lengthening(phonemes: List[Phoneme], 
                                     initial_vowel: str = 'a',
                                     context: dict = None) -> List[Phoneme]:
    """
    Regla: Vocal → Vocal larga (compensación por gutural perdida)
    
    Contexto: I/voc, gutural perdida (*ʔ, *h, *ʕ, *ḥ → Ø) causa alargamiento
    
    Proceso histórico:
        Proto-semítico: *yaʔḥuz → *yaḥuz → *yēḥuz → ēḥuz
        
    Aplicación en OA:
        - Pretérito: SIEMPRE vocal larga (ēḥuz, āḥuz)
        - Perfect: SIEMPRE vocal larga (ētaḥaz, ātaḥaz)
        - Presente: Probablemente larga (ortografía ambigua)
    
    Referencias: § 18.3.1, Tabla 18.6
    
    Args:
        phonemes: Secuencia con vocal inicial
        initial_vowel: Cuál vocal debe ser larga ('a' para I/a, 'e' para I/e)
        context: Información sobre forma verbal
    
    Returns:
        Secuencia con vocal inicial alargada
    
    Examples:
        ahāzum Pret 1s: [a, ḥ, u, z] → [ā, ḥ, u, z]
        ahāzum Pret 3sm: [e, ḥ, u, z] → [ē, ḥ, u, z]
        epāšum Pret 1s: [e, p, u, š] → [ē, p, u, š]
    """
    if not phonemes:
        return phonemes
    
    result = []
    for i, p in enumerate(phonemes):
        # Alargar vocal inicial si coincide con initial_vowel
        if (i == 0 and isinstance(p, Vowel) and 
            p.symbol == initial_vowel and not p.features.is_long):
            result.append(_make_vowel(initial_vowel, 'long'))
        else:
            result.append(p)
    
    return result


@phonological_rule
def lengthen_prefix_vowel_in_preterite(phonemes: List[Phoneme],
                                        person: int = 3,
                                        context: dict = None) -> List[Phoneme]:
    """
    Regla: Vocal de prefijo → larga en pretérito I/voc
    
    Contexto: Pretérito y Perfect de I/voc
    
    Mapeo persona → vocal larga:
        1s:  a → ā (ā-ḥuz)
        3s:  e → ē (ē-ḥuz) [< *ya-]
        2s:  t+a → tā (tā-ḥuz)
        1p:  n+e → nē (nē-ḥuz)
    
    Referencias: § 18.3.1, Tabla 18.6
    
    Args:
        phonemes: Secuencia de fonemas del pretérito
        person: 1, 2, o 3
        context: Información adicional
    
    Returns:
        Secuencia con vocal de prefijo alargada
    
    Examples:
        ahāzum Pret 1s: [a, ...] → [ā, ...]
        ahāzum Pret 3sm: [e, ...] → [ē, ...]
        ahāzum Pret 2sm: [t, a, ...] → [t, ā, ...]
    """
    if not phonemes:
        return phonemes
    
    result = []
    
    if person == 1:
        # 1s o 1p: buscar 'a' o 'e' inicial (después de n-)
        for i, p in enumerate(phonemes):
            if isinstance(p, Vowel) and p.symbol in ['a', 'e'] and not p.features.is_long:
                # Primera vocal → alargar
                result.append(_make_vowel(p.symbol.lower(), 'long'))
                result.extend(phonemes[i+1:])
                break
            else:
                result.append(p)
    
    elif person == 2:
        # 2s o 2p: buscar 'a' después de 't'
        for i, p in enumerate(phonemes):
            if isinstance(p, Vowel) and p.symbol.lower() == 'a' and not p.features.is_long:
                result.append(_make_vowel('a', 'long'))
                result.extend(phonemes[i+1:])
                break
            else:
                result.append(p)
    
    elif person == 3:
        # 3s o 3p: buscar 'e' inicial
        for i, p in enumerate(phonemes):
            if isinstance(p, Vowel) and p.symbol.lower() == 'e' and not p.features.is_long:
                result.append(_make_vowel('e', 'long'))
                result.extend(phonemes[i+1:])
                break
            else:
                result.append(p)
    
    return result if result else phonemes


# ============================================================================
# I/N RULES - Asimilación y pérdida
# ============================================================================

@phonological_rule
def assimilate_n_to_following_consonant(phonemes: List[Phoneme], 
                                         context: dict = None) -> List[Phoneme]:
    """
    Regla: n + C → CC (asimilación total de n)
    
    Contexto: I/n, n forma cluster con consonante siguiente
    
    Proceso:
        naṣārum Pret: *i-nṣur → i-ṣṣur
        nadā'um Pret: *i-ndi → i-ddi
        naṣārum Perf: *i-ntaṣar → it-taṣar
    
    EXCEPCIONES (n NO asimila):
        - n + w → nw (w es débil)
        - n + m → nm (ambos nasales)
        - n + r, l → nr, nl (en algunos contextos)
    
    Referencias: § 18.4, § 3.2.4.1, Tabla 18.13
    
    Args:
        phonemes: Secuencia con n seguida de consonante
        context: Información adicional
    
    Returns:
        Secuencia con n asimilada (geminación de C)
    
    Examples:
        naṣārum Pret: [i, n, ṣ, u, r] → [i, ṣ, ṣ, u, r]
        nadā'um Pret: [i, n, d, i] → [i, d, d, i]
        naṣārum Perf: [i, n, t, a, ṣ, a, r] → [i, t, t, a, ṣ, a, r]
    """
    if len(phonemes) < 2:
        return phonemes
    
    result = []
    i = 0
    
    while i < len(phonemes):
        if i < len(phonemes) - 1:
            current = phonemes[i]
            next_p = phonemes[i + 1]
            
            # Detectar n + consonante
            if (isinstance(current, Consonant) and current.symbol == 'n' and
                isinstance(next_p, Consonant)):
                
                # Verificar excepciones
                if next_p.symbol in ['w', 'm', 'r', 'l', 'y']:
                    # NO asimilar (preservar n)
                    result.append(current)
                    i += 1
                else:
                    # Asimilar: n desaparece, C se gemina
                    result.append(next_p)  # Primera C
                    result.append(next_p)  # Segunda C (geminación)
                    i += 2  # Saltar n y C original
            else:
                result.append(current)
                i += 1
        else:
            result.append(phonemes[i])
            i += 1
    
    return result


@phonological_rule
def drop_initial_n_before_high_vowel(phonemes: List[Phoneme], 
                                       context: dict = None) -> List[Phoneme]:
    """
    Regla: #n + i/u → #i/u (pérdida de n inicial)
    
    Contexto: I/n, palabra inicial + vocal alta
    
    # = límite de palabra (word-initial)
    
    Aplicación:
        - Imperativo G: *nuṣur → uṣur, *niker → iker
        - Gt/Gtn sin prefijo: *nitaddi → itaddi
        - Ntn sin prefijo: *nitaddi → itaddi
    
    IMPORTANTE: Solo en inicio de palabra
    
    Referencias: § 18.4, Tabla 18.13
    
    Args:
        phonemes: Secuencia con n inicial + vocal alta
        context: Debe contener 'word_initial': True
    
    Returns:
        [i/u, ...resto] sin n
    
    Examples:
        naṣārum Imp: [n, u, ṣ, u, r] → [u, ṣ, u, r]
        nakārum Imp: [n, i, k, e, r] → [i, k, e, r]
        nadā'um Gtn Imp: [n, i, t, a, d, d, i] → [i, t, a, d, d, i]
    """
    if len(phonemes) < 2:
        return phonemes
    
    # Verificar contexto word-initial
    if not (context and context.get('word_initial', False)):
        return phonemes
    
    # Detectar n inicial + vocal alta (i, u)
    if (isinstance(phonemes[0], Consonant) and phonemes[0].symbol == 'n' and
        isinstance(phonemes[1], Vowel) and phonemes[1].symbol in ['i', 'u']):
        # Eliminar n, preservar vocal
        return phonemes[1:]
    
    return phonemes


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def is_high_vowel(phoneme: Phoneme) -> bool:
    """
    Verifica si fonema es vocal alta (i, u).
    
    Args:
        phoneme: Fonema a verificar
    
    Returns:
        True si es vocal i o u
    """
    return isinstance(phoneme, Vowel) and phoneme.symbol in ['i', 'u']


def is_low_vowel(phoneme: Phoneme) -> bool:
    """
    Verifica si fonema es vocal baja (a, e).
    
    Args:
        phoneme: Fonema a verificar
    
    Returns:
        True si es vocal a o e
    """
    return isinstance(phoneme, Vowel) and phoneme.symbol in ['a', 'e']


def can_assimilate_n(consonant: Phoneme, following: Phoneme) -> bool:
    """
    Determina si n puede asimilar a consonante siguiente.
    
    Args:
        consonant: Consonante 'n'
        following: Consonante siguiente
    
    Returns:
        True si puede asimilar, False si es excepción
    """
    if not (isinstance(consonant, Consonant) and consonant.symbol == 'n'):
        return False
    
    if not isinstance(following, Consonant):
        return False
    
    # n NO asimila a estas consonantes
    if following.symbol in ['w', 'm', 'r', 'l', 'y']:
        return False
    
    return True


def phonemes_to_string(phonemes: List[Phoneme]) -> str:
    """
    Convierte lista de fonemas a string legible.
    
    Útil para tests y debugging.
    
    Convenciones:
        - Vocal larga: símbolo + 'ː' marca de longitud
        - Consonante: símbolo solo
    
    Args:
        phonemes: Lista de fonemas
    
    Returns:
        String representativo
    
    Examples:
        [u, š, a, b] → "ušab"
        [ū, š, i, b] → "ūšib" (con marca implícita de longitud)
        [i, ṣ, ṣ, u, r] → "iṣṣur"
    """
    result = ""
    for p in phonemes:
        result += p.symbol
        if isinstance(p, Vowel) and p.length == 'long':
            # La longitud está en p.length
            # Para visualización, podríamos agregar 'ː' pero lo dejamos implícito
            pass
    return result


def get_rule_by_name(rule_name: str) -> Optional[Callable]:
    """
    Obtiene regla fonológica por nombre.
    
    Args:
        rule_name: Nombre de la regla (ej: 'contract_w_i_to_u')
    
    Returns:
        Función regla si existe, None si no
    
    Example:
        rule = get_rule_by_name('contract_w_i_to_u')
        result = rule(phonemes)
    """
    # Buscar en globals()
    rule = globals().get(rule_name)
    
    if rule and hasattr(rule, '_is_phonological_rule'):
        return rule
    
    return None


def list_all_rules() -> List[str]:
    """
    Lista todas las reglas fonológicas disponibles.
    
    Returns:
        Lista de nombres de reglas
    
    Example:
        rules = list_all_rules()
        print(rules)
        # ['contract_w_i_to_u', 'contract_w_i_to_u_long', ...]
    """
    rules = []
    
    for name, obj in globals().items():
        if hasattr(obj, '_is_phonological_rule') and obj._is_phonological_rule:
            rules.append(name)
    
    return sorted(rules)


# ============================================================================
# COMBINADORES DE REGLAS
# ============================================================================

def apply_rules_sequentially(phonemes: List[Phoneme], 
                               rules: List[Callable],
                               context: dict = None) -> List[Phoneme]:
    """
    Aplica múltiples reglas en secuencia.
    
    Args:
        phonemes: Secuencia inicial
        rules: Lista de funciones regla
        context: Contexto para todas las reglas
    
    Returns:
        Secuencia después de aplicar todas las reglas
    
    Example:
        result = apply_rules_sequentially(
            phonemes,
            [contract_w_i_to_u, drop_initial_w],
            context={'word_initial': True}
        )
    """
    result = phonemes
    
    for rule in rules:
        result = rule(result, context)
    
    return result


def apply_rule_conditionally(phonemes: List[Phoneme],
                               rule: Callable,
                               condition: Callable[[List[Phoneme]], bool],
                               context: dict = None) -> List[Phoneme]:
    """
    Aplica regla solo si condición se cumple.
    
    Args:
        phonemes: Secuencia de fonemas
        rule: Regla a aplicar
        condition: Función que retorna True si regla debe aplicarse
        context: Contexto para la regla
    
    Returns:
        Secuencia modificada o sin cambios
    
    Example:
        result = apply_rule_conditionally(
            phonemes,
            contract_w_i_to_u,
            lambda p: len(p) >= 2 and p[0].symbol == 'w'
        )
    """
    if condition(phonemes):
        return rule(phonemes, context)
    else:
        return phonemes

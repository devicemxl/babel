"""
Tabla de clusters consonánticos permitidos y prohibidos en Old Assyrian.

Basado en Kouwenberg (2017) § 3.2.2.
"""

from typing import Dict, Tuple, Optional
from .enums import ClusterType


# ============================================================================
# CLUSTERS PERMITIDOS (divididos por frontera silábica)
# ============================================================================

ALLOWED_CLUSTERS: Dict[Tuple[str, str], str] = {
    # Formato: (C₁, C₂) → nota/comportamiento
    
    # ========== OBSTRUENT + OBSTRUENT ==========
    ('d', 'm'): 'allowed',      # damqum → dam.qum
    ('š', 't'): 'allowed',      # ištaknū → iš.tak.nū
    ('p', 'r'): 'allowed',      # ipparras → ip.par.ras (con geminada)
    ('b', 't'): 'allowed',      # ibtalkit → ib.tal.kit
    ('k', 't'): 'allowed',      # iktalʾū → ik.tal.ʾū
    
    # ========== NASAL + OBSTRUENT ==========
    # NOTA: n típicamente ASIMILA (Iter 3), no forma cluster estable
    ('n', 'p'): 'assimilates_to_pp',  # in-paras → ipparas
    ('n', 't'): 'assimilates_to_tt',  # in-taqqul → ittaqqul
    ('n', 'k'): 'assimilates_to_kk',  # in-kasad → ikkasad
    ('m', 'q'): 'assimilates_to_qq',  # am-qut → aqqut
    
    # m gramatical también asimila
    ('m', 'k'): 'assimilates',
    ('m', 'š'): 'assimilates',
    
    # ========== LÍQUIDA + CONSONANTE ==========
    # Pueden disparar EPÉNTESIS (Iter 5)
    ('r', 'C'): 'epenthesis_common',  # kabrū → kāberu
    ('l', 'C'): 'epenthesis_common',  # šuqlum → šuqulum
    
    # Específicos permitidos (sin epéntesis necesaria)
    ('r', 'd'): 'allowed',
    ('r', 'k'): 'allowed',
    ('r', 't'): 'allowed',
    ('l', 'd'): 'allowed',
    ('l', 'k'): 'allowed',
    
    # ========== h + CONSONANTE ==========
    ('h', 'C'): 'epenthesis_possible',  # miḫram → miḫiram
    ('h', 'd'): 'epenthesis',
    ('h', 'l'): 'epenthesis',
    ('h', 'r'): 'epenthesis',
    
    # ========== GEMINADAS ==========
    # Siempre divididas por frontera silábica
    ('p', 'p'): 'geminate',     # ipparras → ip.par.ras
    ('t', 't'): 'geminate',     # ittaqqul → it.taq.qul
    ('k', 'k'): 'geminate',
    ('b', 'b'): 'geminate',
    ('d', 'd'): 'geminate',
    ('g', 'g'): 'geminate',
    ('s', 's'): 'geminate',
    ('š', 'š'): 'geminate',
    ('z', 'z'): 'geminate',
    ('ṣ', 'ṣ'): 'geminate',
    ('ḫ', 'ḫ'): 'geminate',
    ('r', 'r'): 'geminate',
    ('l', 'l'): 'geminate',
    ('m', 'm'): 'geminate',
    ('n', 'n'): 'geminate',
    ('w', 'w'): 'geminate',
    ('y', 'y'): 'geminate',
}


# ============================================================================
# CLUSTERS PROHIBIDOS (nunca permitidos)
# ============================================================================

PROHIBITED_CLUSTERS: Dict[str, list] = {
    # Clusters en ONSET (inicio de sílaba)
    'initial_clusters': [
        # TODOS los clusters CC prohibidos en onset
        # OA no permite inicio con cluster
    ],
    
    # Clusters en CODA (final de sílaba)
    'final_clusters': [
        # Máximo 1 consonante en coda
        # CC en coda prohibido
    ],
    
    # Clusters específicos bloqueados
    'blocked_combinations': [
        # Combinaciones que siempre asimilan o se resuelven
        # (ya cubiertos en ALLOWED_CLUSTERS con nota)
    ],
    
    # Clusters TRIPLES
    'triple_clusters': [
        # NUNCA permitidos
        # Si surgen por morfología → epéntesis obligatoria
        # Ej: šiprum + -šu → šiparšu (NO **šiprušu)
    ],
}


# ============================================================================
# FUNCIONES DE CONSULTA
# ============================================================================

def is_cluster_allowed(c1: str, c2: str) -> bool:
    """
    Verifica si cluster C₁C₂ es permitido (con frontera silábica).
    
    Args:
        c1: Primera consonante
        c2: Segunda consonante
    
    Returns:
        True si cluster permitido (dividido por frontera)
    """
    # Verificar tabla
    if (c1, c2) in ALLOWED_CLUSTERS:
        note = ALLOWED_CLUSTERS[(c1, c2)]
        # Clusters que asimilan no son "clusters" en superficie
        if 'assimilate' in note:
            return False  # Se convierte en geminada
        return True
    
    # Genérico líquida + C
    if c1 in ['r', 'l'] and ('r', 'C') in ALLOWED_CLUSTERS:
        return True
    
    # Genérico h + C
    if c1 == 'h' and ('h', 'C') in ALLOWED_CLUSTERS:
        return True
    
    # Default: permitido pero con frontera
    return True


def cluster_requires_assimilation(c1: str, c2: str) -> bool:
    """
    Verifica si cluster requiere asimilación (Iter 3).
    
    Args:
        c1: Primera consonante
        c2: Segunda consonante
    
    Returns:
        True si debe asimilar
    """
    if (c1, c2) in ALLOWED_CLUSTERS:
        note = ALLOWED_CLUSTERS[(c1, c2)]
        return 'assimilate' in note
    
    # n + obstruent siempre asimila
    if c1 == 'n' and c2 in ['p', 't', 'k', 'b', 'd', 'g', 's', 'š', 'z', 'ṣ', 'ḫ']:
        return True
    
    return False


def cluster_may_need_epenthesis(c1: str, c2: str) -> bool:
    """
    Verifica si cluster puede necesitar epéntesis.
    
    Args:
        c1: Primera consonante
        c2: Segunda consonante
    
    Returns:
        True si epéntesis posible
    """
    if (c1, c2) in ALLOWED_CLUSTERS:
        note = ALLOWED_CLUSTERS[(c1, c2)]
        return 'epenthesis' in note
    
    # Líquida + C típicamente sí
    if c1 in ['r', 'l']:
        return True
    
    # h + C posiblemente
    if c1 == 'h':
        return True
    
    return False


def get_cluster_type_from_pair(c1: str, c2: str) -> ClusterType:
    """
    Determina tipo de cluster desde par de consonantes.
    
    Args:
        c1: Primera consonante
        c2: Segunda consonante
    
    Returns:
        ClusterType
    """
    # Geminada
    if c1 == c2:
        return ClusterType.GEMINATE
    
    # Líquida + C
    if c1 in ['r', 'l']:
        return ClusterType.LIQUID_C
    
    # C + líquida
    if c2 in ['r', 'l']:
        return ClusterType.C_LIQUID
    
    # Nasal + C
    if c1 in ['n', 'm']:
        return ClusterType.NASAL_C
    
    # C + nasal
    if c2 in ['n', 'm']:
        return ClusterType.C_NASAL
    
    # h + C
    if c1 == 'h':
        return ClusterType.H_C
    
    # C + h
    if c2 == 'h':
        return ClusterType.C_H
    
    # Sibilante + C
    if c1 in ['s', 'z', 'ṣ', 'š']:
        return ClusterType.SIBILANT_C
    
    # C + sibilante
    if c2 in ['s', 'z', 'ṣ', 'š']:
        return ClusterType.C_SIBILANT
    
    # Default: heterogéneo
    return ClusterType.HETEROGENEOUS


# ============================================================================
# INFORMACIÓN ADICIONAL
# ============================================================================

CLUSTER_NOTES = {
    'general': (
        "Acadio solo permite clusters de 2 consonantes en posición medial "
        "con frontera silábica entre ellas. "
        "Clusters al inicio o final de palabra prohibidos."
    ),
    
    'geminates': (
        "Geminadas siempre divididas por frontera silábica: "
        "C₁VC₁-C₁V no C₁V-C₁C₁V. "
        "Ejemplo: ipparras → ip.par.ras"
    ),
    
    'nasals': (
        "n asimila regresivamente a consonante siguiente (Iter 3). "
        "Resultado: geminada, no cluster estable. "
        "Ejemplo: in-paras → ipparas (pp no np)"
    ),
    
    'liquids': (
        "Líquidas (r, l) + consonante pueden disparar epéntesis vocálica. "
        "Típicamente vocal i o e insertada. "
        "Ejemplo: kabrū → kāberu, šuqlum → šuqulum"
    ),
    
    'h_clusters': (
        "h + consonante puede disolverse con epéntesis (i o u). "
        "Común en formas verbales. "
        "Puede ser ortográfico no fonológico en algunos casos."
    ),
    
    'triple_clusters': (
        "Clusters triples NUNCA permitidos. "
        "Si morfología los crea → epéntesis obligatoria. "
        "Ejemplo: estado constructo šiprum + -šu → šiparšu (NO **šiprušu)"
    ),
}

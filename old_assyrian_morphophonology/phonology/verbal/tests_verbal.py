"""
Tests para el sistema de stems verbales del Old Assyrian.

ITERACIÓN 8 - Tests de stems verbales derivados.

Verifica:
- Creación de raíces verbales
- Formación de todos los stems
- Propiedades y características
- Ejemplos del libro

Basado en Kouwenberg (2017) Capítulo 17.

Autor: Claude
Fecha: 2026-02-10
"""

import sys
from pathlib import Path

# Agregar directorio raíz al path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from phonology.verbal import *
from phonology.verbal.stem import create_root
from phonology.verbal.g_stem import *
from phonology.verbal.d_stem import *
from phonology.verbal.sh_stem import *
from phonology.verbal.n_stem import *


# ============================================================================
# TESTS DE RAÍCES VERBALES
# ============================================================================

def test_verbal_root_creation():
    """Test creación de raíces verbales."""
    print("\n" + "="*70)
    print("TEST 1: CREACIÓN DE RAÍCES VERBALES")
    print("="*70)
    
    # √PRS (parāsum a/u 'decidir')
    prs = create_root('p', 'r', 's', VowelClass.A_U, 'decidir')
    print(f"\n1. {prs}")
    print(f"   Patrón: {prs.pattern}")
    print(f"   Clase: {prs.vowel_class}")
    print(f"   Vocal Pres: {prs.vowel_class.present_vowel}")
    print(f"   Vocal Pret: {prs.vowel_class.preterite_vowel}")
    assert prs.pattern == 'PRS'
    assert prs.vowel_class == VowelClass.A_U
    
    # √ŠʾL (šaʾālum a/a 'preguntar')
    shal = create_root('š', 'ʾ', 'l', VowelClass.A_A, 'preguntar')
    print(f"\n2. {shal}")
    print(f"   Patrón: {shal.pattern}")
    print(f"   Clase: {shal.vowel_class}")
    
    # √MLʾ (malāʾum a/u 'ser lleno')
    mla = create_root('m', 'l', 'ʾ', VowelClass.A_U, 'ser lleno')
    print(f"\n3. {mla}")
    print(f"   Gloss: {mla.gloss}")
    
    print("\n✓ Raíces verbales creadas correctamente")


# ============================================================================
# TESTS DE G-STEM Y DERIVADOS
# ============================================================================

def test_g_stem():
    """Test G-stem (base)."""
    print("\n" + "="*70)
    print("TEST 2: G-STEM (BASE)")
    print("="*70)
    
    prs = create_root('p', 'r', 's', VowelClass.A_U, 'decidir')
    g_stem = G_Stem(root=prs)
    
    print(f"\n1. G-stem de {prs}")
    print(f"   Tipo: {g_stem.stem_type}")
    print(f"   Función: {g_stem.semantic_function}")
    print(f"   Voz: {g_stem.voice}")
    print(f"   Patrón: {g_stem.pattern_template}")
    print(f"   Vocal Pres: {g_stem.present_vowel}")
    print(f"   Vocal Pret: {g_stem.preterite_vowel}")
    print(f"   Distingue clases: {g_stem.distinguishes_vowel_classes()}")
    print(f"   Permite perfecto: {g_stem.allows_perfect()}")
    
    assert g_stem.stem_type == StemType.G
    assert g_stem.semantic_function == SemanticFunction.BASE
    assert g_stem.voice == VoiceType.ACTIVE
    assert g_stem.distinguishes_vowel_classes() == True
    assert g_stem.allows_perfect() == True
    
    print("\n✓ G-stem funciona correctamente")


def test_gt_stem():
    """Test Gt-stem (reciprocal/reflexivo)."""
    print("\n" + "="*70)
    print("TEST 3: GT-STEM (RECIPROCAL/REFLEXIVO)")
    print("="*70)
    
    # Ejemplo reciprocal: šaʾālum Gt 'deliberar'
    shal = create_root('š', 'ʾ', 'l', VowelClass.A_A, 'preguntar')
    gt_recip = form_gt_stem(
        shal,
        SemanticFunction.RECIPROCAL,
        'deliberar, tomar consejo'
    )
    
    print(f"\n1. Gt reciprocal de {shal}")
    print(f"   Tipo: {gt_recip.stem_type}")
    print(f"   Función: {gt_recip.semantic_function}")
    print(f"   Voz: {gt_recip.voice}")
    print(f"   Significado: {gt_recip.meaning}")
    print(f"   Patrón: {gt_recip.pattern_template}")
    print(f"   Tiene infijo -t-: {gt_recip.has_t_infix}")
    print(f"   Permite perfecto: {gt_recip.allows_perfect()}")
    
    # Ejemplo reflexivo: pašāšum Gt 'ungirse'
    psh = create_root('p', 'š', 'š', VowelClass.A_U, 'ungir')
    gt_refl = form_gt_stem(
        psh,
        SemanticFunction.REFLEXIVE,
        'ungirse a sí mismo'
    )
    
    print(f"\n2. Gt reflexivo de {psh}")
    print(f"   Función: {gt_refl.semantic_function}")
    print(f"   Voz: {gt_refl.voice}")
    print(f"   Significado: {gt_refl.meaning}")
    
    assert gt_recip.stem_type == StemType.GT
    assert gt_recip.has_t_infix == True
    assert gt_recip.allows_perfect() == False  # No doble -t-
    assert gt_refl.semantic_function == SemanticFunction.REFLEXIVE
    
    print("\n✓ Gt-stem funciona correctamente")


def test_gtn_stem():
    """Test Gtn-stem (pluraccional)."""
    print("\n" + "="*70)
    print("TEST 4: GTN-STEM (PLURACCIONAL)")
    print("="*70)
    
    # šamāʾum Gtn 'leer cuidadosamente'
    shm = create_root('š', 'm', 'ʾ', VowelClass.A_A, 'oír')
    gtn = form_gtn_stem(shm, 'leer cuidadosamente/repetidamente')
    
    print(f"\n1. Gtn de {shm}")
    print(f"   Tipo: {gtn.stem_type}")
    print(f"   Función: {gtn.semantic_function}")
    print(f"   Significado: {gtn.meaning}")
    print(f"   Es pluraccional: {gtn.is_pluractional}")
    print(f"   Tiene -tan-: {gtn.has_tan_infix}")
    print(f"   Geminación R₂: {gtn.has_r2_gemination}")
    
    assert gtn.stem_type == StemType.GTN
    assert gtn.is_pluractional == True
    assert gtn.semantic_function == SemanticFunction.PLURACTIONAL
    
    print("\n✓ Gtn-stem funciona correctamente")


# ============================================================================
# TESTS DE D-STEM Y DERIVADOS
# ============================================================================

def test_d_stem():
    """Test D-stem (factitivo/intensivo)."""
    print("\n" + "="*70)
    print("TEST 5: D-STEM (FACTITIVO/INTENSIVO)")
    print("="*70)
    
    # Factitivo: malāʾum D 'llenar' (de G 'ser lleno')
    mla = create_root('m', 'l', 'ʾ', VowelClass.A_U, 'ser lleno')
    d_fact = form_d_stem(
        mla,
        D_Function.FACTITIVE,
        SemanticFunction.FACTITIVE,
        'llenar'
    )
    
    print(f"\n1. D factitivo de {mla}")
    print(f"   Tipo: {d_fact.stem_type}")
    print(f"   Función D: {d_fact.d_function}")
    print(f"   Función semántica: {d_fact.semantic_function}")
    print(f"   Significado: {d_fact.meaning}")
    print(f"   Patrón: {d_fact.pattern_template}")
    print(f"   Geminación R₂: {d_fact.has_r2_gemination}")
    print(f"   Distingue clases: {d_fact.distinguishes_vowel_classes()}")
    print(f"   Es factitivo: {d_fact.is_factitive}")
    
    assert d_fact.stem_type == StemType.D
    assert d_fact.has_r2_gemination == True
    assert d_fact.distinguishes_vowel_classes() == False
    assert d_fact.is_factitive == True
    
    print("\n✓ D-stem funciona correctamente")


def test_dt_stem():
    """Test Dt-stem (detransitivo)."""
    print("\n" + "="*70)
    print("TEST 6: DT-STEM (DETRANSITIVO)")
    print("="*70)
    
    # kaʾulum Dt 'ser sostenido'
    kul = create_root('k', 'ʾ', 'l', VowelClass.U_U, 'sostener')
    dt = form_dt_stem(
        kul,
        SemanticFunction.MEDIOPASSIVE,
        VoiceType.PASSIVE,
        'ser sostenido'
    )
    
    print(f"\n1. Dt de {kul}")
    print(f"   Tipo: {dt.stem_type}")
    print(f"   Función: {dt.semantic_function}")
    print(f"   Voz: {dt.voice}")
    print(f"   Significado: {dt.meaning}")
    print(f"   Tiene infijo -t-: {dt.has_t_infix}")
    print(f"   Permite perfecto: {dt.allows_perfect()}")
    
    assert dt.stem_type == StemType.DT
    assert dt.has_t_infix == True
    assert dt.allows_perfect() == False
    
    print("\n✓ Dt-stem funciona correctamente")


# ============================================================================
# TESTS DE Š-STEM Y DERIVADOS
# ============================================================================

def test_sh_stem():
    """Test Š-stem (causativo)."""
    print("\n" + "="*70)
    print("TEST 7: Š-STEM (CAUSATIVO)")
    print("="*70)
    
    # waṣāʾum Š 'sacar' (causativo de 'salir')
    wsa = create_root('w', 'ṣ', 'ʾ', VowelClass.A_U, 'salir')
    sh_caus = form_sh_stem(
        wsa,
        Sh_Function.CAUSATIVE_MOTION,
        SemanticFunction.CAUSATIVE_SH,
        'sacar, hacer salir'
    )
    
    print(f"\n1. Š causativo de {wsa}")
    print(f"   Tipo: {sh_caus.stem_type}")
    print(f"   Función Š: {sh_caus.sh_function}")
    print(f"   Función semántica: {sh_caus.semantic_function}")
    print(f"   Voz: {sh_caus.voice}")
    print(f"   Significado: {sh_caus.meaning}")
    print(f"   Patrón: {sh_caus.pattern_template}")
    print(f"   Es causativo de movimiento: {sh_caus.is_causative_of_motion}")
    
    # muātum Š 'matar' (causativo de 'morir')
    mwt = create_root('m', 'w', 't', VowelClass.U_U, 'morir')
    sh_proc = form_sh_stem(
        mwt,
        Sh_Function.CAUSATIVE_PROCESS,
        SemanticFunction.CAUSATIVE_SH,
        'matar'
    )
    
    print(f"\n2. Š causativo de proceso de {mwt}")
    print(f"   Función Š: {sh_proc.sh_function}")
    print(f"   Es causativo de proceso: {sh_proc.is_causative_of_process}")
    
    assert sh_caus.stem_type == StemType.SH
    assert sh_caus.voice == VoiceType.CAUSATIVE
    assert sh_caus.is_causative_of_motion == True
    
    print("\n✓ Š-stem funciona correctamente")


def test_sht2_stem():
    """Test Št₂-stem (léxico)."""
    print("\n" + "="*70)
    print("TEST 8: ŠT₂-STEM (LÉXICO)")
    print("="*70)
    
    # magārum Št₂ 'hacer estar de acuerdo mutuamente'
    mgr = create_root('m', 'g', 'r', VowelClass.A_U, 'estar de acuerdo')
    sht2 = form_sht2_stem(
        mgr,
        'hacer que estén de acuerdo mutuamente'
    )
    
    print(f"\n1. Št₂ de {mgr}")
    print(f"   Tipo: {sht2.stem_type}")
    print(f"   Función: {sht2.semantic_function}")
    print(f"   Significado: {sht2.meaning}")
    print(f"   Patrón: {sht2.pattern_template}")
    print(f"   Productividad: {sht2.productivity}")
    
    assert sht2.stem_type == StemType.SHT2
    assert sht2.semantic_function == SemanticFunction.LEXICAL_SHT
    
    print("\n✓ Št₂-stem funciona correctamente")


# ============================================================================
# TESTS DE N-STEM Y DERIVADOS
# ============================================================================

def test_n_stem():
    """Test N-stem (medio/pasivo)."""
    print("\n" + "="*70)
    print("TEST 9: N-STEM (MEDIO/PASIVO)")
    print("="*70)
    
    # laqāʾum N 'ser tomado' (pasivo)
    lqa = create_root('l', 'q', 'ʾ', VowelClass.A_I, 'tomar')
    n_pass = form_n_stem(
        lqa,
        N_Function.MEDIOPASSIVE,
        SemanticFunction.PASSIVE_N,
        VoiceType.PASSIVE,
        'ser tomado'
    )
    
    print(f"\n1. N pasivo de {lqa}")
    print(f"   Tipo: {n_pass.stem_type}")
    print(f"   Función N: {n_pass.n_function}")
    print(f"   Función semántica: {n_pass.semantic_function}")
    print(f"   Voz: {n_pass.voice}")
    print(f"   Significado: {n_pass.meaning}")
    print(f"   Patrón: {n_pass.pattern_template}")
    print(f"   Geminación R₁: {n_pass.has_r1_gemination}")
    print(f"   Distingue clases: {n_pass.distinguishes_vowel_classes()}")
    print(f"   Es pasivo: {n_pass.is_passive}")
    
    # magārum N 'llegar a acuerdo' (reciprocal)
    mgr = create_root('m', 'g', 'r', VowelClass.A_U, 'estar de acuerdo')
    n_recip = form_n_stem(
        mgr,
        N_Function.RECIPROCAL,
        SemanticFunction.RECIPROCAL,
        VoiceType.RECIPROCAL,
        'llegar a acuerdo mutuamente'
    )
    
    print(f"\n2. N reciprocal de {mgr}")
    print(f"   Función N: {n_recip.n_function}")
    print(f"   Voz: {n_recip.voice}")
    print(f"   Es reciprocal: {n_recip.is_reciprocal}")
    
    # Proceso de asimilación nasal
    print(f"\n3. Proceso de asimilación nasal:")
    print(f"   {nasal_assimilation_pattern('p')}")
    print(f"   {nasal_assimilation_pattern('l')}")
    
    # Proceso de asimilación vocálica
    print(f"\n4. Asimilación vocálica en pretérito:")
    print(f"   {vowel_assimilation_pattern()}")
    
    assert n_pass.stem_type == StemType.N
    assert n_pass.has_r1_gemination == True
    assert n_pass.distinguishes_vowel_classes() == True
    assert n_pass.is_passive == True
    assert n_recip.is_reciprocal == True
    
    print("\n✓ N-stem funciona correctamente")


def test_ntn_stem():
    """Test Ntn-stem (pluraccional)."""
    print("\n" + "="*70)
    print("TEST 10: NTN-STEM (PLURACCIONAL)")
    print("="*70)
    
    # ṣabātum Ntn 'ser agarrado constantemente'
    sbt = create_root('ṣ', 'b', 't', VowelClass.A_A, 'agarrar')
    ntn = form_ntn_stem(
        sbt,
        VoiceType.PASSIVE,
        'ser agarrado constantemente'
    )
    
    print(f"\n1. Ntn de {sbt}")
    print(f"   Tipo: {ntn.stem_type}")
    print(f"   Función: {ntn.semantic_function}")
    print(f"   Voz: {ntn.voice}")
    print(f"   Significado: {ntn.meaning}")
    print(f"   Es pluraccional: {ntn.is_pluractional}")
    
    assert ntn.stem_type == StemType.NTN
    assert ntn.is_pluractional == True
    
    print("\n✓ Ntn-stem funciona correctamente")


# ============================================================================
# TESTS DE DERIVACIÓN Y JERARQUÍA
# ============================================================================

def test_stem_derivation():
    """Test derivación y jerarquía de stems."""
    print("\n" + "="*70)
    print("TEST 11: DERIVACIÓN Y JERARQUÍA")
    print("="*70)
    
    prs = create_root('p', 'r', 's', VowelClass.A_U, 'decidir')
    
    # Crear diferentes stems
    g = G_Stem(root=prs)
    gt = form_gt_stem(prs)
    gtn = form_gtn_stem(prs)
    d = form_d_stem(prs)
    dt = form_dt_stem(prs)
    
    print("\n1. Verificando stems base:")
    print(f"   Gt deriva de: {gt.base_stem_type}")
    print(f"   Gtn deriva de: {gtn.base_stem_type}")
    print(f"   Dt deriva de: {dt.base_stem_type}")
    
    print("\n2. Verificando funciones is_derived_from:")
    print(f"   Gt deriva de G: {is_derived_from(gt, StemType.G)}")
    print(f"   Gtn deriva de G: {is_derived_from(gtn, StemType.G)}")
    print(f"   Dt deriva de D: {is_derived_from(dt, StemType.D)}")
    print(f"   Dt deriva de G: {is_derived_from(dt, StemType.G)}")
    
    assert gt.base_stem_type == StemType.G
    assert gtn.base_stem_type == StemType.GT
    assert dt.base_stem_type == StemType.D
    assert is_derived_from(gt, StemType.G) == True
    assert is_derived_from(dt, StemType.D) == True
    assert is_derived_from(dt, StemType.G) == False
    
    print("\n✓ Derivación funciona correctamente")


# ============================================================================
# TEST COMPREHENSIVO
# ============================================================================

def test_comprehensive():
    """Test comprehensivo de todo el sistema."""
    print("\n" + "="*70)
    print("TEST 12: COMPREHENSIVO - TODOS LOS STEMS")
    print("="*70)
    
    # Crear una raíz y todos sus stems
    prs = create_root('p', 'r', 's', VowelClass.A_U, 'decidir')
    
    stems = {
        'G': G_Stem(root=prs),
        'Gt': form_gt_stem(prs),
        'Gtn': form_gtn_stem(prs),
        'D': form_d_stem(prs),
        'Dt': form_dt_stem(prs),
        'Dtn': form_dtn_stem(prs),
        'Š': form_sh_stem(prs),
        'Št₂': form_sht2_stem(prs),
        'Štn': form_shtn_stem(prs),
        'N': form_n_stem(prs),
        'Ntn': form_ntn_stem(prs)
    }
    
    print(f"\n√{prs.pattern} - Todos los stems posibles:")
    print("─" * 70)
    
    for name, stem in stems.items():
        print(f"\n{name:4} │ {stem.stem_type:12} │ {stem.pattern_template:15} │ {stem.semantic_function}")
        print(f"     │ Marcadores: {', '.join(str(m) for m in stem.markers)}")
        print(f"     │ Productividad: {stem.productivity}")
        print(f"     │ Permite perfecto: {stem.allows_perfect()}")
        print(f"     │ Distingue clases: {stem.distinguishes_vowel_classes()}")
    
    print("\n✓ Sistema completo funciona correctamente")


# ============================================================================
# RUNNER PRINCIPAL
# ============================================================================

def run_all_tests():
    """Ejecuta todos los tests."""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + " ITERACIÓN 8 - TESTS SISTEMA VERBAL ".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    tests = [
        test_verbal_root_creation,
        test_g_stem,
        test_gt_stem,
        test_gtn_stem,
        test_d_stem,
        test_dt_stem,
        test_sh_stem,
        test_sht2_stem,
        test_n_stem,
        test_ntn_stem,
        test_stem_derivation,
        test_comprehensive
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"\n✗ {test.__name__} FALLÓ: {e}")
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE TESTS")
    print("="*70)
    print(f"Total: {len(tests)}")
    print(f"✓ Pasados: {passed}")
    print(f"✗ Fallados: {failed}")
    
    if failed == 0:
        print("\n" + "🎉 " * 10)
        print("¡TODOS LOS TESTS PASARON!")
        print("🎉 " * 10)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

"""
Tests para formación fonológica de stems verbales.

Author: Claude
Date: 2026-02-11
"""

import sys
sys.path.insert(0, '/home/claude/old_assyrian_morphophonology')

from phonology.verbal.phonological_formation import *
from phonology.verbal.enums import VerbFormType
from phonology.phoneme import Consonant, Vowel
from phonology.inventory import get_vowel, get_consonant


def test_prefix_generation():
    """Test generación de prefijos."""
    print("\n" + "="*70)
    print("TEST INFRAESTRUCTURA 1: Generación de Prefijos")
    print("="*70)
    
    # i/a-prefixes
    prefix_3sm = get_prefix(3, 'sg', 'm', False)
    print(f"3sm i-prefix: {[str(p) for p in prefix_3sm]}")
    assert len(prefix_3sm) == 1
    assert str(prefix_3sm[0]) == 'i'
    
    prefix_2sm = get_prefix(2, 'sg', 'm', False)
    print(f"2sm ta-prefix: {[str(p) for p in prefix_2sm]}")
    assert len(prefix_2sm) == 2
    assert str(prefix_2sm[0]) == 't'
    assert str(prefix_2sm[1]) == 'a'
    
    # u-prefixes
    prefix_3sm_u = get_prefix(3, 'sg', 'm', True)
    print(f"3sm u-prefix: {[str(p) for p in prefix_3sm_u]}")
    assert len(prefix_3sm_u) == 1
    assert str(prefix_3sm_u[0]) == 'u'
    
    print("✓ Prefijos generados correctamente")
    return True


def test_suffix_generation():
    """Test generación de sufijos."""
    print("\n" + "="*70)
    print("TEST INFRAESTRUCTURA 2: Generación de Sufijos")
    print("="*70)
    
    # Singular masculine: no suffix
    suffix_3sm = get_suffix(3, 'sg', 'm')
    print(f"3sm suffix: {[str(p) for p in suffix_3sm]}")
    assert len(suffix_3sm) == 0
    
    # Singular feminine: -ī
    suffix_2sf = get_suffix(2, 'sg', 'f')
    print(f"2sf suffix: {[str(p) for p in suffix_2sf]}")
    assert len(suffix_2sf) == 1
    assert str(suffix_2sf[0]) == 'ī'
    
    # Dual: -ā
    suffix_3du = get_suffix(3, 'du', 'm')
    print(f"3du suffix: {[str(p) for p in suffix_3du]}")
    assert len(suffix_3du) == 1
    assert str(suffix_3du[0]) == 'ā'
    
    # Plural masculine: -ū
    suffix_3pm = get_suffix(3, 'pl', 'm')
    print(f"3pm suffix: {[str(p) for p in suffix_3pm]}")
    assert len(suffix_3pm) == 1
    assert str(suffix_3pm[0]) == 'ū'
    
    print("✓ Sufijos generados correctamente")
    return True


def test_gemination():
    """Test geminación de consonantes."""
    print("\n" + "="*70)
    print("TEST INFRAESTRUCTURA 3: Geminación")
    print("="*70)
    
    # Crear secuencia: i-p-a-r-a-s
    phonemes = [
        get_vowel('i'),
        get_consonant('p'),
        get_vowel('a'),
        get_consonant('r'),  # Index 3 - to be geminated
        get_vowel('a'),
        get_consonant('s')
    ]
    
    print(f"Antes: {phonemes_to_string(phonemes)}")
    
    # Geminar R₂ (index 3)
    geminated = geminate_consonant(phonemes, 3)
    
    print(f"Después: {phonemes_to_string(geminated)}")
    print(f"Longitud: {len(phonemes)} → {len(geminated)}")
    
    assert len(geminated) == 7  # One more
    assert str(geminated[3]) == 'r'
    assert str(geminated[4]) == 'r'
    
    print("✓ Geminación funciona correctamente")
    return True


def test_t_infix_insertion():
    """Test inserción de infijo -t-."""
    print("\n" + "="*70)
    print("TEST INFRAESTRUCTURA 4: Inserción de -t-")
    print("="*70)
    
    # Root consonants: p-r-s
    root = [
        get_consonant('p'),
        get_consonant('r'),
        get_consonant('s')
    ]
    
    print(f"Root: {[str(c) for c in root]}")
    
    # Insert -t- after R₁
    with_t = insert_t_infix(root, 1)
    
    print(f"Con -t-: {[str(c) for c in with_t]}")
    
    assert len(with_t) == 4
    assert str(with_t[0]) == 'p'
    assert str(with_t[1]) == 't'
    assert str(with_t[2]) == 'r'
    assert str(with_t[3]) == 's'
    
    print("✓ Infijo -t- insertado correctamente")
    return True


def test_vowel_assimilation():
    """Test asimilación vocálica."""
    print("\n" + "="*70)
    print("TEST INFRAESTRUCTURA 5: Asimilación Vocálica")
    print("="*70)
    
    # Secuencia: i-p-a-r-r-a-s (iparras)
    phonemes = [
        get_vowel('i'),
        get_consonant('p'),
        get_vowel('a'),
        get_consonant('r'),
        get_consonant('r'),
        get_vowel('a'),  # This 'a' should assimilate
        get_consonant('s')
    ]
    
    print(f"Antes: {phonemes_to_string(phonemes)}")
    
    # Assimilate to 'u' (as in iparras + ū → iparrusū)
    assimilated = apply_vowel_assimilation(phonemes, 'u')
    
    print(f"Después (ending 'u'): {phonemes_to_string(assimilated)}")
    
    assert str(assimilated[5]) == 'u'  # 'a' → 'u'
    
    print("✓ Asimilación vocálica funciona correctamente")
    return True


def run_all_infrastructure_tests():
    """Ejecuta todos los tests de infraestructura."""
    print("\n" + "="*70)
    print("TESTS DE INFRAESTRUCTURA - FASE 1")
    print("="*70)
    
    tests = [
        test_prefix_generation,
        test_suffix_generation,
        test_gemination,
        test_t_infix_insertion,
        test_vowel_assimilation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"\n✗ {test.__name__} FALLÓ: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*70)
    print("RESUMEN DE TESTS DE INFRAESTRUCTURA")
    print("="*70)
    print(f"Total: {len(tests)}")
    print(f"✓ Pasados: {passed}")
    print(f"✗ Fallados: {failed}")
    
    if failed == 0:
        print("\n🎉 ¡TODOS LOS TESTS DE INFRAESTRUCTURA PASARON!")
    
    return failed == 0


def test_g_stem_formation():
    """Test formación de G-stem."""
    print("\n" + "="*70)
    print("TEST FASE 2.1: Formación G-stem")
    print("="*70)
    
    from phonology.verbal.g_stem import G_Stem
    from phonology.verbal.stem import create_root
    from phonology.verbal.enums import VowelClass
    
    # √PRS (parāsum a/u 'separar')
    root = create_root('p', 'r', 's', VowelClass.A_U, 'separar')
    g = G_Stem(root=root)
    
    # Test Presente
    pres = g.form_present(3, 'sg', 'm')
    pres_str = phonemes_to_string(pres)
    print(f"Presente 3sm: {pres_str}")
    assert pres_str == 'iparras', f"Expected 'iparras', got '{pres_str}'"
    
    # Test Pretérito
    pret = g.form_preterite(3, 'sg', 'm')
    pret_str = phonemes_to_string(pret)
    print(f"Pretérito 3sm: {pret_str}")
    assert pret_str == 'iprus', f"Expected 'iprus', got '{pret_str}'"
    
    # Test Perfect
    perf = g.form_perfect(3, 'sg', 'm')
    perf_str = phonemes_to_string(perf)
    print(f"Perfect 3sm: {perf_str}")
    assert perf_str == 'iptaras', f"Expected 'iptaras', got '{perf_str}'"
    
    # Test Imperativo
    imp = g.form_imperative('sg', 'm')
    imp_str = phonemes_to_string(imp)
    print(f"Imperativo sm: {imp_str}")
    assert imp_str == 'purus', f"Expected 'purus', got '{imp_str}'"
    
    print("✓ G-stem formación correcta")
    return True


def test_gt_stem_formation():
    """Test formación de Gt-stem."""
    print("\n" + "="*70)
    print("TEST FASE 2.2: Formación Gt-stem")
    print("="*70)
    
    from phonology.verbal.g_stem import Gt_Stem, form_gt_stem
    from phonology.verbal.stem import create_root
    from phonology.verbal.enums import VowelClass, SemanticFunction
    
    # √PRS Gt 'separarse mutuamente'
    root = create_root('p', 'r', 's', VowelClass.A_U, 'separar')
    gt = form_gt_stem(root, SemanticFunction.RECIPROCAL, 'separarse')
    
    # Test Presente
    pres = gt.form_present(3, 'sg', 'm')
    pres_str = phonemes_to_string(pres)
    print(f"Presente 3sm: {pres_str}")
    assert pres_str == 'iptarras', f"Expected 'iptarras', got '{pres_str}'"
    
    # Test Pretérito
    pret = gt.form_preterite(3, 'sg', 'm')
    pret_str = phonemes_to_string(pret)
    print(f"Pretérito 3sm: {pret_str}")
    assert pret_str == 'iptris', f"Expected 'iptris', got '{pret_str}'"
    
    # Test Perfect (should be None)
    perf = gt.form_perfect(3, 'sg', 'm')
    print(f"Perfect 3sm: {perf}")
    assert perf is None, "Gt should not have perfect"
    
    print("✓ Gt-stem formación correcta")
    return True


def test_vowel_classes():
    """Test todas las clases vocálicas del G-stem."""
    print("\n" + "="*70)
    print("TEST FASE 2.3: Clases Vocálicas")
    print("="*70)
    
    from phonology.verbal.g_stem import G_Stem
    from phonology.verbal.stem import create_root
    from phonology.verbal.enums import VowelClass
    
    test_cases = [
        # (root_letters, vowel_class, expected_pres, expected_pret)
        ('p-q-d', VowelClass.I_I, 'ipaqqid', 'ipqid'),
        ('m-q-t', VowelClass.U_U, 'imaqqut', 'imqut'),
        ('ṣ-b-t', VowelClass.A_A, 'iṣabbat', 'iṣbat'),
        ('p-r-s', VowelClass.A_U, 'iparras', 'iprus'),
    ]
    
    for letters, vclass, exp_pres, exp_pret in test_cases:
        r1, r2, r3 = letters.split('-')
        root = create_root(r1, r2, r3, vclass, 'test')
        g = G_Stem(root=root)
        
        pres = phonemes_to_string(g.form_present(3, 'sg', 'm'))
        pret = phonemes_to_string(g.form_preterite(3, 'sg', 'm'))
        
        print(f"  {vclass.name}: pres={pres}, pret={pret}")
        assert pres == exp_pres, f"{vclass.name} presente incorrecto"
        assert pret == exp_pret, f"{vclass.name} pretérito incorrecto"
    
    print("✓ Todas las clases vocálicas correctas")
    return True


def test_n_stem_formation():
    """Test formación de N-stem con asimilación nasal."""
    print("\n" + "="*70)
    print("TEST FASE 3: Formación N-stem")
    print("="*70)
    
    from phonology.verbal.n_stem import N_Stem, form_n_stem
    from phonology.verbal.stem import create_root
    from phonology.verbal.enums import VowelClass
    
    # √PRS N 'ser separado'
    root = create_root('p', 'r', 's', VowelClass.A_U, 'separar')
    n = form_n_stem(root)
    
    # Test Presente
    pres = n.form_present(3, 'sg', 'm')
    pres_str = phonemes_to_string(pres)
    print(f"Presente 3sm: {pres_str}")
    assert pres_str == 'ipparas', f"Expected 'ipparas', got '{pres_str}'"
    assert pres[1] == pres[2], "R₁ should be geminated"
    
    # Test Pretérito (con asimilación especial a→e)
    pret = n.form_preterite(3, 'sg', 'm')
    pret_str = phonemes_to_string(pret)
    print(f"Pretérito 3sm: {pret_str}")
    assert pret_str == 'ipperis', f"Expected 'ipperis', got '{pret_str}'"
    
    # Test Perfect
    perf = n.form_perfect(3, 'sg', 'm')
    perf_str = phonemes_to_string(perf)
    print(f"Perfect 3sm: {perf_str}")
    assert perf_str == 'ittapras', f"Expected 'ittapras', got '{perf_str}'"
    
    print("✓ N-stem formación correcta (asimilación nasal validada)")
    return True


def test_d_stem_formation():
    """Test formación de D-stem con prefijo u- y vocales fijas."""
    print("\n" + "="*70)
    print("TEST FASE 4: Formación D-stem")
    print("="*70)
    
    from phonology.verbal.d_stem import D_Stem, form_d_stem
    from phonology.verbal.stem import create_root
    from phonology.verbal.enums import VowelClass
    
    # √PRS D 'hacer separar'
    root = create_root('p', 'r', 's', VowelClass.A_U, 'separar')
    d = form_d_stem(root)
    
    # Test Presente
    pres = d.form_present(3, 'sg', 'm')
    pres_str = phonemes_to_string(pres)
    print(f"Presente 3sm: {pres_str}")
    assert pres_str == 'uparras', f"Expected 'uparras', got '{pres_str}'"
    assert str(pres[0]) == 'u', "Should have u-prefix"
    assert pres[3] == pres[4], "R₂ should be geminated"
    
    # Test Pretérito
    pret = d.form_preterite(3, 'sg', 'm')
    pret_str = phonemes_to_string(pret)
    print(f"Pretérito 3sm: {pret_str}")
    assert pret_str == 'uparris', f"Expected 'uparris', got '{pret_str}'"
    assert pret[3] == pret[4], "R₂ should be geminated in preterite too"
    
    # Test Perfect
    perf = d.form_perfect(3, 'sg', 'm')
    perf_str = phonemes_to_string(perf)
    print(f"Perfect 3sm: {perf_str}")
    assert perf_str == 'uptarris', f"Expected 'uptarris', got '{perf_str}'"
    
    print("✓ D-stem formación correcta (u-prefix, R₂R₂, vocales fijas)")
    return True


def test_sh_stem_formation():
    """Test formación de Š-stem con doble prefijo u-š-."""
    print("\n" + "="*70)
    print("TEST FASE 5: Formación Š-stem")
    print("="*70)
    
    from phonology.verbal.sh_stem import Sh_Stem, form_sh_stem
    from phonology.verbal.stem import create_root
    from phonology.verbal.enums import VowelClass
    
    # √PRS Š 'hacer separar'
    root = create_root('p', 'r', 's', VowelClass.A_U, 'separar')
    sh = form_sh_stem(root)
    
    # Test Presente
    pres = sh.form_present(3, 'sg', 'm')
    pres_str = phonemes_to_string(pres)
    print(f"Presente 3sm: {pres_str}")
    assert pres_str == 'ušapras', f"Expected 'ušapras', got '{pres_str}'"
    assert str(pres[0]) == 'u', "Should have u-prefix"
    assert str(pres[1]) == 'š', "Should have š-prefix"
    
    # Test Pretérito
    pret = sh.form_preterite(3, 'sg', 'm')
    pret_str = phonemes_to_string(pret)
    print(f"Pretérito 3sm: {pret_str}")
    assert pret_str == 'ušapris', f"Expected 'ušapris', got '{pret_str}'"
    
    # Test Perfect (special št- pattern)
    perf = sh.form_perfect(3, 'sg', 'm')
    perf_str = phonemes_to_string(perf)
    print(f"Perfect 3sm: {perf_str}")
    assert perf_str == 'uštapris', f"Expected 'uštapris', got '{perf_str}'"
    assert str(perf[1]) == 'š' and str(perf[2]) == 't', "Perfect should have št-"
    
    # Test Imperativo
    imp = sh.form_imperative('sg', 'm')
    imp_str = phonemes_to_string(imp)
    print(f"Imperativo sm: {imp_str}")
    assert imp_str == 'šapris', f"Expected 'šapris', got '{imp_str}'"
    
    print("✓ Š-stem formación correcta (u-š-, perfect št-, NO gemina R₂)")
    return True


def test_complementary_stems():
    """Test de stems complementarios (Dt, Dtn, Štn) - 100% absoluto."""
    print("\n" + "="*70)
    print("TEST MINI-FASE 7: Stems Complementarios (100% ABSOLUTO)")
    print("="*70)
    
    from phonology.verbal.d_stem import Dt_Stem, Dtn_Stem
    from phonology.verbal.sh_stem import Shtn_Stem
    from phonology.verbal.stem import create_root
    from phonology.verbal.enums import VowelClass
    
    root = create_root('p', 'r', 's', VowelClass.A_U, 'separar')
    
    # Dt-stem (presente = pretérito)
    print("\n--- Dt-stem ---")
    dt = Dt_Stem(root=root)
    dt_pres = dt.form_present(3, 'sg', 'm')
    dt_pret = dt.form_preterite(3, 'sg', 'm')
    dt_pres_str = phonemes_to_string(dt_pres)
    dt_pret_str = phonemes_to_string(dt_pret)
    print(f"Dt presente:  {dt_pres_str}")
    print(f"Dt pretérito: {dt_pret_str}")
    assert dt_pres == dt_pret, "Dt presente debe = pretérito (característica única)"
    assert dt_pres_str == 'uptarris', f"Expected 'uptarris', got '{dt_pres_str}'"
    print("✓ Dt: Presente = Pretérito (validado)")
    
    # Dtn-stem (pluraccional de D)
    print("\n--- Dtn-stem ---")
    dtn = Dtn_Stem(root=root)
    dtn_pres = dtn.form_present(3, 'sg', 'm')
    dtn_pret = dtn.form_preterite(3, 'sg', 'm')
    dtn_pres_str = phonemes_to_string(dtn_pres)
    dtn_pret_str = phonemes_to_string(dtn_pret)
    print(f"Dtn presente:  {dtn_pres_str}")
    print(f"Dtn pretérito: {dtn_pret_str}")
    assert 'n' in dtn_pres_str, "Dtn presente debe tener -n-"
    assert 'n' not in dtn_pret_str, "Dtn pretérito NO debe tener -n-"
    assert dtn_pres_str == 'uptanarras', f"Expected 'uptanarras', got '{dtn_pres_str}'"
    assert dtn_pret_str == 'uptarras', f"Expected 'uptarras', got '{dtn_pret_str}'"
    print("✓ Dtn: -tan- en presente, solo -t- en pretérito (validado)")
    
    # Štn-stem (pluraccional de Š)
    print("\n--- Štn-stem ---")
    shtn = Shtn_Stem(root=root)
    shtn_pres = shtn.form_present(3, 'sg', 'm')
    shtn_pret = shtn.form_preterite(3, 'sg', 'm')
    shtn_pres_str = phonemes_to_string(shtn_pres)
    shtn_pret_str = phonemes_to_string(shtn_pret)
    print(f"Štn presente:  {shtn_pres_str}")
    print(f"Štn pretérito: {shtn_pret_str}")
    assert shtn_pres_str.startswith('ušt'), "Štn debe empezar con ušt"
    assert 'n' in shtn_pres_str, "Štn presente debe tener -n-"
    assert 'n' not in shtn_pret_str, "Štn pretérito NO debe tener -n-"
    assert shtn_pres_str == 'uštanapras', f"Expected 'uštanapras', got '{shtn_pres_str}'"
    assert shtn_pret_str == 'uštapras', f"Expected 'uštapras', got '{shtn_pret_str}'"
    print("✓ Štn: u-š-tan- en presente, u-š-t- en pretérito (validado)")
    
    print("\n✓ TODOS los stems complementarios validados")
    print("🎉 ¡100% ABSOLUTO ALCANZADO! 12/12 stems implementados")
    return True


def run_all_tests():
    """Ejecuta todos los tests (infraestructura + formación)."""
    print("\n" + "="*70)
    print("TESTS COMPLETOS - FASES 1 Y 2")
    print("="*70)
    
    tests = [
        # Fase 1
        test_prefix_generation,
        test_suffix_generation,
        test_gemination,
        test_t_infix_insertion,
        test_vowel_assimilation,
        # Fase 2
        test_g_stem_formation,
        test_gt_stem_formation,
        test_vowel_classes,
        # Fase 3
        test_n_stem_formation,
        # Fase 4
        test_d_stem_formation,
        # Fase 5
        test_sh_stem_formation,
        # Mini-Fase 7 (100% absoluto)
        test_complementary_stems,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"\n✗ {test.__name__} FALLÓ: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*70)
    print("RESUMEN FINAL")
    print("="*70)
    print(f"Total: {len(tests)}")
    print(f"✓ Pasados: {passed}")
    print(f"✗ Fallados: {failed}")
    
    if failed == 0:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

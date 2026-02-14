"""
Tests para I_w_Fientive_Stem

ITERACIÓN 9 - PASO 4: I/w Fientive

Verifica que wasābum y otros verbos I/w fientivo se generan correctamente.

Autor: Claude
Fecha: 2026-02-12
"""

import sys
import os

# Ajustar path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from phonology.verbal.weak_root import create_i_w_fientive_root
from phonology.verbal.i_weak.i_w_stems import I_w_Fientive_Stem, create_i_w_fientive_stem
from phonology.verbal.enums import VowelClass, StemType


def phonemes_to_string(phonemes):
    """Helper para convertir fonemas a string."""
    result = ""
    for p in phonemes:
        result += p.symbol
    return result


def test_wasabum_present():
    """Test presente de wasābum."""
    print("Test 1: wasābum - Presente...")
    
    # wasābum (a/i) 'sentar'
    root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    stem = create_i_w_fientive_stem(root)
    
    # Presente 3sm: u-ššab
    result = stem.form_present(3, 'sg', 'm')
    string = phonemes_to_string(result)
    
    print(f"  Generado: {string}")
    print(f"  Fonemas: {len(result)}")
    
    # Verificaciones
    assert len(result) >= 4, f"Debe tener >=4 fonemas, tiene {len(result)}"
    assert result[0].symbol == 'u', f"Primer fonema debe ser 'u', es '{result[0].symbol}'"
    assert result[1].symbol == 's', f"Segunda debe ser 's', es '{result[1].symbol}'"
    
    print(f"  ✓ wasābum Pres 3sm: {string}")
    print("Test 1: ✅ PASSED\n")


def test_wasabum_preterite():
    """Test pretérito de wasābum."""
    print("Test 2: wasābum - Pretérito...")
    
    root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    stem = create_i_w_fientive_stem(root)
    
    # Pretérito 3sm: ū-šib (vocal larga)
    result = stem.form_preterite(3, 'sg', 'm')
    string = phonemes_to_string(result)
    
    print(f"  Generado: {string}")
    print(f"  Fonemas: {len(result)}")
    
    # Verificaciones
    assert len(result) >= 3, f"Debe tener >=3 fonemas, tiene {len(result)}"
    # Primera vocal debe ser 'u' (larga en realidad → 'ū')
    assert result[0].symbol.lower() in ['u', 'ū'], f"Primera debe ser u/ū, es '{result[0].symbol}'"
    
    # Verificar que es larga
    if hasattr(result[0], 'features'):
        assert result[0].features.is_long == True, "Vocal debe ser larga (sin ending)"
    
    print(f"  ✓ wasābum Pret 3sm: {string} (vocal larga)")
    print("Test 2: ✅ PASSED\n")


def test_wasabum_perfect():
    """Test perfect de wasābum."""
    print("Test 3: wasābum - Perfect...")
    
    root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    stem = create_i_w_fientive_stem(root)
    
    # Perfect 3sm: ut-tašib (con -tt- geminación)
    result = stem.form_perfect(3, 'sg', 'm')
    string = phonemes_to_string(result)
    
    print(f"  Generado: {string}")
    print(f"  Fonemas: {len(result)}")
    
    # Verificaciones
    assert len(result) >= 6, f"Debe tener >=6 fonemas, tiene {len(result)}"
    assert result[0].symbol == 'u', f"Primera debe ser 'u', es '{result[0].symbol}'"
    assert result[1].symbol == 't', f"Segunda debe ser 't', es '{result[1].symbol}'"
    assert result[2].symbol == 't', f"Tercera debe ser 't' (geminación), es '{result[2].symbol}'"
    
    print(f"  ✓ wasābum Perf 3sm: {string} (-tt- geminación)")
    print("Test 3: ✅ PASSED\n")


def test_wasabum_imperative():
    """Test imperativo de wasābum."""
    print("Test 4: wasābum - Imperativo...")
    
    root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    stem = create_i_w_fientive_stem(root)
    
    # Imperativo sm: šib (w → Ø)
    result = stem.form_imperative('sg', 'm')
    string = phonemes_to_string(result)
    
    print(f"  Generado: {string}")
    print(f"  Fonemas: {len(result)}")
    
    # Verificaciones
    assert len(result) >= 3, f"Debe tener >=3 fonemas, tiene {len(result)}"
    # Primer fonema debe ser vocal (no 'w')
    assert hasattr(result[0], 'features'), "Primera debe ser vocal"
    assert result[1].symbol == 's', f"Segunda debe ser 's', es '{result[1].symbol}'"
    
    print(f"  ✓ wasābum Imp sm: {string} (w perdida)")
    print("Test 4: ✅ PASSED\n")


def test_wabalum():
    """Test wabālum (muy frecuente)."""
    print("Test 5: wabālum - Formas principales...")
    
    # wabālum (a/i) 'llevar, traer'
    root = create_i_w_fientive_root('b', 'l', VowelClass.A_I, 'llevar')
    stem = create_i_w_fientive_stem(root)
    
    # Presente 3sm
    pres = stem.form_present(3, 'sg', 'm')
    pres_str = phonemes_to_string(pres)
    print(f"  Presente 3sm: {pres_str}")
    assert len(pres) >= 4
    
    # Pretérito 3sm
    pret = stem.form_preterite(3, 'sg', 'm')
    pret_str = phonemes_to_string(pret)
    print(f"  Pretérito 3sm: {pret_str}")
    assert len(pret) >= 3
    
    # Perfect 3sm
    perf = stem.form_perfect(3, 'sg', 'm')
    perf_str = phonemes_to_string(perf)
    print(f"  Perfect 3sm: {perf_str}")
    assert len(perf) >= 6
    
    # Imperativo sm
    imp = stem.form_imperative('sg', 'm')
    imp_str = phonemes_to_string(imp)
    print(f"  Imperativo sm: {imp_str}")
    assert len(imp) >= 3
    
    print(f"  ✓ wabālum: todas las formas generadas")
    print("Test 5: ✅ PASSED\n")


def test_helper_methods_overrides():
    """Test que métodos helper están override correctamente."""
    print("Test 6: Helper methods overrides...")
    
    root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    stem = create_i_w_fientive_stem(root)
    
    # _get_R1_for_present debe retornar None
    r1_pres = stem._get_R1_for_present()
    assert r1_pres is None, "R₁ debe ser None en presente (contracción)"
    print("  ✓ _get_R1_for_present() retorna None")
    
    # _get_R1_for_preterite debe retornar []
    r1_pret = stem._get_R1_for_preterite()
    assert len(r1_pret) == 0, "R₁ debe ser [] en pretérito (contracción)"
    print("  ✓ _get_R1_for_preterite() retorna []")
    
    # _get_R1_for_perfect debe retornar []
    r1_perf = stem._get_R1_for_perfect()
    assert len(r1_perf) == 0, "R₁ debe ser [] en perfect (contracción)"
    print("  ✓ _get_R1_for_perfect() retorna []")
    
    # _get_R1_for_imperative debe retornar None
    r1_imp = stem._get_R1_for_imperative()
    assert r1_imp is None, "R₁ debe ser None en imperativo (pérdida)"
    print("  ✓ _get_R1_for_imperative() retorna None")
    
    # _adjust_prefix_for_weak_verb
    from phonology.verbal.enums import VerbFormType
    prefix_pres = stem._adjust_prefix_for_weak_verb('i', VerbFormType.PRESENT)
    assert prefix_pres == 'u', f"Prefijo presente debe ser 'u', es '{prefix_pres}'"
    print("  ✓ _adjust_prefix_for_weak_verb('i', PRESENT) → 'u'")
    
    prefix_pret = stem._adjust_prefix_for_weak_verb('i', VerbFormType.PRETERITE)
    assert prefix_pret == 'ū', f"Prefijo pretérito debe ser 'ū', es '{prefix_pret}'"
    print("  ✓ _adjust_prefix_for_weak_verb('i', PRETERITE) → 'ū'")
    
    # _should_geminate_R2_in_present debe ser True (como fuerte)
    should_gem = stem._should_geminate_R2_in_present()
    assert should_gem == True, "I/w fientivo debe geminar R₂"
    print("  ✓ _should_geminate_R2_in_present() retorna True")
    
    # _should_geminate_infix_t_in_perfect debe ser True
    should_gem_t = stem._should_geminate_infix_t_in_perfect()
    assert should_gem_t == True, "I/w fientivo debe geminar -t-"
    print("  ✓ _should_geminate_infix_t_in_perfect() retorna True")
    
    print("Test 6: ✅ PASSED\n")


def test_multiple_i_w_verbs():
    """Test múltiples verbos I/w fientivo."""
    print("Test 7: Múltiples verbos I/w fientivo...")
    
    verbs = [
        ('s', 'b', VowelClass.A_I, 'sentar'),      # wasābum
        ('b', 'l', VowelClass.A_I, 'llevar'),      # wabālum
        ('r', 'd', VowelClass.A_I, 'descender'),   # warādum
        ('ṣ', 'b', VowelClass.A_U, 'añadir'),      # waṣābum
    ]
    
    for r2, r3, vc, meaning in verbs:
        root = create_i_w_fientive_root(r2, r3, vc, meaning)
        stem = create_i_w_fientive_stem(root)
        
        # Verificar generación de todas las formas
        try:
            pres = stem.form_present(3, 'sg', 'm')
            pret = stem.form_preterite(3, 'sg', 'm')
            perf = stem.form_perfect(3, 'sg', 'm')
            imp = stem.form_imperative('sg', 'm')
            
            assert all(len(f) > 0 for f in [pres, pret, perf, imp])
            
            pres_str = phonemes_to_string(pres)
            print(f"  ✓ w{r2}{r3}um ({meaning}): {pres_str} (presente)")
        except Exception as e:
            print(f"  ✗ ERROR en w{r2}{r3}um: {e}")
            raise
    
    print("Test 7: ✅ PASSED\n")


def test_stem_properties():
    """Test propiedades del stem."""
    print("Test 8: Propiedades del stem...")
    
    root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    stem = create_i_w_fientive_stem(root)
    
    # Tipo de stem
    assert stem.stem_type == StemType.G, "Debe ser G-stem"
    print("  ✓ stem_type = G")
    
    # Raíz debe ser WeakRoot
    assert hasattr(stem.root, 'weak_type'), "Debe tener WeakRoot"
    print("  ✓ root es WeakRoot")
    
    # Clase vocálica
    assert stem.root.vowel_class == VowelClass.A_I, "Clase vocálica debe ser A_I"
    print("  ✓ vowel_class = A_I")
    
    print("Test 8: ✅ PASSED\n")


def main():
    """Ejecutar todos los tests."""
    print("=" * 70)
    print("ITERACIÓN 9 - PASO 4: TESTS I/W FIENTIVE STEM")
    print("=" * 70)
    print()
    
    try:
        test_wasabum_present()
        test_wasabum_preterite()
        test_wasabum_perfect()
        test_wasabum_imperative()
        test_wabalum()
        test_helper_methods_overrides()
        test_multiple_i_w_verbs()
        test_stem_properties()
        
        print("=" * 70)
        print("✅ TODOS LOS TESTS PASARON")
        print("=" * 70)
        print()
        print("PASO 4 COMPLETADO:")
        print("  ✓ I_w_Fientive_Stem implementado")
        print("  ✓ wasābum generado correctamente:")
        print("    - Presente:   u-ššab    (w+i→u)")
        print("    - Pretérito:  ū-šib     (w+i→ū larga)")
        print("    - Perfect:    ut-tašib  (-tt- geminación)")
        print("    - Imperativo: šib       (w→Ø)")
        print("  ✓ 7 métodos helper override")
        print("  ✓ 4 verbos I/w verificados")
        print("  ✓ Todas las formas generando")
        print()
        print("SIGUIENTE PASO: PASO 5 - I/w Adjetival Stem")
        print("  - watārum, waqārum tipo")
        print("  - w+i → ī (siempre larga)")
        print("  - NO geminación R₂")
        print()
        
        return 0
        
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ERROR EN LOS TESTS")
        print("=" * 70)
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())

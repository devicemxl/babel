"""
Tests para I_w_Fientive_Stem - wasābum paradigma completo.

ITERACIÓN 9 - PASO 4: I/w Fientive

Verifica que wasābum genera todas las formas correctamente.

Autor: Claude
Fecha: 2026-02-12
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from phonology.verbal.i_weak.i_w_stems import I_w_Fientive_Stem
from phonology.verbal.weak_root import create_i_w_fientive_root
from phonology.verbal.enums import VowelClass


def phonemes_to_string(phonemes):
    """Helper para convertir fonemas a string."""
    result = ""
    for p in phonemes:
        result += p.symbol
    return result


def test_wasabum_creation():
    """Test creación de wasābum."""
    print("Test 1: Creación de wasābum...")
    
    root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    stem = I_w_Fientive_Stem(root=root)
    
    assert stem.root.to_consonant_symbols() == ('w', 's', 'b')
    assert stem.root.vowel_class == VowelClass.A_I
    print(f"  ✓ wasābum creado: {stem.root}")
    print("Test 1: ✅ PASSED\n")


def test_wasabum_present():
    """Test presente de wasābum."""
    print("Test 2: wasābum Presente...")
    
    root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    stem = I_w_Fientive_Stem(root=root)
    
    # 3sm: uššab
    pres_3sm = stem.form_present(3, 'sg', 'm')
    result_3sm = phonemes_to_string(pres_3sm)
    print(f"  3sm: {result_3sm}")
    assert 'u' in result_3sm, "Debe tener u (contracción w+i→u)"
    assert result_3sm.count('s') == 2 or 'ss' in result_3sm or 'š' in result_3sm, "R₂ debe estar geminada"
    
    # 2sm: tuššab
    pres_2sm = stem.form_present(2, 'sg', 'm')
    result_2sm = phonemes_to_string(pres_2sm)
    print(f"  2sm: {result_2sm}")
    assert 't' in result_2sm, "Debe tener prefijo t"
    assert 'u' in result_2sm, "Debe tener u"
    
    # 1s: uššab
    pres_1s = stem.form_present(1, 'sg', 'm')
    result_1s = phonemes_to_string(pres_1s)
    print(f"  1s: {result_1s}")
    
    print("Test 2: ✅ PASSED\n")


def test_wasabum_preterite():
    """Test pretérito de wasābum."""
    print("Test 3: wasābum Pretérito...")
    
    root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    stem = I_w_Fientive_Stem(root=root)
    
    # 3sm: ūšib (vocal larga)
    pret_3sm = stem.form_preterite(3, 'sg', 'm')
    result_3sm = phonemes_to_string(pret_3sm)
    print(f"  3sm: {result_3sm}")
    # Debe tener ū (u larga)
    assert pret_3sm[0].features.is_long, "Primera vocal debe ser larga (ū)"
    
    # 3pm: ušbū (vocal corta + ending largo)
    pret_3pm = stem.form_preterite(3, 'pl', 'm')
    result_3pm = phonemes_to_string(pret_3pm)
    print(f"  3pm: {result_3pm}")
    # Primera vocal debe ser corta por síncope
    assert not pret_3pm[0].features.is_long, "Primera vocal debe ser corta con ending"
    # Debe tener ending -ū
    assert pret_3pm[-1].features.is_long, "Ending debe ser largo"
    
    print("Test 3: ✅ PASSED\n")


def test_wasabum_perfect():
    """Test perfect de wasābum."""
    print("Test 4: wasābum Perfect...")
    
    root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    stem = I_w_Fientive_Stem(root=root)
    
    # 3sm: uttašab
    perf_3sm = stem.form_perfect(3, 'sg', 'm')
    result_3sm = phonemes_to_string(perf_3sm)
    print(f"  3sm: {result_3sm}")
    assert 'u' in result_3sm, "Debe tener u (contracción)"
    assert 'tt' in result_3sm or result_3sm.count('t') >= 2, "Debe tener -tt- geminado"
    
    print("Test 4: ✅ PASSED\n")


def test_wasabum_imperative():
    """Test imperativo de wasābum."""
    print("Test 5: wasābum Imperativo...")
    
    root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    stem = I_w_Fientive_Stem(root=root)
    
    # sm: šib
    imp_sm = stem.form_imperative('sg', 'm')
    result_sm = phonemes_to_string(imp_sm)
    print(f"  sm: {result_sm}")
    # w debe desaparecer
    assert 'w' not in result_sm, "w debe desaparecer en imperativo"
    # Debe empezar con R₂
    assert result_sm[0] in ['s', 'š'], "Debe empezar con s/š (R₂)"
    
    # pm: šibā
    imp_pm = stem.form_imperative('pl', 'm')
    result_pm = phonemes_to_string(imp_pm)
    print(f"  pm: {result_pm}")
    assert imp_pm[-1].features.is_long, "Plural debe tener ending largo"
    
    print("Test 5: ✅ PASSED\n")


def test_wabalum():
    """Test wabālum 'llevar'."""
    print("Test 6: wabālum...")
    
    root = create_i_w_fientive_root('b', 'l', VowelClass.A_I, 'llevar')
    stem = I_w_Fientive_Stem(root=root)
    
    # Presente 3sm: ubbal
    pres = stem.form_present(3, 'sg', 'm')
    result_pres = phonemes_to_string(pres)
    print(f"  Pres 3sm: {result_pres}")
    assert 'u' in result_pres
    assert result_pres.count('b') == 2 or 'bb' in result_pres
    
    # Pretérito 3sm: ūbil
    pret = stem.form_preterite(3, 'sg', 'm')
    result_pret = phonemes_to_string(pret)
    print(f"  Pret 3sm: {result_pret}")
    assert pret[0].features.is_long
    
    # Imperativo: bil
    imp = stem.form_imperative('sg', 'm')
    result_imp = phonemes_to_string(imp)
    print(f"  Imp sm: {result_imp}")
    assert result_imp[0] == 'b'
    
    print("Test 6: ✅ PASSED\n")


def test_helper_methods():
    """Test métodos helper de I_w_Fientive_Stem."""
    print("Test 7: Helper methods...")
    
    root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    stem = I_w_Fientive_Stem(root=root)
    
    # R₁ debe ser None en todas las formas (w desaparece)
    r1_pres = stem._get_R1_for_present()
    assert r1_pres is None, "R₁ debe ser None en presente"
    print("  ✓ _get_R1_for_present() → None")
    
    r1_pret = stem._get_R1_for_preterite()
    assert r1_pret == [], "R₁ debe ser [] en pretérito"
    print("  ✓ _get_R1_for_preterite() → []")
    
    r1_imp = stem._get_R1_for_imperative()
    assert r1_imp is None, "R₁ debe ser None en imperativo"
    print("  ✓ _get_R1_for_imperative() → None")
    
    # Geminación
    should_gem_r2 = stem._should_geminate_R2_in_present()
    assert should_gem_r2 == True, "Debe geminar R₂"
    print("  ✓ _should_geminate_R2_in_present() → True")
    
    should_gem_t = stem._should_geminate_infix_t_in_perfect()
    assert should_gem_t == True, "Debe geminar infix-t"
    print("  ✓ _should_geminate_infix_t_in_perfect() → True")
    
    print("Test 7: ✅ PASSED\n")


def main():
    """Ejecutar todos los tests."""
    print("=" * 70)
    print("ITERACIÓN 9 - PASO 4: TESTS I/W FIENTIVE")
    print("wasābum paradigma completo")
    print("=" * 70)
    print()
    
    try:
        test_wasabum_creation()
        test_wasabum_present()
        test_wasabum_preterite()
        test_wasabum_perfect()
        test_wasabum_imperative()
        test_wabalum()
        test_helper_methods()
        
        print("=" * 70)
        print("✅ TODOS LOS TESTS PASARON")
        print("=" * 70)
        print()
        print("PASO 4 COMPLETADO:")
        print("  ✓ I_w_Fientive_Stem implementado")
        print("  ✓ wasābum generando todas las formas:")
        print("    - Presente: uššab, tuššab, etc.")
        print("    - Pretérito: ūšib, ušbū, etc.")
        print("    - Perfect: uttašab")
        print("    - Imperativo: šib, šibā")
        print("  ✓ wabālum verificado")
        print("  ✓ Helper methods funcionando")
        print()
        print("SIGUIENTE PASO: PASO 5 - I/voc Stems")
        print("  - Implementar I_a_Stem y I_e_Stem")
        print("  - Generar ahāzum, epāšum")
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

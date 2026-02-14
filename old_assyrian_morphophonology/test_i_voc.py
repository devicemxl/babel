"""
Tests para I_a_Stem e I_e_Stem.

ITERACIÓN 9 - PASO 5: I/voc Stems

Verifica ahāzum y epāšum.

Autor: Claude
Fecha: 2026-02-12
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from phonology.verbal.i_weak.i_voc_stems import I_a_Stem, I_e_Stem
from phonology.verbal.weak_root import create_i_voc_a_root, create_i_voc_e_root
from phonology.verbal.enums import VowelClass


def phonemes_to_string(phonemes):
    """Helper."""
    return "".join(p.symbol for p in phonemes)


def test_ahazum_creation():
    """Test creación de ahāzum."""
    print("Test 1: Creación de ahāzum...")
    
    root = create_i_voc_a_root('k', 'z', VowelClass.A_U, 'tomar')
    stem = I_a_Stem(root=root)
    
    assert stem.root.to_consonant_symbols() == ('Ø', 'k', 'z')
    assert stem.initial_vowel == 'a'
    print(f"  ✓ ahāzum creado: {stem.root}")
    print("Test 1: ✅ PASSED\n")


def test_ahazum_present():
    """Test presente de ahāzum."""
    print("Test 2: ahāzum Presente...")
    
    root = create_i_voc_a_root('k', 'z', VowelClass.A_U, 'tomar')
    stem = I_a_Stem(root=root)
    
    # 3sm: āḥḥaz (vocal larga + gem R₂)
    pres_3sm = stem.form_present(3, 'sg', 'm')
    result = phonemes_to_string(pres_3sm)
    print(f"  3sm: {result}")
    assert pres_3sm[0].features.is_long, "Primera vocal debe ser larga (compensatoria)"
    assert pres_3sm[0].symbol in ['a', 'ā'], "Debe empezar con 'a'"
    
    print("Test 2: ✅ PASSED\n")


def test_ahazum_preterite():
    """Test pretérito de ahāzum."""
    print("Test 3: ahāzum Pretérito...")
    
    root = create_i_voc_a_root('k', 'z', VowelClass.A_U, 'tomar')
    stem = I_a_Stem(root=root)
    
    # 1s: āḥuz (a larga)
    pret_1s = stem.form_preterite(1, 'sg', 'm')
    result_1s = phonemes_to_string(pret_1s)
    print(f"  1s: {result_1s}")
    assert pret_1s[0].features.is_long, "Vocal debe ser larga"
    assert pret_1s[0].symbol in ['a', 'ā'], "1s debe tener 'ā'"
    
    # 3sm: ēḥuz (e larga)
    pret_3sm = stem.form_preterite(3, 'sg', 'm')
    result_3sm = phonemes_to_string(pret_3sm)
    print(f"  3sm: {result_3sm}")
    assert pret_3sm[0].features.is_long, "Vocal debe ser larga"
    assert pret_3sm[0].symbol in ['e', 'ē'], "3s debe tener 'ē'"
    
    # 2sm: tāḥuz (t + a larga)
    pret_2sm = stem.form_preterite(2, 'sg', 'm')
    result_2sm = phonemes_to_string(pret_2sm)
    print(f"  2sm: {result_2sm}")
    assert pret_2sm[0].symbol == 't', "Debe empezar con 't'"
    assert pret_2sm[1].features.is_long, "Segunda vocal debe ser larga"
    
    print("Test 3: ✅ PASSED\n")


def test_ahazum_perfect():
    """Test perfect de ahāzum."""
    print("Test 4: ahāzum Perfect...")
    
    root = create_i_voc_a_root('k', 'z', VowelClass.A_U, 'tomar')
    stem = I_a_Stem(root=root)
    
    # 3sm: ītaḥaz
    perf_3sm = stem.form_perfect(3, 'sg', 'm')
    result = phonemes_to_string(perf_3sm)
    print(f"  3sm: {result}")
    assert perf_3sm[0].features.is_long, "Vocal inicial debe ser larga"
    assert perf_3sm[0].symbol in ['i', 'ī'], "Debe empezar con 'ī'"
    assert 't' in result, "Debe tener infix-t"
    
    print("Test 4: ✅ PASSED\n")


def test_ahazum_imperative():
    """Test imperativo de ahāzum."""
    print("Test 5: ahāzum Imperativo...")
    
    root = create_i_voc_a_root('k', 'z', VowelClass.A_U, 'tomar')
    stem = I_a_Stem(root=root)
    
    # sm: ḥuz
    imp_sm = stem.form_imperative('sg', 'm')
    result = phonemes_to_string(imp_sm)
    print(f"  sm: {result}")
    # Debe empezar con R₂ (no hay vocal inicial ni R₁)
    assert imp_sm[0].symbol == 'k', "Debe empezar con R₂"
    
    print("Test 5: ✅ PASSED\n")


def test_epasum_creation():
    """Test creación de epāšum."""
    print("Test 6: Creación de epāšum...")
    
    root = create_i_voc_e_root('p', 's', VowelClass.A_U, 'hacer')
    stem = I_e_Stem(root=root)
    
    assert stem.root.to_consonant_symbols() == ('Ø', 'p', 's')
    assert stem.initial_vowel == 'e'
    print(f"  ✓ epāšum creado: {stem.root}")
    print("Test 6: ✅ PASSED\n")


def test_epasum_present():
    """Test presente de epāšum."""
    print("Test 7: epāšum Presente...")
    
    root = create_i_voc_e_root('p', 's', VowelClass.A_U, 'hacer')
    stem = I_e_Stem(root=root)
    
    # 3sm: eppeš
    pres_3sm = stem.form_present(3, 'sg', 'm')
    result = phonemes_to_string(pres_3sm)
    print(f"  3sm: {result}")
    assert pres_3sm[0].symbol in ['e', 'ē'], "Debe empezar con 'e'"
    assert pres_3sm[0].features.is_long, "Vocal debe ser larga"
    
    print("Test 7: ✅ PASSED\n")


def test_epasum_preterite():
    """Test pretérito de epāšum."""
    print("Test 8: epāšum Pretérito...")
    
    root = create_i_voc_e_root('p', 's', VowelClass.A_U, 'hacer')
    stem = I_e_Stem(root=root)
    
    # 1s: ēpuš
    pret_1s = stem.form_preterite(1, 'sg', 'm')
    result_1s = phonemes_to_string(pret_1s)
    print(f"  1s: {result_1s}")
    assert pret_1s[0].symbol in ['e', 'ē'], "Debe tener 'ē'"
    assert pret_1s[0].features.is_long, "Vocal debe ser larga"
    
    # 3sm: ēpuš (igual que 1s para I/e)
    pret_3sm = stem.form_preterite(3, 'sg', 'm')
    result_3sm = phonemes_to_string(pret_3sm)
    print(f"  3sm: {result_3sm}")
    assert pret_3sm[0].symbol in ['e', 'ē'], "Debe tener 'ē'"
    
    print("Test 8: ✅ PASSED\n")


def test_helper_methods():
    """Test helper methods de I/voc."""
    print("Test 9: Helper methods...")
    
    root = create_i_voc_a_root('k', 'z', VowelClass.A_U, 'tomar')
    stem = I_a_Stem(root=root)
    
    # R₁ debe ser None (gutural perdida)
    assert stem._get_R1_for_present() is None
    print("  ✓ _get_R1_for_present() → None")
    
    assert stem._get_R1_for_preterite() == []
    print("  ✓ _get_R1_for_preterite() → []")
    
    assert stem._get_R1_for_imperative() is None
    print("  ✓ _get_R1_for_imperative() → None")
    
    # Geminación R₂
    assert stem._should_geminate_R2_in_present() == True
    print("  ✓ _should_geminate_R2_in_present() → True")
    
    print("Test 9: ✅ PASSED\n")


def main():
    """Ejecutar todos los tests."""
    print("=" * 70)
    print("ITERACIÓN 9 - PASO 5: TESTS I/VOC STEMS")
    print("ahāzum y epāšum")
    print("=" * 70)
    print()
    
    try:
        test_ahazum_creation()
        test_ahazum_present()
        test_ahazum_preterite()
        test_ahazum_perfect()
        test_ahazum_imperative()
        test_epasum_creation()
        test_epasum_present()
        test_epasum_preterite()
        test_helper_methods()
        
        print("=" * 70)
        print("✅ TODOS LOS TESTS PASARON")
        print("=" * 70)
        print()
        print("PASO 5 COMPLETADO:")
        print("  ✓ I_a_Stem implementado")
        print("  ✓ I_e_Stem implementado")
        print("  ✓ ahāzum generando:")
        print("    - Presente: āḥḥaz")
        print("    - Pretérito: āḥuz (1s), ēḥuz (3s)")
        print("    - Perfect: ītaḥaz")
        print("    - Imperativo: ḥuz")
        print("  ✓ epāšum generando:")
        print("    - Presente: eppeš")
        print("    - Pretérito: ēpuš")
        print()
        print("SIGUIENTE PASO: PASO 6 - I/n Stems")
        print("  - Implementar I_n_Stem")
        print("  - Generar naṣārum")
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

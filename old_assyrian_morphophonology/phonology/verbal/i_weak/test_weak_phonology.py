"""
Tests para weak_phonology.py

ITERACIÓN 9 - PASO 2: Reglas Fonológicas

Tests para verificar que las 8 reglas principales funcionan correctamente.

Autor: Claude
Fecha: 2026-02-12
"""

import sys
import os

# Ajustar path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from phonology import Vowel, Consonant
from phonology.enums import VowelQuality
from phonology.inventory import get_consonant, get_vowel
from phonology.verbal.weak_phonology import (
    contract_w_i_to_u,
    contract_w_i_to_u_long,
    contract_w_i_to_i_long,
    drop_initial_w,
    apply_compensatory_lengthening,
    lengthen_prefix_vowel_in_preterite,
    assimilate_n_to_following_consonant,
    drop_initial_n_before_high_vowel,
    phonemes_to_string,
    list_all_rules,
    get_rule_by_name
)




# Helper function para crear vocales con longitud
def make_vowel(symbol: str, length: str = 'short'):
    """Crea vocal con longitud especificada."""
    from phonology.enums import VowelQuality, VowelLength
    from phonology.features import VowelFeatures
    
    quality_map = {'a': VowelQuality.A, 'e': VowelQuality.E, 
                   'i': VowelQuality.I, 'u': VowelQuality.U}
    length_enum = VowelLength.LONG if length == 'long' else VowelLength.SHORT
    
    return Vowel(
        features=VowelFeatures(quality=quality_map[symbol], length=length_enum)
    )

def test_contract_w_i_to_u():
    """Test: w + i → u (I/w fientivo presente)."""
    print("Test 1: contract_w_i_to_u...")
    
    # Input: [w, i, š, a, b]
    input_phonemes = [
        get_consonant('w'),
        make_vowel('i', 'short'),
        get_consonant('s'),
        make_vowel('a', 'short'),
        get_consonant('b')
    ]
    
    # Expected: [u, š, a, b]
    result = contract_w_i_to_u(input_phonemes)
    
    assert len(result) == 4, f"Expected 4 phonemes, got {len(result)}"
    assert result[0].features.quality == VowelQuality.U, f"Expected 'u', got '{result[0].symbol}'"
    assert result[0].features.is_long == False, f"Expected short (is_long=False), got is_long={result[0].features.is_long}"
    assert result[1].symbol == 's'
    
    print(f"  ✓ [w, i, s, a, b] → [{phonemes_to_string(result)}]")
    print("Test 1: ✅ PASSED\n")


def test_contract_w_i_to_u_long():
    """Test: w + i → ū (I/w fientivo pretérito - larga)."""
    print("Test 2: contract_w_i_to_u_long...")
    
    # Input: [w, i, š, i, b]
    input_phonemes = [
        get_consonant('w'),
        make_vowel('i', 'short'),
        get_consonant('s'),
        make_vowel('i', 'short'),
        get_consonant('b')
    ]
    
    # Sin ending: ū larga
    result_no_ending = contract_w_i_to_u_long(input_phonemes, {'has_ending': False})
    assert result_no_ending[0].features.quality == VowelQuality.U
    assert result_no_ending[0].features.is_long == True, f"Expected long, got {result_no_ending[0].length}"
    print(f"  ✓ Sin ending: [{phonemes_to_string(result_no_ending)}] (vocal larga)")
    
    # Con ending: u corta
    result_with_ending = contract_w_i_to_u_long(input_phonemes, {'has_ending': True})
    assert result_with_ending[0].features.quality == VowelQuality.U
    assert result_with_ending[0].features.is_long == False, f"Expected short, got {result_with_ending[0].length}"
    print(f"  ✓ Con ending: [{phonemes_to_string(result_with_ending)}] (vocal corta)")
    
    print("Test 2: ✅ PASSED\n")


def test_contract_w_i_to_i_long():
    """Test: w + i → ī (I/w adjetival - siempre larga)."""
    print("Test 3: contract_w_i_to_i_long...")
    
    # Input: [w, i, t, e, r]
    input_phonemes = [
        get_consonant('w'),
        make_vowel('i', 'short'),
        get_consonant('t'),
        make_vowel('e', 'short'),
        get_consonant('r')
    ]
    
    result = contract_w_i_to_i_long(input_phonemes)
    
    assert result[0].features.quality == VowelQuality.I
    assert result[0].features.is_long == True, "I/w adjetival debe tener ī larga"
    assert result[1].symbol == 't'
    
    print(f"  ✓ [w, i, t, e, r] → [{phonemes_to_string(result)}] (ī siempre larga)")
    print("Test 3: ✅ PASSED\n")


def test_drop_initial_w():
    """Test: w inicial → Ø (pérdida en imperativo)."""
    print("Test 4: drop_initial_w...")
    
    # Input: [w, š, i, b]
    input_phonemes = [
        get_consonant('w'),
        get_consonant('s'),
        make_vowel('i', 'short'),
        get_consonant('b')
    ]
    
    # Con word_initial: True → pérdida
    result_initial = drop_initial_w(input_phonemes, {'word_initial': True})
    assert len(result_initial) == 3
    assert result_initial[0].symbol == 's', "w debe desaparecer"
    print(f"  ✓ Con word_initial: [w, s, i, b] → [{phonemes_to_string(result_initial)}]")
    
    # Sin word_initial → preservar
    result_no_initial = drop_initial_w(input_phonemes, {'word_initial': False})
    assert len(result_no_initial) == 4
    assert result_no_initial[0].symbol == 'w', "w debe preservarse"
    print(f"  ✓ Sin word_initial: preserva w")
    
    print("Test 4: ✅ PASSED\n")


def test_apply_compensatory_lengthening():
    """Test: Vocal → Vocal larga (I/voc compensación)."""
    print("Test 5: apply_compensatory_lengthening...")
    
    # Input: [a, k, u, z] (ahāzum)
    input_phonemes = [
        make_vowel('a', 'short'),
        get_consonant('k'),
        make_vowel('u', 'short'),
        get_consonant('z')
    ]
    
    result = apply_compensatory_lengthening(input_phonemes, initial_vowel='a')
    
    assert result[0].features.quality == VowelQuality.A
    assert result[0].features.is_long == True, "Vocal inicial debe alargarse"
    print(f"  ✓ [a, k, u, z] → [ā, k, u, z] (vocal larga compensatoria)")
    
    # Test con 'e' para I/e
    input_e = [
        make_vowel('e', 'short'),
        get_consonant('p'),
        make_vowel('u', 'short'),
        get_consonant('s')
    ]
    result_e = apply_compensatory_lengthening(input_e, initial_vowel='e')
    assert result_e[0].features.quality == VowelQuality.E
    assert result_e[0].features.is_long == True
    print(f"  ✓ [e, p, u, s] → [ē, p, u, s] (vocal larga compensatoria)")
    
    print("Test 5: ✅ PASSED\n")


def test_lengthen_prefix_vowel_in_preterite():
    """Test: Vocal de prefijo → larga en pretérito I/voc."""
    print("Test 6: lengthen_prefix_vowel_in_preterite...")
    
    # Persona 1: a → ā
    input_1s = [make_vowel('a', 'short'), get_consonant('k'), make_vowel('u', 'short'), get_consonant('z')]
    result_1s = lengthen_prefix_vowel_in_preterite(input_1s, person=1)
    assert result_1s[0].features.is_long == True
    print(f"  ✓ Persona 1: a → ā")
    
    # Persona 3: e → ē
    input_3s = [make_vowel('e', 'short'), get_consonant('k'), make_vowel('u', 'short'), get_consonant('z')]
    result_3s = lengthen_prefix_vowel_in_preterite(input_3s, person=3)
    assert result_3s[0].features.is_long == True
    print(f"  ✓ Persona 3: e → ē")
    
    # Persona 2: t+a → t+ā
    input_2s = [get_consonant('t'), make_vowel('a', 'short'), get_consonant('k'), make_vowel('u', 'short'), get_consonant('z')]
    result_2s = lengthen_prefix_vowel_in_preterite(input_2s, person=2)
    assert result_2s[1].features.is_long == True
    print(f"  ✓ Persona 2: t+a → t+ā")
    
    print("Test 6: ✅ PASSED\n")


def test_assimilate_n_to_following_consonant():
    """Test: n + C → CC (asimilación I/n)."""
    print("Test 7: assimilate_n_to_following_consonant...")
    
    # Test 1: n + ṣ → ṣṣ
    input_1 = [
        make_vowel('i', 'short'),
        get_consonant('n'),
        get_consonant('s'),  # usando 's' como proxy de 'ṣ'
        make_vowel('u', 'short'),
        get_consonant('r')
    ]
    result_1 = assimilate_n_to_following_consonant(input_1)
    assert len(result_1) == 5, f"Expected 5 phonemes, got {len(result_1)}"
    assert result_1[1].symbol == 's', "Primera s (geminada)"
    assert result_1[2].symbol == 's', "Segunda s (geminada)"
    assert 'n' not in [p.symbol for p in result_1], "n debe desaparecer"
    print(f"  ✓ [i, n, s, u, r] → [{phonemes_to_string(result_1)}] (n+s → ss)")
    
    # Test 2: n + t → tt
    input_2 = [
        make_vowel('i', 'short'),
        get_consonant('n'),
        get_consonant('t'),
        make_vowel('a', 'short'),
        get_consonant('s')
    ]
    result_2 = assimilate_n_to_following_consonant(input_2)
    assert result_2[1].symbol == 't'
    assert result_2[2].symbol == 't'
    print(f"  ✓ [i, n, t, a, s] → [{phonemes_to_string(result_2)}] (n+t → tt)")
    
    # Test 3: EXCEPCIÓN n + w → nw (NO asimila)
    input_3 = [
        make_vowel('u', 'short'),
        get_consonant('n'),
        get_consonant('w'),
        make_vowel('a', 'short'),
        get_consonant('r')
    ]
    result_3 = assimilate_n_to_following_consonant(input_3)
    assert result_3[1].symbol == 'n', "n debe preservarse ante w"
    assert result_3[2].symbol == 'w', "w debe preservarse"
    print(f"  ✓ [u, n, w, a, r] → [{phonemes_to_string(result_3)}] (n+w NO asimila)")
    
    print("Test 7: ✅ PASSED\n")


def test_drop_initial_n_before_high_vowel():
    """Test: #n + i/u → #i/u (pérdida I/n imperativo)."""
    print("Test 8: drop_initial_n_before_high_vowel...")
    
    # Test 1: n + u → u
    input_1 = [
        get_consonant('n'),
        make_vowel('u', 'short'),
        get_consonant('s'),
        make_vowel('u', 'short'),
        get_consonant('r')
    ]
    result_1 = drop_initial_n_before_high_vowel(input_1, {'word_initial': True})
    assert len(result_1) == 4
    assert result_1[0].features.quality == VowelQuality.U, "n debe desaparecer"
    print(f"  ✓ [n, u, s, u, r] → [{phonemes_to_string(result_1)}]")
    
    # Test 2: n + i → i
    input_2 = [
        get_consonant('n'),
        make_vowel('i', 'short'),
        get_consonant('k'),
        make_vowel('e', 'short'),
        get_consonant('r')
    ]
    result_2 = drop_initial_n_before_high_vowel(input_2, {'word_initial': True})
    assert result_2[0].features.quality == VowelQuality.I, "n debe desaparecer"
    print(f"  ✓ [n, i, k, e, r] → [{phonemes_to_string(result_2)}]")
    
    # Test 3: Sin word_initial → preservar
    result_3 = drop_initial_n_before_high_vowel(input_1, {'word_initial': False})
    assert result_3[0].symbol == 'n', "n debe preservarse"
    print(f"  ✓ Sin word_initial: n preservada")
    
    # Test 4: n + a (vocal baja) → no pérdida
    input_4 = [
        get_consonant('n'),
        make_vowel('a', 'short'),
        get_consonant('s')
    ]
    result_4 = drop_initial_n_before_high_vowel(input_4, {'word_initial': True})
    assert result_4[0].symbol == 'n', "n debe preservarse ante vocal baja"
    print(f"  ✓ n + a (vocal baja): n preservada")
    
    print("Test 8: ✅ PASSED\n")


def test_utility_functions():
    """Test funciones de utilidad."""
    print("Test 9: Utility functions...")
    
    # list_all_rules
    rules = list_all_rules()
    assert len(rules) >= 8, f"Expected >=8 rules, got {len(rules)}"
    assert 'contract_w_i_to_u' in rules
    assert 'assimilate_n_to_following_consonant' in rules
    print(f"  ✓ list_all_rules() retorna {len(rules)} reglas")
    
    # get_rule_by_name
    rule = get_rule_by_name('contract_w_i_to_u')
    assert rule is not None
    assert callable(rule)
    print(f"  ✓ get_rule_by_name() funciona")
    
    # phonemes_to_string
    phonemes = [make_vowel('u', 'short'), get_consonant('s'), make_vowel('a', 'short'), get_consonant('b')]
    string = phonemes_to_string(phonemes)
    assert string == 'usab'
    print(f"  ✓ phonemes_to_string() funciona: {string}")
    
    print("Test 9: ✅ PASSED\n")


def main():
    """Ejecutar todos los tests."""
    print("=" * 70)
    print("ITERACIÓN 9 - PASO 2: TESTS DE REGLAS FONOLÓGICAS")
    print("=" * 70)
    print()
    
    try:
        test_contract_w_i_to_u()
        test_contract_w_i_to_u_long()
        test_contract_w_i_to_i_long()
        test_drop_initial_w()
        test_apply_compensatory_lengthening()
        test_lengthen_prefix_vowel_in_preterite()
        test_assimilate_n_to_following_consonant()
        test_drop_initial_n_before_high_vowel()
        test_utility_functions()
        
        print("=" * 70)
        print("✅ TODOS LOS TESTS PASARON")
        print("=" * 70)
        print()
        print("PASO 2 COMPLETADO:")
        print("  ✓ weak_phonology.py creado (650+ líneas)")
        print("  ✓ 8 reglas fonológicas implementadas:")
        print("    - 4 reglas I/w (contracciones)")
        print("    - 2 reglas I/voc (compensación)")
        print("    - 2 reglas I/n (asimilación/pérdida)")
        print("  ✓ Funciones de utilidad implementadas")
        print("  ✓ Todos los tests pasando")
        print()
        print("SIGUIENTE PASO: PASO 3 - Modificar VerbalStem (base)")
        print("  - Agregar métodos helper a stem.py")
        print("  - Permitir pre-procesamiento de prefijos")
        print("  - Tests de regresión (verbos fuertes siguen funcionando)")
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

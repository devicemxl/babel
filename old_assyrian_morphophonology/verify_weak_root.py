"""
Script de verificación simple para weak_root.py (sin pytest).

ITERACIÓN 9 - PASO 1: Verificación de fundamentos

Autor: Claude
Fecha: 2026-02-12
"""

import sys
import os

# Ajustar path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from phonology.verbal.weak_root import (
    WeakConsonant,
    WeakRoot,
    create_i_w_fientive_root,
    create_i_w_adjectival_root,
    create_i_voc_a_root,
    create_i_voc_e_root,
    create_i_n_root,
    create_atawwum_root,
    is_weak_root,
    get_weak_type_from_root
)
from phonology.verbal.enums import (
    WeakVerbType,
    WeakPosition,
    VowelClass
)


def test_weak_consonant():
    """Test WeakConsonant creation."""
    print("Test 1: WeakConsonant...")
    
    # Test w consonant
    wc = WeakConsonant('w', WeakPosition.R1, 'contracts')
    assert wc.symbol == 'w'
    assert wc.contracts_with_i()
    print("  ✓ WeakConsonant('w') funciona")
    
    # Test guttural lost
    wc2 = WeakConsonant('Ø', WeakPosition.R1, 'compensatory_lengthening')
    assert wc2.is_lost_guttural()
    print("  ✓ WeakConsonant('Ø') funciona")
    
    # Test n
    wc3 = WeakConsonant('n', WeakPosition.R1, 'assimilates')
    assert wc3.can_assimilate()
    print("  ✓ WeakConsonant('n') funciona")
    
    print("Test 1: ✅ PASSED\n")


def test_weak_root_creation():
    """Test WeakRoot creation with helpers."""
    print("Test 2: WeakRoot creation...")
    
    # I/w fientive
    root1 = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    assert root1.weak_type == WeakVerbType.I_W_FIENTIVE
    assert root1.R1.symbol == 'w'
    assert root1.to_consonant_symbols() == ('w', 's', 'b')
    print(f"  ✓ wasābum: {root1}")
    
    # I/w adjectival
    root2 = create_i_w_adjectival_root('t', 'r', VowelClass.I_I, 'exceder')
    assert root2.weak_type == WeakVerbType.I_W_ADJECTIVAL
    print(f"  ✓ watārum: {root2}")
    
    # I/voc a
    root3 = create_i_voc_a_root('k', 'z', VowelClass.A_U, 'tomar')
    assert root3.weak_type == WeakVerbType.I_VOC_A
    assert root3.R1.is_lost_guttural()
    print(f"  ✓ ahāzum: {root3}")
    
    # I/voc e
    root4 = create_i_voc_e_root('p', 'š', VowelClass.A_U, 'hacer')
    assert root4.weak_type == WeakVerbType.I_VOC_E
    print(f"  ✓ epāšum: {root4}")
    
    # I/n
    root5 = create_i_n_root('ṣ', 'r', VowelClass.A_U, 'guardar')
    assert root5.weak_type == WeakVerbType.I_N
    print(f"  ✓ naṣārum: {root5}")
    
    # I/n našā'um special
    root6 = create_i_n_root('š', 'm', VowelClass.I_I, 'transportar', special_nasaum=True)
    assert root6.weak_type == WeakVerbType.I_N_NASAUM
    print(f"  ✓ našā'um: {root6}")
    
    # atawwum
    root7 = create_atawwum_root()
    assert root7.weak_type == WeakVerbType.I_ATAWWUM
    assert root7.to_consonant_symbols() == ('Ø', 'w', 'w')
    print(f"  ✓ atawwum: {root7}")
    
    print("Test 2: ✅ PASSED\n")


def test_weak_root_validation():
    """Test WeakRoot validation."""
    print("Test 3: WeakRoot validation...")
    
    from phonology.inventory import get_consonant
    
    # I/w debe tener R1 = w
    try:
        WeakRoot(
            R1=get_consonant('p'),  # ERROR
            R2=get_consonant('s'),
            R3=get_consonant('b'),
            vowel_class=VowelClass.A_I,
            meaning='test',
            weak_type=WeakVerbType.I_W_FIENTIVE
        )
        assert False, "Debería haber lanzado error"
    except ValueError as e:
        assert "I/w verb debe tener R1" in str(e)
        print("  ✓ Validación I/w funciona")
    
    # I/voc debe tener R1 = Ø (gutural perdida)
    try:
        WeakRoot(
            R1=get_consonant('p'),  # ERROR: debería ser WeakConsonant('Ø')
            R2=get_consonant('k'),
            R3=get_consonant('z'),
            vowel_class=VowelClass.A_U,
            meaning='test',
            weak_type=WeakVerbType.I_VOC_A
        )
        assert False, "Debería haber lanzado error"
    except ValueError as e:
        assert "I/voc verb debe tener R1" in str(e)
        print("  ✓ Validación I/voc funciona")
    
    # I/n debe tener R1 = n
    try:
        WeakRoot(
            R1=get_consonant('m'),  # ERROR
            R2=get_consonant('ṣ'),
            R3=get_consonant('r'),
            vowel_class=VowelClass.A_U,
            meaning='test',
            weak_type=WeakVerbType.I_N
        )
        assert False, "Debería haber lanzado error"
    except ValueError as e:
        assert "I/n verb debe tener R1" in str(e)
        print("  ✓ Validación I/n funciona")
    
    print("Test 3: ✅ PASSED\n")


def test_utility_functions():
    """Test utility functions."""
    print("Test 4: Utility functions...")
    
    root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    
    # is_weak_root
    assert is_weak_root(root)
    print("  ✓ is_weak_root() funciona")
    
    # get_weak_type_from_root
    weak_type = get_weak_type_from_root(root)
    assert weak_type == WeakVerbType.I_W_FIENTIVE
    print("  ✓ get_weak_type_from_root() funciona")
    
    # get_weak_positions
    positions = root.get_weak_positions()
    assert len(positions) == 1
    assert WeakPosition.R1 in positions
    print("  ✓ get_weak_positions() funciona")
    
    # to_consonant_symbols
    symbols = root.to_consonant_symbols()
    assert symbols == ('w', 's', 'b')
    print("  ✓ to_consonant_symbols() funciona")
    
    print("Test 4: ✅ PASSED\n")


def test_kouwenberg_examples():
    """Test con ejemplos específicos de Kouwenberg (2017)."""
    print("Test 5: Ejemplos de Kouwenberg...")
    
    examples = [
        ('wasābum', create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar'), ('w', 's', 'b')),
        ('wabālum', create_i_w_fientive_root('b', 'l', VowelClass.A_I, 'llevar'), ('w', 'b', 'l')),
        ('watārum', create_i_w_adjectival_root('t', 'r', VowelClass.I_I, 'exceder'), ('w', 't', 'r')),
        ('ahāzum', create_i_voc_a_root('k', 'z', VowelClass.A_U, 'tomar'), ('Ø', 'k', 'z')),
        ('epāšum', create_i_voc_e_root('p', 'š', VowelClass.A_U, 'hacer'), ('Ø', 'p', 'š')),
        ('naṣārum', create_i_n_root('ṣ', 'r', VowelClass.A_U, 'guardar'), ('n', 'ṣ', 'r')),
        ('našāʔum', create_i_n_root('š', 'm', VowelClass.I_I, 'transportar', True), ('n', 'š', 'm')),
        ('atawwum', create_atawwum_root(), ('Ø', 'w', 'w')),
    ]
    
    for name, root, expected_symbols in examples:
        assert root.to_consonant_symbols() == expected_symbols
        print(f"  ✓ {name}: √{expected_symbols[0]}{expected_symbols[1]}{expected_symbols[2]}")
    
    print("Test 5: ✅ PASSED\n")


def main():
    """Ejecutar todos los tests."""
    print("=" * 70)
    print("ITERACIÓN 9 - PASO 1: VERIFICACIÓN DE FUNDAMENTOS")
    print("=" * 70)
    print()
    
    try:
        test_weak_consonant()
        test_weak_root_creation()
        test_weak_root_validation()
        test_utility_functions()
        test_kouwenberg_examples()
        
        print("=" * 70)
        print("✅ TODOS LOS TESTS PASARON")
        print("=" * 70)
        print()
        print("PASO 1 COMPLETADO:")
        print("  ✓ enums.py actualizado con nuevos tipos")
        print("  ✓ weak_root.py creado y funcionando")
        print("  ✓ Todas las raíces débiles se pueden crear")
        print("  ✓ Validación funciona correctamente")
        print()
        print("SIGUIENTE PASO: PASO 2 - Reglas Fonológicas")
        print("  - Crear weak_phonology.py")
        print("  - Implementar reglas I/w, I/voc, I/n")
        print("  - Tests para cada regla")
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

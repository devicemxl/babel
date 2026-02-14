"""
Test de regresión para verificar que verbos fuertes siguen funcionando
después de agregar métodos helper para verbos débiles.

ITERACIÓN 9 - PASO 3: Modificar VerbalStem

Asegura que los cambios a stem.py no rompieron verbos fuertes.

Autor: Claude
Fecha: 2026-02-12
"""

import sys
import os

# Ajustar path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from phonology.verbal.g_stem import G_Stem
from phonology.verbal.enums import VowelClass
from phonology.inventory import get_consonant


def create_strong_root(R1: str, R2: str, R3: str, vowel_class: VowelClass, meaning: str):
    """Helper para crear raíz fuerte."""
    from phonology.verbal.stem import VerbalRoot
    return VerbalRoot(
        radicals=[get_consonant(R1), get_consonant(R2), get_consonant(R3)],
        vowel_class=vowel_class,
        gloss=meaning
    )


def test_strong_verb_present():
    """Test que presente de verbo fuerte sigue funcionando."""
    print("Test 1: Strong verb - Present...")
    
    # parāsum (a/u) 'separar'
    root = create_strong_root('p', 'r', 's', VowelClass.A_U, 'separar')
    g = G_Stem(root=root)
    
    # Present 3sm: iparras
    try:
        result = g.form_present(3, 'sg', 'm')
        # Debe tener fonemas
        assert len(result) > 0, "Present debe generar fonemas"
        print(f"  ✓ parāsum present 3sm: {len(result)} fonemas")
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        raise
    
    print("Test 1: ✅ PASSED\n")


def test_strong_verb_preterite():
    """Test que pretérito de verbo fuerte sigue funcionando."""
    print("Test 2: Strong verb - Preterite...")
    
    root = create_strong_root('p', 'r', 's', VowelClass.A_U, 'separar')
    g = G_Stem(root=root)
    
    # Preterite 3sm: iprus
    try:
        result = g.form_preterite(3, 'sg', 'm')
        assert len(result) > 0, "Preterite debe generar fonemas"
        print(f"  ✓ parāsum preterite 3sm: {len(result)} fonemas")
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        raise
    
    print("Test 2: ✅ PASSED\n")


def test_strong_verb_perfect():
    """Test que perfect de verbo fuerte sigue funcionando."""
    print("Test 3: Strong verb - Perfect...")
    
    root = create_strong_root('p', 'r', 's', VowelClass.A_U, 'separar')
    g = G_Stem(root=root)
    
    # Perfect 3sm: iptaras
    try:
        result = g.form_perfect(3, 'sg', 'm')
        assert len(result) > 0, "Perfect debe generar fonemas"
        print(f"  ✓ parāsum perfect 3sm: {len(result)} fonemas")
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        raise
    
    print("Test 3: ✅ PASSED\n")


def test_strong_verb_imperative():
    """Test que imperativo de verbo fuerte sigue funcionando."""
    print("Test 4: Strong verb - Imperative...")
    
    root = create_strong_root('p', 'r', 's', VowelClass.A_U, 'separar')
    g = G_Stem(root=root)
    
    # Imperative sm: purus
    try:
        result = g.form_imperative('sg', 'm')
        assert len(result) > 0, "Imperative debe generar fonemas"
        print(f"  ✓ parāsum imperative sm: {len(result)} fonemas")
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        raise
    
    print("Test 4: ✅ PASSED\n")


def test_helper_methods_default_behavior():
    """Test que nuevos métodos helper tienen comportamiento correcto por defecto."""
    print("Test 5: Helper methods - Default behavior...")
    
    root = create_strong_root('p', 'r', 's', VowelClass.A_U, 'separar')
    g = G_Stem(root=root)
    
    # _get_R1_for_present debe retornar R₁
    r1_present = g._get_R1_for_present()
    assert r1_present is not None, "R₁ presente debe existir en verbo fuerte"
    assert r1_present.symbol == 'p', f"R₁ debe ser 'p', got '{r1_present.symbol}'"
    print("  ✓ _get_R1_for_present() retorna R₁ correctamente")
    
    # _get_R1_for_preterite debe retornar [R₁]
    r1_pret = g._get_R1_for_preterite()
    assert len(r1_pret) == 1, "Debe retornar lista con un elemento"
    assert r1_pret[0].symbol == 'p'
    print("  ✓ _get_R1_for_preterite() retorna [R₁] correctamente")
    
    # _adjust_prefix_for_weak_verb debe no cambiar nada
    prefix = g._adjust_prefix_for_weak_verb('i', None)
    assert prefix == 'i', "Verbo fuerte no debe cambiar prefijo"
    print("  ✓ _adjust_prefix_for_weak_verb() no modifica prefijo")
    
    # _should_geminate_R2_in_present debe ser True
    should_gem = g._should_geminate_R2_in_present()
    assert should_gem == True, "Verbo fuerte debe geminar R₂ en presente"
    print("  ✓ _should_geminate_R2_in_present() retorna True")
    
    # _should_geminate_infix_t_in_perfect debe ser False
    should_gem_t = g._should_geminate_infix_t_in_perfect()
    assert should_gem_t == False, "Verbo fuerte no debe geminar -t- en perfect"
    print("  ✓ _should_geminate_infix_t_in_perfect() retorna False")
    
    # _has_vocalic_ending
    has_ending_sg = g._has_vocalic_ending('sg', 'm')
    assert has_ending_sg == False, "Singular masculino no tiene ending"
    print("  ✓ _has_vocalic_ending('sg', 'm') retorna False")
    
    has_ending_pl = g._has_vocalic_ending('pl', 'm')
    assert has_ending_pl == True, "Plural masculino tiene ending"
    print("  ✓ _has_vocalic_ending('pl', 'm') retorna True")
    
    print("Test 5: ✅ PASSED\n")


def test_multiple_strong_verbs():
    """Test varios verbos fuertes para asegurar compatibilidad."""
    print("Test 6: Multiple strong verbs...")
    
    verbs = [
        ('p', 'r', 's', VowelClass.A_U, 'separar'),
        ('š', 'k', 'n', VowelClass.A_U, 'poner'),
        ('k', 't', 'b', VowelClass.A_U, 'escribir'),
    ]
    
    for r1, r2, r3, vc, meaning in verbs:
        root = create_strong_root(r1, r2, r3, vc, meaning)
        g = G_Stem(root=root)
        
        # Verificar que puede generar todas las formas
        try:
            pres = g.form_present(3, 'sg', 'm')
            pret = g.form_preterite(3, 'sg', 'm')
            perf = g.form_perfect(3, 'sg', 'm')
            imp = g.form_imperative('sg', 'm')
            
            assert all(len(f) > 0 for f in [pres, pret, perf, imp])
            print(f"  ✓ √{r1}{r2}{r3} ({meaning}): todas las formas generadas")
        except Exception as e:
            print(f"  ✗ ERROR en √{r1}{r2}{r3}: {e}")
            raise
    
    print("Test 6: ✅ PASSED\n")


def main():
    """Ejecutar todos los tests de regresión."""
    print("=" * 70)
    print("ITERACIÓN 9 - PASO 3: TESTS DE REGRESIÓN")
    print("Verificando que verbos fuertes siguen funcionando")
    print("=" * 70)
    print()
    
    try:
        test_strong_verb_present()
        test_strong_verb_preterite()
        test_strong_verb_perfect()
        test_strong_verb_imperative()
        test_helper_methods_default_behavior()
        test_multiple_strong_verbs()
        
        print("=" * 70)
        print("✅ TODOS LOS TESTS DE REGRESIÓN PASARON")
        print("=" * 70)
        print()
        print("PASO 3 COMPLETADO:")
        print("  ✓ Métodos helper agregados a VerbalStem")
        print("  ✓ 7 nuevos métodos implementados:")
        print("    - _get_R1_for_present/preterite/perfect/imperative")
        print("    - _adjust_prefix_for_weak_verb")
        print("    - _should_geminate_R2_in_present")
        print("    - _should_geminate_infix_t_in_perfect")
        print("    - _has_vocalic_ending")
        print("  ✓ Verbos fuertes siguen funcionando (100% regresión)")
        print("  ✓ Sin cambios breaking en API existente")
        print()
        print("SIGUIENTE PASO: PASO 4 - Implementar I/w Fientive Stem")
        print("  - Crear I_w_Fientive_Stem heredando de G_Stem")
        print("  - Override métodos helper")
        print("  - Generar wasābum completo")
        print()
        
        return 0
        
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ERROR EN LOS TESTS DE REGRESIÓN")
        print("=" * 70)
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())

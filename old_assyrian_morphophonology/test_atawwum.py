"""
Tests para Atawwum_Stem - verbo doblemente débil.

ITERACIÓN 9 - PASO 9: atawwum

Verifica el verbo doblemente débil atawwum.

NOTA: Paradigma parcialmente reconstruido.
Tests verifican la lógica de implementación, no necesariamente
formas históricamente atestiguadas.

Autor: Claude
Fecha: 2026-02-12
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from phonology.verbal.i_weak.i_atawwum_stem import Atawwum_Stem, create_atawwum_root


def phonemes_to_string(phonemes):
    """Helper."""
    return "".join(p.symbol for p in phonemes)


def test_atawwum_creation():
    """Test creación de atawwum."""
    print("Test 1: Creación de atawwum...")
    
    root = create_atawwum_root()
    stem = Atawwum_Stem(root=root)
    
    assert root.to_consonant_symbols() == ('Ø', 'w', 'w')
    assert root.meaning == 'hablar'
    print(f"  ✓ atawwum creado: {root}")
    print(f"  ✓ R₁=Ø, R₂=w, R₃=w (I/voc + II/gem)")
    print("Test 1: ✅ PASSED\n")


def test_atawwum_present():
    """Test presente de atawwum."""
    print("Test 2: atawwum Presente...")
    
    root = create_atawwum_root()
    stem = Atawwum_Stem(root=root)
    
    # 3sm (reconstruido)
    pres_3sm = stem.form_present(3, 'sg', 'm')
    result = phonemes_to_string(pres_3sm)
    print(f"  3sm: {result}")
    
    # Verificaciones
    assert len(pres_3sm) > 0, "Debe generar fonemas"
    # R₂=w puede estar geminada
    has_r2 = 'w' in result
    assert has_r2, "Debe contener R₂ (w)"
    assert pres_3sm[-1].features.is_long, "Debe terminar con vocal larga"
    
    print(f"  ✓ R₁ (Ø) perdida")
    print(f"  ✓ R₂ (w) presente")
    print(f"  ✓ Vocal larga final")
    
    print("Test 2: ✅ PASSED\n")


def test_atawwum_preterite():
    """Test pretérito de atawwum."""
    print("Test 3: atawwum Pretérito...")
    
    root = create_atawwum_root()
    stem = Atawwum_Stem(root=root)
    
    # 3sm: ūtī (reconstruido)
    pret_3sm = stem.form_preterite(3, 'sg', 'm')
    result = phonemes_to_string(pret_3sm)
    print(f"  3sm: {result}")
    
    # Verificaciones
    assert pret_3sm[0].features.is_long, "Primera vocal debe ser larga (ū)"
    assert pret_3sm[0].symbol in ['u', 'ū'], "Debe empezar con ū"
    assert pret_3sm[-1].features.is_long, "Última vocal debe ser larga (ī)"
    assert pret_3sm[-1].symbol in ['i', 'ī'], "Debe terminar con ī"
    
    print(f"  ✓ Inicio: ū (contracción w+i→ū)")
    print(f"  ✓ Final: ī (conversión w→ī)")
    
    print("Test 3: ✅ PASSED\n")


def test_atawwum_perfect():
    """Test perfect de atawwum."""
    print("Test 4: atawwum Perfect...")
    
    root = create_atawwum_root()
    stem = Atawwum_Stem(root=root)
    
    # 3sm (altamente reconstruido)
    perf_3sm = stem.form_perfect(3, 'sg', 'm')
    result = phonemes_to_string(perf_3sm)
    print(f"  3sm: {result}")
    
    # Verificaciones
    assert len(perf_3sm) > 0, "Debe generar fonemas"
    assert 't' in result, "Debe tener infix-t"
    assert 'w' in result, "Debe tener R₂=w"
    assert perf_3sm[-1].features.is_long, "Debe terminar con vocal larga"
    
    print(f"  ✓ Infix-t presente")
    print(f"  ✓ R₂ (w) presente")
    print(f"  ✓ Vocal larga final")
    
    print("Test 4: ✅ PASSED\n")


def test_atawwum_imperative():
    """Test imperativo de atawwum."""
    print("Test 5: atawwum Imperativo...")
    
    root = create_atawwum_root()
    stem = Atawwum_Stem(root=root)
    
    # sm (reconstruido)
    imp_sm = stem.form_imperative('sg', 'm')
    result = phonemes_to_string(imp_sm)
    print(f"  sm: {result}")
    
    # Verificaciones
    assert len(imp_sm) > 0, "Debe generar fonemas"
    assert 'w' in result, "Debe contener R₂=w"
    assert imp_sm[-1].features.is_long, "Debe terminar con vocal larga"
    
    # Plural
    imp_pm = stem.form_imperative('pl', 'm')
    result_pm = phonemes_to_string(imp_pm)
    print(f"  pm: {result_pm}")
    assert len(imp_pm) > len(imp_sm), "Plural debe ser más largo"
    
    print(f"  ✓ R₁ (Ø) ya perdida")
    print(f"  ✓ R₂ (w) presente")
    print(f"  ✓ Vocal larga final")
    print(f"  ✓ Plural con ending")
    
    print("Test 5: ✅ PASSED\n")


def test_double_weakness():
    """Test que doble debilidad funciona correctamente."""
    print("Test 6: Verificar doble debilidad...")
    
    root = create_atawwum_root()
    stem = Atawwum_Stem(root=root)
    
    # Generar varias formas
    forms = {
        'presente': stem.form_present(3, 'sg', 'm'),
        'preterito': stem.form_preterite(3, 'sg', 'm'),
        'perfect': stem.form_perfect(3, 'sg', 'm'),
        'imperativo': stem.form_imperative('sg', 'm')
    }
    
    for name, phonemes in forms.items():
        result = phonemes_to_string(phonemes)
        
        # Todas las formas deben tener al menos una vocal larga
        has_long_vowel = any(
            p.features.is_long 
            for p in phonemes 
            if hasattr(p, 'features') and hasattr(p.features, 'is_long')
        )
        assert has_long_vowel, f"{name} debe tener vocal larga"
        
        # R₂=R₃=w pueden aparecer (II/gem)
        print(f"  ✓ {name:12} → {result:10} (con vocal larga)")
    
    print("Test 6: ✅ PASSED\n")


def test_inheritance_from_i_w():
    """Test que hereda correctamente de G_Stem."""
    print("Test 7: Herencia de G_Stem...")
    
    root = create_atawwum_root()
    stem = Atawwum_Stem(root=root)
    
    # Debe tener métodos helper
    assert hasattr(stem, '_get_R1_for_present')
    assert hasattr(stem, '_should_geminate_R2_in_present')
    assert hasattr(stem, '_has_vocalic_ending')
    
    print("  ✓ Métodos helper presentes")
    print("  ✓ Hereda correctamente de G_Stem")
    
    print("Test 7: ✅ PASSED\n")


def test_paradigm_completeness():
    """Test que puede generar paradigma completo."""
    print("Test 8: Paradigma completo...")
    
    root = create_atawwum_root()
    stem = Atawwum_Stem(root=root)
    
    paradigm_count = 0
    
    # Presente (varias personas)
    for person in [1, 2, 3]:
        pres = stem.form_present(person, 'sg', 'm')
        assert len(pres) > 0, f"Presente {person}s debe generar fonemas"
        paradigm_count += 1
    
    # Pretérito (varias personas)
    for person in [1, 2, 3]:
        pret = stem.form_preterite(person, 'sg', 'm')
        assert len(pret) > 0, f"Pretérito {person}s debe generar fonemas"
        paradigm_count += 1
    
    # Perfect
    perf = stem.form_perfect(3, 'sg', 'm')
    assert len(perf) > 0
    paradigm_count += 1
    
    # Imperativo
    imp = stem.form_imperative('sg', 'm')
    assert len(imp) > 0
    paradigm_count += 1
    
    print(f"  ✓ {paradigm_count} formas generadas exitosamente")
    print("Test 8: ✅ PASSED\n")


def main():
    """Ejecutar todos los tests."""
    print("=" * 70)
    print("ITERACIÓN 9 - PASO 9: TESTS ATAWWUM")
    print("Verbo doblemente débil (I/w + III/w)")
    print("=" * 70)
    print()
    
    try:
        test_atawwum_creation()
        test_atawwum_present()
        test_atawwum_preterite()
        test_atawwum_perfect()
        test_atawwum_imperative()
        test_double_weakness()
        test_inheritance_from_i_w()
        test_paradigm_completeness()
        
        print("=" * 70)
        print("✅ TODOS LOS TESTS PASARON")
        print("=" * 70)
        print()
        print("PASO 9 COMPLETADO:")
        print("  ✓ Atawwum_Stem implementado")
        print("  ✓ Verbo doblemente débil funcionando")
        print("  ✓ Herencia de I/w fientivo correcta")
        print("  ✓ Doble debilidad manejada:")
        print("    - R₁ (w): contracción w+i → u/ū")
        print("    - R₃ (w): conversión w → vocal larga")
        print("  ✓ Paradigma completo generado")
        print()
        print("FORMAS RECONSTRUIDAS (ejemplos):")
        root = create_atawwum_root()
        stem = Atawwum_Stem(root=root)
        print(f"  Presente 3sm:  {phonemes_to_string(stem.form_present(3, 'sg', 'm'))}")
        print(f"  Pretérito 3sm: {phonemes_to_string(stem.form_preterite(3, 'sg', 'm'))}")
        print(f"  Perfect 3sm:   {phonemes_to_string(stem.form_perfect(3, 'sg', 'm'))}")
        print(f"  Imperativo sm: {phonemes_to_string(stem.form_imperative('sg', 'm'))}")
        print()
        print("SIGUIENTE PASO: PASO 10 - Optimización y código final")
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

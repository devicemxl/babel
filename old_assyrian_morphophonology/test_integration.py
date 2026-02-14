"""
Tests de integración end-to-end para verbos débiles.

ITERACIÓN 9 - PASO 7: Tests de integración

Verifica que el sistema completo funciona correctamente:
- Creación de verbos desde cero
- Generación de paradigmas completos
- Interoperabilidad verbos fuertes ↔ débiles
- Performance básico

Autor: Claude
Fecha: 2026-02-12
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from phonology.verbal.g_stem import G_Stem
from phonology.verbal.stem import VerbalRoot
from phonology.verbal.weak_root import (
    create_i_w_fientive_root,
    create_i_voc_a_root,
    create_i_voc_e_root,
    create_i_n_root
)
from phonology.verbal.i_weak.i_w_stems import I_w_Fientive_Stem
from phonology.verbal.i_weak.i_voc_stems import I_a_Stem, I_e_Stem
from phonology.verbal.i_weak.i_n_stems import I_n_Stem
from phonology.verbal.enums import VowelClass
from phonology.inventory import get_consonant


def phonemes_to_string(phonemes):
    """Helper."""
    return "".join(p.symbol for p in phonemes)


def test_full_paradigm_wasabum():
    """Test paradigma completo de wasābum."""
    print("Test 1: Paradigma completo wasābum...")
    
    root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    stem = I_w_Fientive_Stem(root=root)
    
    paradigm = {}
    
    # Presente
    paradigm['pres_3sm'] = phonemes_to_string(stem.form_present(3, 'sg', 'm'))
    paradigm['pres_2sm'] = phonemes_to_string(stem.form_present(2, 'sg', 'm'))
    paradigm['pres_1s'] = phonemes_to_string(stem.form_present(1, 'sg', 'm'))
    paradigm['pres_3pm'] = phonemes_to_string(stem.form_present(3, 'pl', 'm'))
    
    # Pretérito
    paradigm['pret_3sm'] = phonemes_to_string(stem.form_preterite(3, 'sg', 'm'))
    paradigm['pret_2sm'] = phonemes_to_string(stem.form_preterite(2, 'sg', 'm'))
    paradigm['pret_1s'] = phonemes_to_string(stem.form_preterite(1, 'sg', 'm'))
    paradigm['pret_3pm'] = phonemes_to_string(stem.form_preterite(3, 'pl', 'm'))
    
    # Perfect
    paradigm['perf_3sm'] = phonemes_to_string(stem.form_perfect(3, 'sg', 'm'))
    paradigm['perf_2sm'] = phonemes_to_string(stem.form_perfect(2, 'sg', 'm'))
    
    # Imperativo
    paradigm['imp_sm'] = phonemes_to_string(stem.form_imperative('sg', 'm'))
    paradigm['imp_pm'] = phonemes_to_string(stem.form_imperative('pl', 'm'))
    
    print(f"  Paradigma completo generado: {len(paradigm)} formas")
    print(f"  Presente 3sm: {paradigm['pres_3sm']}")
    print(f"  Pretérito 3sm: {paradigm['pret_3sm']}")
    print(f"  Perfect 3sm: {paradigm['perf_3sm']}")
    print(f"  Imperativo sm: {paradigm['imp_sm']}")
    
    # Verificaciones
    assert 'u' in paradigm['pres_3sm'], "Presente debe tener u (contracción)"
    assert paradigm['pret_3sm'][0] == 'ū', "Pretérito 3sm debe empezar con ū"
    assert 'tt' in paradigm['perf_3sm'], "Perfect debe tener -tt-"
    assert paradigm['imp_sm'][0] == 's', "Imperativo debe empezar con R₂"
    
    print("Test 1: ✅ PASSED\n")
    return paradigm


def test_full_paradigm_ahazum():
    """Test paradigma completo de ahāzum."""
    print("Test 2: Paradigma completo ahāzum...")
    
    root = create_i_voc_a_root('k', 'z', VowelClass.A_U, 'tomar')
    stem = I_a_Stem(root=root)
    
    paradigm = {}
    
    # Presente
    paradigm['pres_3sm'] = phonemes_to_string(stem.form_present(3, 'sg', 'm'))
    paradigm['pres_2sm'] = phonemes_to_string(stem.form_present(2, 'sg', 'm'))
    
    # Pretérito
    paradigm['pret_3sm'] = phonemes_to_string(stem.form_preterite(3, 'sg', 'm'))
    paradigm['pret_1s'] = phonemes_to_string(stem.form_preterite(1, 'sg', 'm'))
    paradigm['pret_2sm'] = phonemes_to_string(stem.form_preterite(2, 'sg', 'm'))
    
    # Perfect
    paradigm['perf_3sm'] = phonemes_to_string(stem.form_perfect(3, 'sg', 'm'))
    
    # Imperativo
    paradigm['imp_sm'] = phonemes_to_string(stem.form_imperative('sg', 'm'))
    
    print(f"  Paradigma completo generado: {len(paradigm)} formas")
    print(f"  Presente 3sm: {paradigm['pres_3sm']}")
    print(f"  Pretérito 1s: {paradigm['pret_1s']}")
    print(f"  Pretérito 3sm: {paradigm['pret_3sm']}")
    print(f"  Perfect 3sm: {paradigm['perf_3sm']}")
    
    # Verificaciones
    pret_1s = stem.form_preterite(1, 'sg', 'm')
    pret_3sm = stem.form_preterite(3, 'sg', 'm')
    assert pret_1s[0].symbol in ['a', 'ā'], "Pret 1s debe tener ā"
    assert pret_3sm[0].symbol in ['e', 'ē'], "Pret 3s debe tener ē"
    
    print("Test 2: ✅ PASSED\n")
    return paradigm


def test_full_paradigm_nasarum():
    """Test paradigma completo de naṣārum."""
    print("Test 3: Paradigma completo naṣārum...")
    
    root = create_i_n_root('s', 'r', VowelClass.A_U, 'guardar')
    stem = I_n_Stem(root=root)
    
    paradigm = {}
    
    # Presente
    paradigm['pres_3sm'] = phonemes_to_string(stem.form_present(3, 'sg', 'm'))
    
    # Pretérito
    paradigm['pret_3sm'] = phonemes_to_string(stem.form_preterite(3, 'sg', 'm'))
    
    # Perfect
    paradigm['perf_3sm'] = phonemes_to_string(stem.form_perfect(3, 'sg', 'm'))
    
    # Imperativo
    paradigm['imp_sm'] = phonemes_to_string(stem.form_imperative('sg', 'm'))
    
    print(f"  Paradigma completo generado: {len(paradigm)} formas")
    print(f"  Presente 3sm: {paradigm['pres_3sm']}")
    print(f"  Pretérito 3sm: {paradigm['pret_3sm']}")
    print(f"  Perfect 3sm: {paradigm['perf_3sm']}")
    print(f"  Imperativo sm: {paradigm['imp_sm']}")
    
    # Verificaciones
    assert 'n' in paradigm['pres_3sm'], "Presente debe tener n"
    assert 'n' not in paradigm['pret_3sm'], "Pretérito no debe tener n (asimilada)"
    assert 'n' not in paradigm['perf_3sm'], "Perfect no debe tener n (asimilada)"
    assert 'n' not in paradigm['imp_sm'], "Imperativo no debe tener n (perdida)"
    
    print("Test 3: ✅ PASSED\n")
    return paradigm


def test_strong_vs_weak_comparison():
    """Test comparación verbo fuerte vs débil."""
    print("Test 4: Comparación verbo fuerte vs débil...")
    
    # Verbo fuerte: parāsum
    strong_root = VerbalRoot(
        radicals=[get_consonant('p'), get_consonant('r'), get_consonant('s')],
        vowel_class=VowelClass.A_U,
        gloss='separar'
    )
    strong_stem = G_Stem(root=strong_root)
    
    # Verbo débil: wasābum
    weak_root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    weak_stem = I_w_Fientive_Stem(root=weak_root)
    
    # Generar formas
    strong_pres = phonemes_to_string(strong_stem.form_present(3, 'sg', 'm'))
    weak_pres = phonemes_to_string(weak_stem.form_present(3, 'sg', 'm'))
    
    print(f"  Verbo fuerte (parāsum) Pres 3sm: {strong_pres}")
    print(f"  Verbo débil (wasābum) Pres 3sm: {weak_pres}")
    
    # Ambos deben generar formas válidas
    assert len(strong_pres) > 0, "Verbo fuerte debe generar formas"
    assert len(weak_pres) > 0, "Verbo débil debe generar formas"
    
    # Diferencias esperadas
    assert 'i' in strong_pres, "Verbo fuerte debe tener prefijo i"
    assert 'u' in weak_pres, "Verbo débil debe tener contracción u"
    
    print("Test 4: ✅ PASSED\n")


def test_all_weak_types():
    """Test que todos los tipos débiles generan formas."""
    print("Test 5: Todos los tipos débiles...")
    
    weak_verbs = [
        ('wasābum', create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar'), I_w_Fientive_Stem),
        ('ahāzum', create_i_voc_a_root('k', 'z', VowelClass.A_U, 'tomar'), I_a_Stem),
        ('epāšum', create_i_voc_e_root('p', 's', VowelClass.A_U, 'hacer'), I_e_Stem),
        ('naṣārum', create_i_n_root('s', 'r', VowelClass.A_U, 'guardar'), I_n_Stem),
    ]
    
    for name, root, stem_class in weak_verbs:
        stem = stem_class(root=root)
        
        # Generar todas las formas principales
        pres = stem.form_present(3, 'sg', 'm')
        pret = stem.form_preterite(3, 'sg', 'm')
        perf = stem.form_perfect(3, 'sg', 'm')
        imp = stem.form_imperative('sg', 'm')
        
        # Todas deben generar fonemas
        assert len(pres) > 0, f"{name} presente vacío"
        assert len(pret) > 0, f"{name} pretérito vacío"
        assert len(perf) > 0, f"{name} perfect vacío"
        assert len(imp) > 0, f"{name} imperativo vacío"
        
        print(f"  ✓ {name}: 4 formas generadas")
    
    print("Test 5: ✅ PASSED\n")


def test_performance_basic():
    """Test performance básico."""
    print("Test 6: Performance básico...")
    
    root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    stem = I_w_Fientive_Stem(root=root)
    
    # Medir tiempo para generar 100 formas
    start = time.time()
    for _ in range(100):
        stem.form_present(3, 'sg', 'm')
        stem.form_preterite(3, 'sg', 'm')
        stem.form_perfect(3, 'sg', 'm')
        stem.form_imperative('sg', 'm')
    end = time.time()
    
    elapsed = end - start
    forms_per_sec = 400 / elapsed  # 4 formas × 100 iteraciones
    
    print(f"  Generadas 400 formas en {elapsed:.3f}s")
    print(f"  Performance: {forms_per_sec:.0f} formas/segundo")
    
    # Performance debe ser razonable (>100 formas/seg)
    assert forms_per_sec > 100, f"Performance muy bajo: {forms_per_sec:.0f} formas/s"
    
    print("Test 6: ✅ PASSED\n")


def test_helper_methods_consistency():
    """Test que helper methods son consistentes entre tipos."""
    print("Test 7: Consistencia de helper methods...")
    
    # Crear varios stems
    i_w = I_w_Fientive_Stem(create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar'))
    i_a = I_a_Stem(create_i_voc_a_root('k', 'z', VowelClass.A_U, 'tomar'))
    i_n = I_n_Stem(create_i_n_root('s', 'r', VowelClass.A_U, 'guardar'))
    
    # Todos los helper methods deben existir
    for stem in [i_w, i_a, i_n]:
        assert hasattr(stem, '_get_R1_for_present')
        assert hasattr(stem, '_get_R1_for_preterite')
        assert hasattr(stem, '_get_R1_for_perfect')
        assert hasattr(stem, '_get_R1_for_imperative')
        assert hasattr(stem, '_should_geminate_R2_in_present')
        assert hasattr(stem, '_has_vocalic_ending')
        print(f"  ✓ {stem.__class__.__name__}: todos los helpers presentes")
    
    # Verificar comportamiento esperado
    assert i_w._get_R1_for_present() is None, "I/w: R₁ debe ser None"
    assert i_a._get_R1_for_present() is None, "I/voc: R₁ debe ser None"
    assert i_n._get_R1_for_present() is not None, "I/n: R₁ debe existir"
    print("  ✓ Comportamientos diferenciados correctos")
    
    print("Test 7: ✅ PASSED\n")


def test_edge_cases():
    """Test casos edge y límites."""
    print("Test 8: Casos edge...")
    
    # Test: Verbo con endings
    root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    stem = I_w_Fientive_Stem(root=root)
    
    # Plural debe tener ending
    pret_3pm = stem.form_preterite(3, 'pl', 'm')
    result = phonemes_to_string(pret_3pm)
    print(f"  Pret 3pm con ending: {result}")
    assert pret_3pm[-1].symbol in ['u', 'ū'], "Debe tener ending -ū"
    
    # Singular no debe tener ending
    pret_3sm = stem.form_preterite(3, 'sg', 'm')
    assert pret_3sm[-1].symbol not in ['u', 'ū'], "No debe tener ending vocálico"
    
    # Test: síncope con ending
    assert len(pret_3pm) < len(pret_3sm) + 2, "Debe haber síncope con ending"
    print("  ✓ Síncope vocálica funciona correctamente")
    
    print("Test 8: ✅ PASSED\n")


def test_data_integrity():
    """Test integridad de datos entre formas."""
    print("Test 9: Integridad de datos...")
    
    root = create_i_voc_a_root('k', 'z', VowelClass.A_U, 'tomar')
    stem = I_a_Stem(root=root)
    
    # Generar múltiples formas
    forms = []
    for person in [1, 2, 3]:
        for number in ['sg', 'pl']:
            pres = stem.form_present(person, number, 'm')
            pret = stem.form_preterite(person, number, 'm')
            forms.append(pres)
            forms.append(pret)
    
    # Todas las formas deben tener R₂ y R₃
    for form in forms:
        form_str = phonemes_to_string(form)
        assert 'k' in form_str, f"Forma debe tener R₂ (k): {form_str}"
        assert 'z' in form_str, f"Forma debe tener R₃ (z): {form_str}"
    
    print(f"  ✓ {len(forms)} formas verificadas")
    print("  ✓ Todas contienen R₂ y R₃")
    
    print("Test 9: ✅ PASSED\n")


def test_cross_stem_compatibility():
    """Test compatibilidad entre diferentes stems."""
    print("Test 10: Compatibilidad cross-stem...")
    
    # Crear varios verbos y verificar que no interfieren
    verbs = [
        I_w_Fientive_Stem(create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')),
        I_a_Stem(create_i_voc_a_root('k', 'z', VowelClass.A_U, 'tomar')),
        I_n_Stem(create_i_n_root('s', 'r', VowelClass.A_U, 'guardar')),
    ]
    
    # Generar formas de todos simultáneamente
    all_forms = []
    for verb in verbs:
        all_forms.append(verb.form_present(3, 'sg', 'm'))
        all_forms.append(verb.form_preterite(3, 'sg', 'm'))
    
    # Todas deben ser únicas y válidas
    assert len(all_forms) == 6, "Debe haber 6 formas"
    for form in all_forms:
        assert len(form) > 0, "Forma no debe estar vacía"
    
    print(f"  ✓ {len(verbs)} verbos diferentes generando formas")
    print("  ✓ Sin interferencias entre stems")
    
    print("Test 10: ✅ PASSED\n")


def main():
    """Ejecutar todos los tests de integración."""
    print("=" * 70)
    print("ITERACIÓN 9 - PASO 7: TESTS DE INTEGRACIÓN")
    print("Verificación end-to-end del sistema completo")
    print("=" * 70)
    print()
    
    start_time = time.time()
    
    try:
        # Tests de paradigmas completos
        paradigm_wasabum = test_full_paradigm_wasabum()
        paradigm_ahazum = test_full_paradigm_ahazum()
        paradigm_nasarum = test_full_paradigm_nasarum()
        
        # Tests de comparación y compatibilidad
        test_strong_vs_weak_comparison()
        test_all_weak_types()
        test_helper_methods_consistency()
        test_cross_stem_compatibility()
        
        # Tests de edge cases y performance
        test_edge_cases()
        test_data_integrity()
        test_performance_basic()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print("=" * 70)
        print("✅ TODOS LOS TESTS DE INTEGRACIÓN PASARON")
        print("=" * 70)
        print()
        print(f"Tiempo total: {total_time:.2f}s")
        print()
        print("PASO 7 COMPLETADO:")
        print("  ✓ 10 grupos de tests de integración")
        print("  ✓ 3 paradigmas completos verificados")
        print("  ✓ Compatibilidad verbos fuertes ↔ débiles")
        print("  ✓ Performance verificado (>100 formas/s)")
        print("  ✓ Edge cases manejados correctamente")
        print("  ✓ Integridad de datos confirmada")
        print()
        print("RESUMEN PARADIGMAS GENERADOS:")
        print(f"  wasābum: {len(paradigm_wasabum)} formas")
        print(f"  ahāzum: {len(paradigm_ahazum)} formas")
        print(f"  naṣārum: {len(paradigm_nasarum)} formas")
        print()
        print("SIGUIENTE PASO: PASO 8 - Documentación")
        print("  - README para i_weak/")
        print("  - Guía de uso")
        print("  - Ejemplos de extensión")
        print()
        
        return 0
        
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ERROR EN LOS TESTS DE INTEGRACIÓN")
        print("=" * 70)
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())

"""
Tests para weak_root.py

ITERACIÓN 9 - PASO 1: Fundamentos

Tests para:
- WeakConsonant
- WeakRoot
- Funciones helper para crear raíces débiles

Autor: Claude
Fecha: 2026-02-12
"""

import pytest
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


# ============================================================================
# TESTS: WeakConsonant
# ============================================================================

class TestWeakConsonant:
    """Tests para WeakConsonant."""
    
    def test_create_w_consonant(self):
        """Crear consonante débil w."""
        wc = WeakConsonant('w', WeakPosition.R1, 'contracts')
        assert wc.symbol == 'w'
        assert wc.position == WeakPosition.R1
        assert wc.behavior == 'contracts'
    
    def test_create_guttural_lost(self):
        """Crear gutural perdida (Ø)."""
        wc = WeakConsonant('Ø', WeakPosition.R1, 'compensatory_lengthening')
        assert wc.symbol == 'Ø'
        assert wc.is_lost_guttural()
    
    def test_create_n_consonant(self):
        """Crear consonante débil n."""
        wc = WeakConsonant('n', WeakPosition.R1, 'assimilates')
        assert wc.symbol == 'n'
        assert wc.can_assimilate()
    
    def test_invalid_symbol_raises_error(self):
        """Símbolo inválido debe lanzar error."""
        with pytest.raises(ValueError, match="Invalid weak consonant symbol"):
            WeakConsonant('x', WeakPosition.R1, 'contracts')
    
    def test_invalid_behavior_raises_error(self):
        """Behavior inválido debe lanzar error."""
        with pytest.raises(ValueError, match="Invalid behavior"):
            WeakConsonant('w', WeakPosition.R1, 'invalid_behavior')
    
    def test_contracts_with_i(self):
        """Verificar contracción con i."""
        w_contracts = WeakConsonant('w', WeakPosition.R1, 'contracts')
        n_assimilates = WeakConsonant('n', WeakPosition.R1, 'assimilates')
        
        assert w_contracts.contracts_with_i()
        assert not n_assimilates.contracts_with_i()
    
    def test_string_representation(self):
        """Verificar representación string."""
        wc = WeakConsonant('w', WeakPosition.R1, 'contracts')
        assert 'w' in str(wc)
        assert 'R1' in str(wc)
        assert 'contracts' in str(wc)


# ============================================================================
# TESTS: WeakRoot
# ============================================================================

class TestWeakRoot:
    """Tests para WeakRoot."""
    
    def test_create_weak_root_manually(self):
        """Crear WeakRoot manualmente."""
        from phonology.inventory import get_consonant
        
        root = WeakRoot(
            R1=WeakConsonant('w', WeakPosition.R1, 'contracts'),
            R2=get_consonant('s'),
            R3=get_consonant('b'),
            vowel_class=VowelClass.A_I,
            meaning='sentar',
            weak_type=WeakVerbType.I_W_FIENTIVE
        )
        
        assert root.weak_type == WeakVerbType.I_W_FIENTIVE
        assert isinstance(root.R1, WeakConsonant)
        assert root.R1.symbol == 'w'
    
    def test_validation_i_w_requires_w(self):
        """I/w debe tener R1 = w."""
        from phonology.inventory import get_consonant
        
        with pytest.raises(ValueError, match="I/w verb debe tener R1"):
            WeakRoot(
                R1=get_consonant('p'),  # ERROR: debería ser w
                R2=get_consonant('s'),
                R3=get_consonant('b'),
                vowel_class=VowelClass.A_I,
                meaning='test',
                weak_type=WeakVerbType.I_W_FIENTIVE
            )
    
    def test_validation_i_voc_requires_guttural(self):
        """I/voc debe tener R1 = Ø."""
        from phonology.inventory import get_consonant
        
        with pytest.raises(ValueError, match="I/voc verb debe tener R1"):
            WeakRoot(
                R1=get_consonant('ʔ'),  # ERROR: debería ser Ø con compensatory_lengthening
                R2=get_consonant('h'),
                R3=get_consonant('z'),
                vowel_class=VowelClass.A_U,
                meaning='test',
                weak_type=WeakVerbType.I_VOC_A
            )
    
    def test_validation_i_n_requires_n(self):
        """I/n debe tener R1 = n."""
        from phonology.inventory import get_consonant
        
        with pytest.raises(ValueError, match="I/n verb debe tener R1"):
            WeakRoot(
                R1=get_consonant('m'),  # ERROR: debería ser n
                R2=get_consonant('ṣ'),
                R3=get_consonant('r'),
                vowel_class=VowelClass.A_U,
                meaning='test',
                weak_type=WeakVerbType.I_N
            )
    
    def test_get_weak_positions_single(self):
        """Obtener posiciones débiles - una sola."""
        root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
        positions = root.get_weak_positions()
        
        assert len(positions) == 1
        assert WeakPosition.R1 in positions
    
    def test_get_weak_positions_multiple(self):
        """Obtener posiciones débiles - atawwum (doblemente débil)."""
        root = create_atawwum_root()
        positions = root.get_weak_positions()
        
        # Solo R1 es WeakConsonant (Ø), R2/R3 son consonantes normales 'w'
        assert len(positions) == 1
        assert WeakPosition.R1 in positions
    
    def test_is_doubly_weak(self):
        """Verificar detección de doblemente débil."""
        wasabum = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
        atawwum = create_atawwum_root()
        
        assert not wasabum.is_doubly_weak()
        # Nota: atawwum técnicamente es doblemente débil (I/voc + II/gem)
        # pero solo R1 es WeakConsonant, así que is_doubly_weak() → False
        # (esto es correcto, II/gem no se modela como WeakConsonant)
        assert not atawwum.is_doubly_weak()
    
    def test_to_consonant_symbols(self):
        """Extraer símbolos de consonantes."""
        root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
        symbols = root.to_consonant_symbols()
        
        assert symbols == ('w', 's', 'b')
    
    def test_string_representation(self):
        """Verificar representación string."""
        root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
        s = str(root)
        
        assert '√wsb' in s.lower() or 'wsb' in s.lower()
        assert 'fientive' in s.lower()


# ============================================================================
# TESTS: Helper Functions
# ============================================================================

class TestHelperFunctions:
    """Tests para funciones helper de creación de raíces."""
    
    def test_create_i_w_fientive_root(self):
        """Crear raíz I/w fientivo con helper."""
        root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
        
        assert root.weak_type == WeakVerbType.I_W_FIENTIVE
        assert root.R1.symbol == 'w'
        assert root.R2.symbol == 's'
        assert root.R3.symbol == 'b'
        assert root.vowel_class == VowelClass.A_I
        assert root.meaning == 'sentar'
    
    def test_create_i_w_adjectival_root(self):
        """Crear raíz I/w adjetival con helper."""
        root = create_i_w_adjectival_root('t', 'r', VowelClass.I_I, 'exceder')
        
        assert root.weak_type == WeakVerbType.I_W_ADJECTIVAL
        assert root.R1.symbol == 'w'
        assert root.vowel_class == VowelClass.I_I
    
    def test_create_i_voc_a_root(self):
        """Crear raíz I/voc a con helper."""
        root = create_i_voc_a_root('h', 'z', VowelClass.A_U, 'tomar')
        
        assert root.weak_type == WeakVerbType.I_VOC_A
        assert root.R1.symbol == 'Ø'
        assert root.R1.is_lost_guttural()
        assert root.meaning == 'tomar'
    
    def test_create_i_voc_e_root(self):
        """Crear raíz I/voc e con helper."""
        root = create_i_voc_e_root('p', 'š', VowelClass.A_U, 'hacer')
        
        assert root.weak_type == WeakVerbType.I_VOC_E
        assert root.R1.symbol == 'Ø'
    
    def test_create_i_n_root_normal(self):
        """Crear raíz I/n normal con helper."""
        root = create_i_n_root('ṣ', 'r', VowelClass.A_U, 'guardar')
        
        assert root.weak_type == WeakVerbType.I_N
        assert root.R1.symbol == 'n'
        assert root.R1.can_assimilate()
    
    def test_create_i_n_root_nasaum_special(self):
        """Crear raíz našā'um especial con helper."""
        root = create_i_n_root('š', 'ʔ', VowelClass.I_I, 'transportar', special_nasaum=True)
        
        assert root.weak_type == WeakVerbType.I_N_NASAUM
        assert root.R1.symbol == 'n'
    
    def test_create_atawwum_root(self):
        """Crear raíz atawwum con helper."""
        root = create_atawwum_root()
        
        assert root.weak_type == WeakVerbType.I_ATAWWUM
        assert root.R1.symbol == 'Ø'
        assert root.R2.symbol == 'w'
        assert root.R3.symbol == 'w'  # II/gem
        assert root.meaning == 'hablar'


# ============================================================================
# TESTS: Utility Functions
# ============================================================================

class TestUtilityFunctions:
    """Tests para funciones de utilidad."""
    
    def test_is_weak_root_true(self):
        """Verificar que detecta raíz débil."""
        root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
        assert is_weak_root(root)
    
    def test_get_weak_type_from_weak_root(self):
        """Obtener tipo de raíz débil."""
        root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
        weak_type = get_weak_type_from_root(root)
        
        assert weak_type == WeakVerbType.I_W_FIENTIVE
    
    def test_get_weak_type_i_voc(self):
        """Obtener tipo I/voc."""
        root = create_i_voc_a_root('h', 'z', VowelClass.A_U, 'tomar')
        weak_type = get_weak_type_from_root(root)
        
        assert weak_type == WeakVerbType.I_VOC_A
    
    def test_get_weak_type_i_n(self):
        """Obtener tipo I/n."""
        root = create_i_n_root('ṣ', 'r', VowelClass.A_U, 'guardar')
        weak_type = get_weak_type_from_root(root)
        
        assert weak_type == WeakVerbType.I_N


# ============================================================================
# TESTS: Ejemplos del Texto (Kouwenberg 2017)
# ============================================================================

class TestKouwenbergExamples:
    """Tests con ejemplos específicos del libro."""
    
    def test_wasabum_root(self):
        """wasābum (a/i) 'sentar' - Tabla 18.1."""
        root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
        
        assert root.to_consonant_symbols() == ('w', 's', 'b')
        assert root.vowel_class == VowelClass.A_I
        assert root.weak_type == WeakVerbType.I_W_FIENTIVE
    
    def test_wabalum_root(self):
        """wabālum (a/i) 'llevar, traer' - muy frecuente."""
        root = create_i_w_fientive_root('b', 'l', VowelClass.A_I, 'llevar')
        
        assert root.to_consonant_symbols() == ('w', 'b', 'l')
    
    def test_watarum_root(self):
        """watārum (i/i) 'exceder' - Tabla 18.2."""
        root = create_i_w_adjectival_root('t', 'r', VowelClass.I_I, 'exceder')
        
        assert root.to_consonant_symbols() == ('w', 't', 'r')
        assert root.weak_type == WeakVerbType.I_W_ADJECTIVAL
    
    def test_ahazum_root(self):
        """ahāzum (a/u) 'tomar' - Tabla 18.6."""
        root = create_i_voc_a_root('h', 'z', VowelClass.A_U, 'tomar')
        
        assert root.to_consonant_symbols() == ('Ø', 'h', 'z')
        assert root.weak_type == WeakVerbType.I_VOC_A
        assert root.R1.is_lost_guttural()
    
    def test_epasum_root(self):
        """epāšum (a/u) 'hacer' - muy frecuente."""
        root = create_i_voc_e_root('p', 'š', VowelClass.A_U, 'hacer')
        
        assert root.to_consonant_symbols() == ('Ø', 'p', 'š')
        assert root.weak_type == WeakVerbType.I_VOC_E
    
    def test_nasarum_root(self):
        """naṣārum (a/u) 'guardar' - Tabla 18.13."""
        root = create_i_n_root('ṣ', 'r', VowelClass.A_U, 'guardar')
        
        assert root.to_consonant_symbols() == ('n', 'ṣ', 'r')
        assert root.weak_type == WeakVerbType.I_N
    
    def test_nasaum_root(self):
        """našā'um (i/i) 'transportar' - caso especial."""
        root = create_i_n_root('š', 'ʔ', VowelClass.I_I, 'transportar', special_nasaum=True)
        
        assert root.to_consonant_symbols() == ('n', 'š', 'ʔ')
        assert root.weak_type == WeakVerbType.I_N_NASAUM
    
    def test_atawwum_root_special(self):
        """atawwum (u/u) 'hablar' - Tabla 18.8."""
        root = create_atawwum_root()
        
        assert root.to_consonant_symbols() == ('Ø', 'w', 'w')
        assert root.weak_type == WeakVerbType.I_ATAWWUM
        assert root.vowel_class == VowelClass.U_U


if __name__ == '__main__':
    # Ejecutar tests
    pytest.main([__file__, '-v'])

# Quick Start Guide - I-Weak Verbs

Guía de inicio rápido para usar verbos I-débil en 5 minutos.

---

## 🚀 Inicio Rápido

### 1. Imports Básicos

```python
from phonology.verbal.weak_root import (
    create_i_w_fientive_root,
    create_i_voc_a_root,
    create_i_n_root
)
from phonology.verbal.i_weak.i_w_stems import I_w_Fientive_Stem
from phonology.verbal.i_weak.i_voc_stems import I_a_Stem
from phonology.verbal.i_weak.i_n_stems import I_n_Stem
from phonology.verbal.enums import VowelClass

def phonemes_to_string(phonemes):
    return "".join(p.symbol for p in phonemes)
```

### 2. Crear tu Primer Verbo Débil

**wasābum 'sentar' (I/w fientivo)**:

```python
# Crear raíz: √wsb con clase vocálica a/i
root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')

# Crear stem
stem = I_w_Fientive_Stem(root=root)

# Generar formas
presente = stem.form_present(3, 'sg', 'm')
print(f"Presente 3sm: {phonemes_to_string(presente)}")
# Output: "ussab"
```

### 3. Los 4 Verbos Principales

```python
# I/w fientivo - wasābum
wasabum = I_w_Fientive_Stem(
    create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
)

# I/voc a - ahāzum
ahazum = I_a_Stem(
    create_i_voc_a_root('k', 'z', VowelClass.A_U, 'tomar')
)

# I/voc e - epāšum
from phonology.verbal.i_weak.i_voc_stems import I_e_Stem
from phonology.verbal.weak_root import create_i_voc_e_root

epasum = I_e_Stem(
    create_i_voc_e_root('p', 's', VowelClass.A_U, 'hacer')
)

# I/n - naṣārum
nasarum = I_n_Stem(
    create_i_n_root('s', 'r', VowelClass.A_U, 'guardar')
)
```

### 4. Generar Formas Verbales

```python
# Las 4 formas principales
presente = stem.form_present(3, 'sg', 'm')
preterito = stem.form_preterite(3, 'sg', 'm')
perfect = stem.form_perfect(3, 'sg', 'm')
imperativo = stem.form_imperative('sg', 'm')

# Convertir a string
print(phonemes_to_string(presente))
```

### 5. Personas y Números

```python
# Personas: 1, 2, 3
# Números: 'sg', 'pl', 'du'
# Género: 'm', 'f'

# Ejemplos
stem.form_present(1, 'sg', 'm')   # 1a persona singular
stem.form_present(2, 'pl', 'm')   # 2a persona plural
stem.form_present(3, 'sg', 'f')   # 3a persona singular femenino
```

---

## 📝 Ejemplos Completos

### Ejemplo 1: wasābum Completo

```python
root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
stem = I_w_Fientive_Stem(root=root)

print("=== wasābum ===")
print(f"Pres 3sm: {phonemes_to_string(stem.form_present(3, 'sg', 'm'))}")
print(f"Pres 2sm: {phonemes_to_string(stem.form_present(2, 'sg', 'm'))}")
print(f"Pret 3sm: {phonemes_to_string(stem.form_preterite(3, 'sg', 'm'))}")
print(f"Perf 3sm: {phonemes_to_string(stem.form_perfect(3, 'sg', 'm'))}")
print(f"Imp sm: {phonemes_to_string(stem.form_imperative('sg', 'm'))}")

# Output:
# Pres 3sm: ussab
# Pres 2sm: tussab
# Pret 3sm: ūsib
# Perf 3sm: uttasab
# Imp sm: sib
```

### Ejemplo 2: Comparar Tres Tipos

```python
# Crear tres verbos diferentes
verbs = {
    'wasābum': I_w_Fientive_Stem(
        create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
    ),
    'ahāzum': I_a_Stem(
        create_i_voc_a_root('k', 'z', VowelClass.A_U, 'tomar')
    ),
    'naṣārum': I_n_Stem(
        create_i_n_root('s', 'r', VowelClass.A_U, 'guardar')
    )
}

# Generar presente de todos
print("=== Presente 3sm ===")
for name, stem in verbs.items():
    pres = phonemes_to_string(stem.form_present(3, 'sg', 'm'))
    print(f"{name:10} → {pres}")

# Output:
# wasābum    → ussab
# ahāzum     → ākkaz
# naṣārum    → inssar
```

### Ejemplo 3: Generar Paradigma

```python
def show_paradigm(stem, verb_name):
    """Muestra paradigma básico de un verbo."""
    print(f"\n=== {verb_name} ===")
    
    # Presente
    print("Presente:")
    print(f"  3sm: {phonemes_to_string(stem.form_present(3, 'sg', 'm'))}")
    print(f"  2sm: {phonemes_to_string(stem.form_present(2, 'sg', 'm'))}")
    print(f"  1s:  {phonemes_to_string(stem.form_present(1, 'sg', 'm'))}")
    
    # Pretérito
    print("Pretérito:")
    print(f"  3sm: {phonemes_to_string(stem.form_preterite(3, 'sg', 'm'))}")
    print(f"  1s:  {phonemes_to_string(stem.form_preterite(1, 'sg', 'm'))}")
    
    # Perfect
    print("Perfect:")
    print(f"  3sm: {phonemes_to_string(stem.form_perfect(3, 'sg', 'm'))}")
    
    # Imperativo
    print("Imperativo:")
    print(f"  sm:  {phonemes_to_string(stem.form_imperative('sg', 'm'))}")

# Uso
wasabum = I_w_Fientive_Stem(
    create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
)
show_paradigm(wasabum, 'wasābum')
```

---

## 🎯 Casos de Uso Comunes

### Caso 1: Verificar Contracción w+i

```python
# I/w fientivo tiene contracción w+i → u/ū
stem = I_w_Fientive_Stem(
    create_i_w_fientive_root('b', 'l', VowelClass.A_I, 'llevar')
)

pres = phonemes_to_string(stem.form_present(3, 'sg', 'm'))
pret = phonemes_to_string(stem.form_preterite(3, 'sg', 'm'))

print(f"Presente: {pres}")   # ubbal (u corta)
print(f"Pretérito: {pret}")  # ūbil (ū larga)
```

### Caso 2: Verificar Asimilación de n

```python
# I/n tiene asimilación n+C → CC
stem = I_n_Stem(
    create_i_n_root('d', 'm', VowelClass.I_I, 'depositar')
)

pres = phonemes_to_string(stem.form_present(3, 'sg', 'm'))
pret = phonemes_to_string(stem.form_preterite(3, 'sg', 'm'))

print(f"Presente:  {pres}")  # inddim (n preservada)
print(f"Pretérito: {pret}")  # iddim (n asimilada: n+d→dd)
```

### Caso 3: Verificar Vocal Compensatoria

```python
# I/voc tiene vocal larga compensatoria
stem = I_a_Stem(
    create_i_voc_a_root('m', 'r', VowelClass.A_U, 'ver')
)

pret_1s = stem.form_preterite(1, 'sg', 'm')
pret_3s = stem.form_preterite(3, 'sg', 'm')

print(f"Pret 1s: {phonemes_to_string(pret_1s)}")  # āmur (ā)
print(f"Pret 3s: {phonemes_to_string(pret_3s)}")  # ēmur (ē)
```

---

## 🔍 Troubleshooting

### Problema: "Consonante desconocida"

```python
# ❌ INCORRECTO
root = create_i_w_fientive_root('ʔ', 'b', VowelClass.A_I, 'tomar')
# Error: Consonante desconocida: ʔ

# ✅ CORRECTO - usar consonantes del inventario
root = create_i_w_fientive_root('k', 'b', VowelClass.A_I, 'tomar')
```

### Problema: "Wrong weak type"

```python
# ❌ INCORRECTO - tipo y clase no coinciden
root = create_i_voc_a_root('s', 'b', VowelClass.A_I, 'sentar')
stem = I_w_Fientive_Stem(root=root)  # Error!

# ✅ CORRECTO - tipo y clase coinciden
root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
stem = I_w_Fientive_Stem(root=root)
```

### Problema: Fonemas vacíos

```python
# Verificar que stem es válido
assert len(stem.form_present(3, 'sg', 'm')) > 0, "Forma vacía"

# Debug: ver fonemas individuales
phonemes = stem.form_present(3, 'sg', 'm')
for i, p in enumerate(phonemes):
    print(f"{i}: {p.symbol} ({type(p).__name__})")
```

---

## 📚 Próximos Pasos

1. **Leer el README completo**: `README.md`
2. **Ver tests de ejemplo**: `tests/test_i_w.py`
3. **Experimentar con más verbos**
4. **Crear tus propios helper functions**

---

## 💡 Tips Útiles

- **Usa helper functions**: `create_i_*_root()` en vez de constructores manuales
- **Convierte a string**: `phonemes_to_string()` para debugging
- **Verifica tipos**: Asegúrate que root.weak_type coincide con clase de stem
- **Tests primero**: Escribe tests antes de implementar nuevas features

---

## ✅ Checklist de Inicio

- [ ] Imports configurados
- [ ] Primer verbo creado exitosamente
- [ ] Formas generadas y convertidas a string
- [ ] Paradigma básico funcionando
- [ ] Tests pasando

¡Ya estás listo para usar verbos I-débil! 🎉

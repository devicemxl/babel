# Old Assyrian Morphophonology System

Sistema computacional completo de morfología y fonología del Old Assyrian.

**Versión**: Iteraciones 1-9 Completas  
**Fecha**: 2026-02-12  
**Autor**: David (con Claude)

---

## ✅ COMPLETADO (Iteraciones 1-9)

### Iter 1-5: Sistema Fonológico
- Inventario fonológico completo
- Procesos vocálicos
- Asimilación consonántica
- Sistema silábico
- Consonantes débiles

### Iter 6-7: Morfología Nominal
- Sistema de casos
- Número y estado
- Posesivos
- Derivación
- Patrones

### Iter 8: Verbos Fuertes
- G, D, Š, N stems
- Sistema completo

### ✅ Iter 9: Verbos I-débil (NUEVA)
- **11 verbos funcionando**
- **7 tipos implementados**
- **Performance >400K formas/seg**
- **100% tests pasando**

Ver `ITERACION_9_COMPLETA.md` para detalles.

---

## 📂 Estructura

```
phonology/
├── nominal/           # Iter 6-7
├── verbal/            # Iter 8-9
│   └── i_weak/        # ✅ NUEVO
└── [otros módulos]
```

---

## 🚀 Uso Rápido

```python
# Verbo I-débil (Iter 9)
from phonology.verbal.weak_root import create_i_w_fientive_root
from phonology.verbal.i_weak.i_w_stems import I_w_Fientive_Stem
from phonology.verbal.enums import VowelClass

root = create_i_w_fientive_root('s', 'b', VowelClass.A_I, 'sentar')
stem = I_w_Fientive_Stem(root=root)
presente = stem.form_present(3, 'sg', 'm')  # uššab
```

Ver `phonology/verbal/i_weak/QUICKSTART.md`

---

**Próxima**: Iteración 10 - Verbos II-débil

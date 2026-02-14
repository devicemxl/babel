"""Script para regenerar todos los stems con estructura correcta."""

# Plantilla base para cada stem
STEM_TEMPLATE = '''@dataclass
class {class_name}(VerbalStem):
    """{docstring}"""
    
    stem_type: StemType = field(default=StemType.{stem_enum})
    {extra_fields}
    def __post_init__(self):
        """Inicializa {class_name} con valores por defecto."""
        super().__post_init__(){extra_init}
'''

# Datos de cada stem
stems_data = {
    'd_stem.py': [
        {
            'class_name': 'D_Stem',
            'stem_enum': 'D',
            'docstring': 'D-stem del Old Assyrian. Doubled stem con geminación de R₂.',
            'extra_fields': '\n    d_function: Optional[D_Function] = None\n    ',
            'extra_init': ''
        },
        {
            'class_name': 'Dt_Stem',
            'stem_enum': 'DT',
            'docstring': 'Dt-stem del Old Assyrian. D-stem con infijo -t-.',
            'extra_fields': '',
            'extra_init': ''
        },
        {
            'class_name': 'Dtn_Stem',
            'stem_enum': 'DTN',
            'docstring': 'Dtn-stem del Old Assyrian. D-stem pluraccional.',
            'extra_fields': '',
            'extra_init': '\n        object.__setattr__(self, \'semantic_function\', SemanticFunction.PLURACTIONAL)'
        },
    ],
    'sh_stem.py': [
        {
            'class_name': 'Sh_Stem',
            'stem_enum': 'SH',
            'docstring': 'Š-stem del Old Assyrian. Stem causativo con prefijo š-.',
            'extra_fields': '\n    sh_function: Optional[Sh_Function] = None\n    ',
            'extra_init': ''
        },
        {
            'class_name': 'Sht1_Stem',
            'stem_enum': 'SHT1',
            'docstring': 'Št₁-stem del Old Assyrian. Pasivo/reflexivo de Š.',
            'extra_fields': '',
            'extra_init': ''
        },
        {
            'class_name': 'Sht2_Stem',
            'stem_enum': 'SHT2',
            'docstring': 'Št₂-stem del Old Assyrian. Št léxico.',
            'extra_fields': '',
            'extra_init': ''
        },
        {
            'class_name': 'Shtn_Stem',
            'stem_enum': 'SHTN',
            'docstring': 'Štn-stem del Old Assyrian. Š pluraccional.',
            'extra_fields': '',
            'extra_init': '\n        object.__setattr__(self, \'semantic_function\', SemanticFunction.PLURACTIONAL)'
        },
    ],
    'n_stem.py': [
        {
            'class_name': 'N_Stem',
            'stem_enum': 'N',
            'docstring': 'N-stem del Old Assyrian. Stem medio/pasivo con prefijo nasal.',
            'extra_fields': '\n    n_function: Optional[N_Function] = None\n    ',
            'extra_init': ''
        },
        {
            'class_name': 'Ntn_Stem',
            'stem_enum': 'NTN',
            'docstring': 'Ntn-stem del Old Assyrian. N pluraccional.',
            'extra_fields': '',
            'extra_init': '\n        object.__setattr__(self, \'semantic_function\', SemanticFunction.PLURACTIONAL)'
        },
    ],
}

import re

for filename, stems in stems_data.items():
    print(f'Procesando {filename}...')
    
    with open(filename, 'r') as f:
        content = f.read()
    
    for stem_info in stems:
        class_name = stem_info['class_name']
        
        # Buscar y reemplazar la clase completa
        # Patrón: desde @dataclass\nclass hasta el siguiente comentario o clase
        pattern = rf'(@dataclass\s+class {class_name}\(VerbalStem\):.*?)((?=@dataclass|# ====|$))'
        
        new_class = STEM_TEMPLATE.format(**stem_info)
        
        # Intentar reemplazo
        new_content = re.sub(pattern, new_class + '\n', content, count=1, flags=re.DOTALL)
        
        if new_content != content:
            content = new_content
            print(f'  ✓ Corregido {class_name}')
        else:
            print(f'  ⚠ No se encontró {class_name} o ya estaba correcto')
    
    # Guardar archivo corregido
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f'✓ {filename} guardado\n')

print('✅ Script completado')

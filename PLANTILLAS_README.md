# Instrucciones para Crear Plantillas Word con Formato Profesional

## Paso 1: Crear Plantillas Base
Crea archivos Word (.docx) en la carpeta `plantillas_word/` con nombres como:
- `plantilla_expediente.docx`
- `plantilla_resolucion_directoral.docx`
- `plantilla_acta_conei.docx`
- `plantilla_conformidad.docx`

## Paso 2: Agregar Elementos Visuales

### Marca de Agua
1. Abre Word → Insertar → Marca de agua
2. Elige "Personalizada" → Selecciona una imagen (logo institucional) o texto
3. Ajusta opacidad al 10-20% para que no interfiera con el texto

### Sellos y Firmas
1. Inserta imágenes de sellos/firmas en posiciones específicas
2. O deja espacios en blanco con líneas punteadas para que se rellenen manualmente
3. Ejemplo: "____________________" con texto encima "Firma del Director"

### Campos para Rellenar
Usa placeholders como `{{campo}}` en el documento. El código los reemplazará automáticamente.

Ejemplos de placeholders:
- `{{numero_expediente}}`
- `{{fecha}}`
- `{{remitente}}`
- `{{destinatario}}`
- `{{asunto}}`
- `{{contenido}}`
- `{{antecedentes}}`
- `{{analisis}}`
- `{{conclusion}}`

Para resoluciones: `{{numero_rd}}`, `{{institucion}}`, `{{visto}}`, etc.

## Paso 3: Formato Profesional
- Usa fuentes oficiales (Arial, Times New Roman)
- Márgenes: Superior/Inferior 2.5cm, Izquierdo/Derecho 3cm
- Encabezados centrados y en negrita
- Espacios para firmas al final

## Paso 4: Guardar
Guarda como .docx en `plantillas_word/`

Una vez creadas las plantillas, el sistema las usará automáticamente para generar documentos con formato profesional.
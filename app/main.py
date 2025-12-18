from flask import Flask, render_template, request, send_file, jsonify
from datetime import datetime
import os
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import json
import pytesseract
from PIL import Image
import re

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

# Configuración para producción
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Configuración de carpetas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCUMENTOS_FOLDER = os.path.join(BASE_DIR, 'documentos_generados')
PLANTILLAS_FOLDER = os.path.join(BASE_DIR, 'plantillas_word')

# Asegurarse de que las carpetas existan
os.makedirs(DOCUMENTOS_FOLDER, exist_ok=True)
os.makedirs(PLANTILLAS_FOLDER, exist_ok=True)

# Configuración de Tesseract OCR
# En Docker usa el comando por defecto, en Windows local especificar ruta
if os.name == 'nt':  # Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# En Linux/Docker, tesseract está en PATH por defecto

@app.route('/')
def index():
    """Página principal con selector de tipo de informe"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint para keep-alive"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Generador de Informes'
    }), 200

@app.route('/ping')
def ping():
    """Ping endpoint simple"""
    return 'pong', 200

@app.route('/formulario/<tipo_informe>')
def formulario(tipo_informe):
    """Muestra el formulario según el tipo de informe"""
    tipos_validos = ['expediente', 'resolucion_directoral', 'acta_conei', 'conformidad']
    
    if tipo_informe not in tipos_validos:
        return "Tipo de informe no válido", 404
    
    return render_template(f'formulario_{tipo_informe}.html', tipo=tipo_informe)

@app.route('/generar/<tipo_informe>', methods=['POST'])
def generar_documento(tipo_informe):
    """Genera el documento Word según el tipo de informe usando plantillas"""
    try:
        datos = request.json
        
        # Buscar plantilla apropiada en la carpeta
        plantilla_path = buscar_plantilla(tipo_informe)
        
        if plantilla_path and os.path.exists(plantilla_path):
            # Cargar plantilla existente (preserva marcas de agua, sellos, firmas, etc.)
            doc = Document(plantilla_path)
            usar_plantilla = True
        else:
            # Si no existe plantilla, crear documento básico (fallback)
            doc = Document()
            usar_plantilla = False
            # Configurar márgenes
            sections = doc.sections
            for section in sections:
                section.top_margin = Inches(1)
                section.bottom_margin = Inches(1)
                section.left_margin = Inches(1)
                section.right_margin = Inches(1)
        
        # Generar según tipo
        if tipo_informe == 'expediente':
            generar_expediente(doc, datos, usar_plantilla)
        elif tipo_informe == 'resolucion_directoral':
            generar_resolucion_directoral(doc, datos, usar_plantilla)
        elif tipo_informe == 'acta_conei':
            generar_acta_conei(doc, datos, usar_plantilla)
        elif tipo_informe == 'conformidad':
            generar_conformidad(doc, datos, usar_plantilla)
        
        # Guardar documento
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{tipo_informe}_{timestamp}.docx'
        filepath = os.path.join(DOCUMENTOS_FOLDER, filename)
        doc.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'download_url': f'/descargar/{filename}'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/descargar/<filename>')
def descargar(filename):
    """Descarga el documento generado"""
    filepath = os.path.join(DOCUMENTOS_FOLDER, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "Archivo no encontrado", 404

@app.route('/procesar_imagen', methods=['POST'])
def procesar_imagen():
    """Procesa una imagen subida y extrae datos con OCR"""
    if 'imagen' not in request.files:
        return jsonify({'error': 'No se encontró archivo de imagen'}), 400
    
    file = request.files['imagen']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó archivo'}), 400
    
    if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        try:
            # Abrir imagen con PIL
            imagen = Image.open(file.stream)
            
            # Extraer texto con OCR
            texto_extraido = pytesseract.image_to_string(imagen, lang='spa')
            
            # Extraer datos específicos usando expresiones regulares
            datos_extraidos = extraer_datos_ocr(texto_extraido)
            
            return jsonify({
                'texto_completo': texto_extraido,
                'datos_extraidos': datos_extraidos
            })
            
        except Exception as e:
            return jsonify({'error': f'Error procesando imagen: {str(e)}'}), 500
    
    return jsonify({'error': 'Formato de archivo no soportado'}), 400

def extraer_datos_ocr(texto):
    """Extrae datos específicos del texto OCR"""
    datos = {}
    
    # Patrones comunes para diferentes tipos de documentos
    patrones = {
        'numero_expediente': r'N[°º]\s*(\d{3}-\d{4}-[A-Z]{2})',
        'fecha': r'(\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})',
        'remitente': r'DE[:\s]*([A-ZÁÉÍÓÚÑ\s]+)',
        'destinatario': r'PARA[:\s]*([A-ZÁÉÍÓÚÑ\s]+)',
        'asunto': r'ASUNTO[:\s]*([^\n]+)',
        'numero_resolucion': r'N[°º]\s*(\d{3}-\d{4}-[A-Z]{2}-RD)',
        'numero_acta': r'N[°º]\s*(\d{3}-\d{4}-[A-Z]{2}-ACTA)',
        'numero_conformidad': r'N[°º]\s*(\d{3}-\d{4}-[A-Z]{2}-CONF)'
    }
    
    for campo, patron in patrones.items():
        match = re.search(patron, texto, re.IGNORECASE | re.MULTILINE)
        if match:
            datos[campo] = match.group(1).strip()
    
    return datos

def buscar_plantilla(tipo_informe):
    """Busca la plantilla apropiada para el tipo de informe"""
    # Mapeo de tipos de informe a palabras clave en nombres de archivo
    palabras_clave = {
        'expediente': ['EXPEDIENTE', 'expediente'],
        'resolucion_directoral': ['RD', 'RESOLUCION', 'resolucion'],
        'acta_conei': ['ACTA', 'CONEI', 'acta'],
        'conformidad': ['CONFORMIDAD', 'conformidad']
    }
    
    if tipo_informe not in palabras_clave:
        return None
    
    # Listar archivos en la carpeta de plantillas
    try:
        archivos = os.listdir(PLANTILLAS_FOLDER)
        for archivo in archivos:
            if archivo.endswith('.docx'):
                # Buscar coincidencias con palabras clave
                for palabra in palabras_clave[tipo_informe]:
                    if palabra in archivo:
                        return os.path.join(PLANTILLAS_FOLDER, archivo)
    except Exception as e:
        print(f"Error buscando plantilla: {e}")
    
    return None

def reemplazar_placeholders(doc, datos):
    """Reemplaza placeholders en el documento con datos (preserva formato)"""
    reemplazos_hechos = 0
    
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            texto_original = run.text
            texto_nuevo = texto_original
            for key, value in datos.items():
                placeholder = f'{{{{{key}}}}}'
                if placeholder in texto_nuevo:
                    texto_nuevo = texto_nuevo.replace(placeholder, str(value))
                    reemplazos_hechos += 1
            if texto_nuevo != texto_original:
                run.text = texto_nuevo
    
    # También en tablas si existen
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        texto_original = run.text
                        texto_nuevo = texto_original
                        for key, value in datos.items():
                            placeholder = f'{{{{{key}}}}}'
                            if placeholder in texto_nuevo:
                                texto_nuevo = texto_nuevo.replace(placeholder, str(value))
                                reemplazos_hechos += 1
                        if texto_nuevo != texto_original:
                            run.text = texto_nuevo
    
    return reemplazos_hechos

def generar_expediente(doc, datos, usar_plantilla=False):
    """Genera un expediente administrativo usando plantilla o creando desde cero"""
    if usar_plantilla:
        # Usar plantilla: intentar reemplazar placeholders
        reemplazos = reemplazar_placeholders(doc, datos)
        
        # Si no se encontraron placeholders, agregar contenido al final
        if reemplazos == 0:
            doc.add_page_break()
            agregar_contenido_expediente(doc, datos)
    else:
        # Fallback: generar desde cero
        agregar_contenido_expediente(doc, datos)

def configurar_documento_profesional(doc):
    """Configura márgenes, fuentes y estilos profesionales para el documento"""
    # Configurar márgenes
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(3)
        section.right_margin = Cm(2.5)
    
    # Configurar estilo Normal
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(11)
    style.paragraph_format.line_spacing = 1.5
    style.paragraph_format.space_after = Pt(6)

def agregar_encabezado_institucional(doc, institucion="INSTITUCIÓN EDUCATIVA", codigo=""):
    """Agrega un encabezado institucional profesional"""
    # Logo placeholder y nombre de institución
    header_table = doc.add_table(rows=1, cols=3)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Celda izquierda - Logo/Escudo
    cell_izq = header_table.cell(0, 0)
    cell_izq.width = Cm(3)
    p = cell_izq.paragraphs[0]
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = p.add_run("🏫")
    run.font.size = Pt(28)
    
    # Celda central - Información
    cell_centro = header_table.cell(0, 1)
    cell_centro.width = Cm(10)
    p = cell_centro.paragraphs[0]
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = p.add_run("MINISTERIO DE EDUCACIÓN\n")
    run.font.size = Pt(9)
    run.font.name = 'Arial'
    
    run = p.add_run(f"{institucion}\n")
    run.bold = True
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    
    if codigo:
        run = p.add_run(f"Código Modular: {codigo}")
        run.font.size = Pt(9)
        run.font.name = 'Arial'
    
    # Celda derecha - Escudo nacional
    cell_der = header_table.cell(0, 2)
    cell_der.width = Cm(3)
    p = cell_der.paragraphs[0]
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = p.add_run("🇵🇪")
    run.font.size = Pt(28)
    
    # Línea separadora
    doc.add_paragraph()
    agregar_linea_horizontal(doc)
    doc.add_paragraph()

def agregar_linea_horizontal(doc):
    """Agrega una línea horizontal decorativa"""
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = p.add_run("─" * 60)
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(0, 51, 102)

def agregar_titulo_documento(doc, titulo, numero=""):
    """Agrega un título principal profesional"""
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    
    run = p.add_run(titulo)
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = 'Arial'
    run.font.color.rgb = RGBColor(0, 51, 102)
    
    if numero:
        p = doc.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        run = p.add_run(f"N° {numero}")
        run.font.size = Pt(12)
        run.font.name = 'Arial'
        run.bold = True

def agregar_seccion(doc, titulo):
    """Agrega un título de sección con formato"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(titulo)
    run.bold = True
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    run.font.color.rgb = RGBColor(0, 51, 102)

def agregar_parrafo_justificado(doc, texto, sangria=True):
    """Agrega un párrafo con texto justificado"""
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    if sangria:
        p.paragraph_format.first_line_indent = Cm(1.25)
    run = p.add_run(texto)
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    return p

def agregar_firma_profesional(doc, nombre, cargo, dni=""):
    """Agrega una sección de firma profesional"""
    doc.add_paragraph()
    doc.add_paragraph()
    doc.add_paragraph()
    
    # Línea de firma
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = p.add_run("_" * 35)
    run.font.size = Pt(11)
    
    # Nombre
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(nombre.upper())
    run.bold = True
    run.font.size = Pt(10)
    run.font.name = 'Arial'
    
    # Cargo
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p.paragraph_format.space_before = Pt(0)
    run = p.add_run(cargo)
    run.font.size = Pt(10)
    run.font.name = 'Arial'
    
    # DNI si existe
    if dni:
        p = doc.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p.paragraph_format.space_before = Pt(0)
        run = p.add_run(f"DNI: {dni}")
        run.font.size = Pt(9)
        run.font.name = 'Arial'

def agregar_contenido_expediente(doc, datos):
    """Agrega contenido del expediente al documento - Versión Profesional"""
    # Configurar documento
    configurar_documento_profesional(doc)
    
    # Encabezado institucional
    agregar_encabezado_institucional(
        doc, 
        datos.get('institucion', 'INSTITUCIÓN EDUCATIVA'),
        datos.get('codigo_modular', '')
    )
    
    # Título del documento
    agregar_titulo_documento(doc, "EXPEDIENTE ADMINISTRATIVO", datos.get('numero_expediente', ''))
    
    doc.add_paragraph()
    
    # Tabla de datos del expediente
    tabla_datos = doc.add_table(rows=4, cols=2)
    tabla_datos.style = 'Table Grid'
    
    campos = [
        ("FECHA:", datos.get('fecha', datetime.now().strftime('%d/%m/%Y'))),
        ("DE:", datos.get('remitente', '')),
        ("PARA:", datos.get('destinatario', '')),
        ("ASUNTO:", datos.get('asunto', ''))
    ]
    
    for i, (campo, valor) in enumerate(campos):
        cell_label = tabla_datos.cell(i, 0)
        cell_label.width = Cm(3)
        p = cell_label.paragraphs[0]
        run = p.add_run(campo)
        run.bold = True
        run.font.size = Pt(10)
        run.font.name = 'Arial'
        
        cell_valor = tabla_datos.cell(i, 1)
        p = cell_valor.paragraphs[0]
        run = p.add_run(valor)
        run.font.size = Pt(10)
        run.font.name = 'Arial'
    
    doc.add_paragraph()
    
    # Contenido
    if datos.get('contenido'):
        agregar_parrafo_justificado(doc, datos['contenido'])
    
    # Antecedentes
    if datos.get('antecedentes'):
        agregar_seccion(doc, "I. ANTECEDENTES")
        agregar_parrafo_justificado(doc, datos['antecedentes'])
    
    # Análisis
    if datos.get('analisis'):
        agregar_seccion(doc, "II. ANÁLISIS")
        agregar_parrafo_justificado(doc, datos['analisis'])
    
    # Conclusión
    if datos.get('conclusion'):
        agregar_seccion(doc, "III. CONCLUSIÓN")
        agregar_parrafo_justificado(doc, datos['conclusion'])
    
    # Firma
    agregar_firma_profesional(
        doc,
        datos.get('remitente', 'RESPONSABLE'),
        datos.get('cargo_remitente', 'Cargo'),
        datos.get('dni', '')
    )

def generar_resolucion_directoral(doc, datos, usar_plantilla=False):
    """Genera una Resolución Directoral"""
    if usar_plantilla:
        # Usar plantilla: intentar reemplazar placeholders
        reemplazos = reemplazar_placeholders(doc, datos)
        
        # Si no se encontraron placeholders, agregar contenido al final
        if reemplazos == 0:
            doc.add_page_break()
            agregar_contenido_resolucion(doc, datos)
    else:
        agregar_contenido_resolucion(doc, datos)

def agregar_contenido_resolucion(doc, datos):
    """Agrega contenido de la resolución al documento - Versión Profesional"""
    # Configurar documento
    configurar_documento_profesional(doc)
    
    # Encabezado institucional
    agregar_encabezado_institucional(
        doc, 
        datos.get('institucion', 'INSTITUCIÓN EDUCATIVA'),
        datos.get('codigo_modular', '')
    )
    
    # Título del documento
    agregar_titulo_documento(doc, "RESOLUCIÓN DIRECTORAL", datos.get('numero_rd', ''))
    
    doc.add_paragraph()
    
    # Lugar y fecha
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
    run = p.add_run(f"{datos.get('lugar', 'Lima')}, {datos.get('fecha', datetime.now().strftime('%d de %B de %Y'))}")
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    
    doc.add_paragraph()
    
    # VISTO
    agregar_seccion(doc, "VISTO:")
    agregar_parrafo_justificado(doc, datos.get('visto', ''))
    
    # CONSIDERANDO
    agregar_seccion(doc, "CONSIDERANDO:")
    
    considerandos = datos.get('considerandos', [])
    if isinstance(considerandos, str):
        considerandos = [c.strip() for c in considerandos.split('\n') if c.strip()]
    
    for considerando in considerandos:
        p = doc.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        p.paragraph_format.first_line_indent = Cm(1.25)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(f"Que, {considerando}")
        run.font.size = Pt(11)
        run.font.name = 'Arial'
    
    doc.add_paragraph()
    
    # SE RESUELVE
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run("SE RESUELVE:")
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Arial'
    run.font.color.rgb = RGBColor(0, 51, 102)
    
    articulos = datos.get('articulos', [])
    if isinstance(articulos, str):
        articulos = [a.strip() for a in articulos.split('\n') if a.strip()]
    
    for i, articulo in enumerate(articulos, 1):
        p = doc.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        p.paragraph_format.space_after = Pt(8)
        
        run = p.add_run(f"Artículo {i}°.- ")
        run.bold = True
        run.font.size = Pt(11)
        run.font.name = 'Arial'
        
        run = p.add_run(articulo)
        run.font.size = Pt(11)
        run.font.name = 'Arial'
    
    # REGÍSTRESE Y COMUNÍQUESE
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = p.add_run("REGÍSTRESE, COMUNÍQUESE Y ARCHÍVESE")
    run.bold = True
    run.font.size = Pt(10)
    run.font.name = 'Arial'
    
    # Firma
    agregar_firma_profesional(
        doc,
        datos.get('firmante', 'DIRECTOR'),
        datos.get('cargo_firmante', 'Director(a)'),
        datos.get('dni_firmante', '')
    )

def generar_acta_conei(doc, datos, usar_plantilla=False):
    """Genera un Acta de CONEI"""
    if usar_plantilla:
        # Usar plantilla: intentar reemplazar placeholders
        reemplazos = reemplazar_placeholders(doc, datos)
        
        # Si no se encontraron placeholders, agregar contenido al final
        if reemplazos == 0:
            doc.add_page_break()
            agregar_contenido_acta(doc, datos)
    else:
        agregar_contenido_acta(doc, datos)

def agregar_contenido_acta(doc, datos):
    """Agrega contenido del acta al documento - Versión Profesional"""
    # Configurar documento
    configurar_documento_profesional(doc)
    
    # Encabezado institucional
    agregar_encabezado_institucional(
        doc, 
        datos.get('institucion', 'INSTITUCIÓN EDUCATIVA'),
        datos.get('codigo_modular', '')
    )
    
    # Título del documento
    agregar_titulo_documento(doc, "ACTA DE REUNIÓN DEL CONSEJO EDUCATIVO INSTITUCIONAL", datos.get('numero_acta', ''))
    
    doc.add_paragraph()
    
    # Tabla de información de la reunión
    tabla_info = doc.add_table(rows=5, cols=2)
    tabla_info.style = 'Table Grid'
    
    info_reunion = [
        ("INSTITUCIÓN EDUCATIVA:", datos.get('institucion', '')),
        ("FECHA:", datos.get('fecha', datetime.now().strftime('%d/%m/%Y'))),
        ("HORA DE INICIO:", datos.get('hora_inicio', '')),
        ("HORA DE TÉRMINO:", datos.get('hora_termino', '')),
        ("LUGAR:", datos.get('lugar', ''))
    ]
    
    for i, (campo, valor) in enumerate(info_reunion):
        cell_label = tabla_info.cell(i, 0)
        cell_label.width = Cm(5)
        p = cell_label.paragraphs[0]
        run = p.add_run(campo)
        run.bold = True
        run.font.size = Pt(10)
        run.font.name = 'Arial'
        
        cell_valor = tabla_info.cell(i, 1)
        p = cell_valor.paragraphs[0]
        run = p.add_run(valor)
        run.font.size = Pt(10)
        run.font.name = 'Arial'
    
    doc.add_paragraph()
    
    # ASISTENTES
    agregar_seccion(doc, "I. ASISTENTES")
    
    asistentes = datos.get('asistentes', [])
    if isinstance(asistentes, str):
        asistentes = [a.strip() for a in asistentes.split('\n') if a.strip()]
    
    # Tabla de asistentes
    if asistentes:
        tabla_asist = doc.add_table(rows=len(asistentes)+1, cols=3)
        tabla_asist.style = 'Table Grid'
        
        # Encabezados
        headers = ["N°", "NOMBRE COMPLETO", "CARGO"]
        for j, header in enumerate(headers):
            cell = tabla_asist.cell(0, j)
            p = cell.paragraphs[0]
            run = p.add_run(header)
            run.bold = True
            run.font.size = Pt(9)
            run.font.name = 'Arial'
        
        for i, asistente in enumerate(asistentes, 1):
            tabla_asist.cell(i, 0).paragraphs[0].add_run(str(i)).font.size = Pt(9)
            tabla_asist.cell(i, 1).paragraphs[0].add_run(asistente).font.size = Pt(9)
            tabla_asist.cell(i, 2).paragraphs[0].add_run("").font.size = Pt(9)
    
    doc.add_paragraph()
    
    # AGENDA
    agregar_seccion(doc, "II. AGENDA")
    
    agenda = datos.get('agenda', [])
    if isinstance(agenda, str):
        agenda = [a.strip() for a in agenda.split('\n') if a.strip()]
    
    for i, punto in enumerate(agenda, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.5)
        run = p.add_run(f"{i}. {punto}")
        run.font.size = Pt(11)
        run.font.name = 'Arial'
    
    doc.add_paragraph()
    
    # DESARROLLO
    agregar_seccion(doc, "III. DESARROLLO DE LA REUNIÓN")
    agregar_parrafo_justificado(doc, datos.get('desarrollo', ''))
    
    doc.add_paragraph()
    
    # ACUERDOS
    agregar_seccion(doc, "IV. ACUERDOS")
    
    acuerdos = datos.get('acuerdos', [])
    if isinstance(acuerdos, str):
        acuerdos = [a.strip() for a in acuerdos.split('\n') if a.strip()]
    
    for i, acuerdo in enumerate(acuerdos, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.5)
        run = p.add_run(f"ACUERDO {i}.- ")
        run.bold = True
        run.font.size = Pt(11)
        run.font.name = 'Arial'
        
        run = p.add_run(acuerdo)
        run.font.size = Pt(11)
        run.font.name = 'Arial'
    
    doc.add_paragraph()
    
    # Cierre
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    run = p.add_run("Sin otro particular que tratar, siendo las ")
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    run = p.add_run(datos.get('hora_termino', '____'))
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    run = p.add_run(" horas del día ")
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    run = p.add_run(datos.get('fecha', '____'))
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    run = p.add_run(", se da por concluida la reunión, firmando los presentes en señal de conformidad.")
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    
    doc.add_paragraph()
    doc.add_paragraph()
    
    # Firmas (2 columnas)
    tabla_firmas = doc.add_table(rows=2, cols=2)
    tabla_firmas.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    for i in range(2):
        for j in range(2):
            cell = tabla_firmas.cell(i, j)
            cell.width = Cm(7)
            p = cell.paragraphs[0]
            p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            if i == 0:
                p.add_run("\n\n\n_________________________\n").font.size = Pt(10)
            else:
                run = p.add_run("FIRMA")
                run.font.size = Pt(9)
                run.font.name = 'Arial'

def generar_conformidad(doc, datos, usar_plantilla=False):
    """Genera un documento de conformidad"""
    if usar_plantilla:
        # Usar plantilla: intentar reemplazar placeholders
        reemplazos = reemplazar_placeholders(doc, datos)
        
        # Si no se encontraron placeholders, agregar contenido al final
        if reemplazos == 0:
            doc.add_page_break()
            agregar_contenido_conformidad(doc, datos)
    else:
        agregar_contenido_conformidad(doc, datos)

def agregar_contenido_conformidad(doc, datos):
    """Agrega contenido de conformidad al documento - Versión Profesional"""
    # Configurar documento
    configurar_documento_profesional(doc)
    
    # Encabezado institucional
    agregar_encabezado_institucional(
        doc, 
        datos.get('institucion', 'INSTITUCIÓN EDUCATIVA'),
        datos.get('codigo_modular', '')
    )
    
    # Título del documento
    agregar_titulo_documento(doc, "CONSTANCIA DE CONFORMIDAD", datos.get('numero_conformidad', ''))
    
    doc.add_paragraph()
    
    # Fecha alineada a la derecha
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
    run = p.add_run(f"{datos.get('lugar', 'Lima')}, {datos.get('fecha', datetime.now().strftime('%d de %B de %Y'))}")
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    
    doc.add_paragraph()
    
    # Cuerpo del documento
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(1.25)
    p.paragraph_format.line_spacing = 1.5
    
    run = p.add_run("El/La que suscribe, ")
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    
    run = p.add_run(f"{datos.get('nombre_responsable', '________________')}")
    run.bold = True
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    
    run = p.add_run(", identificado(a) con DNI N° ")
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    
    run = p.add_run(f"{datos.get('dni', '________________')}")
    run.bold = True
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    
    run = p.add_run(", en mi calidad de ")
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    
    run = p.add_run(f"{datos.get('cargo', '________________')}")
    run.bold = True
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    
    run = p.add_run(" de la ")
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    
    run = p.add_run(f"{datos.get('institucion', 'Institución Educativa')}")
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    
    run = p.add_run(", dejo constancia de conformidad de lo siguiente:")
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    
    doc.add_paragraph()
    
    # Descripción en recuadro
    tabla_desc = doc.add_table(rows=1, cols=1)
    tabla_desc.style = 'Table Grid'
    cell = tabla_desc.cell(0, 0)
    p = cell.paragraphs[0]
    p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    run = p.add_run(datos.get('descripcion', ''))
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    
    doc.add_paragraph()
    
    # Detalles adicionales si existen
    if datos.get('proveedor'):
        p = doc.add_paragraph()
        run = p.add_run("Proveedor/Contratista: ")
        run.bold = True
        run.font.size = Pt(11)
        run.font.name = 'Arial'
        run = p.add_run(datos.get('proveedor', ''))
        run.font.size = Pt(11)
        run.font.name = 'Arial'
    
    if datos.get('monto'):
        p = doc.add_paragraph()
        run = p.add_run("Monto: ")
        run.bold = True
        run.font.size = Pt(11)
        run.font.name = 'Arial'
        run = p.add_run(f"S/ {datos.get('monto', '')}")
        run.font.size = Pt(11)
        run.font.name = 'Arial'
    
    if datos.get('periodo'):
        p = doc.add_paragraph()
        run = p.add_run("Periodo: ")
        run.bold = True
        run.font.size = Pt(11)
        run.font.name = 'Arial'
        run = p.add_run(datos.get('periodo', ''))
        run.font.size = Pt(11)
        run.font.name = 'Arial'
    
    # Observaciones
    if datos.get('observaciones'):
        doc.add_paragraph()
        agregar_seccion(doc, "OBSERVACIONES:")
        agregar_parrafo_justificado(doc, datos['observaciones'])
    
    doc.add_paragraph()
    
    # Párrafo de cierre
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(1.25)
    run = p.add_run("Se expide la presente constancia para los fines que el interesado estime conveniente.")
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    
    # Firma
    agregar_firma_profesional(
        doc,
        datos.get('nombre_responsable', 'RESPONSABLE'),
        datos.get('cargo', 'Cargo'),
        datos.get('dni', '')
    )

if __name__ == '__main__':
    # Configuración según el entorno
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host='0.0.0.0', port=port, debug=debug)

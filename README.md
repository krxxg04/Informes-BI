# Informes-BI

Sistema de generación automática de informes administrativos.

## 🚀 Inicio Rápido

### Opción 1: Docker (Recomendado)
```bash
docker build -t informes-bi .
docker run -d -p 5000:5000 informes-bi
```

### Opción 2: Desarrollo Local
```bash
pip install -r requirements.txt
python app/main.py
```

## 📷 Nueva Funcionalidad: OCR (Reconocimiento de Texto)

Ahora puedes subir imágenes de documentos existentes y extraer automáticamente los datos:

### Instalación de Tesseract OCR (requerido para OCR local)
1. Descarga desde: https://github.com/UB-Mannheim/tesseract/wiki
2. Instala el ejecutable para Windows
3. Asegúrate de que esté en PATH

### Cómo usar OCR:
1. Ve a cualquier formulario (Expediente, RD, Acta, etc.)
2. En la sección "Extraer Datos de Imagen (OCR)":
   - Selecciona una imagen de documento
   - Haz clic en "Procesar Imagen"
   - Revisa el texto extraído
   - Haz clic en "Rellenar Formulario" para auto-completar

### Tipos de documentos soportados:
- Expedientes administrativos
- Resoluciones directorales
- Actas CONEI
- Constancias de conformidad

## 📋 Tipos de Informes

- **Expediente Administrativo**: Documentos oficiales con formato estándar
- **Resolución Directo**: Decisiones administrativas con visto, considerandos y artículos
- **Acta CONEI**: Reuniones del Consejo Educativo Institucional
- **Conformidad**: Constancias de cumplimiento de servicios/productos
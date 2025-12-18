# Instalación de Tesseract OCR para Windows

Para usar la funcionalidad de OCR (reconocimiento de texto en imágenes), necesitas instalar Tesseract OCR:

## Pasos de instalación:

1. **Descargar Tesseract OCR:**
   - Ve a: https://github.com/UB-Mannheim/tesseract/wiki
   - Descarga la versión para Windows (tesseract-ocr-w64-setup-5.3.4.20240210.exe o similar)

2. **Instalar:**
   - Ejecuta el instalador como administrador
   - Asegúrate de marcar "Add to PATH" durante la instalación
   - El idioma español se instala automáticamente

3. **Verificar instalación:**
   - Abre PowerShell y ejecuta: `tesseract --version`
   - Deberías ver la versión instalada

## Si hay problemas:

- La ruta por defecto es: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- Si está en otra ubicación, actualiza la ruta en `app/main.py`

## Uso:

Una vez instalado, puedes:
- Subir imágenes de documentos existentes
- El sistema extraerá automáticamente datos como números de expediente, fechas, remitentes, etc.
- Rellenará el formulario automáticamente</content>
<parameter name="filePath">c:\Users\ASUS\Desktop\UPC\Bart Industries\Software Informes\INSTALAR_TESSERACT.md
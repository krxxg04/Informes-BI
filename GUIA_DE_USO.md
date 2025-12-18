# 📖 GUÍA RÁPIDA DE USO

## Para tu mamá ❤️

### 🚀 ¿Cómo iniciar el programa?

1. **Busca el archivo `INICIAR.bat`** en esta carpeta
2. **Haz doble clic** sobre él
3. Espera a que aparezca una ventana negra (no la cierres)
4. Se abrirá automáticamente tu navegador en la página del programa
   - Si no se abre solo, abre Chrome/Edge y escribe: `http://localhost:5000`

### 📝 ¿Cómo crear un informe?

#### Paso 1: Elegir tipo de informe
En la página principal verás 4 opciones:
- **📋 Expediente Administrativo** - Para trámites administrativos
- **📜 Resolución Directoral** - Para RDs oficiales
- **👥 Acta CONEI** - Para reuniones del CONEI
- **✅ Conformidad** - Para dar conformidad a algo

Haz clic en el que necesites.

#### Paso 2: Llenar el formulario
- Los campos con **asterisco (*)** son obligatorios
- Escribe con cuidado, tal como quieres que aparezca en el documento
- La fecha se puede cambiar haciendo clic en el calendario
- Puedes agregar más puntos con los botones verdes **"+ Agregar"**

#### Paso 3: Generar el documento
- Cuando termines de llenar todo, haz clic en **"Generar Documento"**
- Espera unos segundos (verás un mensaje de "Generando...")
- El documento se descargará automáticamente en formato Word
- ¡Listo! Ya puedes abrir el documento y hacer ajustes si necesitas

### 💡 Consejos útiles

1. **No cierres la ventana negra** mientras uses el programa
2. **Guarda tus documentos** después de generarlos en una carpeta segura
3. Si cometes un error, puedes editar el documento Word después
4. Los documentos se guardan también en la carpeta `documentos_generados`
5. Puedes copiar y pegar texto desde otros documentos

### 🎨 Características especiales

#### Expediente Administrativo
- Puedes agregar: Antecedentes, Análisis y Conclusión (opcionales)
- Formato oficial automático

#### Resolución Directoral
- Agrega los considerandos que necesites (botón verde)
- Agrega los artículos que necesites (botón verde)
- Si te equivocas, usa el botón rojo "Eliminar"

#### Acta CONEI
- Agrega todos los asistentes que vinieron
- Agrega los puntos de la agenda
- Agrega los acuerdos tomados
- Todo con botones verdes para agregar más

#### Conformidad
- Simple y rápido
- Solo llena los datos principales

### ❓ Problemas comunes

**"No se abre el programa"**
- Asegúrate de tener Python instalado
- Haz doble clic en `INICIAR.bat` nuevamente

**"El botón no responde"**
- Verifica que todos los campos con * estén llenos
- Revisa que las fechas estén correctas

**"¿Dónde está mi documento?"**
- Se descarga automáticamente (mira la carpeta de Descargas)
- También está en la carpeta `documentos_generados` del programa

### 🆘 ¿Necesitas ayuda?

Para cerrar el programa:
1. Cierra la página del navegador
2. Ve a la ventana negra
3. Presiona `Ctrl + C`
4. Cierra la ventana

---

## 👨‍💻 Para el que mantiene el sistema

### Personalización

#### Cambiar formatos de documentos
Edita las funciones en `app/main.py`:
- `generar_expediente()` - línea 61
- `generar_resolucion_directoral()` - línea 100
- `generar_acta_conei()` - línea 156
- `generar_conformidad()` - línea 218

#### Agregar nuevo tipo de informe
1. Crea función generadora en `app/main.py`
2. Crea template HTML en `templates/`
3. Agrega card en `templates/index.html`
4. Agrega ruta en el decorador `@app.route()`

#### Cambiar estilos
Edita `static/style.css` para cambiar colores, fuentes, etc.

### Actualización
```bash
pip install -r requirements.txt --upgrade
```

### Backup
Haz copias de:
- `documentos_generados/` (documentos creados)
- Todo el proyecto (por si necesitas restaurar)

---

**Fecha de creación:** Diciembre 2025  
**Versión:** 1.0  
**Hecho con ❤️ para facilitar el trabajo**

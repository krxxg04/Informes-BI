# Sistema de Generación de Informes

Sistema web para facilitar la creación de informes administrativos del sector público.

## 🚀 Acceso Rápido

**URL de Producción:** [Agregar después del deployment]

## 🌟 Características

- ✅ Expedientes Administrativos
- ✅ Resoluciones Directorales
- ✅ Actas CONEI
- ✅ Constancias de Conformidad
- ✅ Interfaz amigable
- ✅ Generación automática de documentos Word
- ✅ Accesible 24/7 desde cualquier dispositivo

## 📖 Documentación

- [Guía de Uso](GUIA_DE_USO.md) - Para usuarios finales
- [Guía de Deployment](DEPLOYMENT.md) - Para deployar el sistema
- [README Técnico](README.md) - Información técnica del proyecto

## 🛠️ Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app/main.py

# O usar el script de inicio
./INICIAR.bat  # Windows
```

## 🌐 Deployment

El sistema está configurado para deployar en:
- ✅ Render.com (recomendado)
- ✅ Railway.app
- ✅ PythonAnywhere
- ✅ Fly.io
- ✅ Cualquier servidor con Docker

Ver [DEPLOYMENT.md](DEPLOYMENT.md) para instrucciones detalladas.

## 📊 Stack Tecnológico

- **Backend:** Python 3.11 + Flask
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Documentos:** python-docx
- **Servidor:** Gunicorn
- **Deployment:** Render/Railway (gratis)

## 🔒 Seguridad

- Sin base de datos (no almacena información sensible)
- Documentos generados temporalmente
- HTTPS en producción
- Sin cookies ni tracking

## 📝 Licencia

Proyecto privado para uso institucional.

---

**Hecho con ❤️ para facilitar el trabajo administrativo**

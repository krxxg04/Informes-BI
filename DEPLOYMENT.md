# 🚀 GUÍA DE DEPLOYMENT - Sistema de Informes

## 🎯 Objetivo
Deployar tu aplicación de forma **100% GRATUITA** y que **NUNCA muera**.

---

## 📊 Comparación de Servicios Gratuitos

| Servicio | Pros | Contras | Recomendación |
|----------|------|---------|---------------|
| **Render.com** | ✓ Fácil setup<br>✓ 750hrs gratis/mes<br>✓ Auto-deploy desde GitHub | Sleep después 15 min inactividad | ⭐⭐⭐⭐⭐ MEJOR OPCIÓN |
| **Railway.app** | ✓ $5 crédito gratis/mes<br>✓ No duerme<br>✓ Muy rápido | Límite de crédito | ⭐⭐⭐⭐ Excelente |
| **PythonAnywhere** | ✓ Específico para Python<br>✓ Siempre activo | Plan gratis muy limitado | ⭐⭐⭐ Bueno |
| **Fly.io** | ✓ Buenos recursos gratis | Setup más complejo | ⭐⭐⭐ Bueno |

---

## 🏆 OPCIÓN 1: RENDER.COM (RECOMENDADO)

### ✅ Ventajas
- Setup en 5 minutos
- Deploy automático desde GitHub
- SSL gratis
- 750 horas gratis al mes (suficiente para 24/7)

### 📝 Pasos para Deployar

#### 1. Preparar GitHub
```bash
# En tu terminal, dentro de la carpeta del proyecto:
git init
git add .
git commit -m "Initial commit - Sistema de Informes"
```

Luego sube a GitHub:
1. Ve a github.com y crea un nuevo repositorio
2. Copia los comandos que te da GitHub
3. Pégalos en tu terminal

#### 2. Crear cuenta en Render
1. Ve a https://render.com
2. Regístrate con tu cuenta de GitHub (Sign Up with GitHub)
3. Autoriza a Render para acceder a tus repos

#### 3. Crear Web Service
1. Click en "New +" → "Web Service"
2. Conecta tu repositorio de GitHub
3. Configuración:
   - **Name:** generador-informes
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app.main:app`
   - **Plan:** Free

4. Click "Create Web Service"

#### 4. Esperar el Deploy
- Render construirá y desplegará automáticamente
- En 5-10 minutos tendrás tu URL: `https://generador-informes.onrender.com`

#### 5. Configurar Keep-Alive (Evitar Sleep)

**Opción A: UptimeRobot (RECOMENDADO - Gratis)**
1. Ve a https://uptimerobot.com
2. Crea cuenta gratis
3. Add New Monitor:
   - Monitor Type: HTTP(s)
   - URL: `https://tu-app.onrender.com/ping`
   - Monitoring Interval: 5 minutos
4. ¡Listo! Tu app NUNCA dormirá

**Opción B: Cron-Job.org**
1. Ve a https://cron-job.org
2. Crea cuenta gratis
3. Create Cronjob:
   - URL: `https://tu-app.onrender.com/ping`
   - Interval: Every 5 minutes

**Opción C: Script local (requiere PC encendida)**
```bash
# Edita keep_alive.py con tu URL
# Luego ejecuta:
pip install -r requirements-keepalive.txt
python keep_alive.py
```

---

## 🚂 OPCIÓN 2: RAILWAY.APP (MUY BUENA)

### ✅ Ventajas
- $5 USD gratis cada mes
- NO duerme por inactividad
- Más rápido que Render

### 📝 Pasos para Deployar

#### 1. Preparar proyecto en GitHub (igual que Render)

#### 2. Deployar en Railway
1. Ve a https://railway.app
2. Sign up with GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Selecciona tu repositorio
5. Railway detectará automáticamente que es Python
6. Deploy se hace solo

#### 3. Obtener URL
1. Ve a Settings → Domains
2. Click "Generate Domain"
3. Copia tu URL

**Nota:** Con $5/mes gratis, tienes ~500 horas. Si se acaba, la app para hasta el siguiente mes.

---

## 🐍 OPCIÓN 3: PYTHONANYWHERE

### 📝 Pasos para Deployar

1. Ve a https://www.pythonanywhere.com
2. Crea cuenta gratuita
3. En Dashboard → "Web" → "Add a new web app"
4. Selecciona "Flask" y Python 3.10
5. Sube tus archivos o clona desde GitHub:
```bash
git clone https://github.com/tu-usuario/tu-repo.git
```
6. Configura WSGI file apuntando a `app.main`
7. Reload web app

**Ventaja:** Siempre activo, no duerme  
**Desventaja:** Muy limitado en recursos, solo 1 web app en plan gratis

---

## 🎨 OPCIÓN 4: FLY.IO

### 📝 Pasos para Deployar

1. Instala flyctl:
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

2. Autentícate:
```bash
fly auth signup
```

3. Deploy:
```bash
cd "tu-carpeta-proyecto"
fly launch
# Responde las preguntas (usa defaults)
fly deploy
```

---

## 🎯 MI RECOMENDACIÓN FINAL

### Para tu mamá (fácil y confiable):

**🥇 Primera opción: Render + UptimeRobot**
- Deploy en Render (5 min)
- Keep-alive con UptimeRobot (2 min)
- Total: 7 minutos para tener 24/7 gratis

**🥈 Segunda opción: Railway**
- Si Render no funciona
- Más simple, sin keep-alive necesario
- Pero tiene límite mensual

---

## 📱 DESPUÉS DEL DEPLOYMENT

### 1. Guarda la URL
Ejemplo: `https://generador-informes.onrender.com`

### 2. Crea un acceso directo para tu mamá
- En su escritorio, crea archivo `Informes.url`:
```
[InternetShortcut]
URL=https://tu-app.onrender.com
```

### 3. Explícale que:
- Ya NO necesita hacer doble click en `INICIAR.bat`
- Solo abre el acceso directo del escritorio
- Funciona desde cualquier dispositivo (PC, tablet, celular)

---

## 🔧 MANTENIMIENTO

### Si el servicio tiene problemas:
1. Verifica en https://render.com que el servicio esté "Running"
2. Verifica que UptimeRobot esté monitoreando
3. Mira los logs en Render Dashboard

### Actualizar el código:
```bash
git add .
git commit -m "Actualización"
git push
# Render auto-deploya en 1-2 minutos
```

---

## 💰 COSTOS
- **Render:** $0 (gratis para siempre)
- **Railway:** $0 (hasta $5/mes en uso)
- **UptimeRobot:** $0 (gratis para siempre)
- **Dominio personalizado:** $0 (usa el que te dan gratis)

**Total: $0/mes** ✅

---

## 🆘 PROBLEMAS COMUNES

**"La app tarda en cargar"**
- Normal en servicios gratuitos
- Primera carga: 30 segundos
- Después: instantáneo
- Solución: Usa keep-alive

**"La app no se ve"**
- Verifica la URL en Render
- Chequea los logs de deploy
- Asegúrate que todos los archivos estén en GitHub

**"Error 500"**
- Mira los logs en Render Dashboard
- Usualmente falta alguna dependencia
- Verifica que `requirements.txt` esté correcto

---

## 📞 SOPORTE

Si algo no funciona:
1. Revisa los logs en tu plataforma (Render/Railway)
2. Verifica que todos los archivos estén en GitHub
3. Asegúrate que `requirements.txt` esté completo

---

## ✅ CHECKLIST DE DEPLOYMENT

- [ ] Código en GitHub
- [ ] Cuenta en Render/Railway
- [ ] Web Service creado
- [ ] Deploy exitoso
- [ ] URL funcionando
- [ ] Keep-alive configurado (UptimeRobot)
- [ ] Acceso directo creado para tu mamá
- [ ] Probado en diferentes dispositivos

**¡Cuando completes todo, tu mamá tendrá su sistema disponible 24/7 GRATIS!** 🎉

---

**Tiempo total de setup: 10-15 minutos**  
**Costo: $0**  
**Disponibilidad: 99.9%**  
**Felicidad de tu mamá: ∞** ❤️

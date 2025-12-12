# ✅ Checklist de Deployment - TrackVis

## 📋 RESUMEN: ¿Qué falta para deployment en GitHub?

### ✅ YA ESTÁ LISTO:
- [x] README.md completo con instrucciones de instalación
- [x] requirements.txt con todas las dependencias
- [x] .gitignore configurado correctamente
- [x] Scripts de inicio cross-platform (run.sh / run.bat)
- [x] Scripts de limpieza (scripts/cleanup.sh / cleanup.bat)
- [x] Guía de deployment completa (DEPLOYMENT_GUIDE.md)
- [x] Código limpio y funcional (main.py)
- [x] **🐳 Dockerfile y docker-compose.yml**
- [x] **🐳 Scripts de descarga desde Google Drive (Linux/Windows)**
- [x] **🐳 Guía completa de Docker (DOCKER_GUIDE.md)**

### ⚠️ PENDIENTE (IMPORTANTE):

#### 1. **Gestión de datos (638 MB)**
**Problema:** Los datos son muy grandes para GitHub

**Opción A - Git LFS (recomendado):**
```bash
# Instalar Git LFS
git lfs install

# Track archivos grandes
git lfs track "static/data/*.csv"
git lfs track "static/data/*.json"

# Commit
git add .gitattributes
git commit -m "Add Git LFS tracking"
```

**Opción B - Descarga externa:**
1. Subir datos a Google Drive/Dropbox/Zenodo
2. Crear link de descarga pública
3. Agregar instrucciones en README.md

**Opción C - Datos de ejemplo (demo):**
```bash
# Crear subset pequeño
head -1000 static/data/df_final1.csv > static/data/sample/df_final1_sample.csv
head -100 static/data/ivt_precalculated.csv > static/data/sample/ivt_precalculated_sample.csv
```

---

#### 2. **Limpiar archivos innecesarios**
```bash
# Ejecutar script de limpieza
./scripts/cleanup.sh     # Linux/Mac
scripts\cleanup.bat      # Windows
```

Esto eliminará:
- Documentos de análisis (ARCHIVOS_NO_USADOS.md, etc.)
- Controllers renombrados (*__.py)
- Templates renombrados (*__.html)
- Logs (*.log)
- Cache de Python (__pycache__)

---

#### 3. **Licencia**
Agregar archivo `LICENSE`:
```bash
# Crear LICENSE con licencia MIT
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 [Tu Nombre]
...
EOF
```

---

#### 4. **Testing en diferentes plataformas**

**Windows:**
```bash
run.bat
# ¿Funciona? ✅ / ❌
```

**Linux:**
```bash
chmod +x run.sh
./run.sh
# ¿Funciona? ✅ / ❌
```

**Mac:**
```bash
chmod +x run.sh
./run.sh
# ¿Funciona? ✅ / ❌
```

---

#### 5. **Documentación adicional (opcional pero recomendado)**

**Screenshots:**
```bash
mkdir -p docs/screenshots
# Agregar capturas de pantalla:
# - docs/screenshots/view1.png
# - docs/screenshots/view2.png
# - docs/screenshots/glyph.png
```

**Actualizar README.md:**
```markdown
## 📸 Screenshots

![Vista por imagen](docs/screenshots/view1.png)
![Radial Glyph](docs/screenshots/glyph.png)
```

---

## 🎯 PASOS PARA DEPLOYMENT

### Paso 1: Limpiar repositorio
```bash
# Ejecutar script de limpieza
./scripts/cleanup.sh      # Linux/Mac
scripts\cleanup.bat       # Windows

# Verificar qué archivos se subirán
git status
```

### Paso 2: Configurar Git LFS (si usas opción A)
```bash
git lfs install
git lfs track "static/data/*.csv"
git lfs track "static/data/*.json"
git add .gitattributes
```

### Paso 3: Commit y push
```bash
git add .
git commit -m "chore: prepare for deployment - v2.0"
git push origin main
```

### Paso 4: Crear Release en GitHub
1. Ve a GitHub → Releases → "Create new release"
2. Tag: `v2.0.0`
3. Title: "TrackVis v2.0 - Interactive Eye Tracking Visualization"
4. Description:
```markdown
## 🎉 TrackVis v2.0

Sistema de visualización interactiva de eye tracking con:
- ✅ Brush interactivo para selección de áreas
- ✅ Radial Glyph con análisis detallado
- ✅ Heatmaps y scarf plots
- ✅ Análisis por participante
- ✅ Proyecciones t-SNE

### Instalación
Ver README.md

### Datos
[Si NO usas Git LFS, agregar link de descarga aquí]
```

### Paso 5: Testing post-deployment
```bash
# Clonar en carpeta temporal
cd /tmp
git clone https://github.com/tuusuario/trackvis.git
cd trackvis

# Probar instalación
./run.sh      # Linux/Mac
run.bat       # Windows

# ¿Funciona? ✅ / ❌
```

---

## 📊 Tamaños estimados

### Sin datos (código solo):
```
Código Python + HTML/JS: ~2 MB
Imágenes (150): ~5 MB
Total: ~7 MB ✅ Perfecto para GitHub
```

### Con datos (Git LFS):
```
CSV: 638 MB
JSON: ~5 MB
Total: ~643 MB ✅ Dentro del límite de GitHub LFS (1 GB)
```

### Con datos (SIN Git LFS):
```
Total: ~650 MB ❌ Demasiado grande - usa descarga externa
```

---

## ⚙️ Configuración adicional (opcional)

### GitHub Actions (CI/CD)
Crear `.github/workflows/test.yml`:
```yaml
name: Test TrackVis
on: [push, pull_request]
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: [3.8, 3.9, '3.10']
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Test imports
      run: python -c "from app.controllers.heatmap import *"
```

### 🐳 Docker (máxima portabilidad) - RECOMENDADO

**Ver guía completa:** [DOCKER_GUIDE.md](DOCKER_GUIDE.md)

**Ventajas:**
- ✅ Funciona en Windows, Linux y Mac sin cambios
- ✅ No requiere instalar Python ni dependencias manualmente
- ✅ Descarga automática de imágenes desde Google Drive
- ✅ Un solo comando para ejecutar todo

**Quick Start:**
```bash
# 1. Configurar FILE_IDs en scripts/download_images.sh (o .bat para Windows)

# 2. Descargar imágenes desde Google Drive
./scripts/download_images.sh      # Linux/Mac
scripts\download_images.bat        # Windows

# 3. Ejecutar con Docker Compose
docker-compose up -d

# 4. Acceder a http://localhost:8081
```

**Archivos Docker ya incluidos:**
- ✅ `Dockerfile` - Imagen Docker optimizada
- ✅ `docker-compose.yml` - Orquestación de contenedores
- ✅ `.dockerignore` - Optimización de build
- ✅ `scripts/download_images.sh` - Descarga automática (Linux/Mac)
- ✅ `scripts/download_images.bat` - Descarga automática (Windows)

---

## 🐛 Problemas comunes

### "Git push rejected (file too large)"
**Solución:** Usar Git LFS o descarga externa

### "ModuleNotFoundError: No module named 'flask'"
**Solución:** Ejecutar `pip install -r requirements.txt`

### "Port 8081 already in use"
**Solución:**
```bash
# Linux/Mac
lsof -ti:8081 | xargs kill

# Windows
netstat -ano | findstr :8081
taskkill /PID [PID] /F
```

---

## ✅ CHECKLIST FINAL

Antes de hacer `git push`:

- [ ] README.md actualizado
- [ ] .gitignore configurado
- [ ] Scripts de inicio funcionan (run.sh / run.bat)
- [ ] Archivos innecesarios eliminados
- [ ] Datos gestionados (Git LFS o link externo)
- [ ] Licencia agregada
- [ ] Testing en al menos 2 plataformas
- [ ] Git LFS configurado (si aplica)
- [ ] `.gitattributes` commiteado (si aplica)

Después de `git push`:

- [ ] Release creado en GitHub
- [ ] README actualizado con link de datos (si aplica)
- [ ] Testing de instalación desde GitHub
- [ ] Documentación revisada

---

## 📧 Contacto

Si tienes problemas con el deployment, revisa:
1. DEPLOYMENT_GUIDE.md (guía detallada)
2. README.md (instrucciones de instalación)
3. GitHub Issues (reportar problemas)

---

**Última actualización:** Diciembre 2024
**Estado:** ✅ Listo para deployment (pendiente gestión de datos)

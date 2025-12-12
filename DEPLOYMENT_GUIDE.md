# 🚀 Guía de Deployment - TrackVis

Esta guía te ayudará a preparar y desplegar TrackVis para que cualquier usuario pueda ejecutarlo desde GitHub.

## ✅ Checklist de Deployment

### 1. **Limpieza del repositorio**

- [x] README.md completo y actualizado
- [x] .gitignore configurado correctamente
- [x] requirements.txt con todas las dependencias
- [x] Scripts de inicio (run.sh / run.bat)
- [x] Git LFS configurado (`git lfs install` + `git lfs pull` antes de empaquetar)
- [ ] Eliminar archivos innecesarios

### 2. **Gestión de datos (importante)**

**Problema:** Los datos pesan 638 MB - demasiado para GitHub

**Soluciones:**

#### **Opción A: Git LFS (recomendado para datasets públicos)**
```bash
# Instalar Git LFS
git lfs install

# Track archivos grandes
git lfs track "static/data/*.csv"
git lfs track "static/data/*.json"
git lfs track "static/images/images/*.jpg"

# Commit .gitattributes
git add .gitattributes
git commit -m "Add Git LFS tracking"
```

**Límites:** GitHub LFS gratis = 1GB storage + 1GB bandwidth/mes

#### **Opción B: Descarga externa (recomendado para datasets privados)**

1. Subir datos a:
   - **Google Drive** (público/privado)
   - **Dropbox** (público)
   - **Zenodo** (datasets científicos)
   - **OSF** (Open Science Framework)

2. Crear script de descarga:
```python
# scripts/download_data.py
import requests
import zipfile

DATASET_URL = "https://drive.google.com/uc?id=YOUR_FILE_ID"
print("Descargando datos...")
# ... código de descarga ...
```

3. Actualizar README con instrucciones:
```markdown
### Descargar datos
python scripts/download_data.py
# O manualmente desde: [LINK]
```

#### **Opción C: Datos de ejemplo (para demo)**

Crear subset pequeño de datos:
```bash
# Crear carpeta de datos de ejemplo
mkdir -p static/data/sample

# Copiar primeras 1000 líneas
head -1000 static/data/df_final1.csv > static/data/sample/df_final1_sample.csv
```

---

### 3. **Archivos a eliminar antes del deploy**

```bash
# Archivos de análisis (no necesarios en prod)
rm ARCHIVOS_NO_USADOS.md
rm CSV_NO_USADOS.md
rm JSON_NO_USADOS.md
rm CONTROLLERS_NO_USADOS.md
rm BRUSH_IMPLEMENTACION.md

# Controllers renombrados
rm app/controllers/*__.py 2>/dev/null

# Templates renombrados
rm templates/*__.html 2>/dev/null

# Logs
rm *.log

# Resultados CSV generados
rm RESULTADO_*.csv

# Cache
rm -rf static/cache/tsne/*
rm glyph_data.json
```

---

### 4. **Estructura final del repositorio**

```
trackvis/
├── .gitignore              ✅ Completo
├── .gitattributes          ⚠️ Solo si usas Git LFS
├── README.md               ✅ Documentación completa
├── requirements.txt        ✅ Dependencias
├── run.sh                  ✅ Script Linux/Mac
├── run.bat                 ✅ Script Windows
├── main2.py                ✅ Aplicación principal
├── app/
│   ├── controllers/        ✅ Solo archivos usados
│   ├── services/          ✅ Servicios
│   └── shared/            ✅ Utilidades compartidas
├── static/
│   ├── main2.js           ✅ JavaScript principal
│   ├── glyph_brush2.js    ✅ Glyph brush
│   ├── styles.css         ✅ Estilos
│   ├── data/              ⚠️ NO incluir en Git (muy grande)
│   └── images/            ⚠️ Solo imágenes necesarias
├── templates/
│   └── index2.html        ✅ Template principal
└── scripts/               ⚠️ Opcional: scripts de utilidades
    └── download_data.py   ⚠️ Si usas descarga externa
```

---

### 5. **Configuración cross-platform**

#### **Python version**
- Mínimo: Python 3.8
- Recomendado: Python 3.9-3.11
- Verificar en requirements.txt:

```txt
# Agregar al inicio de requirements.txt
# Requires Python 3.8+
```

#### **Dependencias específicas de plataforma**

Todas las dependencias en `requirements.txt` son cross-platform ✅

**Verificado:**
- Flask ✅
- numpy ✅
- pandas ✅
- opencv-python-headless ✅ (sin GUI, funciona en servidores)
- scikit-learn ✅
- scipy ✅

---

### 6. **Testing en diferentes plataformas**

#### **Windows:**
```bash
# PowerShell o CMD
run.bat
```

#### **Linux:**
```bash
chmod +x run.sh
./run.sh
```

#### **Mac:**
```bash
chmod +x run.sh
./run.sh
```

#### **Docker (opcional, máxima portabilidad):**

Crear `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8081

CMD ["python", "main2.py"]
```

Crear `docker-compose.yml`:
```yaml
version: '3.8'
services:
  trackvis:
    build: .
    ports:
      - "8081:8081"
    volumes:
      - ./static/data:/app/static/data
```

---

### 7. **GitHub Actions (CI/CD opcional)**

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
        python-version: [3.8, 3.9, '3.10', 3.11]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Test imports
      run: |
        python -c "from app.controllers.heatmap import *"
        python -c "import flask; print('Flask:', flask.__version__)"
```

---

### 8. **Licencia**

Crear `LICENSE`:
```txt
MIT License

Copyright (c) 2024 [Tu Nombre]

Permission is hereby granted, free of charge, to any person obtaining a copy...
[... texto completo de licencia MIT ...]
```

---

### 9. **Releases y Versiones**

#### **Crear tags en Git:**
```bash
# Version 2.0 (main2.py)
git tag -a v2.0.0 -m "Release version 2.0 - main2.py with brush"
git push origin v2.0.0
```

#### **GitHub Releases:**
1. Ve a GitHub → Releases → Create new release
2. Tag: v2.0.0
3. Title: "TrackVis v2.0 - Interactive Brush & Glyph"
4. Description: Changelog
5. Assets: Subir datos (si no usas Git LFS)

---

### 10. **Documentación adicional**

#### **Wiki de GitHub:**
- Installation troubleshooting
- Data format specifications
- API documentation
- Development guide

#### **Screenshots:**
Agregar a README.md:
```markdown
## 📸 Screenshots

![Vista por imagen](docs/screenshots/view1.png)
![Vista por participante](docs/screenshots/view2.png)
![Radial Glyph](docs/screenshots/glyph.png)
```

---

## 🎯 Pasos finales antes del deploy

### 1. Limpiar repositorio
```bash
# Ejecutar script de limpieza
bash scripts/cleanup.sh
```

### 2. Verificar .gitignore
```bash
git status
# Verificar que no haya archivos grandes en stage
```

### 3. Test en local
```bash
# Windows
run.bat

# Linux/Mac
./run.sh
```

### 4. Commit y push
```bash
git add .
git commit -m "chore: prepare for deployment"
git push origin main
```

### 5. Crear release en GitHub
- Tag: v2.0.0
- Incluir datos o link de descarga
- Documentar changelog

---

## 📊 Tamaños de archivos

**Antes de limpieza:**
- CSV: 958 MB
- Total repo: ~1.2 GB ❌ Demasiado grande

**Después de limpieza (sin datos):**
- Código: ~5 MB
- Total repo: ~10 MB (con imágenes) ✅ Aceptable

**Con datos (Git LFS):**
- 638 MB (dentro del límite de 1 GB) ✅

---

## ⚠️ Problemas comunes y soluciones

### Problema 1: "Git push timeout"
**Causa:** Archivos muy grandes
**Solución:** Usar Git LFS o descarga externa

### Problema 2: "ModuleNotFoundError"
**Causa:** Entorno virtual no activado
**Solución:** Seguir instrucciones en README.md

### Problema 3: "Port 8081 already in use"
**Solución:** Cambiar puerto en main2.py o matar proceso:
```bash
# Linux/Mac
lsof -ti:8081 | xargs kill

# Windows
netstat -ano | findstr :8081
taskkill /PID [PID] /F
```

---

## 🎉 ¡Listo para deploy!

Una vez completados todos los pasos, tu repositorio estará listo para que cualquier usuario pueda:

1. Clonar el repo
2. Ejecutar `run.sh` o `run.bat`
3. Abrir http://localhost:8081
4. ¡Usar TrackVis!

---

**Última actualización:** Diciembre 2024

# 👁️ TrackVis - Eye Tracking Visualization System

Sistema de visualización interactiva de datos de eye tracking con análisis de fijaciones, heatmaps y Radial Glyphs.

## 📋 Características

- ✅ Visualización de gaze points y fixations (algoritmo I-VT)
- ✅ Heatmaps de atención por imagen
- ✅ Scarf plots temporales
- ✅ Brush interactivo para selección de áreas
- ✅ Radial Glyph para análisis detallado
- ✅ Análisis por participante
- ✅ Proyecciones t-SNE
- ✅ Saliency coverage analysis
- ✅ Soporte para múltiples datasets (ADE20K, agrupados, disorder)

## 🚀 Instalación

### Requisitos previos

- Python 3.8 o superior
- pip (incluido con Python)
- Git

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tuusuario/trackvis.git
cd trackvis
```

### 2️⃣ Instalar dependencias

#### **En Windows:**

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

#### **En Linux/Mac:**

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3️⃣ Descargar datos (si no están incluidos)

Si los datos no están en el repositorio (debido a tamaño), descárgalos:

```bash
# Opción 1: Desde Google Drive/Dropbox (proporciona el link)
# Descargar y extraer en la carpeta static/data/

# Opción 2: Usar script de descarga
python scripts/download_data.py
```

**Archivos de datos necesarios:**
- `static/data/df_final1.csv` (109 MB) - Datos principales de gaze tracking
- `static/data/ivt_precalculated.csv` (2 MB) - Fijaciones precalculadas
- `static/data/data_hololens.json` (221 KB) - Scores de participantes
- `static/data/data_hololens_vectors.json` (4.6 MB) - Vectores de características
- `static/data/upd_segmentations.csv` (3.7 MB) - Segmentaciones de imágenes
- `static/data/precalculated_saliency_coverage.csv` (72 KB) - Cobertura de saliency

### 4️⃣ Ejecutar la aplicación

#### **Opción 1: Script de inicio (recomendado)**

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

#### **Opción 2: Comando directo**

**Windows:**
```bash
venv\Scripts\python.exe main2.py
```

**Linux/Mac:**
```bash
source venv/bin/activate
python main2.py
```

### 5️⃣ Abrir en el navegador

Abre tu navegador en: **http://localhost:8081**

## 📁 Estructura del proyecto

```
trackvis/
├── main2.py                    # Aplicación principal Flask
├── requirements.txt            # Dependencias Python
├── README.md                   # Este archivo
├── run.sh / run.bat           # Scripts de inicio
├── app/
│   ├── controllers/           # Controllers (blueprints)
│   │   ├── glyph.py          # Radial Glyph
│   │   ├── heatmap.py        # Heatmaps
│   │   ├── scarf_plot.py     # Scarf plots
│   │   └── by_participant.py # Análisis por participante
│   ├── services/             # Servicios
│   │   └── fixation_detection_ivt.py  # Detección de fijaciones I-VT
│   └── shared/               # Servicios compartidos
│       └── tsne_cache_service.py  # Cache de proyecciones t-SNE
├── static/
│   ├── main2.js              # JavaScript principal
│   ├── glyph_brush2.js       # Glyph con brush D3
│   ├── styles.css            # Estilos
│   ├── data/                 # Datos CSV/JSON (NO incluir en Git)
│   └── images/               # Imágenes del estudio
└── templates/
    └── index2.html           # Template principal
```

## 🎮 Uso

### Vista por Imagen (View 1)

1. Selecciona una imagen en el dropdown
2. Elige tipo de datos: Gaze Points o Fixations
3. Selecciona un participante (opcional)
4. Arrastra un rectángulo sobre la imagen (brush)
5. Visualiza el Radial Glyph con análisis del área

### Vista por Participante (View 2)

1. Cambia a la pestaña "By participant"
2. Selecciona un participante
3. Visualiza:
   - Heatmap de atención en todas las imágenes
   - Proyección t-SNE de imágenes
   - Gráfico de saliency coverage

### Overlays disponibles

- **Points:** Muestra puntos de gaze o fixations
- **Contour:** Contorno de fijaciones
- **Heatmap:** Mapa de calor de atención

## 🛠️ Configuración

### Puerto

Por defecto corre en puerto `8081`. Para cambiar:

```python
# En main2.py línea 592
app.run(debug=True, port=8081)  # Cambiar 8081 por el puerto deseado
```

### Datos

Para usar tus propios datos, asegúrate de que tengan el formato correcto:

**df_final1.csv:**
```csv
participante,ImageName,ImageIndex,pixelX,pixelY,Time
1,0,0,400,300,1234567.89
```

**ivt_precalculated.csv:**
```csv
participante,ImageName,ImageIndex,start,end,duration,x_centroid,y_centroid,pointCount
1,0,0,1234567.89,1234568.12,0.23,400,300,15
```

## 🐛 Troubleshooting

### Error: "No module named 'flask'"

```bash
# Asegúrate de activar el entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "Gaze data not loaded"

```bash
# Verifica que los archivos CSV existen
ls static/data/df_final1.csv
ls static/data/ivt_precalculated.csv
```

### El brush no aparece

- Verifica que D3.js se carga correctamente (abre consola del navegador F12)
- Recarga la página con Ctrl+F5 (hard refresh)

### Performance lento

- Los datos se procesan en tiempo real
- Para mejorar performance:
  - Filtra por participante
  - Reduce el área del brush
  - Usa "Fixations" en lugar de "Gaze Points"

## 📊 Algoritmo I-VT

El sistema usa el algoritmo I-VT (Velocity-Threshold Identification) para detección de fijaciones:

- **Velocity threshold:** 1.15 unidades
- **Minimum duration:** 0.0 segundos
- **Image dimensions:** 800x600 pixels

## 🔧 Desarrollo

### Estructura de rutas (main2.py)

```python
/                                          # Vista principal (index2.html)
/api/heatmap/<image_id>                   # Heatmap data
/api/scarf-plot/<image_id>                # Scarf plot data
/api/analyze-area/<image_id>              # Análisis de área (brush)
/api/participants/<image_id>              # Participantes por imagen
```

### Agregar nuevos features

1. Crear controller en `app/controllers/`
2. Registrar blueprint en `main2.py`
3. Agregar ruta en el controller
4. Actualizar `index2.html` y `main2.js`

## 📝 Licencia

[Tu licencia aquí - ej. MIT, GPL, etc.]

## 👥 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📧 Contacto

[Tu email o información de contacto]

## 🙏 Agradecimientos

- Dataset: [Nombre del dataset]
- Segmentación: ADE20K
- Framework: Flask + D3.js
- Algoritmo I-VT: [Referencia al paper]

---

**Última actualización:** Diciembre 2024
**Versión:** 2.0 (main2.py)

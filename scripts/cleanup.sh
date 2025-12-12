#!/bin/bash

# Script de limpieza para preparar el repositorio para deployment
# TrackVis - Eye Tracking Visualization System

echo "🧹 Limpiando repositorio para deployment..."
echo ""

# Contador de archivos eliminados
count=0

# Eliminar documentación de análisis
echo "📄 Eliminando documentación de análisis..."
rm -f ARCHIVOS_NO_USADOS.md && ((count++))
rm -f CSV_NO_USADOS.md && ((count++))
rm -f JSON_NO_USADOS.md && ((count++))
rm -f CONTROLLERS_NO_USADOS.md && ((count++))
rm -f BRUSH_IMPLEMENTACION.md && ((count++))

# Eliminar controllers renombrados
echo "🗑️  Eliminando controllers renombrados..."
find app/controllers -name "*__.py" -delete && ((count++))
find app/controllers -name "*_old.py" -delete && ((count++))

# Eliminar templates renombrados
echo "🗑️  Eliminando templates renombrados..."
find templates -name "*__.html" -delete && ((count++))
find templates -name "*_old.html" -delete && ((count++))

# Eliminar logs
echo "📝 Eliminando logs..."
rm -f *.log && ((count++))
rm -f flask.log flask_new.log server.log && ((count++))

# Eliminar resultados CSV generados
echo "📊 Eliminando resultados CSV generados..."
rm -f RESULTADO_*.csv && ((count++))

# Eliminar glyph data generado
echo "🎯 Eliminando glyph data generado..."
rm -f glyph_data.json && ((count++))

# Limpiar cache de Python
echo "🐍 Limpiando cache de Python..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null
find . -name "*.pyo" -delete 2>/dev/null

# Limpiar cache de notebooks
echo "📓 Limpiando cache de notebooks..."
find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null

# Limpiar archivos temporales
echo "⏳ Limpiando archivos temporales..."
find . -name "*.tmp" -delete 2>/dev/null
find . -name "*.bak" -delete 2>/dev/null
find . -name "*~" -delete 2>/dev/null

echo ""
echo "✅ Limpieza completada"
echo ""
echo "📊 Verificando tamaño del repositorio..."
du -sh . 2>/dev/null | awk '{print "   Tamaño total: " $1}'

echo ""
echo "⚠️  IMPORTANTE: Los archivos de datos (static/data/) no se eliminaron"
echo "   Para deployment en GitHub, considera:"
echo "   1. Usar Git LFS para archivos grandes"
echo "   2. Subir datos a Google Drive/Dropbox"
echo "   3. Ver DEPLOYMENT_GUIDE.md para más información"
echo ""

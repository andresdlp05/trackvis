#!/bin/bash

# Script de inicio para Linux/Mac
# TrackVis - Eye Tracking Visualization System

echo "🚀 Iniciando TrackVis..."
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python 3 no está instalado${NC}"
    echo "Por favor instala Python 3.8 o superior"
    exit 1
fi

echo -e "${GREEN}✅ Python encontrado:${NC} $(python3 --version)"

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Entorno virtual no encontrado. Creando...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Entorno virtual creado${NC}"
fi

# Activar entorno virtual
echo -e "${YELLOW}📦 Activando entorno virtual...${NC}"
source venv/bin/activate

# Verificar si las dependencias están instaladas
if ! python3 -c "import flask" &> /dev/null; then
    echo -e "${YELLOW}⚠️  Dependencias no encontradas. Instalando...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Dependencias instaladas${NC}"
fi

# Verificar que existan los archivos de datos
if [ ! -f "static/data/df_final1.csv" ]; then
    echo -e "${RED}❌ Error: Archivo df_final1.csv no encontrado${NC}"
    echo "Por favor descarga los datos necesarios en static/data/"
    echo "Ver README.md para más información"
    exit 1
fi

if [ ! -f "static/data/ivt_precalculated.csv" ]; then
    echo -e "${RED}❌ Error: Archivo ivt_precalculated.csv no encontrado${NC}"
    echo "Por favor descarga los datos necesarios en static/data/"
    echo "Ver README.md para más información"
    exit 1
fi

echo -e "${GREEN}✅ Archivos de datos encontrados${NC}"
echo ""
echo -e "${GREEN}🎉 Iniciando servidor Flask...${NC}"
echo -e "${YELLOW}📍 URL: http://localhost:8081${NC}"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

# Iniciar la aplicación
python3 main2.py

# 🎯 TrackVis - Eye Tracking Visualization System

Sistema interactivo de visualización de eye tracking con soporte para múltiples datasets de segmentación (ADE20K).

## 🚀 Quick Start con Docker (Recomendado)

La forma más fácil de ejecutar TrackVis en **cualquier sistema operativo** (Windows, Linux, Mac):

### 1. Instalar Docker
- [Docker Desktop para Windows/Mac](https://www.docker.com/products/docker-desktop)
- [Docker para Linux](https://docs.docker.com/engine/install/)

### 2. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/trackvis.git
cd trackvis
```

### 3. Ejecutar con Docker
```bash
docker-compose up -d
```

**¡Eso es todo!** 🎉

Los datos se descargarán automáticamente desde Google Drive la primera vez (~650 MB).

### 4. Acceder
```
http://localhost:8081
```

---

## 📚 Documentación Completa

| Guía | Descripción |
|------|-------------|
| [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) | **Deployment desde GitHub con descarga automática** ⭐ |
| [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md) | Quick start en 4 pasos |
| [DOCKER_GUIDE.md](DOCKER_GUIDE.md) | Guía completa y detallada de Docker |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Deployment sin Docker (manual) |

---

## ✨ Características

- **🖼️ 4 tipos de segmentación:** ADE20K Classes, Groups, Disorder, GroupDisorder
- **🎨 Visualizaciones interactivas:**
  - Heatmaps de atención
  - Scarf plots temporales
  - Radial Glyphs con análisis detallado
  - Brush selection interactivo
  - Proyecciones t-SNE
- **📊 Análisis por participante**
- **🔄 Cambio dinámico entre datasets**
- **🎯 Cross-filtering entre visualizaciones**

---

## 🛠️ Comandos Útiles

### Ver logs
```bash
docker-compose logs -f
```

### Detener la aplicación
```bash
docker-compose down
```

### Reiniciar
```bash
docker-compose restart
```

### Actualizar
```bash
git pull
docker-compose up -d --build
```

---

## 📦 Datos

Los datos se descargan automáticamente desde Google Drive al ejecutar por primera vez:

| Archivo | Tamaño | Contenido |
|---------|--------|-----------|
| data.zip | ~638 MB | Archivos CSV con datos de eye tracking |
| images.zip | ~5 MB | 150 imágenes originales |
| images_seg.zip | Variable | Segmentación ADE20K Classes |
| ADE20K-Group.zip | Variable | Segmentación por grupos |
| ADE20K-Disorder.zip | Variable | Segmentación con disorders |
| ADE20K-GroupDisorder.zip | Variable | Segmentación grupos + disorders |

---

## 🔧 Instalación Manual (Sin Docker)

Si prefieres no usar Docker, consulta [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) para instalación manual.

---

## 📊 Tecnologías

- **Backend:** Flask (Python)
- **Frontend:** D3.js, Vanilla JavaScript
- **Visualización:** D3.js, Canvas API
- **Análisis:** Pandas, NumPy, Scikit-learn
- **Deployment:** Docker, Docker Compose

---

## 🐛 Troubleshooting

### Puerto 8081 ya en uso
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8082:8081"
```

### Descarga falla
```bash
# Ver logs
docker-compose logs

# Descargar manualmente
./scripts/download_images_configured.sh  # Linux/Mac
scripts\download_images_configured.bat    # Windows
```

### Problemas con Docker
Ver [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) para soluciones completas.

---

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE)

---

## 📧 Contacto

Para problemas o preguntas:
1. Revisar [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)
2. Abrir un issue en GitHub

---

**Versión:** 2.0
**Última actualización:** Diciembre 2024

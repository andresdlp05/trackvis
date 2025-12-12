# 🐳 TrackVis - Deployment desde GitHub con Docker

## 📋 Resumen

Esta guía te muestra cómo desplegar TrackVis desde GitHub con Docker. Los datos se descargan **automáticamente** desde Google Drive al iniciar por primera vez.

---

## 🎯 Para Usuarios (Deployment desde GitHub)

### Paso 1: Instalar Docker

**Windows/Mac:**
1. Descargar [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Instalar y reiniciar si es necesario
3. Verificar que Docker Desktop esté corriendo

**Linux (Ubuntu/Debian):**
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo apt-get install docker-compose-plugin

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker
```

### Paso 2: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/trackvis.git
cd trackvis
```

### Paso 3: Ejecutar con Docker

```bash
# Construir y ejecutar (descargará datos automáticamente la primera vez)
docker-compose up -d
```

**IMPORTANTE:** La primera vez tardará más porque descargará:
- Datos CSV (~638 MB)
- Imágenes originales (~5 MB)
- Imágenes de segmentación (~varios MB)

**Progreso de descarga:**
```bash
# Ver logs en tiempo real para ver el progreso
docker-compose logs -f
```

### Paso 4: Acceder a la Aplicación

Una vez completada la descarga:
```
http://localhost:8081
```

---

## 🔄 Uso Diario

### Iniciar la aplicación
```bash
docker-compose up -d
```

### Detener la aplicación
```bash
docker-compose down
```

### Ver logs
```bash
docker-compose logs -f
```

### Reiniciar
```bash
docker-compose restart
```

---

## 📦 Para Mantenedores (Actualizar datos en Google Drive)

Si eres el mantenedor y necesitas actualizar los archivos en Google Drive:

### 1. Comprimir las carpetas

**Windows (PowerShell):**
```powershell
# Data
Compress-Archive -Path static\data\* -DestinationPath data.zip -Force

# Imágenes originales
Compress-Archive -Path static\images\images\images\* -DestinationPath images.zip -Force

# Segmentación - ADE20K Classes
Compress-Archive -Path static\images\images\images_seg\* -DestinationPath images_seg.zip -Force

# Segmentación - Groups
Compress-Archive -Path static\images\images\ADE20K-Group\* -DestinationPath ADE20K-Group.zip -Force

# Segmentación - Disorder
Compress-Archive -Path static\images\images\ADE20K-Disorder\* -DestinationPath ADE20K-Disorder.zip -Force

# Segmentación - GroupDisorder
Compress-Archive -Path static\images\images\ADE20K-GroupDisorder\* -DestinationPath ADE20K-GroupDisorder.zip -Force
```

**Linux/Mac:**
```bash
# Data
zip -r data.zip static/data/

# Imágenes originales
zip -r images.zip static/images/images/images/

# Segmentación - ADE20K Classes
zip -r images_seg.zip static/images/images/images_seg/

# Segmentación - Groups
zip -r ADE20K-Group.zip static/images/images/ADE20K-Group/

# Segmentación - Disorder
zip -r ADE20K-Disorder.zip static/images/images/ADE20K-Disorder/

# Segmentación - GroupDisorder
zip -r ADE20K-GroupDisorder.zip static/images/images/ADE20K-GroupDisorder/
```

### 2. Subir a Google Drive

1. Ir a https://drive.google.com
2. Subir cada archivo .zip
3. Para cada archivo:
   - Clic derecho → Compartir
   - Cambiar a "Cualquier persona con el enlace"
   - Rol: Lector
   - Copiar enlace

### 3. Actualizar FILE_IDs en los scripts

Extraer FILE_ID del enlace de Google Drive:
```
Enlace: https://drive.google.com/file/d/1abc123XYZ456/view?usp=sharing
FILE_ID: 1abc123XYZ456
```

**Editar `scripts/download_images_configured.sh`:**
```bash
DATA_ZIP_ID="TU_NUEVO_FILE_ID"
IMAGES_ORIGINAL_ID="TU_NUEVO_FILE_ID"
IMAGES_SEG_ID="TU_NUEVO_FILE_ID"
IMAGES_GROUP_ID="TU_NUEVO_FILE_ID"
IMAGES_DISORDER_ID="TU_NUEVO_FILE_ID"
IMAGES_GROUP_DISORDER_ID="TU_NUEVO_FILE_ID"
```

**Editar `scripts/download_images_configured.bat`:**
```batch
SET DATA_ZIP_ID=TU_NUEVO_FILE_ID
SET IMAGES_ORIGINAL_ID=TU_NUEVO_FILE_ID
SET IMAGES_SEG_ID=TU_NUEVO_FILE_ID
SET IMAGES_GROUP_ID=TU_NUEVO_FILE_ID
SET IMAGES_DISORDER_ID=TU_NUEVO_FILE_ID
SET IMAGES_GROUP_DISORDER_ID=TU_NUEVO_FILE_ID
```

### 4. Commit y push

```bash
git add scripts/download_images_configured.sh scripts/download_images_configured.bat
git commit -m "Update Google Drive FILE_IDs"
git push origin main
```

---

## 🎓 FILE_IDs Actuales

Los FILE_IDs actualmente configurados son:

| Archivo | FILE_ID |
|---------|---------|
| data.zip | `1VKLKNJts-bRPuXT3i34NpPLjF-RksI9G` |
| images.zip | `14rCekowQUwjdVTEyRvDkbPpYRgRiXYuZ` |
| images_seg.zip | `1uMGA7TJia_VDh5sFz0gGSFU9vNuEAQop` |
| ADE20K-Group.zip | `1P5axVPdDNwCuaXIlWpTwdQ408RFt_HQm` |
| ADE20K-Disorder.zip | `1tbY9eN_WOS3-1RD5lziXB_4RS3TowLzM` |
| ADE20K-GroupDisorder.zip | `1sjLgAjqbX0by5x-8VkSQWoqWORrC5Uxr` |

---

## 🔧 Troubleshooting

### La descarga falla

**Solución 1:** Verificar que los archivos en Google Drive sean públicos
```bash
# Ver logs de error
docker-compose logs
```

**Solución 2:** Descargar manualmente antes de ejecutar Docker
```bash
# Windows
scripts\download_images_configured.bat

# Linux/Mac
chmod +x scripts/download_images_configured.sh
./scripts/download_images_configured.sh

# Luego ejecutar Docker
docker-compose up -d
```

### Puerto 8081 ya en uso

Editar `docker-compose.yml`:
```yaml
ports:
  - "8082:8081"  # Cambiar a puerto 8082
```

### Los datos no persisten

Los datos se guardan en volúmenes Docker nombrados. Para limpiarlos:
```bash
docker-compose down -v  # ADVERTENCIA: Esto eliminará los datos descargados
```

### Actualizar la aplicación

```bash
# Detener
docker-compose down

# Actualizar código
git pull

# Reconstruir y ejecutar
docker-compose up -d --build
```

---

## 📊 Estructura de Archivos Descargados

Después de la primera ejecución, tendrás:

```
trackvis/
├── static/
│   ├── data/
│   │   ├── df_final1.csv
│   │   ├── FINAL_Group.csv
│   │   ├── FINAL_20kDisorder.csv
│   │   ├── FINAL_GroupDisorder.csv
│   │   └── ... (otros archivos CSV/JSON)
│   └── images/
│       └── images/
│           ├── images/           # 150 JPG originales
│           ├── images_seg/       # Segmentación ADE20K Classes
│           ├── ADE20K-Group/     # Segmentación Groups
│           ├── ADE20K-Disorder/  # Segmentación Disorder
│           └── ADE20K-GroupDisorder/  # Segmentación GroupDisorder
```

---

## ⚡ Comandos Útiles

### Ver tamaño de volúmenes Docker
```bash
docker system df -v
```

### Limpiar todo Docker (liberar espacio)
```bash
docker system prune -a --volumes
```

### Entrar al contenedor (debug)
```bash
docker exec -it trackvis-app bash
```

### Forzar re-descarga de datos
```bash
# Eliminar volúmenes
docker-compose down -v

# Reconstruir y ejecutar
docker-compose up -d
```

---

## 📚 Más Información

- [DOCKER_GUIDE.md](DOCKER_GUIDE.md) - Guía completa de Docker
- [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md) - Quick start en 4 pasos
- [README.md](README.md) - Documentación principal

---

## ✅ Ventajas de Esta Solución

✅ **Descarga automática** - No necesitas descargar datos manualmente
✅ **Multiplataforma** - Funciona igual en Windows, Linux y Mac
✅ **Persistencia** - Los datos se mantienen entre reinicios
✅ **Un comando** - `docker-compose up -d` para ejecutar todo
✅ **Reproducible** - Mismo entorno para todos los usuarios
✅ **Fácil actualización** - Solo `git pull` y `docker-compose up -d --build`

---

**Última actualización:** Diciembre 2024
**Versión:** 2.0

# 🐳 TrackVis - Docker Quick Start

## Instalación Rápida en 4 Pasos

### 📋 Requisitos
- Docker Desktop instalado ([Descargar aquí](https://www.docker.com/products/docker-desktop))
- Git + Git LFS configurado (`git lfs install` y `git lfs pull` justo después de clonar)
- Archivos de imágenes en Google Drive

---

## 🚀 Paso 1: Preparar Google Drive

### 1.1 Comprimir carpetas de imágenes

**Windows:**
```powershell
cd static\images\images
Compress-Archive -Path images\* -DestinationPath images_original.zip
Compress-Archive -Path images_seg\* -DestinationPath images_seg.zip
Compress-Archive -Path ADE20K-Group\* -DestinationPath images_group.zip
Compress-Archive -Path ADE20K-Disorder\* -DestinationPath images_disorder.zip
Compress-Archive -Path ADE20K-GroupDisorder\* -DestinationPath images_group_disorder.zip
```

**Linux/Mac:**
```bash
cd static/images/images
zip -r images_original.zip images/
zip -r images_seg.zip images_seg/
zip -r images_group.zip ADE20K-Group/
zip -r images_disorder.zip ADE20K-Disorder/
zip -r images_group_disorder.zip ADE20K-GroupDisorder/
```

### 1.2 Subir a Google Drive

1. Ir a https://drive.google.com
2. Crear carpeta "TrackVis-Data"
3. Subir todos los archivos .zip

### 1.3 Obtener FILE_IDs

Para cada archivo:
1. Clic derecho → Compartir
2. Cambiar a "Cualquier persona con el enlace"
3. Copiar enlace: `https://drive.google.com/file/d/1abc123XYZ456/view?usp=sharing`
4. Extraer FILE_ID: `1abc123XYZ456` (entre `/d/` y `/view`)

---

## 🔧 Paso 2: Configurar Scripts de Descarga

### Windows:
```powershell
notepad scripts\download_images.bat
```

Editar:
```batch
SET IMAGES_ORIGINAL_ID=1abc123XYZ456
SET IMAGES_SEG_ID=1def456ABC789
SET IMAGES_GROUP_ID=1ghi789DEF012
SET IMAGES_DISORDER_ID=1jkl012GHI345
SET IMAGES_GROUP_DISORDER_ID=1mno345JKL678
```

### Linux/Mac:
```bash
nano scripts/download_images.sh
```

Editar:
```bash
IMAGES_ORIGINAL_ID="1abc123XYZ456"
IMAGES_SEG_ID="1def456ABC789"
IMAGES_GROUP_ID="1ghi789DEF012"
IMAGES_DISORDER_ID="1jkl012GHI345"
IMAGES_GROUP_DISORDER_ID="1mno345JKL678"
```

---

## 📥 Paso 3: Descargar Imágenes

### Windows:
```powershell
scripts\download_images.bat
```

### Linux/Mac:
```bash
chmod +x scripts/download_images.sh
./scripts/download_images.sh
```

---

## 🎯 Paso 4: Ejecutar con Docker

```bash
# Construir y ejecutar
docker-compose up -d

# Verificar que esté corriendo
docker-compose ps

# Ver logs
docker-compose logs -f
```

**Acceder a:** http://localhost:8081

---

## 🛠️ Comandos Útiles

### Detener
```bash
docker-compose down
```

### Reiniciar
```bash
docker-compose restart
```

### Ver logs
```bash
docker-compose logs -f
```

### Limpiar todo
```bash
docker-compose down -v
docker system prune -a
```

---

## 📚 Más Información

- **Guía completa de Docker:** [DOCKER_GUIDE.md](DOCKER_GUIDE.md)
- **Checklist de deployment:** [CHECKLIST_DEPLOYMENT.md](CHECKLIST_DEPLOYMENT.md)
- **README principal:** [README.md](README.md)

---

## ❓ Problemas Comunes

### Puerto 8081 ya en uso
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8082:8081"  # Usar 8082 en lugar de 8081
```

### Docker no está corriendo
- Windows/Mac: Abrir Docker Desktop
- Linux: `sudo systemctl start docker`

### Error al descargar imágenes
1. Verificar FILE_IDs correctos
2. Verificar archivos en Google Drive sean públicos
3. Instalar gdown: `pip install gdown`

---

**¡Listo! 🎉** Tu aplicación TrackVis está corriendo en Docker.

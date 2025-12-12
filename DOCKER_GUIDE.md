# 🐳 TrackVis - Guía de Deployment con Docker

## 📋 Tabla de Contenidos

1. [¿Por qué Docker?](#por-qué-docker)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación de Docker](#instalación-de-docker)
4. [Preparar Imágenes en Google Drive](#preparar-imágenes-en-google-drive)
5. [Deployment Paso a Paso](#deployment-paso-a-paso)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 ¿Por qué Docker?

✅ **Ventajas de usar Docker:**
- ✅ Funciona en Windows, Linux y Mac sin modificaciones
- ✅ No necesitas instalar Python ni dependencias manualmente
- ✅ Entorno aislado y reproducible
- ✅ Fácil de distribuir y desplegar
- ✅ Un solo comando para ejecutar todo

---

## 📦 Requisitos Previos

### Software Necesario
1. **Docker Desktop** (incluye docker y docker-compose)
   - Windows/Mac: [Descargar Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Linux: Docker Engine + Docker Compose

### Datos Necesarios
2. **Archivos en Google Drive:**
   - Imágenes originales (150 JPG)
   - Imágenes de segmentación (ADE20K Classes, Groups, Disorder, GroupDisorder)
   - Datos CSV (opcional, pueden estar en el repo)

---

## 🔧 Instalación de Docker

### Windows

1. **Descargar Docker Desktop:**
   ```
   https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
   ```

2. **Instalar:**
   - Ejecutar el instalador
   - Seguir los pasos del wizard
   - Reiniciar el PC si es necesario

3. **Verificar instalación:**
   ```powershell
   docker --version
   docker-compose --version
   ```

4. **Asegurarse de que Docker Desktop esté corriendo:**
   - Buscar el ícono de Docker en la bandeja del sistema
   - Debe mostrar "Docker Desktop is running"

### macOS

1. **Descargar Docker Desktop:**
   ```
   https://desktop.docker.com/mac/main/arm64/Docker.dmg  # Apple Silicon (M1/M2)
   https://desktop.docker.com/mac/main/amd64/Docker.dmg  # Intel
   ```

2. **Instalar:**
   - Arrastrar Docker.app a Applications
   - Abrir Docker desde Applications
   - Seguir el setup inicial

3. **Verificar instalación:**
   ```bash
   docker --version
   docker-compose --version
   ```

### Linux (Ubuntu/Debian)

```bash
# 1. Actualizar sistema
sudo apt-get update

# 2. Instalar prerequisitos
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 3. Agregar GPG key de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 4. Agregar repositorio de Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Instalar Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 6. Agregar tu usuario al grupo docker (para no usar sudo)
sudo usermod -aG docker $USER
newgrp docker

# 7. Verificar instalación
docker --version
docker compose version
```

---

## 📤 Preparar Imágenes en Google Drive

### Paso 1: Subir archivos a Google Drive

1. **Comprimir cada carpeta de imágenes:**

   ```bash
   # En Linux/Mac
   cd static/images/images
   zip -r images_original.zip images/
   zip -r images_seg.zip images_seg/
   zip -r images_group.zip ADE20K-Group/
   zip -r images_disorder.zip ADE20K-Disorder/
   zip -r images_group_disorder.zip ADE20K-GroupDisorder/
   ```

   ```powershell
   # En Windows (PowerShell)
   cd static\images\images
   Compress-Archive -Path images\* -DestinationPath images_original.zip
   Compress-Archive -Path images_seg\* -DestinationPath images_seg.zip
   Compress-Archive -Path ADE20K-Group\* -DestinationPath images_group.zip
   Compress-Archive -Path ADE20K-Disorder\* -DestinationPath images_disorder.zip
   Compress-Archive -Path ADE20K-GroupDisorder\* -DestinationPath images_group_disorder.zip
   ```

2. **Subir a Google Drive:**
   - Ir a [Google Drive](https://drive.google.com)
   - Crear una carpeta "TrackVis-Data"
   - Subir todos los archivos .zip

### Paso 2: Obtener FILE_IDs de Google Drive

Para cada archivo ZIP:

1. **Clic derecho en el archivo** → "Compartir"

2. **Cambiar permisos:**
   - "Restringido" → "Cualquier persona con el enlace"
   - Rol: "Lector"

3. **Copiar enlace**
   ```
   Ejemplo: https://drive.google.com/file/d/1abc123XYZ456def789/view?usp=sharing
   ```

4. **Extraer el FILE_ID** (la parte entre `/d/` y `/view`)
   ```
   FILE_ID = 1abc123XYZ456def789
   ```

5. **Guardar los FILE_IDs** en un documento temporal:
   ```
   IMAGES_ORIGINAL_ID=1abc123XYZ456def789
   IMAGES_SEG_ID=1def456ABC789ghi012
   IMAGES_GROUP_ID=1ghi789DEF012jkl345
   IMAGES_DISORDER_ID=1jkl012GHI345mno678
   IMAGES_GROUP_DISORDER_ID=1mno345JKL678pqr901
   ```

### Paso 3: Configurar scripts de descarga

**Linux/Mac:**
```bash
# Editar el script
nano scripts/download_images.sh

# Reemplazar "YOUR_FILE_ID_HERE" con tus FILE_IDs reales
IMAGES_ORIGINAL_ID="1abc123XYZ456def789"
IMAGES_SEG_ID="1def456ABC789ghi012"
# ... etc
```

**Windows:**
```powershell
# Editar el script
notepad scripts\download_images.bat

# Reemplazar "YOUR_FILE_ID_HERE" con tus FILE_IDs reales
SET IMAGES_ORIGINAL_ID=1abc123XYZ456def789
SET IMAGES_SEG_ID=1def456ABC789ghi012
REM ... etc
```

---

## 🚀 Deployment Paso a Paso

### Opción A: Usando Docker Compose (Recomendado)

**1. Clonar el repositorio:**
```bash
git clone https://github.com/tu-usuario/trackvis.git
cd trackvis
git lfs install
git lfs pull
```

**2. Descargar imágenes desde Google Drive:**

**Linux/Mac:**
```bash
chmod +x scripts/download_images.sh
./scripts/download_images.sh
```

**Windows:**
```powershell
scripts\download_images.bat
```

**3. Construir y ejecutar con Docker Compose:**
```bash
docker-compose up -d
```

**4. Verificar que esté corriendo:**
```bash
docker-compose ps
```

**5. Acceder a la aplicación:**
```
http://localhost:8081
```

**6. Ver logs (si hay problemas):**
```bash
docker-compose logs -f
```

**7. Detener la aplicación:**
```bash
docker-compose down
```

---

### Opción B: Usando Docker sin Compose

**1. Construir la imagen:**
```bash
docker build -t trackvis:latest .
```

**2. Ejecutar el contenedor:**
```bash
docker run -d \
  --name trackvis-app \
  -p 8081:8081 \
  -v $(pwd)/static/data:/app/static/data \
  -v $(pwd)/static/images:/app/static/images \
  trackvis:latest
```

**Windows PowerShell:**
```powershell
docker run -d `
  --name trackvis-app `
  -p 8081:8081 `
  -v ${PWD}/static/data:/app/static/data `
  -v ${PWD}/static/images:/app/static/images `
  trackvis:latest
```

**3. Ver logs:**
```bash
docker logs -f trackvis-app
```

**4. Detener:**
```bash
docker stop trackvis-app
docker rm trackvis-app
```

---

## 🎯 Comandos Útiles

### Ver contenedores corriendo
```bash
docker ps
```

### Ver todos los contenedores (incluidos detenidos)
```bash
docker ps -a
```

### Ver logs en tiempo real
```bash
docker-compose logs -f
# o
docker logs -f trackvis-app
```

### Reiniciar el contenedor
```bash
docker-compose restart
# o
docker restart trackvis-app
```

### Entrar al contenedor (para debug)
```bash
docker exec -it trackvis-app bash
```

### Limpiar todo (contenedores, imágenes, volúmenes)
```bash
docker-compose down -v
docker system prune -a
```

---

## 📊 Estructura de Volúmenes

Los datos persistentes se montan en:

```
./static/data      →  /app/static/data      (CSV files)
./static/images    →  /app/static/images    (Image folders)
```

Esto significa que:
- ✅ Los datos no se pierden si reinicias el contenedor
- ✅ Puedes actualizar imágenes sin reconstruir la imagen Docker
- ✅ Puedes compartir datos entre host y contenedor

---

## 🔍 Troubleshooting

### Problema: "Port 8081 is already allocated"

**Solución:** Cambiar el puerto en docker-compose.yml:
```yaml
ports:
  - "8082:8081"  # Usar puerto 8082 en lugar de 8081
```

### Problema: "Cannot connect to Docker daemon"

**Solución:**
- Windows/Mac: Asegúrate de que Docker Desktop esté corriendo
- Linux: `sudo systemctl start docker`

### Problema: "ERROR: download failed"

**Solución:**
1. Verificar que los FILE_IDs sean correctos
2. Verificar que los archivos en Google Drive sean públicos (Anyone with the link)
3. Instalar gdown manualmente: `pip install gdown`

### Problema: "Container exits immediately"

**Solución:**
```bash
# Ver logs de error
docker-compose logs

# Entrar al contenedor para debug
docker-compose run trackvis bash
python main.py
```

### Problema: "Module not found"

**Solución:** Reconstruir la imagen:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Problema: Imágenes no se ven

**Solución:**
1. Verificar que las carpetas de imágenes estén pobladas:
   ```bash
   ls -la static/images/images/images/
   ```
2. Verificar volúmenes:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

---

## 📝 Notas Finales

### Para desarrollo
```bash
# Usar docker-compose.dev.yml (si existe)
docker-compose -f docker-compose.dev.yml up
```

### Para producción
```bash
# Usar docker-compose.yml
docker-compose up -d
```

### Actualizar la aplicación
```bash
# 1. Detener contenedor
docker-compose down

# 2. Actualizar código
git pull

# 3. Reconstruir imagen
docker-compose build

# 4. Reiniciar
docker-compose up -d
```

---

## 🎓 Recursos Adicionales

- [Documentación oficial de Docker](https://docs.docker.com/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Docker Hub](https://hub.docker.com/)
- [Best practices for Dockerfile](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

## 📧 Soporte

Si tienes problemas con el deployment de Docker:
1. Revisa esta guía completa
2. Verifica los logs: `docker-compose logs -f`
3. Abre un issue en GitHub con los logs de error

---

**Última actualización:** Diciembre 2024
**Versión de Docker:** 24.0+
**Versión de Docker Compose:** 2.0+

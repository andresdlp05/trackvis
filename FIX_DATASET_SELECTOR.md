# 🔧 Fix: Dataset Selector (Segmentation Class)

## 🐛 Problema Reportado

Al seleccionar diferentes opciones en "Segmentation Class", todas mostraban los mismos resultados:
- ❌ ADE20K Classes = ADE20K + Disorder Classes
- ❌ ADE20K + Grouped Classes = ADE20K + Grouped + Disorder Classes

## ✅ Solución Implementada

### 1. **Creado DataService** ([app/shared/data_service.py](app/shared/data_service.py))

Servicio singleton que carga los CSVs correctos según el dataset seleccionado:

```python
dataset_files = {
    'main_class': 'static/data/df_final1.csv',              # ✅ ADE20K Classes
    'grouped': 'static/data/FINAL_Group.csv',               # ✅ ADE20K + Grouped
    'disorder': 'static/data/FINAL_20kDisorder.csv',        # ✅ ADE20K + Disorder
    'grouped_disorder': 'static/data/FINAL_GroupDisorder.csv' # ✅ All combined
}
```

### 2. **Actualizado app/shared/__init__.py**

Exporta correctamente el DataService para que los controllers puedan usarlo.

### 3. **Verificado rutas de imágenes de segmentación**

```javascript
// main2.js - getSegmentationPath()
'main_class'        → /static/images/images/images_seg/{id}.JPEG
'grouped'           → /static/images/images/ADE20K-Group/images/{id}.png
'disorder'          → /static/images/images/ADE20K-Disorder/images/{id}.png
'grouped_disorder'  → /static/images/images/ADE20K-GroupDisorder/images/{id}.png
```

✅ Todas las carpetas y archivos existen correctamente.

---

## 🚀 Cómo Aplicar el Fix

### 1. **Reiniciar el servidor**

El DataService se carga al iniciar, por lo que debes reiniciar:

```bash
# Detener el servidor (Ctrl+C)

# Reiniciar
./run.sh      # Linux/Mac
run.bat       # Windows
```

### 2. **Verificar que carga correctamente**

Al iniciar, deberías ver en la consola:

```
✅ DataService importado correctamente
✅ PrecomputedFixationService importado correctamente
✅ TSNECacheService importado correctamente
✅ OK: Heatmap: Servicio compartido de datos HABILITADO
DataService: Scores cargados (150 imágenes)
```

### 3. **Probar en el navegador**

1. Abre http://localhost:8081
2. Selecciona una imagen
3. Cambia "Segmentation Class" entre las opciones
4. **Verifica que:**
   - Las imágenes de segmentación cambien
   - El heatmap muestre diferentes clases
   - El scarf plot se actualice

---

## 🔍 Cómo verificar que funciona

### Test 1: Cambiar dataset y ver la imagen de segmentación

1. Selecciona "ADE20K Classes" → Ver segmentación
2. Selecciona "ADE20K + Grouped Classes" → Ver segmentación
3. Las imágenes deberían ser **diferentes**

### Test 2: Ver en la consola del navegador (F12)

Al cambiar dataset, deberías ver:

```
DATA SET SELECTOR CHANGED - New value: grouped
Reloading heatmap and scarf plot with dataset_select=grouped
Updated segmentation path: /static/images/images/ADE20K-Group/images/5.png
```

### Test 3: Ver en la consola del servidor

Al cargar datos, deberías ver:

```
DataService: Cargando dataset 'grouped' desde static/data/FINAL_Group.csv...
✅ DataService: Dataset 'grouped' cargado (XXX filas, YY columnas)
   Columnas encontradas: group ✅
```

---

## 📊 Datasets Disponibles

| Opción | CSV | Tamaño | Clases |
|--------|-----|--------|--------|
| **ADE20K Classes** | df_final1.csv | 109 MB | Solo clases base ADE20K |
| **ADE20K + Grouped** | FINAL_Group.csv | 172 MB | Clases base + agrupadas |
| **ADE20K + Disorder** | FINAL_20kDisorder.csv | 161 MB | Clases base + disorder |
| **ADE20K + Grouped + Disorder** | FINAL_GroupDisorder.csv | 177 MB | Todas las clases combinadas |

---

## 🐛 Troubleshooting

### Error: "Dataset 'grouped' no disponible"

**Causa:** El archivo CSV no existe
**Solución:**
```bash
# Verificar que el archivo existe
ls static/data/FINAL_Group.csv
ls static/data/FINAL_20kDisorder.csv
ls static/data/FINAL_GroupDisorder.csv
```

Si no existen, necesitas descargarlos o generarlos.

### Error: "No group column found in dataset"

**Causa:** El CSV no tiene la columna esperada
**Solución:** Verificar que el CSV tenga las columnas correctas:
- FINAL_Group.csv debe tener columna `group`, `group_name` o `grupo`
- FINAL_20kDisorder.csv debe tener columna `main_class`
- FINAL_GroupDisorder.csv debe tener ambas

### Las imágenes de segmentación no cambian

**Causa:** Rutas incorrectas o archivos faltantes
**Solución:**
```bash
# Verificar que las carpetas existen
ls static/images/images/images_seg/
ls static/images/images/ADE20K-Group/images/
ls static/images/images/ADE20K-Disorder/images/
ls static/images/images/ADE20K-GroupDisorder/images/
```

### El heatmap muestra las mismas clases

**Causa:** DataService no está cargando los CSVs correctos
**Solución:**
1. Reiniciar el servidor
2. Verificar en la consola que DataService se importó correctamente
3. Verificar en los logs que está cargando el CSV correcto

---

## 📝 Archivos Modificados

1. **Creados:**
   - `app/shared/data_service.py` - Servicio para gestionar múltiples datasets

2. **Actualizados:**
   - `app/shared/__init__.py` - Exporta DataService

3. **Ya existían (sin cambios):**
   - `app/controllers/heatmap.py` - Ya tenía código para usar DataService
   - `app/controllers/scarf_plot.py` - Ya tenía código para usar DataService
   - `static/main2.js` - getSegmentationPath ya estaba correcta

---

## ✅ Checklist de Verificación

Después de reiniciar el servidor:

- [ ] Servidor inicia sin errores
- [ ] Consola muestra "✅ DataService importado correctamente"
- [ ] Puedo seleccionar una imagen
- [ ] Al cambiar "Segmentation Class", la imagen de segmentación cambia
- [ ] El heatmap muestra diferentes clases según el dataset
- [ ] El scarf plot se actualiza con el nuevo dataset
- [ ] La consola del navegador muestra los mensajes de cambio de dataset

---

**Fecha:** 11 de Diciembre, 2024
**Estado:** ✅ Fix Implementado - Requiere reinicio del servidor

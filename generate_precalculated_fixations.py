#!/usr/bin/env python3
"""
Script para pre-calcular todas las fijaciones usando I-VT y guardarlas en CSV
Esto hace el sistema mucho más rápido al evitar cálculos en tiempo real.
"""

import pandas as pd
import numpy as np
import os
import time
from fixation_detection_ivt import FixationDetectorIVT

def load_main_data():
    """Cargar datos principales del eye tracking"""
    data_path = os.path.join('static', 'data', 'df_final1.csv')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"No se encontró el archivo: {data_path}")
    
    print(f"📂 Cargando datos desde: {data_path}")
    df = pd.read_csv(data_path)
    print(f"✅ Datos cargados: {len(df)} filas")
    print(f"📊 Participantes: {df['participante'].nunique()}")
    print(f"🖼️ Imágenes: {df['ImageName'].nunique()}")
    
    return df

def calculate_all_fixations(df, velocity_threshold=1.15, min_duration=0.0):
    """
    Calcular todas las fijaciones para todos los participantes e imágenes
    
    Args:
        df: DataFrame con datos de eye tracking
        velocity_threshold: Umbral de velocidad en px/s
        min_duration: Duración mínima de fijación en segundos
        
    Returns:
        DataFrame con todas las fijaciones calculadas
    """
    
    print(f"🎯 Iniciando cálculo de fijaciones con parámetros:")
    print(f"   - Umbral velocidad: {velocity_threshold} px/s")
    print(f"   - Duración mínima: {min_duration} s")
    
    # Crear detector I-VT
    detector = FixationDetectorIVT(velocity_threshold=velocity_threshold, 
                                  min_duration=min_duration)
    
    # Lista para almacenar todas las fijaciones
    all_fixations = []
    
    # Obtener combinaciones únicas de participante e imagen
    combinations = df.groupby(['participante', 'ImageName']).size().reset_index()
    total_combinations = len(combinations)
    
    print(f"🔄 Procesando {total_combinations} combinaciones participante-imagen...")
    
    start_time = time.time()
    processed = 0
    
    for _, row in combinations.iterrows():
        participant_id = row['participante']
        image_id = row['ImageName']
        
        # Filtrar datos para esta combinación
        participant_data = df[
            (df['participante'] == participant_id) & 
            (df['ImageName'] == image_id)
        ].copy()
        
        if len(participant_data) == 0:
            continue
            
        try:
            # Detectar fijaciones usando I-VT
            fixations = detector.detect_fixations(participant_data, 800, 600)
            
            # Agregar información adicional a cada fijación
            for fixation in fixations:
                fixation_record = {
                    'participante': participant_id,
                    'ImageName': image_id,
                    'ImageIndex': image_id,  # Para compatibilidad
                    'start_time': fixation['start'],
                    'end_time': fixation['end'],
                    'duration': fixation['duration'],
                    'x_centroid': fixation['x_centroid'],
                    'y_centroid': fixation['y_centroid'],
                    'point_count': fixation['pointCount'],
                    
                    # Calcular índices de patch para diferentes tamaños
                    'patch_10_x': int(fixation['x_centroid'] // 10),
                    'patch_10_y': int(fixation['y_centroid'] // 10),
                    'patch_10_index': int(fixation['y_centroid'] // 10) * (800 // 10) + int(fixation['x_centroid'] // 10),
                    
                    'patch_20_x': int(fixation['x_centroid'] // 20),
                    'patch_20_y': int(fixation['y_centroid'] // 20),
                    'patch_20_index': int(fixation['y_centroid'] // 20) * (800 // 20) + int(fixation['x_centroid'] // 20),
                    
                    'patch_40_x': int(fixation['x_centroid'] // 40),
                    'patch_40_y': int(fixation['y_centroid'] // 40),
                    'patch_40_index': int(fixation['y_centroid'] // 40) * (800 // 40) + int(fixation['x_centroid'] // 40),
                    
                    # Metadata
                    'algorithm': 'I-VT',
                    'velocity_threshold': velocity_threshold,
                    'min_duration': min_duration,
                    'raw_gaze_points': len(participant_data)
                }
                
                all_fixations.append(fixation_record)
                
        except Exception as e:
            print(f"❌ Error procesando participante {participant_id}, imagen {image_id}: {e}")
            continue
        
        processed += 1
        
        # Mostrar progreso cada 100 combinaciones
        if processed % 100 == 0 or processed == total_combinations:
            elapsed = time.time() - start_time
            rate = processed / elapsed if elapsed > 0 else 0
            eta = (total_combinations - processed) / rate if rate > 0 else 0
            
            print(f"⏳ Progreso: {processed}/{total_combinations} ({processed/total_combinations*100:.1f}%) "
                  f"- {rate:.1f} comb/s - ETA: {eta:.0f}s")
    
    # Crear DataFrame con todas las fijaciones
    fixations_df = pd.DataFrame(all_fixations)
    
    total_time = time.time() - start_time
    print(f"✅ Procesamiento completo en {total_time:.2f} segundos")
    print(f"🎯 Total fijaciones detectadas: {len(fixations_df)}")
    
    if len(fixations_df) > 0:
        print(f"📊 Estadísticas:")
        print(f"   - Fijaciones por participante: {fixations_df.groupby('participante').size().mean():.1f}")
        print(f"   - Duración promedio: {fixations_df['duration'].mean():.3f}s")
        print(f"   - Puntos promedio por fijación: {fixations_df['point_count'].mean():.1f}")
    
    return fixations_df

def save_fixations_csv(fixations_df, output_path):
    """Guardar fijaciones en CSV"""
    
    print(f"💾 Guardando fijaciones en: {output_path}")
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Guardar CSV
    fixations_df.to_csv(output_path, index=False)
    
    # Verificar archivo guardado
    file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
    print(f"✅ Archivo guardado: {file_size:.2f} MB")
    
    return output_path

def create_summary_stats(fixations_df):
    """Crear estadísticas resumen"""
    
    if len(fixations_df) == 0:
        return {}
    
    stats = {
        'total_fixations': len(fixations_df),
        'unique_participants': fixations_df['participante'].nunique(),
        'unique_images': fixations_df['ImageName'].nunique(),
        'avg_duration': fixations_df['duration'].mean(),
        'median_duration': fixations_df['duration'].median(),
        'min_duration': fixations_df['duration'].min(),
        'max_duration': fixations_df['duration'].max(),
        'avg_points_per_fixation': fixations_df['point_count'].mean(),
        'total_raw_points': fixations_df['raw_gaze_points'].sum(),
        
        # Estadísticas por patch size
        'patches_10x10_used': fixations_df['patch_10_index'].nunique(),
        'patches_20x20_used': fixations_df['patch_20_index'].nunique(),
        'patches_40x40_used': fixations_df['patch_40_index'].nunique(),
        
        # Por participante
        'fixations_per_participant': fixations_df.groupby('participante').size().to_dict(),
        'fixations_per_image': fixations_df.groupby('ImageName').size().to_dict()
    }
    
    return stats

def main():
    """Función principal"""
    
    print("🚀 GENERADOR DE FIJACIONES PRE-CALCULADAS")
    print("=" * 50)
    
    try:
        # 1. Cargar datos principales
        df = load_main_data()
        
        # 2. Calcular todas las fijaciones
        fixations_df = calculate_all_fixations(df)
        
        if len(fixations_df) == 0:
            print("❌ No se detectaron fijaciones. Verifica los datos de entrada.")
            return
        
        # 3. Guardar CSV principal
        output_path = os.path.join('static', 'data', 'precalculated_fixations.csv')
        save_fixations_csv(fixations_df, output_path)
        
        # 4. Crear estadísticas resumen
        stats = create_summary_stats(fixations_df)
        
        # 5. Guardar estadísticas
        stats_path = os.path.join('static', 'data', 'fixation_stats.json')
        import json
        with open(stats_path, 'w') as f:
            # Convertir sets y otros tipos no serializables
            serializable_stats = {}
            for key, value in stats.items():
                if isinstance(value, (dict, list, str, int, float, bool, type(None))):
                    serializable_stats[key] = value
                else:
                    serializable_stats[key] = str(value)
            
            json.dump(serializable_stats, f, indent=2)
        
        print(f"📊 Estadísticas guardadas en: {stats_path}")
        
        # 6. Resumen final
        print("\n🎉 GENERACIÓN COMPLETADA")
        print("=" * 30)
        print(f"✅ Fijaciones: {stats['total_fixations']}")
        print(f"✅ Participantes: {stats['unique_participants']}")
        print(f"✅ Imágenes: {stats['unique_images']}")
        print(f"✅ Duración promedio: {stats['avg_duration']:.3f}s")
        print(f"✅ Archivo principal: {output_path}")
        print(f"✅ Estadísticas: {stats_path}")
        
        print(f"\n💡 El sistema ahora puede usar fijaciones pre-calculadas para mayor velocidad!")
        
    except Exception as e:
        print(f"❌ Error durante la generación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
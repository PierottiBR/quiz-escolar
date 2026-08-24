"""
Script de prueba para funciones de torneos.
Ejecutar: python test_tournament_functions.py
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent))

from app_utils import (
    crear_torneo,
    obtener_torneo,
    listar_torneos_activos,
    listar_todos_torneos,
    actualizar_torneo,
    eliminar_torneo,
    registrar_respuesta_torneo,
    contar_preguntas_hoy_alumno,
    puede_responder_hoy,
    obtener_respuestas_alumno_torneo,
    obtener_ranking_torneo,
    obtener_estadisticas_torneo,
    GRADE_OPTIONS,
    COURSE_OPTIONS,
)


def test_torneo_crud():
    print("\n🧪 PRUEBA: CRUD de Torneos")
    print("=" * 60)
    
    # Test 1: Crear torneo
    try:
        hoy = datetime.now().strftime("%d/%m/%Y")
        manana = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")
        
        torneo_id = crear_torneo(
            nombre="Torneo Matemáticas 4°",
            descripcion="Competencia de matemáticas para Primaria",
            fecha_inicio=hoy,
            fecha_limite=manana,
            preguntas_por_dia=10,
            grado="Primaria",
            materia="Matemática",
            creador="maestro"
        )
        print(f"✓ Crear torneo: OK (ID: {torneo_id})")
    except Exception as e:
        print(f"✗ Crear torneo: FALLO - {e}")
        return
    
    # Test 2: Obtener torneo
    try:
        torneo = obtener_torneo(torneo_id)
        if torneo and torneo.get("nombre") == "Torneo Matemáticas 4°":
            print("✓ Obtener torneo: OK")
        else:
            print("✗ Obtener torneo: FALLO")
    except Exception as e:
        print(f"✗ Obtener torneo: FALLO - {e}")
    
    # Test 3: Listar torneos activos
    try:
        torneos = listar_torneos_activos()
        if len(torneos) > 0:
            print(f"✓ Listar torneos activos: OK ({len(torneos)} torneos)")
        else:
            print("✗ Listar torneos activos: FALLO - Lista vacía")
    except Exception as e:
        print(f"✗ Listar torneos activos: FALLO - {e}")
    
    # Test 4: Actualizar torneo
    try:
        actualizar_torneo(torneo_id, nombre="Torneo Matemáticas 4° - Actualizado")
        torneo_actualizado = obtener_torneo(torneo_id)
        if torneo_actualizado.get("nombre") == "Torneo Matemáticas 4° - Actualizado":
            print("✓ Actualizar torneo: OK")
        else:
            print("✗ Actualizar torneo: FALLO")
    except Exception as e:
        print(f"✗ Actualizar torneo: FALLO - {e}")
    
    # Test 5: Eliminar torneo
    try:
        eliminar_torneo(torneo_id)
        torneo_eliminado = obtener_torneo(torneo_id)
        if torneo_eliminado is None:
            print("✓ Eliminar torneo: OK")
        else:
            print("✗ Eliminar torneo: FALLO")
    except Exception as e:
        print(f"✗ Eliminar torneo: FALLO - {e}")


def test_respuestas_torneo():
    print("\n🧪 PRUEBA: Respuestas y Límites Diarios")
    print("=" * 60)
    
    # Crear un torneo de prueba
    try:
        hoy = datetime.now().strftime("%d/%m/%Y")
        manana = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")
        
        torneo_id = crear_torneo(
            nombre="Torneo Prueba Respuestas",
            descripcion="Torneo para probar respuestas",
            fecha_inicio=hoy,
            fecha_limite=manana,
            preguntas_por_dia=3,
            grado="Primaria",
            materia="Matemática",
            creador="maestro"
        )
    except Exception as e:
        print(f"✗ No se pudo crear torneo de prueba: {e}")
        return
    
    # Test 1: Registrar respuesta
    try:
        registrar_respuesta_torneo(torneo_id, "alumno_test", "pregunta_1", "Opción A", True)
        print("✓ Registrar respuesta: OK")
    except Exception as e:
        print(f"✗ Registrar respuesta: FALLO - {e}")
    
    # Test 2: Contar preguntas hoy
    try:
        contador = contar_preguntas_hoy_alumno(torneo_id, "alumno_test")
        if contador == 1:
            print(f"✓ Contar preguntas hoy: OK ({contador} pregunta)")
        else:
            print(f"✗ Contar preguntas hoy: FALLO (esperado 1, obtuvo {contador})")
    except Exception as e:
        print(f"✗ Contar preguntas hoy: FALLO - {e}")
    
    # Test 3: Registrar más respuestas para probar límite
    try:
        registrar_respuesta_torneo(torneo_id, "alumno_test", "pregunta_2", "Opción B", False)
        registrar_respuesta_torneo(torneo_id, "alumno_test", "pregunta_3", "Opción C", True)
        
        contador = contar_preguntas_hoy_alumno(torneo_id, "alumno_test")
        if contador == 3:
            print(f"✓ Múltiples respuestas: OK ({contador} preguntas)")
        else:
            print(f"✗ Múltiples respuestas: FALLO")
    except Exception as e:
        print(f"✗ Múltiples respuestas: FALLO - {e}")
    
    # Test 4: Verificar límite diario
    try:
        puede_responder = puede_responder_hoy(torneo_id, "alumno_test", 3)
        if not puede_responder:
            print("✓ Límite diario: OK (No puede responder más)")
        else:
            print("✗ Límite diario: FALLO (Debería estar bloqueado)")
    except Exception as e:
        print(f"✗ Límite diario: FALLO - {e}")
    
    # Test 5: Obtener respuestas del alumno
    try:
        respuestas = obtener_respuestas_alumno_torneo(torneo_id, "alumno_test")
        if len(respuestas) == 3:
            print(f"✓ Obtener respuestas alumno: OK ({len(respuestas)} respuestas)")
        else:
            print(f"✗ Obtener respuestas alumno: FALLO")
    except Exception as e:
        print(f"✗ Obtener respuestas alumno: FALLO - {e}")
    
    # Test 6: Obtener ranking
    try:
        ranking = obtener_ranking_torneo(torneo_id)
        if len(ranking) > 0:
            usuario, stats = ranking[0]
            print(f"✓ Obtener ranking: OK ({usuario}: {stats['correctas']}/{stats['total']} correctas)")
        else:
            print("✗ Obtener ranking: FALLO")
    except Exception as e:
        print(f"✗ Obtener ranking: FALLO - {e}")
    
    # Test 7: Estadísticas del torneo
    try:
        stats = obtener_estadisticas_torneo(torneo_id)
        print(f"✓ Estadísticas torneo: OK")
        print(f"   - Total respuestas: {stats['total_respuestas']}")
        print(f"   - Correctas: {stats['respuestas_correctas']}")
        print(f"   - Incorrectas: {stats['respuestas_incorrectas']}")
        print(f"   - Porcentaje acierto: {stats['porcentaje_acierto']}%")
        print(f"   - Estudiantes: {stats['estudiantes_participantes']}")
    except Exception as e:
        print(f"✗ Estadísticas torneo: FALLO - {e}")
    
    # Limpiar
    try:
        eliminar_torneo(torneo_id)
    except:
        pass


def main():
    print("\n" + "=" * 60)
    print("🧪 SUITE DE PRUEBAS: Funciones de Torneos")
    print("=" * 60)
    
    test_torneo_crud()
    test_respuestas_torneo()
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

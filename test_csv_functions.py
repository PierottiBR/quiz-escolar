"""
Script de prueba para verificar las funciones de actualización de CSV.
Ejecutar: python test_csv_functions.py
"""
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

from app_utils import (
    guardar_alumno,
    guardar_docente,
    guardar_pregunta_csv,
    actualizar_password_alumno,
    actualizar_grado_alumno,
    actualizar_password_docente,
    actualizar_curso_docente,
    actualizar_pregunta_csv,
    eliminar_alumno,
    eliminar_docente,
    eliminar_pregunta_csv,
    obtener_alumno,
    obtener_docente,
    listar_alumnos,
    listar_docentes,
    cargar_preguntas_csv,
    GRADE_OPTIONS,
    COURSE_OPTIONS,
)


def test_estudiantes():
    print("\n🧪 PRUEBA: Funciones de Alumnos")
    print("=" * 50)
    
    # Test 1: Crear alumno
    try:
        guardar_alumno("test_alumno", "password123", "4° Grado")
        print("✓ Crear alumno: OK")
    except Exception as e:
        print(f"✗ Crear alumno: FALLO - {e}")
    
    # Test 2: Obtener alumno
    try:
        alumno = obtener_alumno("test_alumno")
        if alumno and alumno.get("usuario") == "test_alumno":
            print("✓ Obtener alumno: OK")
        else:
            print("✗ Obtener alumno: FALLO - No se encontró")
    except Exception as e:
        print(f"✗ Obtener alumno: FALLO - {e}")
    
    # Test 3: Actualizar contraseña
    try:
        actualizar_password_alumno("test_alumno", "nueva_password")
        alumno = obtener_alumno("test_alumno")
        if alumno.get("password") == "nueva_password":
            print("✓ Actualizar contraseña: OK")
        else:
            print("✗ Actualizar contraseña: FALLO - Contraseña no se actualizó")
    except Exception as e:
        print(f"✗ Actualizar contraseña: FALLO - {e}")
    
    # Test 4: Actualizar grado
    try:
        actualizar_grado_alumno("test_alumno", "5° Grado")
        alumno = obtener_alumno("test_alumno")
        if alumno.get("grado") == "5° Grado":
            print("✓ Actualizar grado: OK")
        else:
            print("✗ Actualizar grado: FALLO - Grado no se actualizó")
    except Exception as e:
        print(f"✗ Actualizar grado: FALLO - {e}")
    
    # Test 5: Listar alumnos
    try:
        alumnos = listar_alumnos()
        if len(alumnos) > 0:
            print(f"✓ Listar alumnos: OK ({len(alumnos)} alumnos)")
        else:
            print("✗ Listar alumnos: FALLO - Lista vacía")
    except Exception as e:
        print(f"✗ Listar alumnos: FALLO - {e}")
    
    # Test 6: Eliminar alumno
    try:
        eliminar_alumno("test_alumno")
        alumno = obtener_alumno("test_alumno")
        if alumno is None:
            print("✓ Eliminar alumno: OK")
        else:
            print("✗ Eliminar alumno: FALLO - Alumno aún existe")
    except Exception as e:
        print(f"✗ Eliminar alumno: FALLO - {e}")


def test_docentes():
    print("\n🧪 PRUEBA: Funciones de Docentes")
    print("=" * 50)
    
    # Test 1: Crear docente
    try:
        guardar_docente("test_docente", "password123", "Matemática")
        print("✓ Crear docente: OK")
    except Exception as e:
        print(f"✗ Crear docente: FALLO - {e}")
    
    # Test 2: Obtener docente
    try:
        docente = obtener_docente("test_docente")
        if docente and docente.get("usuario") == "test_docente":
            print("✓ Obtener docente: OK")
        else:
            print("✗ Obtener docente: FALLO - No se encontró")
    except Exception as e:
        print(f"✗ Obtener docente: FALLO - {e}")
    
    # Test 3: Actualizar contraseña docente
    try:
        actualizar_password_docente("test_docente", "nueva_password")
        docente = obtener_docente("test_docente")
        if docente.get("password") == "nueva_password":
            print("✓ Actualizar contraseña docente: OK")
        else:
            print("✗ Actualizar contraseña docente: FALLO")
    except Exception as e:
        print(f"✗ Actualizar contraseña docente: FALLO - {e}")
    
    # Test 4: Actualizar curso docente
    try:
        actualizar_curso_docente("test_docente", "Lengua")
        docente = obtener_docente("test_docente")
        if docente.get("curso") == "Lengua":
            print("✓ Actualizar curso docente: OK")
        else:
            print("✗ Actualizar curso docente: FALLO")
    except Exception as e:
        print(f"✗ Actualizar curso docente: FALLO - {e}")
    
    # Test 5: Listar docentes
    try:
        docentes = listar_docentes()
        if len(docentes) > 0:
            print(f"✓ Listar docentes: OK ({len(docentes)} docentes)")
        else:
            print("✗ Listar docentes: FALLO - Lista vacía")
    except Exception as e:
        print(f"✗ Listar docentes: FALLO - {e}")
    
    # Test 6: Eliminar docente
    try:
        eliminar_docente("test_docente")
        docente = obtener_docente("test_docente")
        if docente is None:
            print("✓ Eliminar docente: OK")
        else:
            print("✗ Eliminar docente: FALLO - Docente aún existe")
    except Exception as e:
        print(f"✗ Eliminar docente: FALLO - {e}")


def test_preguntas():
    print("\n🧪 PRUEBA: Funciones de Preguntas")
    print("=" * 50)
    
    grado = GRADE_OPTIONS[0]
    materia = COURSE_OPTIONS[0]
    
    # Test 1: Crear pregunta
    try:
        guardar_pregunta_csv(
            grado,
            materia,
            "¿Pregunta de prueba?",
            ["Opción A", "Opción B", "Opción C", "Opción D"],
            "Opción A"
        )
        print("✓ Crear pregunta: OK")
    except Exception as e:
        print(f"✗ Crear pregunta: FALLO - {e}")
    
    # Test 2: Cargar preguntas
    try:
        preguntas = cargar_preguntas_csv(grado, materia)
        if len(preguntas) > 0:
            print(f"✓ Cargar preguntas: OK ({len(preguntas)} preguntas)")
        else:
            print("✗ Cargar preguntas: FALLO - Lista vacía")
    except Exception as e:
        print(f"✗ Cargar preguntas: FALLO - {e}")
    
    # Test 3: Actualizar pregunta
    try:
        preguntas = cargar_preguntas_csv(grado, materia)
        if len(preguntas) > 0:
            idx_test = len(preguntas) - 1
            actualizar_pregunta_csv(
                grado,
                materia,
                idx_test,
                "¿Pregunta actualizada?",
                ["Actualizada A", "Actualizada B", "Actualizada C", "Actualizada D"],
                "Actualizada A"
            )
            preguntas_updated = cargar_preguntas_csv(grado, materia)
            if preguntas_updated[idx_test]["pregunta"] == "¿Pregunta actualizada?":
                print("✓ Actualizar pregunta: OK")
            else:
                print("✗ Actualizar pregunta: FALLO - No se actualizó")
    except Exception as e:
        print(f"✗ Actualizar pregunta: FALLO - {e}")
    
    # Test 4: Eliminar pregunta
    try:
        preguntas_before = cargar_preguntas_csv(grado, materia)
        eliminar_pregunta_csv(grado, materia, len(preguntas_before) - 1)
        preguntas_after = cargar_preguntas_csv(grado, materia)
        if len(preguntas_after) < len(preguntas_before):
            print("✓ Eliminar pregunta: OK")
        else:
            print("✗ Eliminar pregunta: FALLO - No se eliminó")
    except Exception as e:
        print(f"✗ Eliminar pregunta: FALLO - {e}")


def main():
    print("\n" + "=" * 50)
    print("🧪 SUITE DE PRUEBAS: Funciones de Actualización CSV")
    print("=" * 50)
    
    test_estudiantes()
    test_docentes()
    test_preguntas()
    
    print("\n" + "=" * 50)
    print("✅ Pruebas completadas")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()

import csv
import random
from datetime import datetime
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOGO_PATH = BASE_DIR / "LOGO EP 5020 HD.jpg"
DATA_DIR.mkdir(exist_ok=True)

TEACHER_FILE = DATA_DIR / "docentes.csv"
STUDENT_FILE = DATA_DIR / "alumnos.csv"
RESULT_FILE = DATA_DIR / "resultados.csv"
TOURNAMENT_FILE = DATA_DIR / "torneos.csv"
TOURNAMENT_RESPONSES_FILE = DATA_DIR / "respuestas_torneo.csv"
GRADE_OPTIONS = ["Primaria", "Secundaria"]
QUESTION_HEADERS = ["pregunta", "opcion_1", "opcion_2", "opcion_3", "opcion_4", "respuesta"]
RESULT_HEADERS = ["usuario", "grado", "puntaje", "total", "fecha"]
TOURNAMENT_HEADERS = ["torneo_id", "nombre", "descripcion", "fecha_inicio", "fecha_limite", "preguntas_por_dia", "grado", "creador", "fecha_creacion"]
TOURNAMENT_RESPONSES_HEADERS = ["torneo_id", "usuario", "pregunta_id", "respuesta", "es_correcta", "fecha", "hora"]


def apply_custom_style():
    st.markdown(
        """
        <style>
            :root {
                --escuela-cielo: #8fb6d9;
                --escuela-azul: #386da8;
                --escuela-dorado: #cda66a;
                --escuela-tinta: #1d2730;
                --escuela-fondo: #d4e0e8;
                --escuela-superficie: #e8e3d9;
            }

            html, body, [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #d4e0e8 0%, #c6d6e1 52%, #d9d5cc 100%);
                color: var(--escuela-tinta);
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #234b78 0%, #386da8 100%);
                border-right: 1px solid rgba(255,255,255,0.12);
            }

            [data-testid="stSidebar"] * {
                color: white !important;
            }

            .brand-header {
                background: linear-gradient(135deg, #386da8 0%, #234b78 100%);
                border-radius: 16px;
                padding: 1.2rem 1.4rem;
                box-shadow: 0 12px 25px rgba(35, 75, 120, 0.18);
                border: 1px solid rgba(205, 166, 106, 0.45);
            }

            .brand-title {
                font-size: 2.5rem;
                font-weight: 900;
                letter-spacing: 0.05em;
                margin: 0;
                color: white;
                text-transform: uppercase;
            }

            .brand-subtitle {
                font-size: 0.98rem;
                color: #fff4df;
                margin-top: 0.35rem;
                margin-bottom: 0;
            }

            .stTabs [role="tablist"] {
                gap: 0.6rem;
            }

            .stTabs [role="tab"] {
                border-radius: 12px 12px 0 0;
                background: rgba(205, 166, 106, 0.14);
                color: #171717;
                padding: 0.7rem 1.2rem;
                font-weight: 700;
                border: 1px solid rgba(205, 166, 106, 0.36);
            }

            .stTabs [role="tab"][aria-selected="true"] {
                background: linear-gradient(180deg, #386da8 0%, #234b78 100%);
                color: white;
            }

            .stButton > button {
                background: linear-gradient(180deg, #386da8 0%, #234b78 100%);
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: 700;
                box-shadow: 0 8px 18px rgba(35, 75, 120, 0.16);
            }

            .stTextInput > div > div > input,
            .stSelectbox > div > div,
            .stTextArea > div > div > textarea {
                border-radius: 10px;
                border: 1px solid rgba(56, 109, 168, 0.28);
                background: rgba(232, 227, 217, 0.78);
            }

            div[data-testid="stVerticalBlock"] > div {
                background: rgba(255,255,255,0.08);
                border-radius: 16px;
            }

            img {
                border-radius: 18px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def normalize_grade_name(grade: str) -> str:
    cleaned_grade = grade.strip()
    return cleaned_grade if cleaned_grade in GRADE_OPTIONS else GRADE_OPTIONS[0]


def grade_to_filename(grade: str) -> str:
    normalized_grade = normalize_grade_name(grade)
    return f"{normalized_grade.replace('°', '').replace(' ', '').lower()}.csv"


def ensure_csv(path: Path, headers):
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()


def read_csv_rows(path: Path):
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv_rows(path: Path, rows, headers):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({header: row.get(header, "") for header in headers})


def ensure_seed_data():
    ensure_csv(TEACHER_FILE, ["usuario", "password", "curso"])
    teachers = read_csv_rows(TEACHER_FILE)
    if not teachers:
        with TEACHER_FILE.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["maestro", "escuela123", "Matemática"])

    ensure_csv(STUDENT_FILE, ["usuario", "password", "grado"])
    students = read_csv_rows(STUDENT_FILE)
    students_changed = False
    for student in students:
        normalized_grade = normalize_grade_name(student.get("grado", ""))
        if normalized_grade != student.get("grado", ""):
            student["grado"] = normalized_grade
            students_changed = True
    if students_changed:
        write_csv_rows(STUDENT_FILE, students, ["usuario", "password", "grado"])
    ensure_csv(RESULT_FILE, RESULT_HEADERS)

    for grado in GRADE_OPTIONS:
        grade_file = DATA_DIR / grade_to_filename(grado)
        ensure_csv(grade_file, QUESTION_HEADERS)
        rows = read_csv_rows(grade_file)
        if rows:
            write_csv_rows(grade_file, rows, QUESTION_HEADERS)
            continue

        seed_rows = [
            ["Matemática", "¿Cuánto es 12 + 8?", "18", "20", "22", "16", "20"],
            ["Lengua", "¿Cuál es el sinónimo de 'rápido'?", "Lento", "Veloz", "Triste", "Grande", "Veloz"],
            ["Ciencias", "¿Qué planeta es conocido como el planeta rojo?", "Venus", "Marte", "Júpiter", "Mercurio", "Marte"],
            ["Sociales", "¿Qué es una comunidad?", "Un conjunto de personas que viven juntas", "Un río", "Una montaña", "Un libro", "Un conjunto de personas que viven juntas"],
        ]
        write_csv_rows(
            grade_file,
            [
                {
                    "pregunta": r[1],
                    "opcion_1": r[2],
                    "opcion_2": r[3],
                    "opcion_3": r[4],
                    "opcion_4": r[5],
                    "respuesta": r[6],
                }
                for r in seed_rows
            ],
            QUESTION_HEADERS,
        )


ensure_seed_data()


def get_grade_file(grade: str) -> Path:
    return DATA_DIR / grade_to_filename(grade)


def cargar_preguntas_csv(grade: str, curso=None):
    rows = []
    with get_grade_file(grade).open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("pregunta"):
                continue
            rows.append(
                {
                    "grado": grade,
                    "pregunta": row["pregunta"],
                    "opciones": [
                        row.get("opcion_1", ""),
                        row.get("opcion_2", ""),
                        row.get("opcion_3", ""),
                        row.get("opcion_4", ""),
                    ],
                    "respuesta": row.get("respuesta", ""),
                }
            )
    return rows


def mezclar_opciones_preguntas(preguntas):
    """Devuelve preguntas con sus opciones en un orden aleatorio."""
    preguntas_mezcladas = []
    for pregunta in preguntas:
        pregunta_copia = pregunta.copy()
        pregunta_copia["opciones"] = list(pregunta["opciones"])
        random.shuffle(pregunta_copia["opciones"])
        preguntas_mezcladas.append(pregunta_copia)
    return preguntas_mezcladas


def guardar_pregunta_csv(grade: str, question: str, options, answer: str, course=None):
    path = get_grade_file(grade)
    rows = read_csv_rows(path)
    rows.append(
        {
            "pregunta": question,
            "opcion_1": options[0],
            "opcion_2": options[1],
            "opcion_3": options[2],
            "opcion_4": options[3],
            "respuesta": answer,
        }
    )
    write_csv_rows(path, rows, QUESTION_HEADERS)


def eliminar_pregunta_csv(grade: str, idx: int, course=None):
    path = get_grade_file(grade)
    rows = read_csv_rows(path)
    if idx < 0 or idx >= len(rows):
        return
    rows.pop(idx)
    write_csv_rows(path, rows, QUESTION_HEADERS)


def iniciar_partida(grade: str, course=None):
    preguntas = cargar_preguntas_csv(grade)
    if not preguntas:
        st.warning("Todavía no hay preguntas cargadas para ese nivel.")
        return
    st.session_state.game = {
        "grado": grade,
        "curso": "",
        "preguntas": mezclar_opciones_preguntas(random.sample(preguntas, k=len(preguntas))),
        "indice": 0,
        "puntaje": 0,
        "finalizado": False,
        "respuesta_actual": None,
    }


def get_teacher_by_login(username: str, password: str):
    for row in read_csv_rows(TEACHER_FILE):
        if row.get("usuario") == username and row.get("password") == password:
            return row
    return None


def get_student_by_login(username: str, password: str):
    for row in read_csv_rows(STUDENT_FILE):
        if row.get("usuario") == username and row.get("password") == password:
            return row
    return None


def guardar_alumno(username: str, password: str, grade: str):
    rows = read_csv_rows(STUDENT_FILE)
    if any(r.get("usuario") == username for r in rows):
        raise ValueError("Ese nombre de usuario ya existe.")
    rows.append({"usuario": username, "password": password, "grado": normalize_grade_name(grade)})
    write_csv_rows(STUDENT_FILE, rows, ["usuario", "password", "grado"])


def actualizar_password_alumno(username: str, nueva_password: str):
    rows = read_csv_rows(STUDENT_FILE)
    for row in rows:
        if row.get("usuario") == username:
            row["password"] = nueva_password
            break
    write_csv_rows(STUDENT_FILE, rows, ["usuario", "password", "grado"])


def actualizar_grado_alumno(username: str, nuevo_grado: str):
    rows = read_csv_rows(STUDENT_FILE)
    for row in rows:
        if row.get("usuario") == username:
            row["grado"] = normalize_grade_name(nuevo_grado)
            break
    write_csv_rows(STUDENT_FILE, rows, ["usuario", "password", "grado"])


def registrar_resultado_alumno(usuario: str, grado: str, materia_or_puntaje, puntaje_or_total=None, total=None):
    if total is None:
        puntaje = materia_or_puntaje
        total = puntaje_or_total
    else:
        puntaje = puntaje_or_total
    rows = read_csv_rows(RESULT_FILE)
    rows.append(
        {
            "usuario": usuario,
            "grado": grado,
            "puntaje": str(puntaje),
            "total": str(total),
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        }
    )
    write_csv_rows(RESULT_FILE, rows, RESULT_HEADERS)


def get_historial_resultados():
    return read_csv_rows(RESULT_FILE)


def get_historial_por_alumno(usuario: str):
    return [row for row in read_csv_rows(RESULT_FILE) if row.get("usuario") == usuario]


def guardar_docente(username: str, password: str, curso=""):
    rows = read_csv_rows(TEACHER_FILE)
    if any(r.get("usuario") == username for r in rows):
        raise ValueError("Ese docente ya existe.")
    rows.append({"usuario": username, "password": password, "curso": curso})
    write_csv_rows(TEACHER_FILE, rows, ["usuario", "password", "curso"])


def actualizar_password_docente(username: str, nueva_password: str):
    """Actualiza la contraseña de un docente."""
    rows = read_csv_rows(TEACHER_FILE)
    found = False
    for row in rows:
        if row.get("usuario") == username:
            row["password"] = nueva_password
            found = True
            break
    if not found:
        raise ValueError(f"Docente '{username}' no encontrado.")
    write_csv_rows(TEACHER_FILE, rows, ["usuario", "password", "curso"])


def actualizar_curso_docente(username: str, nuevo_curso: str):
    """Actualiza el curso asignado a un docente."""
    rows = read_csv_rows(TEACHER_FILE)
    found = False
    for row in rows:
        if row.get("usuario") == username:
            row["curso"] = nuevo_curso
            found = True
            break
    if not found:
        raise ValueError(f"Docente '{username}' no encontrado.")
    write_csv_rows(TEACHER_FILE, rows, ["usuario", "password", "curso"])


def eliminar_docente(username: str):
    """Elimina un docente del sistema."""
    rows = read_csv_rows(TEACHER_FILE)
    rows_updated = [r for r in rows if r.get("usuario") != username]
    if len(rows_updated) == len(rows):
        raise ValueError(f"Docente '{username}' no encontrado.")
    write_csv_rows(TEACHER_FILE, rows_updated, ["usuario", "password", "curso"])


def eliminar_alumno(username: str):
    """Elimina un alumno del sistema."""
    rows = read_csv_rows(STUDENT_FILE)
    rows_updated = [r for r in rows if r.get("usuario") != username]
    if len(rows_updated) == len(rows):
        raise ValueError(f"Alumno '{username}' no encontrado.")
    write_csv_rows(STUDENT_FILE, rows_updated, ["usuario", "password", "grado"])


def actualizar_pregunta_csv(grade: str, idx: int, nueva_pregunta: str, nuevas_opciones: list, nueva_respuesta: str, course=None):
    """Actualiza una pregunta existente por su índice."""
    path = get_grade_file(grade)
    rows = read_csv_rows(path)
    if idx < 0 or idx >= len(rows):
        raise ValueError("Índice de pregunta inválido.")
    rows[idx] = {
        "pregunta": nueva_pregunta,
        "opcion_1": nuevas_opciones[0],
        "opcion_2": nuevas_opciones[1],
        "opcion_3": nuevas_opciones[2],
        "opcion_4": nuevas_opciones[3],
        "respuesta": nueva_respuesta,
    }
    write_csv_rows(path, rows, QUESTION_HEADERS)


def obtener_alumno(username: str):
    """Obtiene los datos de un alumno específico."""
    for row in read_csv_rows(STUDENT_FILE):
        if row.get("usuario") == username:
            return row
    return None


def obtener_docente(username: str):
    """Obtiene los datos de un docente específico."""
    for row in read_csv_rows(TEACHER_FILE):
        if row.get("usuario") == username:
            return row
    return None


def listar_alumnos():
    """Retorna lista de todos los alumnos."""
    return read_csv_rows(STUDENT_FILE)


def listar_docentes():
    """Retorna lista de todos los docentes."""
    return read_csv_rows(TEACHER_FILE)


# ===== FUNCIONES DE TORNEOS =====

def crear_torneo(nombre: str, descripcion: str, fecha_inicio: str, fecha_limite: str, preguntas_por_dia: int, grado: str, creador: str, materia=None):
    """Crea un nuevo torneo."""
    ensure_csv(TOURNAMENT_FILE, TOURNAMENT_HEADERS)
    rows = read_csv_rows(TOURNAMENT_FILE)
    
    # Generar torneo_id basado en timestamp
    torneo_id = f"torneo_{int(datetime.now().timestamp())}"
    
    rows.append({
        "torneo_id": torneo_id,
        "nombre": nombre,
        "descripcion": descripcion,
        "fecha_inicio": fecha_inicio,
        "fecha_limite": fecha_limite,
        "preguntas_por_dia": str(preguntas_por_dia),
        "grado": grado,
        "creador": creador,
        "fecha_creacion": datetime.now().strftime("%d/%m/%Y %H:%M"),
    })
    write_csv_rows(TOURNAMENT_FILE, rows, TOURNAMENT_HEADERS)
    return torneo_id


def obtener_torneo(torneo_id: str):
    """Obtiene los datos de un torneo específico."""
    for row in read_csv_rows(TOURNAMENT_FILE):
        if row.get("torneo_id") == torneo_id:
            return row
    return None


def listar_torneos_activos():
    """Retorna lista de torneos cuya fecha límite aún no ha pasado."""
    ensure_csv(TOURNAMENT_FILE, TOURNAMENT_HEADERS)
    torneos = read_csv_rows(TOURNAMENT_FILE)
    hoy = datetime.now().strftime("%d/%m/%Y")
    
    # Convertir fechas en formato DD/MM/YYYY para comparación simple
    torneos_activos = []
    for t in torneos:
        fecha_limite = t.get("fecha_limite", "")
        if fecha_limite >= hoy:
            torneos_activos.append(t)
    
    return torneos_activos


def listar_todos_torneos():
    """Retorna lista de todos los torneos."""
    ensure_csv(TOURNAMENT_FILE, TOURNAMENT_HEADERS)
    return read_csv_rows(TOURNAMENT_FILE)


def actualizar_torneo(torneo_id: str, nombre: str = None, descripcion: str = None, fecha_limite: str = None, preguntas_por_dia: int = None):
    """Actualiza los datos de un torneo."""
    rows = read_csv_rows(TOURNAMENT_FILE)
    found = False
    
    for row in rows:
        if row.get("torneo_id") == torneo_id:
            if nombre:
                row["nombre"] = nombre
            if descripcion:
                row["descripcion"] = descripcion
            if fecha_limite:
                row["fecha_limite"] = fecha_limite
            if preguntas_por_dia:
                row["preguntas_por_dia"] = str(preguntas_por_dia)
            found = True
            break
    
    if not found:
        raise ValueError(f"Torneo '{torneo_id}' no encontrado.")
    
    write_csv_rows(TOURNAMENT_FILE, rows, TOURNAMENT_HEADERS)


def eliminar_torneo(torneo_id: str):
    """Elimina un torneo."""
    rows = read_csv_rows(TOURNAMENT_FILE)
    rows_updated = [r for r in rows if r.get("torneo_id") != torneo_id]
    
    if len(rows_updated) == len(rows):
        raise ValueError(f"Torneo '{torneo_id}' no encontrado.")
    
    write_csv_rows(TOURNAMENT_FILE, rows_updated, TOURNAMENT_HEADERS)
    
    # También eliminar las respuestas asociadas
    resp_rows = read_csv_rows(TOURNAMENT_RESPONSES_FILE)
    resp_rows_updated = [r for r in resp_rows if r.get("torneo_id") != torneo_id]
    write_csv_rows(TOURNAMENT_RESPONSES_FILE, resp_rows_updated, TOURNAMENT_RESPONSES_HEADERS)


def registrar_respuesta_torneo(torneo_id: str, usuario: str, pregunta_id: str, respuesta: str, es_correcta: bool):
    """Registra una respuesta en un torneo."""
    ensure_csv(TOURNAMENT_RESPONSES_FILE, TOURNAMENT_RESPONSES_HEADERS)
    rows = read_csv_rows(TOURNAMENT_RESPONSES_FILE)
    
    ahora = datetime.now()
    rows.append({
        "torneo_id": torneo_id,
        "usuario": usuario,
        "pregunta_id": pregunta_id,
        "respuesta": respuesta,
        "es_correcta": "1" if es_correcta else "0",
        "fecha": ahora.strftime("%d/%m/%Y"),
        "hora": ahora.strftime("%H:%M:%S"),
    })
    write_csv_rows(TOURNAMENT_RESPONSES_FILE, rows, TOURNAMENT_RESPONSES_HEADERS)


def contar_preguntas_hoy_alumno(torneo_id: str, usuario: str):
    """Cuenta cuántas preguntas respondió un alumno hoy en un torneo."""
    ensure_csv(TOURNAMENT_RESPONSES_FILE, TOURNAMENT_RESPONSES_HEADERS)
    rows = read_csv_rows(TOURNAMENT_RESPONSES_FILE)
    hoy = datetime.now().strftime("%d/%m/%Y")
    
    contador = 0
    for row in rows:
        if (row.get("torneo_id") == torneo_id and 
            row.get("usuario") == usuario and 
            row.get("fecha") == hoy):
            contador += 1
    
    return contador


def puede_responder_hoy(torneo_id: str, usuario: str, preguntas_por_dia: int):
    """Verifica si un alumno puede responder más preguntas hoy en el torneo."""
    preguntas_respondidas = contar_preguntas_hoy_alumno(torneo_id, usuario)
    return preguntas_respondidas < preguntas_por_dia


def obtener_respuestas_alumno_torneo(torneo_id: str, usuario: str):
    """Obtiene todas las respuestas de un alumno en un torneo."""
    ensure_csv(TOURNAMENT_RESPONSES_FILE, TOURNAMENT_RESPONSES_HEADERS)
    rows = read_csv_rows(TOURNAMENT_RESPONSES_FILE)
    
    return [r for r in rows if r.get("torneo_id") == torneo_id and r.get("usuario") == usuario]


def obtener_ranking_torneo(torneo_id: str):
    """Obtiene el ranking de un torneo (alumnos ordenados por respuestas correctas)."""
    ensure_csv(TOURNAMENT_RESPONSES_FILE, TOURNAMENT_RESPONSES_HEADERS)
    rows = read_csv_rows(TOURNAMENT_RESPONSES_FILE)
    
    # Filtrar respuestas del torneo
    respuestas_torneo = [r for r in rows if r.get("torneo_id") == torneo_id]
    
    # Contar respuestas correctas por alumno
    ranking = {}
    for row in respuestas_torneo:
        usuario = row.get("usuario", "")
        es_correcta = row.get("es_correcta") == "1"
        
        if usuario not in ranking:
            ranking[usuario] = {"correctas": 0, "total": 0}
        
        ranking[usuario]["total"] += 1
        if es_correcta:
            ranking[usuario]["correctas"] += 1
    
    # Ordenar por respuestas correctas (descendente)
    ranking_ordenado = sorted(ranking.items(), key=lambda x: x[1]["correctas"], reverse=True)
    
    return ranking_ordenado


def obtener_estadisticas_torneo(torneo_id: str):
    """Obtiene estadísticas generales de un torneo."""
    ensure_csv(TOURNAMENT_RESPONSES_FILE, TOURNAMENT_RESPONSES_HEADERS)
    rows = read_csv_rows(TOURNAMENT_RESPONSES_FILE)
    
    respuestas_torneo = [r for r in rows if r.get("torneo_id") == torneo_id]
    
    total_respuestas = len(respuestas_torneo)
    respuestas_correctas = sum(1 for r in respuestas_torneo if r.get("es_correcta") == "1")
    estudiantes_participantes = set(r.get("usuario") for r in respuestas_torneo)
    
    porcentaje_acierto = (respuestas_correctas / total_respuestas * 100) if total_respuestas > 0 else 0
    
    return {
        "total_respuestas": total_respuestas,
        "respuestas_correctas": respuestas_correctas,
        "respuestas_incorrectas": total_respuestas - respuestas_correctas,
        "porcentaje_acierto": round(porcentaje_acierto, 2),
        "estudiantes_participantes": len(estudiantes_participantes),
    }

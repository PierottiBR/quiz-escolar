import csv
import random
from datetime import datetime
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOGO_PATH = BASE_DIR / "LOGO ESCUELA 16.jpg"
DATA_DIR.mkdir(exist_ok=True)

TEACHER_FILE = DATA_DIR / "docentes.csv"
STUDENT_FILE = DATA_DIR / "alumnos.csv"
RESULT_FILE = DATA_DIR / "resultados.csv"
GRADE_OPTIONS = ["4° Grado", "5° Grado", "6° Grado"]
COURSE_OPTIONS = ["Matemática", "Lengua", "Ciencias", "Sociales"]
QUESTION_HEADERS = ["materia", "pregunta", "opcion_1", "opcion_2", "opcion_3", "opcion_4", "respuesta"]
RESULT_HEADERS = ["usuario", "grado", "materia", "puntaje", "total", "fecha"]


def apply_custom_style():
    st.markdown(
        """
        <style>
            :root {
                --escuela-azul-oscuro: #0d3a66;
                --escuela-azul-medio: #1d6ea7;
                --escuela-azul-claro: #4ca3d9;
                --escuela-blanco: #f4f7fb;
                --escuela-plata: #dfeaf5;
            }

            html, body, [data-testid="stAppViewContainer"] {
                background: linear-gradient(180deg, #e4e9ee 0%, #d9dfe7 100%);
                color: var(--escuela-azul-oscuro);
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #123d67 0%, #1f5d93 100%);
                border-right: 1px solid rgba(255,255,255,0.12);
            }

            [data-testid="stSidebar"] * {
                color: white !important;
            }

            .brand-header {
                background: linear-gradient(135deg, #173e68 0%, #2d628f 100%);
                border-radius: 24px;
                padding: 1.2rem 1.4rem;
                box-shadow: 0 12px 25px rgba(18, 61, 103, 0.14);
                border: 1px solid rgba(255,255,255,0.1);
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
                color: #eaf3fb;
                margin-top: 0.35rem;
                margin-bottom: 0;
            }

            .stTabs [role="tablist"] {
                gap: 0.6rem;
            }

            .stTabs [role="tab"] {
                border-radius: 12px 12px 0 0;
                background: rgba(23, 62, 104, 0.06);
                color: var(--escuela-azul-oscuro);
                padding: 0.7rem 1.2rem;
                font-weight: 700;
                border: 1px solid rgba(23, 62, 104, 0.08);
            }

            .stTabs [role="tab"][aria-selected="true"] {
                background: linear-gradient(180deg, #123d67 0%, #1d6ea7 100%);
                color: white;
            }

            .stButton > button {
                background: linear-gradient(180deg, #2d628f 0%, #173e68 100%);
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: 700;
                box-shadow: 0 8px 18px rgba(23, 62, 104, 0.12);
            }

            .stTextInput > div > div > input,
            .stSelectbox > div > div,
            .stTextArea > div > div > textarea {
                border-radius: 10px;
                border: 1px solid rgba(18, 61, 103, 0.18);
                background: rgba(255,255,255,0.34);
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
    return grade.strip()


def grade_to_filename(grade: str) -> str:
    return f"{grade.replace('°', '').replace(' ', '').lower()}.csv"


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
            writer.writerow(row)


def ensure_seed_data():
    ensure_csv(TEACHER_FILE, ["usuario", "password", "curso"])
    teachers = read_csv_rows(TEACHER_FILE)
    if not teachers:
        with TEACHER_FILE.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["maestro", "escuela123", "Matemática"])

    ensure_csv(STUDENT_FILE, ["usuario", "password", "grado"])
    ensure_csv(RESULT_FILE, RESULT_HEADERS)

    for grado in GRADE_OPTIONS:
        grade_file = DATA_DIR / grade_to_filename(grado)
        ensure_csv(grade_file, QUESTION_HEADERS)
        rows = read_csv_rows(grade_file)
        if rows:
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
                    "materia": r[0],
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


def listar_materias_del_grado(grade: str):
    materias = set()
    with get_grade_file(grade).open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            materia = (row.get("materia") or "").strip()
            if materia:
                materias.add(materia)
    return sorted(materias)


def cargar_preguntas_csv(grade: str, curso: str):
    rows = []
    with get_grade_file(grade).open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("pregunta"):
                continue
            if (row.get("materia") or "").strip() != curso:
                continue
            rows.append(
                {
                    "grado": grade,
                    "curso": row["materia"],
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


def guardar_pregunta_csv(grade: str, course: str, question: str, options, answer: str):
    path = get_grade_file(grade)
    rows = read_csv_rows(path)
    rows.append(
        {
            "materia": course,
            "pregunta": question,
            "opcion_1": options[0],
            "opcion_2": options[1],
            "opcion_3": options[2],
            "opcion_4": options[3],
            "respuesta": answer,
        }
    )
    write_csv_rows(path, rows, QUESTION_HEADERS)


def eliminar_pregunta_csv(grade: str, course: str, idx: int):
    path = get_grade_file(grade)
    rows = read_csv_rows(path)
    matches = [i for i, row in enumerate(rows) if (row.get("materia") or "").strip() == course]
    if idx < 0 or idx >= len(matches):
        return
    rows.pop(matches[idx])
    write_csv_rows(path, rows, QUESTION_HEADERS)


def iniciar_partida(grade: str, course: str):
    preguntas = cargar_preguntas_csv(grade, course)
    if not preguntas:
        st.warning("Todavía no hay preguntas cargadas para esa materia.")
        return
    st.session_state.game = {
        "grado": grade,
        "curso": course,
        "preguntas": random.sample(preguntas, k=min(5, len(preguntas))),
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
    rows.append({"usuario": username, "password": password, "grado": grade})
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
            row["grado"] = nuevo_grado
            break
    write_csv_rows(STUDENT_FILE, rows, ["usuario", "password", "grado"])


def registrar_resultado_alumno(usuario: str, grado: str, materia: str, puntaje: int, total: int):
    rows = read_csv_rows(RESULT_FILE)
    rows.append(
        {
            "usuario": usuario,
            "grado": grado,
            "materia": materia,
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


def guardar_docente(username: str, password: str, curso: str):
    rows = read_csv_rows(TEACHER_FILE)
    if any(r.get("usuario") == username for r in rows):
        raise ValueError("Ese docente ya existe.")
    rows.append({"usuario": username, "password": password, "curso": curso})
    write_csv_rows(TEACHER_FILE, rows, ["usuario", "password", "curso"])

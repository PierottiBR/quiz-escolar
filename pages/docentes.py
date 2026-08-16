import streamlit as st

from app_utils import (
    COURSE_OPTIONS,
    GRADE_OPTIONS,
    LOGO_PATH,
    apply_custom_style,
    cargar_preguntas_csv,
    eliminar_pregunta_csv,
    get_historial_por_alumno,
    get_historial_resultados,
    get_student_by_login,
    get_teacher_by_login,
    guardar_docente,
    guardar_pregunta_csv,
    read_csv_rows,
    actualizar_grado_alumno,
    actualizar_password_alumno,
    STUDENT_FILE,
    TEACHER_FILE,
)

apply_custom_style()
st.set_page_config(page_title="Docentes", page_icon="👩‍🏫", layout="wide")

if "teacher" not in st.session_state:
    st.session_state.teacher = None

logo_col, title_col = st.columns([1.3, 3.7])
with logo_col:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=220)
with title_col:
    st.markdown(
        """
        <div class="brand-header">
            <p class="brand-title">Docentes</p>
            <p class="brand-subtitle">Panel exclusivo del personal escolar</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if st.session_state.teacher is None:
    st.subheader("Ingresar como docente")
    teacher_user = st.text_input("Usuario", key="teacher_user")
    teacher_pass = st.text_input("Contraseña", type="password", key="teacher_pass")

    if st.button("Entrar al panel docente"):
        teacher = get_teacher_by_login(teacher_user, teacher_pass)
        if teacher:
            st.session_state.teacher = teacher
            st.success("Docente logueado correctamente.")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")
else:
    st.success(f"Docente activo: {st.session_state.teacher['usuario']}")
    st.write(f"Curso asignado: {st.session_state.teacher['curso']}")
    if st.button("Cerrar sesión"):
        st.session_state.teacher = None
        st.rerun()

    st.header("Administración de alumnos")
    estudiantes = read_csv_rows(STUDENT_FILE)
    if not estudiantes:
        st.info("Todavía no hay alumnos registrados.")
    else:
        for alumno in estudiantes:
            with st.expander(f"{alumno['usuario']} · {alumno['grado']}"):
                nuevo_pass = st.text_input(f"Nueva contraseña para {alumno['usuario']}", type="password", key=f"pw_{alumno['usuario']}")
                nuevo_grado = st.selectbox(
                    "Cambiar grado",
                    GRADE_OPTIONS,
                    index=GRADE_OPTIONS.index(alumno.get("grado", GRADE_OPTIONS[0])),
                    key=f"g_{alumno['usuario']}",
                )
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Guardar contraseña", key=f"save_pw_{alumno['usuario']}"):
                        if nuevo_pass.strip():
                            actualizar_password_alumno(alumno["usuario"], nuevo_pass.strip())
                            st.success("Contraseña actualizada.")
                            st.rerun()
                with c2:
                    if st.button("Actualizar grado", key=f"save_grade_{alumno['usuario']}"):
                        actualizar_grado_alumno(alumno["usuario"], nuevo_grado)
                        st.success("Grado actualizado.")
                        st.rerun()

    st.divider()
    st.header("Crear docente")
    nuevo_docente = st.text_input("Usuario docente", key="new_teacher_user")
    nueva_pass_docente = st.text_input("Contraseña", type="password", key="new_teacher_pass")
    nuevo_curso_docente = st.selectbox("Curso asignado", COURSE_OPTIONS, key="new_teacher_course")
    if st.button("Guardar docente"):
        if not nuevo_docente.strip() or not nueva_pass_docente.strip():
            st.warning("Completá usuario y contraseña.")
        else:
            try:
                guardar_docente(nuevo_docente.strip(), nueva_pass_docente.strip(), nuevo_curso_docente)
                st.success("Docente creado correctamente.")
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))

    st.divider()
    st.header("Historial de puntajes")
    historial = get_historial_resultados()
    if not historial:
        st.info("Todavía no hay resultados registrados.")
    else:
        st.dataframe(
            [
                {
                    "Usuario": fila.get("usuario", ""),
                    "Grado": fila.get("grado", ""),
                    "Materia": fila.get("materia", ""),
                    "Puntaje": f"{fila.get('puntaje', '0')}/{fila.get('total', '0')}",
                    "Fecha": fila.get("fecha", ""),
                }
                for fila in historial
            ],
            use_container_width=True,
            hide_index=True,
        )

    st.divider()
    st.header("Resultados por alumno")
    if estudiantes:
        alumno_seleccionado = st.selectbox("Alumno", [a["usuario"] for a in estudiantes], key="teacher_results_student")
        historial_alumno = get_historial_por_alumno(alumno_seleccionado)
        if not historial_alumno:
            st.info(f"{alumno_seleccionado} todavía no tiene resultados registrados.")
        else:
            st.dataframe(
                [
                    {
                        "Materia": fila.get("materia", ""),
                        "Puntaje": f"{fila.get('puntaje', '0')}/{fila.get('total', '0')}",
                        "Fecha": fila.get("fecha", ""),
                    }
                    for fila in historial_alumno
                ],
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.info("No hay alumnos para consultar.")

    st.divider()
    st.header("Banco de preguntas")
    grado_admin = st.selectbox("Grado", GRADE_OPTIONS, key="admin_grade")
    curso_admin = st.selectbox("Materia", COURSE_OPTIONS, key="admin_course")

    preguntas_admin = cargar_preguntas_csv(grado_admin, curso_admin)
    if not preguntas_admin:
        st.info("No hay preguntas cargadas para este curso.")
    else:
        for i, pregunta in enumerate(preguntas_admin):
            with st.expander(f"Pregunta {i + 1}: {pregunta['pregunta'][:60]}..."):
                st.write("Opciones:")
                for option in pregunta["opciones"]:
                    st.write(f"- {option}")
                st.write(f"Respuesta correcta: {pregunta['respuesta']}")
                if st.button(f"Eliminar pregunta {i + 1}", key=f"del_q_{grado_admin}_{curso_admin}_{i}"):
                    eliminar_pregunta_csv(grado_admin, curso_admin, i)
                    st.rerun()

    st.subheader("Agregar nueva pregunta")
    nueva_pregunta = st.text_area("Texto de la pregunta", key="admin_question_text")
    nuevas_opciones = []
    for n in range(1, 5):
        nuevas_opciones.append(st.text_input(f"Opción {n}", key=f"admin_option_{n}"))

    if all(opcion.strip() for opcion in nuevas_opciones):
        respuesta_correcta = st.selectbox("Respuesta correcta", nuevas_opciones, key="admin_correct_answer")
    else:
        respuesta_correcta = ""

    if st.button("Guardar pregunta"):
        if not nueva_pregunta.strip():
            st.warning("La pregunta no puede estar vacía.")
        elif not all(opcion.strip() for opcion in nuevas_opciones):
            st.warning("Completa las 4 opciones.")
        elif not respuesta_correcta:
            st.warning("Selecciona la respuesta correcta.")
        else:
            guardar_pregunta_csv(grado_admin, curso_admin, nueva_pregunta.strip(), [op.strip() for op in nuevas_opciones], respuesta_correcta.strip())
            st.success("Pregunta guardada correctamente.")
            st.rerun()

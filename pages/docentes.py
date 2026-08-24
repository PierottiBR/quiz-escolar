import streamlit as st
from datetime import datetime, timedelta

from app_utils import (
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
    crear_torneo,
    listar_torneos_activos,
    listar_todos_torneos,
    actualizar_torneo,
    eliminar_torneo,
    obtener_ranking_torneo,
    obtener_estadisticas_torneo,
    obtener_respuestas_alumno_torneo,
)

apply_custom_style()
st.set_page_config(page_title="Docentes · Escuela Especial N° 502", page_icon="👩‍🏫", layout="wide")

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
                    "Cambiar nivel educativo",
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
                    if st.button("Actualizar nivel", key=f"save_grade_{alumno['usuario']}"):
                        actualizar_grado_alumno(alumno["usuario"], nuevo_grado)
                        st.success("Nivel educativo actualizado.")
                        st.rerun()

    st.divider()
    st.header("Crear docente")
    nuevo_docente = st.text_input("Usuario docente", key="new_teacher_user")
    nueva_pass_docente = st.text_input("Contraseña", type="password", key="new_teacher_pass")
    if st.button("Guardar docente"):
        if not nuevo_docente.strip() or not nueva_pass_docente.strip():
            st.warning("Completá usuario y contraseña.")
        else:
            try:
                guardar_docente(nuevo_docente.strip(), nueva_pass_docente.strip())
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
    grado_admin = st.selectbox("Nivel educativo", GRADE_OPTIONS, key="admin_grade")
    preguntas_admin = cargar_preguntas_csv(grado_admin)
    if not preguntas_admin:
        st.info("No hay preguntas cargadas para este nivel.")
    else:
        for i, pregunta in enumerate(preguntas_admin):
            with st.expander(f"Pregunta {i + 1}: {pregunta['pregunta'][:60]}..."):
                st.write("Opciones:")
                for option in pregunta["opciones"]:
                    st.write(f"- {option}")
                st.write(f"Respuesta correcta: {pregunta['respuesta']}")
                if st.button(f"Eliminar pregunta {i + 1}", key=f"del_q_{grado_admin}_{i}"):
                    eliminar_pregunta_csv(grado_admin, i)
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
            guardar_pregunta_csv(grado_admin, nueva_pregunta.strip(), [op.strip() for op in nuevas_opciones], respuesta_correcta.strip())
            st.success("Pregunta guardada correctamente.")
            st.rerun()

    st.divider()
    st.header("Gestión de Torneos")
    
    tab_crear, tab_ver, tab_ranking = st.tabs(["Crear Torneo", "Ver Torneos", "Rankings"])
    
    with tab_crear:
        st.subheader("Crear nuevo torneo")
        nombre_torneo = st.text_input("Nombre del torneo", key="torneo_nombre")
        desc_torneo = st.text_area("Descripción", key="torneo_desc")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha_inicio = st.date_input("Fecha de inicio", key="torneo_inicio")
        with col2:
            fecha_limite = st.date_input("Fecha límite", value=datetime.now() + timedelta(days=7), key="torneo_limite")
        with col3:
            preguntas_dia = st.number_input("Preguntas por día", min_value=1, max_value=50, value=10, key="torneo_preguntas_dia")
        
        grado_torneo = st.selectbox("Nivel educativo", GRADE_OPTIONS, key="torneo_grado")
        
        if st.button("Crear torneo"):
            if not nombre_torneo.strip():
                st.warning("Ingresa un nombre para el torneo.")
            elif not desc_torneo.strip():
                st.warning("Ingresa una descripción.")
            else:
                try:
                    torneo_id = crear_torneo(
                        nombre=nombre_torneo.strip(),
                        descripcion=desc_torneo.strip(),
                        fecha_inicio=fecha_inicio.strftime("%d/%m/%Y"),
                        fecha_limite=fecha_limite.strftime("%d/%m/%Y"),
                        preguntas_por_dia=int(preguntas_dia),
                        grado=grado_torneo,
                        creador=st.session_state.teacher["usuario"]
                    )
                    st.success(f"Torneo creado correctamente. ID: {torneo_id}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al crear torneo: {e}")
    
    with tab_ver:
        st.subheader("Torneos activos")
        torneos_activos = listar_torneos_activos()
        
        if not torneos_activos:
            st.info("No hay torneos activos en este momento.")
        else:
            for torneo in torneos_activos:
                with st.expander(f"🏆 {torneo['nombre']} ({torneo['grado']})"):
                    st.write(f"**Descripción:** {torneo['descripcion']}")
                    st.write(f"**Fecha inicio:** {torneo['fecha_inicio']}")
                    st.write(f"**Fecha límite:** {torneo['fecha_limite']}")
                    st.write(f"**Preguntas por día:** {torneo['preguntas_por_dia']}")
                    st.write(f"**Creador:** {torneo['creador']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        nueva_fecha = st.date_input("Cambiar fecha límite", key=f"fecha_limite_{torneo['torneo_id']}")
                        if st.button("Actualizar fecha", key=f"actualizar_fecha_{torneo['torneo_id']}"):
                            try:
                                actualizar_torneo(torneo['torneo_id'], fecha_limite=nueva_fecha.strftime("%d/%m/%Y"))
                                st.success("Fecha actualizada.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")
                    
                    with col2:
                        if st.button("Eliminar torneo", key=f"eliminar_torneo_{torneo['torneo_id']}"):
                            try:
                                eliminar_torneo(torneo['torneo_id'])
                                st.success("Torneo eliminado.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")
    
    with tab_ranking:
        st.subheader("Ranking de torneos")
        todos_torneos = listar_todos_torneos()
        
        if not todos_torneos:
            st.info("No hay torneos disponibles.")
        else:
            torneo_seleccionado = st.selectbox(
                "Selecciona un torneo",
                [t["nombre"] for t in todos_torneos],
                key="ranking_torneo_select"
            )
            
            torneo_obj = next(t for t in todos_torneos if t["nombre"] == torneo_seleccionado)
            
            # Estadísticas
            stats = obtener_estadisticas_torneo(torneo_obj["torneo_id"])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Respuestas", stats["total_respuestas"])
            with col2:
                st.metric("Respuestas Correctas", stats["respuestas_correctas"])
            with col3:
                st.metric("Porcentaje Acierto", f"{stats['porcentaje_acierto']}%")
            with col4:
                st.metric("Estudiantes", stats["estudiantes_participantes"])
            
            st.divider()
            
            # Ranking
            ranking = obtener_ranking_torneo(torneo_obj["torneo_id"])
            
            if ranking:
                st.subheader("Posiciones")
                ranking_data = []
                for pos, (usuario, stats_user) in enumerate(ranking, 1):
                    ranking_data.append({
                        "Posición": pos,
                        "Usuario": usuario,
                        "Correctas": stats_user["correctas"],
                        "Total": stats_user["total"],
                        "Porcentaje": f"{round(stats_user['correctas'] / stats_user['total'] * 100, 1)}%"
                    })
                
                st.dataframe(ranking_data, use_container_width=True, hide_index=True)
                
                # Detalles de cada alumno
                st.divider()
                st.subheader("Detalles por estudiante")
                
                alumno_ver = st.selectbox("Selecciona un alumno", [r[0] for r in ranking], key="ranking_alumno_ver")
                respuestas_alumno = obtener_respuestas_alumno_torneo(torneo_obj["torneo_id"], alumno_ver)
                
                if respuestas_alumno:
                    respuestas_data = []
                    for resp in respuestas_alumno:
                        respuestas_data.append({
                            "Fecha": resp.get("fecha"),
                            "Hora": resp.get("hora"),
                            "Pregunta ID": resp.get("pregunta_id"),
                            "Respuesta": resp.get("respuesta"),
                            "Correcta": "✓" if resp.get("es_correcta") == "1" else "✗"
                        })
                    
                    st.dataframe(respuestas_data, use_container_width=True, hide_index=True)
            else:
                st.info("No hay respuestas registradas en este torneo aún.")

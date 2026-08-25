import streamlit as st
from datetime import datetime

from app_utils import (
    GRADE_OPTIONS,
    LOGO_PATH,
    apply_custom_style,
    get_historial_por_alumno,
    get_student_by_login,
    guardar_alumno,
    iniciar_partida,
    read_csv_rows,
    registrar_resultado_alumno,
    cargar_preguntas_csv,
    mezclar_opciones_preguntas,
    mezclar_opciones_preguntas,
    listar_torneos_activos,
    obtener_torneo,
    registrar_respuesta_torneo,
    contar_preguntas_hoy_alumno,
    puede_responder_hoy,
)

apply_custom_style()
st.set_page_config(page_title="Alumnos · Escuela Especial N° 502", page_icon="🧑‍🎓", layout="wide")

if "student" not in st.session_state:
    st.session_state.student = None
if "game" not in st.session_state:
    st.session_state.game = None

logo_col, title_col = st.columns([1.3, 3.7])
with logo_col:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=220)
with title_col:
    st.markdown(
        """
        <div class="brand-header">
            <p class="brand-title">Alumnos</p>
            <p class="brand-subtitle">Acceso para estudiantes</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if st.session_state.student is None:
    st.subheader("Ingresar como alumno")
    alumno_user = st.text_input("Usuario", key="alumno_user")
    alumno_pass = st.text_input("Contraseña", type="password", key="alumno_pass")

    if st.button("Iniciar sesión"):
        student = get_student_by_login(alumno_user, alumno_pass)
        if student:
            st.session_state.student = student
            st.success("Alumno logueado correctamente.")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")

    st.divider()
    st.subheader("Crear cuenta")
    nuevo_usuario = st.text_input("Nuevo usuario", key="new_student_user")
    nueva_pass = st.text_input("Contraseña", type="password", key="new_student_pass")
    nuevo_grado = st.selectbox("Nivel educativo", GRADE_OPTIONS, key="new_student_grade")

    if st.button("Crear cuenta"):
        if not nuevo_usuario.strip() or not nueva_pass.strip():
            st.warning("Completá usuario y contraseña.")
        else:
            try:
                guardar_alumno(nuevo_usuario.strip(), nueva_pass.strip(), nuevo_grado)
                st.success("Cuenta creada. Ahora podés iniciar sesión.")
            except ValueError as e:
                st.error(str(e))
else:
    st.success(f"Alumno activo: {st.session_state.student['usuario']}")
    st.write(f"Nivel educativo: {st.session_state.student['grado']}")
    if st.button("Cerrar sesión"):
        st.session_state.student = None
        st.session_state.game = None
        st.rerun()

    grado_jugador = st.session_state.student["grado"]
    tab_jugar, tab_perfil = st.tabs(["Jugar", "Mi perfil y puntaje"])

    with tab_jugar:
        st.header("Jugar")
        preguntas_nivel = cargar_preguntas_csv(grado_jugador)
        if not preguntas_nivel:
            st.warning("Todavía no hay preguntas cargadas para este nivel.")
        else:
            if st.button("Iniciar juego"):
                iniciar_partida(grado_jugador)

        st.divider()
        st.header("🏆 Torneos disponibles")
        torneos_activos = listar_torneos_activos()
        torneos_del_grado = [t for t in torneos_activos if t.get("grado") == grado_jugador]
        if not torneos_del_grado:
            st.info("No hay torneos activos para tu nivel.")
        else:
            torneo_participar = st.selectbox(
                "Seleccioná un torneo",
                [t["nombre"] for t in torneos_del_grado],
                key="torneo_participar_select",
            )
            torneo_obj = next(t for t in torneos_del_grado if t["nombre"] == torneo_participar)
            st.markdown(f"**Descripción:** {torneo_obj['descripcion']}")
            st.markdown(f"**Fecha límite:** {torneo_obj['fecha_limite']}")
            if st.button("Participar en torneo", key=f"btn_torneo_{torneo_obj['torneo_id']}"):
                preguntas_torneo = cargar_preguntas_csv(grado_jugador)
                if not preguntas_torneo:
                    st.error("No hay preguntas cargadas para este torneo.")
                else:
                    preguntas_torneo = mezclar_opciones_preguntas(preguntas_torneo)
                    st.session_state.game = {
                        "grado": grado_jugador,
                        "curso": "",
                        "preguntas": preguntas_torneo,
                        "indice": 0,
                        "puntaje": 0,
                        "finalizado": False,
                        "respuesta_actual": None,
                        "es_torneo": True,
                        "torneo_id": torneo_obj["torneo_id"],
                    }
                    st.rerun()

        if st.session_state.game:
            juego = st.session_state.game
            es_torneo = juego.get("es_torneo", False)
            if not juego["finalizado"]:
                total = len(juego["preguntas"])
                indice = juego["indice"]
                pregunta = juego["preguntas"][indice]
                st.subheader(f"Nivel: {juego['grado']}")
                if es_torneo:
                    torneo_info = obtener_torneo(juego["torneo_id"])
                    st.write(f"🏆 Torneo: {torneo_info['nombre']}")
                st.write(f"Pregunta {indice + 1} de {total}")
                st.progress(indice / total)
                st.markdown(f'<div class="question-heading">{pregunta["pregunta"]}</div>', unsafe_allow_html=True)
                if juego["respuesta_actual"] is None:
                    opcion_elegida = st.radio("Seleccioná la opción correcta:", pregunta["opciones"], key=f"radio_{indice}_{grado_jugador}_{'torneo' if es_torneo else 'juego'}")
                    if st.button("Verificar respuesta"):
                        es_correcta = opcion_elegida == pregunta["respuesta"]
                        if es_torneo:
                            registrar_respuesta_torneo(juego["torneo_id"], st.session_state.student["usuario"], f"pregunta_{indice}", opcion_elegida, es_correcta)
                        juego["respuesta_actual"] = opcion_elegida
                        if es_correcta:
                            juego["puntaje"] += 1
                            st.balloons()
                            st.success("¡Correcto! Sumaste 1 punto.")
                        else:
                            st.error(f"Incorrecto. La respuesta correcta era: {pregunta['respuesta']}")
                        if indice == total - 1:
                            juego["finalizado"] = True
                            if not es_torneo:
                                resultado_sincronizado = registrar_resultado_alumno(st.session_state.student["usuario"], juego["grado"], juego["puntaje"], total)
                        st.session_state.game = juego
                        if juego["finalizado"]:
                            incorrectas = total - juego["puntaje"]
                            st.success("🎉 Completaste todas las preguntas")
                            st.write(f"Respuestas correctas: {juego['puntaje']}")
                            st.write(f"Respuestas incorrectas: {incorrectas}")
                            if not es_torneo and not resultado_sincronizado:
                                st.info("El resultado quedó guardado localmente. GitHub Secrets aún no está configurado.")
                    
                elif juego["respuesta_actual"] is not None:
                    es_correcta = juego["respuesta_actual"] == pregunta["respuesta"]
                    st.success("¡Correcto! Sumaste 1 punto." if es_correcta else f"Respuesta correcta: {pregunta['respuesta']}")
                    if indice < total - 1 and st.button("Siguiente pregunta"):
                        juego["indice"] += 1
                        juego["respuesta_actual"] = None
                        st.session_state.game = juego
                        st.rerun()
            else:
                st.success("🎉 Pregunta completada")
                if es_torneo:
                    st.markdown(f"**Tu respuesta:** {juego['respuesta_actual']}")
                    incorrectas = len(juego["preguntas"]) - juego["puntaje"]
                    st.markdown(f"**Respuestas correctas:** {juego['puntaje']}")
                    st.markdown(f"**Respuestas incorrectas:** {incorrectas}")
                else:
                    incorrectas = len(juego["preguntas"]) - juego["puntaje"]
                    st.markdown(f"### Resultado final\n**Respuestas correctas:** {juego['puntaje']}\n**Respuestas incorrectas:** {incorrectas}\n\n**Nivel:** {juego['grado']}")
                if st.button("Volver a jugar"):
                    st.session_state.game = None
                    st.rerun()

    with tab_perfil:
        st.header("Mi perfil")
        st.write(f"**Usuario:** {st.session_state.student['usuario']}")
        st.write(f"**Nivel educativo:** {grado_jugador}")
        st.divider()
        st.subheader("Mi historial de puntajes")
        historial_alumno = get_historial_por_alumno(st.session_state.student["usuario"])
        if not historial_alumno:
            st.info("Todavía no realizaste ninguna partida.")
        else:
            st.dataframe(
                [{"Nivel": fila.get("grado", ""), "Puntaje": f"{fila.get('puntaje', '0')}/{fila.get('total', '0')}", "Fecha": fila.get("fecha", "")} for fila in historial_alumno],
                use_container_width=True,
                hide_index=True,
            )

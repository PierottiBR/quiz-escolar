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
    listar_materias_del_grado,
    read_csv_rows,
    registrar_resultado_alumno,
    cargar_preguntas_csv,
    listar_torneos_activos,
    obtener_torneo,
    registrar_respuesta_torneo,
    contar_preguntas_hoy_alumno,
    puede_responder_hoy,
)

apply_custom_style()
st.set_page_config(page_title="Alumnos", page_icon="🧑‍🎓", layout="wide")

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
    nuevo_grado = st.selectbox("Grado", GRADE_OPTIONS, key="new_student_grade")

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
    st.write(f"Grado: {st.session_state.student['grado']}")
    if st.button("Cerrar sesión"):
        st.session_state.student = None
        st.session_state.game = None
        st.rerun()

    st.header("Jugar")
    grado_jugador = st.session_state.student["grado"]
    materias = listar_materias_del_grado(grado_jugador)
    if not materias:
        st.warning("Todavía no hay preguntas cargadas para este grado.")
    else:
        materia_jugador = st.selectbox("Seleccioná la materia", materias, key="student_game_course")
        if st.button("Iniciar juego"):
            iniciar_partida(grado_jugador, materia_jugador)

    st.divider()
    st.subheader("Mi historial")
    historial_alumno = get_historial_por_alumno(st.session_state.student["usuario"])
    if not historial_alumno:
        st.info("Todavía no realizaste ninguna partida.")
    else:
        st.dataframe(
            [
                {
                    "Grado": fila.get("grado", ""),
                    "Materia": fila.get("materia", ""),
                    "Puntaje": f"{fila.get('puntaje', '0')}/{fila.get('total', '0')}",
                    "Fecha": fila.get("fecha", ""),
                }
                for fila in historial_alumno
            ],
            use_container_width=True,
            hide_index=True,
        )

    st.divider()
    st.header("🏆 Torneos Disponibles")
    
    torneos_activos = listar_torneos_activos()
    if not torneos_activos:
        st.info("No hay torneos activos disponibles en este momento.")
    else:
        grado_alumno = st.session_state.student["grado"]
        torneos_del_grado = [t for t in torneos_activos if t.get("grado") == grado_alumno]
        
        if not torneos_del_grado:
            st.info(f"No hay torneos activos para tu grado ({grado_alumno}).")
        else:
            torneo_participar = st.selectbox(
                "Selecciona un torneo para participar",
                [t["nombre"] for t in torneos_del_grado],
                key="torneo_participar_select"
            )
            
            torneo_obj = next(t for t in torneos_del_grado if t["nombre"] == torneo_participar)
            
            st.markdown(f"**Descripción:** {torneo_obj['descripcion']}")
            st.markdown(f"**Materia:** {torneo_obj['materia']}")
            st.markdown(f"**Fecha límite:** {torneo_obj['fecha_limite']}")
            
            preguntas_hoy = contar_preguntas_hoy_alumno(torneo_obj["torneo_id"], st.session_state.student["usuario"])
            limite_diario = int(torneo_obj["preguntas_por_dia"])
            
            st.info(f"Has respondido {preguntas_hoy}/{limite_diario} preguntas hoy")
            
            if puede_responder_hoy(torneo_obj["torneo_id"], st.session_state.student["usuario"], limite_diario):
                if st.button("Participar en torneo", key=f"btn_torneo_{torneo_obj['torneo_id']}"):
                    # Cargar preguntas del torneo
                    preguntas_torneo = cargar_preguntas_csv(grado_alumno, torneo_obj["materia"])
                    
                    if not preguntas_torneo:
                        st.error("No hay preguntas cargadas para este torneo.")
                    else:
                        st.session_state.game = {
                            "grado": grado_alumno,
                            "curso": torneo_obj["materia"],
                            "preguntas": preguntas_torneo[:1],  # Una pregunta por vez en torneos
                            "indice": 0,
                            "puntaje": 0,
                            "finalizado": False,
                            "respuesta_actual": None,
                            "es_torneo": True,
                            "torneo_id": torneo_obj["torneo_id"],
                        }
                        st.rerun()
            else:
                st.warning(f"Has alcanzado tu límite diario de {limite_diario} preguntas para hoy. ¡Vuelve mañana!")

    if st.session_state.game:
        juego = st.session_state.game
        es_torneo = juego.get("es_torneo", False)
        
        if not juego["finalizado"]:
            total = len(juego["preguntas"])
            indice = juego["indice"]
            pregunta = juego["preguntas"][indice]

            st.subheader(f"{juego['grado']} · {juego['curso']}")
            
            if es_torneo:
                torneo_info = obtener_torneo(juego["torneo_id"])
                st.write(f"🏆 Torneo: {torneo_info['nombre']}")
            
            st.write(f"Pregunta {indice + 1} de {total}")
            st.progress(indice / total)
            st.markdown(f"### {pregunta['pregunta']}")

            opcion_elegida = st.radio("Seleccioná la opción correcta:", pregunta["opciones"], key=f"radio_{indice}_{grado_alumno}_{juego['curso']}")

            if st.button("Verificar respuesta"):
                es_correcta = opcion_elegida == pregunta["respuesta"]
                
                # Registrar en torneo si aplica
                if es_torneo:
                    registrar_respuesta_torneo(
                        juego["torneo_id"],
                        st.session_state.student["usuario"],
                        f"pregunta_{indice}",
                        opcion_elegida,
                        es_correcta
                    )
                
                juego["respuesta_actual"] = opcion_elegida
                if es_correcta:
                    juego["puntaje"] += 1
                    st.success("¡Correcto! Sumaste 1 punto.")
                else:
                    st.error(f"Incorrecto. La respuesta correcta era: {pregunta['respuesta']}")
                st.session_state.game = juego

                if es_torneo:
                    # En torneos, terminar después de una pregunta
                    juego["finalizado"] = True
                    st.session_state.game = juego
                elif indice == total - 1:
                    juego["finalizado"] = True
                    registrar_resultado_alumno(
                        st.session_state.student["usuario"],
                        juego["grado"],
                        juego["curso"],
                        juego["puntaje"],
                        len(juego["preguntas"]),
                    )
                    st.session_state.game = juego
                else:
                    if st.button("Siguiente pregunta"):
                        juego["indice"] += 1
                        juego["respuesta_actual"] = None
                        st.session_state.game = juego
                        st.rerun()

            if juego.get("respuesta_actual") is not None and indice < total - 1:
                st.info(f"Tu respuesta: {juego['respuesta_actual']}")
        else:
            st.balloons()
            st.success("🎉 Pregunta completada")
            
            if juego.get("es_torneo"):
                st.markdown(f"**Tu respuesta:** {juego['respuesta_actual']}")
                st.markdown(f"**Resultado:** {'✓ Correcta' if juego.get('respuesta_actual') == juego['preguntas'][juego['indice']]['respuesta'] else '✗ Incorrecta'}")
            else:
                st.markdown(
                    f"### Resultado final\n"
                    f"**Puntaje:** {juego['puntaje']} / {len(juego['preguntas'])}\n\n"
                    f"**Grado:** {juego['grado']}\n"
                    f"**Curso:** {juego['curso']}"
                )

                if juego["puntaje"] == len(juego["preguntas"]):
                    st.markdown("### ¡Excelente! Contestaste todo correctamente.")
                elif juego["puntaje"] >= len(juego["preguntas"]) // 2:
                    st.markdown("### ¡Muy bien! Seguí practicando.")
                else:
                    st.markdown("### ¡Sigue intentando! Cada intento enseña.")

            if st.button("Jugar otra vez"):
                st.session_state.game = None
                st.rerun()

            if st.button("Volver al menú"):
                st.session_state.game = None
                st.rerun()
        juego = st.session_state.game
        if not juego["finalizado"]:
            total = len(juego["preguntas"])
            indice = juego["indice"]
            pregunta = juego["preguntas"][indice]

            st.subheader(f"{juego['grado']} · {juego['curso']}")
            st.write(f"Pregunta {indice + 1} de {total}")
            st.progress(indice / total)
            st.markdown(f"### {pregunta['pregunta']}")

            opcion_elegida = st.radio("Seleccioná la opción correcta:", pregunta["opciones"], key=f"radio_{indice}_{grado_jugador}_{materia_jugador}")

            if st.button("Verificar respuesta"):
                juego["respuesta_actual"] = opcion_elegida
                if opcion_elegida == pregunta["respuesta"]:
                    juego["puntaje"] += 1
                    st.success("¡Correcto! Sumaste 1 punto.")
                else:
                    st.error(f"Incorrecto. La respuesta correcta era: {pregunta['respuesta']}")
                st.session_state.game = juego

                if indice == total - 1:
                    juego["finalizado"] = True
                    registrar_resultado_alumno(
                        st.session_state.student["usuario"],
                        juego["grado"],
                        juego["curso"],
                        juego["puntaje"],
                        len(juego["preguntas"]),
                    )
                    st.session_state.game = juego
                else:
                    if st.button("Siguiente pregunta"):
                        juego["indice"] += 1
                        juego["respuesta_actual"] = None
                        st.session_state.game = juego
                        st.rerun()

            if juego.get("respuesta_actual") is not None and indice < total - 1:
                st.info(f"Tu respuesta: {juego['respuesta_actual']}")
        else:
            st.balloons()
            st.success("🎉 Juego finalizado")
            st.markdown(
                f"### Resultado final\n"
                f"**Puntaje:** {juego['puntaje']} / {len(juego['preguntas'])}\n\n"
                f"**Grado:** {juego['grado']}\n"
                f"**Curso:** {juego['curso']}"
            )

            if juego["puntaje"] == len(juego["preguntas"]):
                st.markdown("### ¡Excelente! Contestaste todo correctamente.")
            elif juego["puntaje"] >= len(juego["preguntas"]) // 2:
                st.markdown("### ¡Muy bien! Seguí practicando.")
            else:
                st.markdown("### ¡Sigue intentando! Cada intento enseña.")

            if st.button("Jugar otra vez"):
                iniciar_partida(juego["grado"], juego["curso"])

            if st.button("Volver al menú"):
                st.session_state.game = None
                st.rerun()

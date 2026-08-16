import streamlit as st

from app_utils import LOGO_PATH, apply_custom_style

st.set_page_config(page_title="Quiz Escolar", page_icon="🏫", layout="wide")
apply_custom_style()

logo_col, title_col = st.columns([1.3, 3.7])
with logo_col:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=220)
with title_col:
    st.markdown(
        """
        <div class="brand-header">
            <p class="brand-title">Quiz Escolar</p>
            <p class="brand-subtitle">Sistema escolar para alumnos y docentes</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.subheader("Seleccioná tu acceso")
col1, col2 = st.columns(2)

with col1:
    if st.button("Entrar como alumno", use_container_width=True):
        st.switch_page("pages/alumnos.py")

with col2:
    if st.button("Entrar como docente", use_container_width=True):
        st.switch_page("pages/docentes.py")

st.divider()
st.info("Los alumnos y docentes tienen acceso separado para mantener la pantalla del docente oculta para estudiantes.")


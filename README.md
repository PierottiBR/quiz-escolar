# 🏫 Quiz Escolar

Una aplicación interactiva de preguntas y respuestas (estilo Preguntados) construida con **Streamlit** y **CSV** para instituciones educativas. Diseñada para que docentes gestionen preguntas por grado y materia, y alumnos participen en juegos de quizzes.

## ✨ Características

- **Acceso Separado**: Interfaz distintas para docentes y alumnos
- **Panel Administrativo de Docentes**: Crear docentes, gestionar alumnos, cargar preguntas, ver historial de resultados
- **Autoregistro de Alumnos**: Los estudiantes pueden crear sus propias cuentas con usuario, contraseña y grado
- **Juego Interactivo**: Alumnos responden 5 preguntas aleatorias por materia con feedback inmediato
- **Historial de Resultados**: Seguimiento de puntuaciones y desempeño de estudiantes
- **Gestión de Preguntas**: Docentes pueden agregar, eliminar y organizar preguntas por grado y materia
- **Almacenamiento CSV**: Base de datos simple y portable basada en archivos CSV
- **Diseño Institucional**: Branding escolar con logo personalizable y paleta de colores profesionales

## 🚀 Inicio Rápido

### Requisitos

- Python 3.8+
- pip

### Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/quiz-escolar.git
cd quiz-escolar
```

2. Crear un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install streamlit
```

### Ejecutar la aplicación

```bash
python -m streamlit run main.py
```

La aplicación se abrirá en `http://localhost:8501`

## 📖 Uso

### Para Alumnos

1. **Crear Cuenta**: Ingresa usuario, contraseña y grado
2. **Iniciar Sesión**: Usa tus credenciales
3. **Seleccionar Materia**: Elige la materia en la que deseas jugar
4. **Responder Preguntas**: Contesta 5 preguntas aleatorias
5. **Ver Historial**: Revisa tu desempeño en el tiempo

### Para Docentes

**Credenciales por defecto**:
- Usuario: `maestro`
- Contraseña: `escuela123`

**Funcionalidades**:
- **Gestionar Alumnos**: Ver lista de estudiantes, cambiar contraseñas y actualizar grados
- **Crear Docentes**: Agregar nuevos docentes del personal
- **Cargar Preguntas**: Agregar preguntas por grado y materia
- **Ver Resultados**: Historial completo de juegos y desempeño individual por estudiante

## 📁 Estructura del Proyecto

```
quiz-escolar/
├── main.py                  # Pantalla de inicio y selector de acceso
├── app_utils.py            # Lógica compartida, CSV, y estilos
├── pages/
│   ├── alumnos.py          # Interfaz para estudiantes
│   └── docentes.py         # Panel administrativo de docentes
├── data/
│   ├── docentes.csv        # Cuentas de personal
│   ├── alumnos.csv         # Cuentas de estudiantes
│   ├── resultados.csv      # Historial de puntuaciones
│   ├── 4to.csv             # Preguntas 4° Grado
│   ├── 5to.csv             # Preguntas 5° Grado
│   └── 6to.csv             # Preguntas 6° Grado
├── LOGO ESCUELA 16.jpg     # Logo de la institución
├── .gitignore              # Configuración de Git
└── README.md               # Este archivo
```

## 🎨 Personalización

### Cambiar el Logo

Reemplaza `LOGO ESCUELA 16.jpg` con tu propio logo. Asegúrate de que el nombre del archivo sea el mismo o actualiza la referencia en `app_utils.py`:

```python
LOGO_PATH = BASE_DIR / "TU_LOGO.jpg"
```

### Ajustar Grados y Materias

Edita las constantes en `app_utils.py`:

```python
GRADE_OPTIONS = ["4° Grado", "5° Grado", "6° Grado"]
COURSE_OPTIONS = ["Matemática", "Lengua", "Ciencias", "Sociales"]
```

### Cambiar Credenciales por Defecto

En `app_utils.py`, función `ensure_seed_data()`:

```python
writer.writerow(["maestro", "escuela123", "Matemática"])
```

## 💾 Datos y Almacenamiento

Todos los datos se guardan en archivos CSV en la carpeta `data/`:

- **docentes.csv**: Usuario, contraseña y materia asignada
- **alumnos.csv**: Usuario, contraseña y grado
- **resultados.csv**: Registros de todas las partidas jugadas
- **Archivos por grado**: Banco de preguntas organizado por grado y materia

Los datos persisten entre sesiones y pueden editarse directamente en Excel o cualquier editor de CSV.

### Funciones de Actualización CSV

La aplicación incluye funciones completas para gestionar todos los datos:

**Gestión de Alumnos:**
- `guardar_alumno()` - Crear nuevo alumno
- `obtener_alumno()` - Obtener datos de alumno
- `actualizar_password_alumno()` - Cambiar contraseña
- `actualizar_grado_alumno()` - Cambiar grado
- `eliminar_alumno()` - Eliminar alumno del sistema
- `listar_alumnos()` - Obtener lista de todos los alumnos

**Gestión de Docentes:**
- `guardar_docente()` - Crear nuevo docente
- `obtener_docente()` - Obtener datos de docente
- `actualizar_password_docente()` - Cambiar contraseña
- `actualizar_curso_docente()` - Cambiar materia asignada
- `eliminar_docente()` - Eliminar docente del sistema
- `listar_docentes()` - Obtener lista de todos los docentes

**Gestión de Preguntas:**
- `guardar_pregunta_csv()` - Agregar nueva pregunta
- `cargar_preguntas_csv()` - Cargar preguntas de una materia
- `actualizar_pregunta_csv()` - Actualizar pregunta existente
- `eliminar_pregunta_csv()` - Eliminar pregunta
- `listar_materias_del_grado()` - Obtener materias disponibles por grado

### Verificación de Funciones

Se incluye un script de prueba (`test_csv_functions.py`) que valida todas las operaciones:

```bash
python test_csv_functions.py
```

Todas las funciones están completamente probadas y validadas.

## 🔐 Seguridad

⚠️ **Nota**: Esta es una aplicación educativa. No usa cifrado de contraseñas ni bases de datos avanzadas. Para un entorno de producción real, se recomienda:
- Implementar autenticación segura (OAuth, JWT)
- Usar una base de datos (PostgreSQL, MongoDB)
- Cifrar contraseñas (bcrypt)
- Usar HTTPS

## 🛠️ Tecnologías

- **Frontend**: Streamlit
- **Almacenamiento**: CSV
- **Lenguaje**: Python
- **Estilo**: CSS personalizado con Streamlit markdown

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo licencia MIT.

## 👨‍💼 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📧 Contacto

Si tienes preguntas o sugerencias, abre un issue en el repositorio.

---

**Versión**: 1.0  
**Última actualización**: 2026-08-16

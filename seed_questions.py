"""
Script para cargar preguntas de referencia en todos los grados y materias.
Ejecutar: python seed_questions.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app_utils import guardar_pregunta_csv

# Preguntas para 4° Grado
PREGUNTAS_4TO = {
    "Matemática": [
        ("¿Cuánto es 15 + 8?", ["18", "23", "25", "20"], "23"),
        ("¿Cuánto es 50 - 12?", ["38", "40", "35", "42"], "38"),
        ("¿Cuánto es 6 × 7?", ["42", "40", "45", "38"], "42"),
        ("¿Cuánto es 36 ÷ 4?", ["8", "9", "10", "7"], "9"),
        ("¿Cuál es el doble de 15?", ["25", "30", "35", "28"], "30"),
        ("¿Cuál es la mitad de 48?", ["24", "22", "26", "20"], "24"),
        ("¿Cuánto es 100 - 37?", ["63", "65", "62", "64"], "63"),
        ("¿Cuánto es 8 × 9?", ["72", "70", "75", "68"], "72"),
        ("¿Cuánto es 81 ÷ 9?", ["8", "9", "10", "7"], "9"),
        ("¿Cuál es el número entre 50 y 60?", ["52", "45", "65", "40"], "52"),
    ],
    "Lengua": [
        ("¿Cuál es el sinónimo de 'feliz'?", ["Triste", "Alegre", "Enojado", "Cansado"], "Alegre"),
        ("¿Cuál es el antónimo de 'grande'?", ["Pequeño", "Gordo", "Alto", "Ancho"], "Pequeño"),
        ("¿Cuántas letras tiene la palabra 'escuela'?", ["6", "7", "8", "9"], "7"),
        ("¿Qué tipo de palabra es 'correr'?", ["Sustantivo", "Verbo", "Adjetivo", "Pronombre"], "Verbo"),
        ("¿Cuál de estas palabras es un sustantivo?", ["Rápido", "Comer", "Mesa", "Hermoso"], "Mesa"),
        ("¿Cómo se escribe correctamente 'hola'?", ["ola", "hola", "olla", "jola"], "hola"),
        ("¿Cuál es la palabra opuesta a 'limpio'?", ["Sucio", "Puro", "Claro", "Blanco"], "Sucio"),
        ("¿Cuántas sílabas tiene 'mariposa'?", ["2", "3", "4", "5"], "4"),
        ("¿Qué es un cuento?", ["Una canción", "Una historia", "Una imagen", "Un juego"], "Una historia"),
        ("¿Cuál es una vocal?", ["B", "A", "C", "D"], "A"),
    ],
    "Ciencias": [
        ("¿Cuál es el planeta más grande del Sistema Solar?", ["Tierra", "Marte", "Júpiter", "Saturno"], "Júpiter"),
        ("¿Cuántos planetas hay en el Sistema Solar?", ["7", "8", "9", "10"], "8"),
        ("¿Qué planeta es conocido como el planeta rojo?", ["Venus", "Marte", "Mercurio", "Neptuno"], "Marte"),
        ("¿Cuál es la principal función de las plantas?", ["Caminar", "Producir oxígeno", "Hablar", "Comer"], "Producir oxígeno"),
        ("¿Qué animales son mamíferos?", ["Peces", "Aves", "Perros", "Insectos"], "Perros"),
        ("¿Cuántas patas tiene una araña?", ["6", "8", "10", "12"], "8"),
        ("¿Cuál es el hueso más largo del cuerpo?", ["Fémur", "Tibia", "Radio", "Húmero"], "Fémur"),
        ("¿Qué órgano bombea la sangre?", ["Pulmón", "Corazón", "Hígado", "Cerebro"], "Corazón"),
        ("¿De qué color es el cielo en un día despejado?", ["Gris", "Azul", "Verde", "Rojo"], "Azul"),
        ("¿Cuál es el satélite natural de la Tierra?", ["Sol", "Luna", "Marte", "Venus"], "Luna"),
    ],
    "Sociales": [
        ("¿Cuál es la capital de Argentina?", ["Córdoba", "Buenos Aires", "Rosario", "Mendoza"], "Buenos Aires"),
        ("¿En qué continente estamos?", ["Asia", "Europa", "América", "África"], "América"),
        ("¿Quién fue el primer presidente de Argentina?", ["San Martín", "Belgrano", "Rivadavia", "Sarmiento"], "Rivadavia"),
        ("¿Cuántas provincias tiene Argentina?", ["21", "23", "24", "25"], "23"),
        ("¿Qué es una comunidad?", ["Un río", "Un grupo de personas que viven juntas", "Una montaña", "Un animal"], "Un grupo de personas que viven juntas"),
        ("¿Cuál es el río más importante de Argentina?", ["Paraná", "Río de la Plata", "Tajo", "Ebro"], "Río de la Plata"),
        ("¿Qué celebramos el 25 de mayo?", ["Navidad", "Año Nuevo", "La Revolución de Mayo", "Independencia"], "La Revolución de Mayo"),
        ("¿Cuál es el documento que nos identifica?", ["Pasaporte", "DNI", "Licencia", "Carnet"], "DNI"),
        ("¿Cuántos continentes hay?", ["5", "6", "7", "8"], "5"),
        ("¿Qué es una familia?", ["Un grupo de amigos", "Un conjunto de personas que viven juntas", "Un grupo de compañeros", "Un equipo"], "Un conjunto de personas que viven juntas"),
    ],
}

# Preguntas para 5° Grado
PREGUNTAS_5TO = {
    "Matemática": [
        ("¿Cuánto es 234 + 456?", ["680", "690", "700", "710"], "690"),
        ("¿Cuánto es 1000 - 345?", ["655", "665", "675", "685"], "655"),
        ("¿Cuánto es 12 × 15?", ["180", "190", "200", "210"], "180"),
        ("¿Cuánto es 144 ÷ 12?", ["10", "11", "12", "13"], "12"),
        ("¿Cuál es el 25% de 100?", ["20", "25", "30", "35"], "25"),
        ("¿Cuánto es 2³?", ["6", "8", "9", "12"], "8"),
        ("¿Cuál es el mínimo común múltiplo de 4 y 6?", ["12", "10", "8", "24"], "12"),
        ("¿Cuánto es 5.5 + 3.2?", ["8.5", "8.6", "8.7", "8.8"], "8.7"),
        ("¿Cuánto es 10² + 5²?", ["100", "125", "150", "175"], "125"),
        ("¿Cuál es el perímetro de un cuadrado de lado 5?", ["20", "25", "30", "35"], "20"),
    ],
    "Lengua": [
        ("¿Qué es un sustantivo?", ["Una acción", "Una palabra que nombra personas, animales o cosas", "Un descriptivo", "Un conectivo"], "Una palabra que nombra personas, animales o cosas"),
        ("¿Cuál es el plural de 'lápiz'?", ["Lápices", "Lapizes", "Lápizs", "Lapis"], "Lápices"),
        ("¿Qué es una oración?", ["Varias palabras sin sentido", "Un conjunto de palabras con sentido completo", "Una palabra", "Un párrafo"], "Un conjunto de palabras con sentido completo"),
        ("¿Cuántos géneros tienen los sustantivos?", ["1", "2", "3", "4"], "2"),
        ("¿Qué es el verbo?", ["Una cualidad", "Una persona", "Una palabra que expresa acción", "Un nombre"], "Una palabra que expresa acción"),
        ("¿Cuál es el diminutivo de 'casa'?", ["Casita", "Casilla", "Caseta", "Casona"], "Casita"),
        ("¿Qué es una metáfora?", ["Una comparación", "Una figura literaria que compara dos cosas sin usar 'como'", "Una pregunta", "Una exclamación"], "Una figura literaria que compara dos cosas sin usar 'como'"),
        ("¿Cuántas sílabas tiene 'hipopótamo'?", ["4", "5", "6", "7"], "5"),
        ("¿Cuál es el sujeto de 'El gato come pescado'?", ["Come", "Pescado", "El gato", "Come pescado"], "El gato"),
        ("¿Qué es una prosa?", ["Un poema", "Un texto sin rima", "Una canción", "Un diálogo"], "Un texto sin rima"),
    ],
    "Ciencias": [
        ("¿Cuántas capas tiene la atmósfera?", ["3", "4", "5", "6"], "5"),
        ("¿Cuál es la velocidad de la luz?", ["300.000 km/s", "100.000 km/s", "500.000 km/s", "200.000 km/s"], "300.000 km/s"),
        ("¿Qué es la fotosíntesis?", ["La respiración de las plantas", "El proceso por el que las plantas producen su propio alimento", "El crecimiento de las plantas", "La reproducción de las plantas"], "El proceso por el que las plantas producen su propio alimento"),
        ("¿Cuántos huesos tiene el cuerpo humano adulto?", ["186", "206", "226", "246"], "206"),
        ("¿Cuál es el órgano más grande del cuerpo?", ["Corazón", "Pulmón", "Piel", "Hígado"], "Piel"),
        ("¿Qué son los minerales?", ["Sustancias líquidas", "Sustancias sólidas naturales con estructura cristalina", "Elementos del aire", "Productos químicos"], "Sustancias sólidas naturales con estructura cristalina"),
        ("¿Cuál es la densidad del agua en g/cm³?", ["0.5", "1.0", "1.5", "2.0"], "1.0"),
        ("¿Qué es la biodiversidad?", ["La cantidad de agua", "La variedad de seres vivos en un lugar", "El número de plantas", "La cantidad de animales"], "La variedad de seres vivos en un lugar"),
        ("¿Cuántos tipos de sangre hay en el sistema ABO?", ["2", "3", "4", "5"], "4"),
        ("¿Qué es un ecosistema?", ["Un parque", "Un sistema formado por seres vivos e interacciones con su ambiente", "Un bosque", "Un grupo de plantas"], "Un sistema formado por seres vivos e interacciones con su ambiente"),
    ],
    "Sociales": [
        ("¿En qué año se declaró la independencia argentina?", ["1810", "1816", "1820", "1825"], "1816"),
        ("¿Cuál es la forma de gobierno en Argentina?", ["Monarquía", "Democracia", "Dictadura", "República Federal"], "República Federal"),
        ("¿Cuántas provincias tiene Argentina?", ["23", "24", "25", "26"], "23"),
        ("¿Quién escribió el Himno Nacional Argentino?", ["San Martín", "Belgrano", "Vicente López y Planes", "Blas Parera"], "Vicente López y Planes"),
        ("¿Cuál es la ciudad más poblada de Argentina?", ["Córdoba", "Rosario", "Buenos Aires", "Mendoza"], "Buenos Aires"),
        ("¿En qué año ocurrió la Revolución de Mayo?", ["1808", "1809", "1810", "1811"], "1810"),
        ("¿Qué es la Constitución?", ["Un edificio", "La ley fundamental de un país", "Un libro de historia", "Un monumento"], "La ley fundamental de un país"),
        ("¿Cuántos poderes tiene el Estado argentino?", ["2", "3", "4", "5"], "3"),
        ("¿Quién es San Martín?", ["Un general que liberó América", "Un presidente", "Un historiador", "Un poeta"], "Un general que liberó América"),
        ("¿Cuál es la flor nacional de Argentina?", ["Rosa", "Girasol", "Ceibo", "Amapola"], "Ceibo"),
    ],
}

# Preguntas para 6° Grado
PREGUNTAS_6TO = {
    "Matemática": [
        ("¿Cuánto es (15 + 25) × 3?", ["100", "110", "120", "130"], "120"),
        ("¿Cuánto es √144?", ["10", "11", "12", "13"], "12"),
        ("¿Cuál es el máximo común divisor de 24 y 36?", ["6", "8", "12", "18"], "12"),
        ("¿Cuánto es 2⁵?", ["16", "32", "64", "128"], "32"),
        ("¿Cuál es el 50% de 200?", ["50", "75", "100", "150"], "100"),
        ("¿Cuánto es 3.5 × 2.4?", ["7.4", "8.0", "8.4", "9.0"], "8.4"),
        ("¿Cuál es el área de un rectángulo de 8 × 5?", ["40", "45", "50", "55"], "40"),
        ("¿Cuánto es (10 - 5)² + 3²?", ["34", "35", "36", "37"], "34"),
        ("¿Cuál es el volumen de un cubo de lado 3?", ["9", "18", "27", "36"], "27"),
        ("¿Cuánto es 1/2 + 1/3?", ["2/5", "5/6", "3/5", "2/3"], "5/6"),
    ],
    "Lengua": [
        ("¿Qué es la literatura?", ["El arte de escribir", "El arte de las palabras", "El estudio de libros", "El género más popular"], "El arte de las palabras"),
        ("¿Cuál es la diferencia entre cuento y novela?", ["El cuento es más corto", "La novela tiene más personajes", "El cuento es más antiguo", "No hay diferencia"], "El cuento es más corto"),
        ("¿Qué es un narrador?", ["El personaje principal", "Quien cuenta la historia", "El autor del libro", "El protagonista"], "Quien cuenta la historia"),
        ("¿Cuál es el punto de vista en tercera persona?", ["El narrador es un personaje", "El narrador es el protagonista", "El narrador no participa en los hechos", "El narrador es el autor"], "El narrador no participa en los hechos"),
        ("¿Qué es una onomatopeya?", ["Una repetición", "Una palabra que imita un sonido", "Una rima", "Una comparación"], "Una palabra que imita un sonido"),
        ("¿Qué es la ironía?", ["Una exageración", "Una broma pesada", "Decir lo contrario de lo que se piensa", "Una mentira"], "Decir lo contrario de lo que se piensa"),
        ("¿Cuál es la estructura de una novela?", ["Prólogo, desarrollo, epílogo", "Introducción, nudo, desenlace", "Inicio, mitad, fin", "Presentación, conflicto, resolución"], "Introducción, nudo, desenlace"),
        ("¿Qué es un soliloquio?", ["Una conversación entre dos personajes", "Un monólogo interior de un personaje", "Una narración del autor", "Una descripción"], "Un monólogo interior de un personaje"),
        ("¿Cuál es el tema de una obra literaria?", ["El asunto principal", "Los personajes principales", "El lugar donde ocurre", "El tiempo en que ocurre"], "El asunto principal"),
        ("¿Qué es la prosa?", ["Un texto con ritmo y rima", "Un texto sin rima organizado en párrafos", "Un poema corto", "Una conversación"], "Un texto sin rima organizado en párrafos"),
    ],
    "Ciencias": [
        ("¿Cuál es el proceso de cambio de agua líquida a gaseosa?", ["Congelación", "Evaporación", "Sublimación", "Licuación"], "Evaporación"),
        ("¿Qué es la presión atmosférica?", ["El peso del aire", "La temperatura del aire", "La velocidad del viento", "La cantidad de oxígeno"], "El peso del aire"),
        ("¿Cuántas capas tiene la Tierra?", ["2", "3", "4", "5"], "3"),
        ("¿Cuál es el ciclo del agua?", ["Evaporación, condensación, precipitación", "Lluvia, nieve, granizo", "Mar, río, océano", "Nube, lluvia, nieve"], "Evaporación, condensación, precipitación"),
        ("¿Qué es un mineral?", ["Un elemento del suelo", "Una sustancia sólida natural con estructura cristalina", "Una roca", "Un metal"], "Una sustancia sólida natural con estructura cristalina"),
        ("¿Cuál es el tipo de sangre más común?", ["A", "B", "O", "AB"], "O"),
        ("¿Qué es la osmosis?", ["Un tipo de movimiento", "El paso de agua a través de una membrana semipermeable", "Una reacción química", "Un proceso de fotosíntesis"], "El paso de agua a través de una membrana semipermeable"),
        ("¿Cuántos huesos tiene la columna vertebral?", ["30", "33", "36", "40"], "33"),
        ("¿Qué es la energía cinética?", ["La energía de movimiento", "La energía almacenada", "La energía térmica", "La energía luminosa"], "La energía de movimiento"),
        ("¿Cuál es la fórmula de la velocidad?", ["V = D × T", "V = D / T", "V = T / D", "V = D + T"], "V = D / T"),
    ],
    "Sociales": [
        ("¿En qué año comenzó la Segunda Guerra Mundial?", ["1937", "1938", "1939", "1940"], "1939"),
        ("¿Cuál fue la causa principal de la Revolución Francesa?", ["Guerras napoleónicas", "Crisis económica y social", "Independencia de colonias", "Problemas religiosos"], "Crisis económica y social"),
        ("¿Quiénes fueron los Reyes Católicos?", ["Fernando e Isabel", "Carlos y Juana", "Felipe e Isabel", "Juan e Catalina"], "Fernando e Isabel"),
        ("¿En qué siglo fue el descubrimiento de América?", ["XIV", "XV", "XVI", "XVII"], "XV"),
        ("¿Cuál fue la causa de la Guerra de la Independencia Argentina?", ["Problemas económicos", "Invasiones inglesas", "La Revolución Francesa", "Todas las anteriores"], "Todas las anteriores"),
        ("¿Qué es la democracia?", ["Un sistema de gobierno de una sola persona", "Un sistema de gobierno donde el poder está en el pueblo", "Un sistema militar", "Un sistema religioso"], "Un sistema de gobierno donde el poder está en el pueblo"),
        ("¿Quién fue Simón Bolívar?", ["Un presidente argentino", "Un general que liberó varios países de América", "Un escritor sudamericano", "Un científico"], "Un general que liberó varios países de América"),
        ("¿Cuál es la capital de América Latina con mayor población?", ["São Paulo", "México", "Bogotá", "Lima"], "São Paulo"),
        ("¿En qué año fue la declaración de la independencia de los EE.UU.?", ["1774", "1775", "1776", "1777"], "1776"),
        ("¿Qué es un tratado internacional?", ["Una ley local", "Un acuerdo entre países", "Una norma escolar", "Una regla de comercio"], "Un acuerdo entre países"),
    ],
}

TODOS_LOS_GRADOS = {
    "Primaria": {
        materia: PREGUNTAS_4TO[materia] + PREGUNTAS_5TO[materia]
        for materia in PREGUNTAS_4TO
    },
    "Secundaria": PREGUNTAS_6TO,
}


def cargar_preguntas_referencia():
    """Carga todas las preguntas de referencia en los archivos CSV."""
    print("\n" + "=" * 60)
    print("📚 CARGANDO PREGUNTAS DE REFERENCIA")
    print("=" * 60)
    
    total_preguntas = 0
    
    for grado, materias in TODOS_LOS_GRADOS.items():
        print(f"\n📖 {grado}")
        print("-" * 60)
        
        for materia, preguntas in materias.items():
            contador = 0
            for pregunta_texto, opciones, respuesta_correcta in preguntas:
                try:
                    guardar_pregunta_csv(
                        grado,
                        materia,
                        pregunta_texto,
                        opciones,
                        respuesta_correcta
                    )
                    contador += 1
                except Exception as e:
                    print(f"  ✗ Error al guardar pregunta de {materia}: {e}")
            
            total_preguntas += contador
            print(f"  ✓ {materia}: {contador} preguntas cargadas")
    
    print("\n" + "=" * 60)
    print(f"✅ TOTAL: {total_preguntas} preguntas cargadas exitosamente")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    cargar_preguntas_referencia()

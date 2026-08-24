"""Carga preguntas de referencia para Primaria y Secundaria."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app_utils import guardar_pregunta_csv

PREGUNTAS = {
    "Primaria": {
        "Matemática": [
            ("¿Cuánto es 15 + 8?", ["18", "23", "25", "20"], "23"),
            ("¿Cuánto es 6 x 7?", ["36", "42", "48", "40"], "42"),
            ("¿Cuál es la mitad de 48?", ["20", "24", "28", "32"], "24"),
        ],
        "Lengua": [
            ("¿Cuál es el sinónimo de rápido?", ["Lento", "Veloz", "Triste", "Grande"], "Veloz"),
            ("¿Qué tipo de palabra es casa?", ["Verbo", "Adjetivo", "Sustantivo", "Pronombre"], "Sustantivo"),
            ("¿Cuál es el antónimo de grande?", ["Pequeño", "Alto", "Ancho", "Largo"], "Pequeño"),
        ],
        "Ciencias": [
            ("¿Qué planeta es conocido como el planeta rojo?", ["Venus", "Marte", "Júpiter", "Mercurio"], "Marte"),
            ("¿Qué necesitamos para respirar?", ["Agua", "Oxígeno", "Sal", "Arena"], "Oxígeno"),
            ("¿Cuál es el satélite natural de la Tierra?", ["El Sol", "La Luna", "Marte", "Venus"], "La Luna"),
        ],
        "Sociales": [
            ("¿Cuál es la capital de Argentina?", ["Córdoba", "Buenos Aires", "Rosario", "Mendoza"], "Buenos Aires"),
            ("¿Qué es una comunidad?", ["Un río", "Un grupo de personas", "Una montaña", "Un animal"], "Un grupo de personas"),
            ("¿Qué documento nos identifica?", ["DNI", "Una receta", "Un mapa", "Un cuento"], "DNI"),
        ],
    },
    "Secundaria": {
        "Matemática": [
            ("¿Cuánto es la raíz cuadrada de 144?", ["10", "11", "12", "14"], "12"),
            ("¿Cuál es el 25 por ciento de 200?", ["25", "40", "50", "75"], "50"),
            ("¿Cuál es el área de un rectángulo de 8 por 5?", ["13", "26", "40", "80"], "40"),
        ],
        "Lengua": [
            ("¿Qué es un narrador?", ["Quien cuenta la historia", "El título", "El escenario", "El lector"], "Quien cuenta la historia"),
            ("¿Qué es una metáfora?", ["Una comparación implícita", "Una pregunta", "Una rima", "Un diálogo"], "Una comparación implícita"),
            ("¿Cuál es la estructura básica de una narración?", ["Inicio, nudo y desenlace", "Título y autor", "Verso y estrofa", "Pregunta y respuesta"], "Inicio, nudo y desenlace"),
        ],
        "Ciencias": [
            ("¿Cuál es el proceso por el que las plantas producen alimento?", ["Digestión", "Fotosíntesis", "Evaporación", "Fermentación"], "Fotosíntesis"),
            ("¿Qué fórmula representa la velocidad?", ["Distancia dividida por tiempo", "Tiempo dividido por distancia", "Distancia por tiempo", "Distancia más tiempo"], "Distancia dividida por tiempo"),
            ("¿Cuántos huesos tiene aproximadamente el cuerpo adulto?", ["106", "206", "306", "406"], "206"),
        ],
        "Sociales": [
            ("¿En qué año se declaró la independencia argentina?", ["1810", "1816", "1820", "1825"], "1816"),
            ("¿Cuántos poderes tiene el Estado?", ["Dos", "Tres", "Cuatro", "Cinco"], "Tres"),
            ("¿Qué es la democracia?", ["Gobierno del pueblo", "Gobierno de una sola persona", "Gobierno militar", "Gobierno hereditario"], "Gobierno del pueblo"),
        ],
    },
}


def cargar_preguntas_referencia():
    total = 0
    for nivel, materias in PREGUNTAS.items():
        for materia, preguntas in materias.items():
            for texto, opciones, respuesta in preguntas:
                guardar_pregunta_csv(nivel, materia, texto, opciones, respuesta)
                total += 1
    print(f"{total} preguntas de referencia cargadas.")


if __name__ == "__main__":
    cargar_preguntas_referencia()

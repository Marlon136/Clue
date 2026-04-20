"""
robo_expreso_sur.py — El Robo en el Expreso del Sur

El collar de esmeraldas de la Marquesa desapareció del vagón privado del tren nocturno.
Elena fue vista en el vagón privado durante el robo; sus huellas están en el estuche de joyas.
Don Rodrigo fue grabado por la cámara de seguridad en el vagón de equipaje durante toda la noche.
El vagón de equipaje es el extremo opuesto al vagón privado; es imposible haber estado en ambos a la vez.
La Marquesa es la víctima directa del robo y presenció el incidente.
La Marquesa acusa a Elena.
Victor declara que Elena estuvo con él en el vagón comedor toda la noche.
Elena declara que Victor estuvo con ella en el vagón comedor toda la noche.

Como detective, he llegado a las siguientes conclusiones:
Quien fue grabado en cámara en un lugar alejado de la escena durante el crimen está descartado.
La víctima del crimen no tiene razón para mentir; es testigo imparcial.
La acusación de un testigo imparcial es creíble.
Quien estaba en la escena y es acusado de forma creíble es culpable.
Quien da coartada a un culpable lo está defendiendo.
Si dos personas se dan coartada mutuamente, tienen una alianza de coartadas entre sí.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    """Construye la KB según la narrativa del módulo."""
    kb = KnowledgeBase()

    # Constantes del caso
    elena          = Term("elena")
    victor         = Term("victor")
    don_rodrigo    = Term("don_rodrigo")
    marquesa       = Term("marquesa")
    estuche_joyas  = Term("estuche_joyas")
    vagon_equipaje = Term("vagon_equipaje")

    kb.add_fact(Predicate("en_escena", (elena,)))
    kb.add_fact(Predicate("huellas_en", (elena, estuche_joyas)))
    kb.add_fact(Predicate("grabado_lejos_escena", (don_rodrigo, vagon_equipaje)))
    kb.add_fact(Predicate("victima", (marquesa,)))
    kb.add_fact(Predicate("acusa", (marquesa, elena)))
    kb.add_fact(Predicate("da_coartada", (victor, elena)))
    kb.add_fact(Predicate("da_coartada", (elena, victor)))

    x = Term("$X")
    y = Term("$Y")
    z = Term("$Z")
    s = Term("$S")


    kb.add_rule(Rule(
        head=Predicate("descartado", (x,)),
        body=(Predicate("grabado_lejos_escena", (x, z)),)
    ))

    kb.add_rule(Rule(
        head=Predicate("testigo_imparcial", (x,)),
        body=(Predicate("victima", (x,)),)
    ))

    kb.add_rule(Rule(
        head=Predicate("acusacion_creible", (x, y)),
        body=(
            Predicate("testigo_imparcial", (x,)),
            Predicate("acusa", (x, y))
        )
    ))

    kb.add_rule(Rule(
        head=Predicate("culpable", (x,)),
        body=(
            Predicate("en_escena", (x,)),
            Predicate("acusacion_creible", (s, x))
        )
    ))

    kb.add_rule(Rule(
        head=Predicate("defiende_al_culpable", (x,)),
        body=(
            Predicate("da_coartada", (x, y)),
            Predicate("culpable", (y,))
        )
    ))

    kb.add_rule(Rule(
        head=Predicate("alianza_coartadas", (x, y)),
        body=(
            Predicate("da_coartada", (x, y)),
            Predicate("da_coartada", (y, x))
        )
    ))
    return kb

CASE = CrimeCase(
    id="robo_expreso_sur",
    title="El Robo en el Expreso del Sur",
    suspects=("elena", "victor", "don_rodrigo"),
    narrative=__doc__,
    description=(
        "El collar de la Marquesa desapareció en un tren nocturno. "
        "Don Rodrigo tiene coartada de cámara. Elena estaba en la escena con huellas en el estuche. "
        "La víctima la acusa. Victor y Elena se cubren mutuamente."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="¿Don Rodrigo está descartado?",
            goal=Predicate("descartado", (Term("don_rodrigo"),)),
        ),
        QuerySpec(
            description="¿La acusación de la Marquesa contra Elena es creíble?",
            goal=Predicate("acusacion_creible", (Term("marquesa"), Term("elena"))),
        ),
        QuerySpec(
            description="¿Elena es culpable?",
            goal=Predicate("culpable", (Term("elena"),)),
        ),
        QuerySpec(
            description="¿Victor defiende al culpable?",
            goal=Predicate("defiende_al_culpable", (Term("victor"),)),
        ),
        QuerySpec(
            description="¿Existe alianza de coartadas entre Elena y Victor?",
            goal=ExistsGoal("$X", Predicate("alianza_coartadas", (Term("$X"), Term("victor")))),
        ),
    ),
)

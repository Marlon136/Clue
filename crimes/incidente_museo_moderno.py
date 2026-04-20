"""
incidente_museo_moderno.py — El Incidente del Museo de Arte Moderno

Una valiosa escultura vanguardista desapareció durante la gala anual del museo. El sistema de seguridad fue vulnerado 
usando una tarjeta maestra. La Curadora Elena posee una tarjeta maestra, pero fue grabada en público durante toda la 
gala. El Guardia Marcos fue visto cerca de la bodega de carga y posee una cojera física distintiva que coincide con 
las grabaciones borrosas del pasillo de seguridad. La Restauradora Sofía estaba en el laboratorio sin testigos y no 
tiene coartada verificada. La Directora Julia también fue grabada en el salón principal atendiendo a los invitados.

Como detective, he llegado a las siguientes conclusiones:
Quien es grabado en público por las cámaras del salón queda descartado inmediatamente por tener coartada física.
No tener una coartada verificada por testigos o cámaras implica que el sospechoso tuvo oportunidad de cometer el robo.
Un sospechoso es considerado sospechoso principal si fue visto cerca de la bodega y posee rasgos físicos que 
coinciden con la evidencia de la cámara (como la cojera).
Quien es un sospechoso principal y además tuvo la oportunidad logística de actuar sin ser visto es culpable del robo.
Cualquier persona que no esté descartada y haya estado en el museo es objeto de investigación activa.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, ForallGoal, KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    """Construye la KB para el caso del Museo de Arte Moderno."""
    kb = KnowledgeBase()

    # Constantes (Sospechosos y Objetos)
    elena   = Term("curadora_elena")
    marcos  = Term("guardia_marcos")
    sofia   = Term("restauradora_sofia")
    julia   = Term("directora_julia")
    bodega  = Term("bodega_carga")

    # Hechos base (Mínimo 6)
    kb.add_fact(Predicate("grabada_en_publico", (elena,)))
    kb.add_fact(Predicate("grabada_en_publico", (julia,)))
    kb.add_fact(Predicate("visto_cerca", (marcos, bodega)))
    kb.add_fact(Predicate("tiene_cojera", (marcos,)))
    kb.add_fact(Predicate("sin_coartada_verificada", (marcos,)))
    kb.add_fact(Predicate("sin_coartada_verificada", (sofia,)))
    kb.add_fact(Predicate("en_el_museo", (elena,)))
    kb.add_fact(Predicate("en_el_museo", (marcos,)))
    kb.add_fact(Predicate("en_el_museo", (sofia,)))
    kb.add_fact(Predicate("en_el_museo", (julia,)))

    # Variables
    x = Term("$X")
    y = Term("$Y")

    # Reglas (Mínimo 4)
    kb.add_rule(Rule(
        head=Predicate("descartado", (x,)),
        body=(Predicate("grabada_en_publico", (x,)),)
    ))

    kb.add_rule(Rule(
        head=Predicate("tiene_oportunidad", (x,)),
        body=(Predicate("sin_coartada_verificada", (x,)),)
    ))

    kb.add_rule(Rule(
        head=Predicate("sospechoso_principal", (x,)),
        body=(
            Predicate("visto_cerca", (x, y)),
            Predicate("tiene_cojera", (x,))
        )
    ))

    kb.add_rule(Rule(
        head=Predicate("culpable", (x,)),
        body=(
            Predicate("sospechoso_principal", (x,)),
            Predicate("tiene_oportunidad", (x,))
        )
    ))

    return kb


CASE = CrimeCase(
    id="incidente_museo_moderno",
    title="El Incidente del Museo de Arte Moderno",
    suspects=("curadora_elena", "guardia_marcos", "restauradora_sofia", "directora_julia"),
    narrative=__doc__,
    description=(
        "Una escultura desapareció de la bodega. El culpable tiene una cojera física "
        "y no tiene coartada. Elena y Julia están descartadas por cámaras."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="¿La Curadora Elena está descartada?",
            goal=Predicate("descartado", (Term("curadora_elena"),)),
        ),
        QuerySpec(
            description="¿El Guardia Marcos es el culpable?",
            goal=Predicate("culpable", (Term("guardia_marcos"),)),
        ),
        QuerySpec(
            description="¿Existe al menos una persona descartada?",
            goal=ExistsGoal("$X", Predicate("descartado", (Term("$X"),))),
        ),
        QuerySpec(
            description="¿Todos los que fueron grabados en público están descartados?",
            goal=ForallGoal("$X", Predicate("grabada_en_publico", (Term("$X"),)), Predicate("descartado", (Term("$X"),))),
        ),
        QuerySpec(
            description="¿La Restauradora Sofía tuvo oportunidad logística?",
            goal=Predicate("tiene_oportunidad", (Term("restauradora_sofia"),)),
        ),
    ),
)
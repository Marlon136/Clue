"""
cnf_transform.py — Transformaciones a Forma Normal Conjuntiva (CNF).
El pipeline completo to_cnf() llama a todas las transformaciones en orden.
"""

from __future__ import annotations

from src.logic_core import And, Atom, Formula, Iff, Implies, Not, Or


# --- FUNCION GUÍA SUMINISTRADA COMPLETA ---


def eliminate_double_negation(formula: Formula) -> Formula:
    """
    Elimina dobles negaciones recursivamente.

    Transformacion:
        Not(Not(a)) -> a

    Se aplica recursivamente hasta que no queden dobles negaciones.

    Ejemplo:
        >>> eliminate_double_negation(Not(Not(Atom('p'))))
        Atom('p')
        >>> eliminate_double_negation(Not(Not(Not(Atom('p')))))
        Not(Atom('p'))
    """
    if isinstance(formula, Atom):
        return formula
    if isinstance(formula, Not):
        if isinstance(formula.operand, Not):
            return eliminate_double_negation(formula.operand.operand)
        return Not(eliminate_double_negation(formula.operand))
    if isinstance(formula, And):
        return And(*(eliminate_double_negation(c) for c in formula.conjuncts))
    if isinstance(formula, Or):
        return Or(*(eliminate_double_negation(d) for d in formula.disjuncts))
    return formula


# --- FUNCIONES QUE DEBEN IMPLEMENTAR ---


def eliminate_iff(formula: Formula) -> Formula:
    """
    Elimina bicondicionales recursivamente.

    Transformacion:
        Iff(a, b) -> And(Implies(a, b), Implies(b, a))

    Debe aplicarse recursivamente a todas las sub-formulas.

    Ejemplo:
        >>> eliminate_iff(Iff(Atom('p'), Atom('q')))
        And(Implies(Atom('p'), Atom('q')), Implies(Atom('q'), Atom('p')))

    Hint: Usa pattern matching sobre el tipo de la formula.
          Para cada tipo, aplica eliminate_iff recursivamente a los operandos,
          y solo transforma cuando encuentras un Iff.
    """
    # === YOUR CODE HERE ===
    if isinstance(formula, Atom):
        return formula

    if isinstance(formula, Iff):
        a = eliminate_iff(formula.left)
        b = eliminate_iff(formula.right)
        return And(Implies(a, b), Implies(b, a))

    if isinstance(formula, Not):
        return Not(eliminate_iff(formula.operand))

    if isinstance(formula, And):
        new_conjuncts = []
        for c in formula.conjuncts:
            new_conjuncts.append(eliminate_iff(c))
        return And(*new_conjuncts)

    if isinstance(formula, Or):
        new_disjuncts = []
        for d in formula.disjuncts:
            new_disjuncts.append(eliminate_iff(d))
        return Or(*new_disjuncts)

    if isinstance(formula, Implies):
        return Implies(
            eliminate_iff(formula.antecedent),
            eliminate_iff(formula.consequent)
        )

    return formula

    # === END YOUR CODE ===


def eliminate_implication(formula: Formula) -> Formula:
    """
    Elimina implicaciones recursivamente.

    Transformacion:
        Implies(a, b) -> Or(Not(a), b)

    Debe aplicarse recursivamente a todas las sub-formulas.

    Ejemplo:
        >>> eliminate_implication(Implies(Atom('p'), Atom('q')))
        Or(Not(Atom('p')), Atom('q'))

    Hint: Similar a eliminate_iff. Recorre recursivamente y transforma
          solo los nodos Implies.
    """
    # === YOUR CODE HERE ===
    if isinstance(formula, Atom):
        return formula

    if isinstance(formula, Implies):
        a = eliminate_implication(formula.antecedent)
        b = eliminate_implication(formula.consequent)
        return Or(Not(a), b)

    if isinstance(formula, Not):
        return Not(eliminate_implication(formula.operand))

    if isinstance(formula, And):
        new_conjuncts = []
        for c in formula.conjuncts:
            new_conjuncts.append(eliminate_implication(c))
        return And(*new_conjuncts)

    if isinstance(formula, Or):
        new_disjuncts = []
        for d in formula.disjuncts:
            new_disjuncts.append(eliminate_implication(d))
        return Or(*new_disjuncts)

    return formula    # === END YOUR CODE ===


def push_negation_inward(formula: Formula) -> Formula:
    """
    Aplica las leyes de De Morgan y mueve negaciones hacia los atomos.

    Transformaciones:
        Not(And(a, b, ...)) -> Or(Not(a), Not(b), ...)   (De Morgan)
        Not(Or(a, b, ...))  -> And(Not(a), Not(b), ...)   (De Morgan)

    Debe aplicarse recursivamente a todas las sub-formulas.

    Ejemplo:
        >>> push_negation_inward(Not(And(Atom('p'), Atom('q'))))
        Or(Not(Atom('p')), Not(Atom('q')))
        >>> push_negation_inward(Not(Or(Atom('p'), Atom('q'))))
        And(Not(Atom('p')), Not(Atom('q')))

    Hint: Cuando encuentres un Not, revisa que hay adentro:
          - Si es Not(And(...)): aplica De Morgan para convertir en Or de negaciones.
          - Si es Not(Or(...)): aplica De Morgan para convertir en And de negaciones.
          - Si es Not(Atom): dejar como esta.
          Para And y Or sin negacion encima, simplemente recursa sobre los hijos.

    Nota: Esta funcion se llama DESPUES de eliminar Iff e Implies,
          asi que no necesitas manejar esos tipos.
    """
    # === YOUR CODE HERE ===
    if isinstance(formula, Atom):
        return formula

    if isinstance(formula, Not):
        inner = formula.operand

        if isinstance(inner, Atom):
            return formula

        if isinstance(inner, Not):
            return push_negation_inward(inner.operand)

        if isinstance(inner, And):
            new_disjuncts = []
            for c in inner.conjuncts:
                new_disjuncts.append(push_negation_inward(Not(c)))
            return Or(*new_disjuncts)

        if isinstance(inner, Or):
            new_conjuncts = []
            for d in inner.disjuncts:
                new_conjuncts.append(push_negation_inward(Not(d)))
            return And(*new_conjuncts)

    if isinstance(formula, And):
        new_conjuncts = []
        for c in formula.conjuncts:
            new_conjuncts.append(push_negation_inward(c))
        return And(*new_conjuncts)

    if isinstance(formula, Or):
        new_disjuncts = []
        for d in formula.disjuncts:
            new_disjuncts.append(push_negation_inward(d))
        return Or(*new_disjuncts)

    return formula
    # === END YOUR CODE ===


def distribute_or_over_and(formula: Formula) -> Formula:
    """
    Distribuye Or sobre And para obtener CNF.

    Transformacion:
        Or(A, And(B, C)) -> And(Or(A, B), Or(A, C))

    Debe aplicarse recursivamente hasta que no queden Or que contengan And.

    Ejemplo:
        >>> distribute_or_over_and(Or(Atom('p'), And(Atom('q'), Atom('r'))))
        And(Or(Atom('p'), Atom('q')), Or(Atom('p'), Atom('r')))

    Hint: Para un nodo Or, primero distribuye recursivamente en los hijos.
          Luego busca si algun hijo es un And. Si lo encuentras, aplica la
          distribucion y recursa sobre el resultado (podria haber mas).
          Para And, simplemente recursa sobre cada conjuncion.
          Atomos y Not se retornan sin cambio.

    Nota: Esta funcion se llama DESPUES de mover negaciones hacia adentro,
          asi que solo veras Atom, Not(Atom), And y Or.
    """
    # === YOUR CODE HERE ===
    if isinstance(formula, Atom) or isinstance(formula, Not):
        return formula

    if isinstance(formula, And):
        new_conjuncts = []
        for c in formula.conjuncts:
            new_conjuncts.append(distribute_or_over_and(c))
        return And(*new_conjuncts)

    if isinstance(formula, Or):
        disjuncts = []
        for d in formula.disjuncts:
            disjuncts.append(distribute_or_over_and(d))

        for i in range(len(disjuncts)):
            if isinstance(disjuncts[i], And):
                and_node = disjuncts[i]

                others = []
                for j in range(len(disjuncts)):
                    if j != i:
                        others.append(disjuncts[j])

                new_conjuncts = []
                for c in and_node.conjuncts:
                    new_or_elements = []
                    for o in others:
                        new_or_elements.append(o)
                    new_or_elements.append(c)

                    new_or = Or(*new_or_elements)
                    new_conjuncts.append(distribute_or_over_and(new_or))

                return And(*new_conjuncts)

        return Or(*disjuncts)

    return formula
    # === END YOUR CODE ===


def flatten(formula: Formula) -> Formula:
    """
    Aplana conjunciones y disyunciones anidadas.

    Transformaciones:
        And(And(a, b), c) -> And(a, b, c)
        Or(Or(a, b), c)   -> Or(a, b, c)

    Debe aplicarse recursivamente.

    Ejemplo:
        >>> flatten(And(And(Atom('a'), Atom('b')), Atom('c')))
        And(Atom('a'), Atom('b'), Atom('c'))
        >>> flatten(Or(Or(Atom('a'), Atom('b')), Atom('c')))
        Or(Atom('a'), Atom('b'), Atom('c'))

    Hint: Para un And, recorre cada hijo. Si un hijo tambien es And,
          agrega sus conjuncts directamente en vez de agregar el And.
          Igual para Or con sus disjuncts.
          Si al final solo queda 1 elemento, retornalo directamente.
    """
    # === YOUR CODE HERE ===
    if isinstance(formula, Atom) or isinstance(formula, Not):
        return formula

    if isinstance(formula, And):
        new_conjuncts = []
        for c in formula.conjuncts:
            c = flatten(c)
            if isinstance(c, And):
                new_conjuncts.extend(c.conjuncts)
            else:
                new_conjuncts.append(c)

        if len(new_conjuncts) == 1:
            return new_conjuncts[0]

        return And(*new_conjuncts)

    if isinstance(formula, Or):
        new_disjuncts = []
        for d in formula.disjuncts:
            d = flatten(d)
            if isinstance(d, Or):
                new_disjuncts.extend(d.disjuncts)
            else:
                new_disjuncts.append(d)

        if len(new_disjuncts) == 1:
            return new_disjuncts[0]

        return Or(*new_disjuncts)

    return formula
    # === END YOUR CODE ===


# --- PIPELINE COMPLETO ---


def to_cnf(formula: Formula) -> Formula:
    """
    [DADO] Pipeline completo de conversion a CNF.

    Aplica todas las transformaciones en el orden correcto:
    1. Eliminar bicondicionales (Iff)
    2. Eliminar implicaciones (Implies)
    3. Mover negaciones hacia adentro (Not)
    4. Eliminar dobles negaciones (Not Not)
    5. Distribuir Or sobre And
    6. Aplanar conjunciones/disyunciones

    Ejemplo:
        >>> to_cnf(Implies(Atom('p'), And(Atom('q'), Atom('r'))))
        And(Or(Not(Atom('p')), Atom('q')), Or(Not(Atom('p')), Atom('r')))
    """
    formula = eliminate_iff(formula)
    formula = eliminate_implication(formula)
    formula = push_negation_inward(formula)
    formula = eliminate_double_negation(formula)
    formula = distribute_or_over_and(formula)
    formula = flatten(formula)
    return formula

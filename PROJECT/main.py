from pysmt.shortcuts import Symbol, LE, GE, Int, And, Equals, Plus, Solver, is_sat,Not, get_model
from pysmt.typing import INT

def process():
    varA = Symbol("A")
    varB = Symbol("B")
    f = And(varA, Not(varB))
    print(f)
    print(is_sat(f))

    hello = [Symbol(s, INT) for s in "hello"]
    world = [Symbol(s, INT) for s in "world"]

    letters = set(hello + world)

    domains = And(And(LE(Int(1), l),
                      GE(Int(10), l)) for l in letters)
    print(domains,'domain')
    sum_hello = Plus(hello)
    sum_world = Plus(world)

    problem = And(Equals(sum_hello, sum_world),
                  Equals(sum_hello, Int(36)))

    formula = And(domains, problem)

    print("Serialization of the formula:")
    print(formula)
    print(formula.serialize())
    print(is_sat(formula))
    print(get_model(formula))

if __name__ == '__main__':
    process()
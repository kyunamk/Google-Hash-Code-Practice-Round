from index import Input, Delivery, Output, wrap_solution
from typing import *

file_a = './a_example'
file_b = './b_little_bit_of_everything.in'
file_c = './c_many_ingredients.in'
file_d = './d_many_pizzas.in'
file_e = './e_many_teams.in'

@wrap_solution(file_d)
def first_solution(obj: Input) -> Output:
    deliveries: List[Delivery] = [] # contains list of pizza list where the pizza are specified by an int.
    unavail_pizzas: Set[int] = set()
    max_team: int = 4
    teams: Dict[int:int] = obj.teams.copy()
    tot_pizzas = obj.total_pizzas
    total_ingredients: Set[str] = set()


    int_top={}
    pizzas=[]
    toppings: Set[int] = set()

    for id_pizza, pizza in enumerate(obj.pizzas):
        p: Set[int] = set()
        for t in pizza:
            if not t in int_top:
                int_top[t]=len(int_top)
            p.add(int_top[t])

        toppings.update(p)
        pizzas+=[(len(p),id_pizza,p)]
    pizzas.sort(key=lambda a:a[0],reverse=True)
    # print(pizzas)
    max_top=len(int_top)
    print(max_top)
    r=0
    while max_team > 0:
        # Select largest team that can be served
        if tot_pizzas >= 4 and teams[4] > 0:
            max_team = 4
        elif tot_pizzas >= 3 and teams[3] > 0:
            max_team = 3
        elif tot_pizzas >= 2 and teams[2] > 0:
            max_team = 2
        else:
            max_team = -1

        # No team can be served --> no delivery / no further choice
        if max_team < 0:
            break

        teams[max_team] -= 1

        # Until there aren't enough pizzas for everyone in the team
        current_pizza: List[int] = []
        current_ingredients: Set[str] = set()
        while len(current_pizza) < max_team: 
            best_pizza_id = -1
            best_pizza = set()
            max_ingredients = -1

            # Find the most stacked out pizza
            for z,_pizza in enumerate(pizzas):
                if _pizza[0]<=max_ingredients:
                    break
                id_pizza=_pizza[1]
                pizza=_pizza[2]

                # Most different ingredients
                diff_ingredients: int = len(pizza.difference(current_ingredients))
                if diff_ingredients >= max_ingredients:
                    ID=z
                    best_pizza_id = id_pizza
                    best_pizza = pizza
                    max_ingredients = diff_ingredients

            # Update remaining pizzas
            tot_pizzas -= 1
            del pizzas[ID]#=(True,best_pizza_id,best_pizza)
            unavail_pizzas.add(best_pizza_id)
            current_pizza.append(best_pizza_id)
            current_ingredients = current_ingredients.union(best_pizza)
            total_ingredients = total_ingredients.union(best_pizza)

        d: Delivery = Delivery(len(current_pizza), current_pizza)
        deliveries.append(d)

        r+=len(current_ingredients)**2
        print(r, len(current_ingredients))
    print(len(total_ingredients),r )
    return Output(deliveries)


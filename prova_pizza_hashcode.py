from index import Input, Delivery, Output, wrap_solution
from typing import *

file_a = './a_example'
file_b = './b_little_bit_of_everything.in'
file_c = './c_many_ingredients.in'
file_d = './d_many_pizzas.in'
file_e = './e_many_teams.in'
import sys
@wrap_solution(sys.argv[1])
def first_solution(obj: Input) -> Output:
    deliveries: List[Delivery] = [] # contains list of pizza list where the pizza are specified by an int.
    max_team: int = 4
    teams: Dict[int:int] = obj.teams.copy()
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
    keys=[r[0]for r in reversed(pizzas)]
    # print(pizzas)
    max_top=len(int_top)
    print(max_top)
    r=0
    sorted_by_team = [4,3,2] #if sum([i*c for i,c in enumerate(teams)])<len(pizzas) else [2,3,4]
    while max_team > 0:
        # Select largest team that can be served
        max_team=-1
        for t in sorted_by_team:
            #sorted([2,3,4],key=lambda a:teams[a],reverse=True):
            if len(pizzas)>=t and teams[t]>0:max_team=t;break

        # No team can be served --> no delivery / no further choice
        if max_team < 0:
            break

        # Until there aren't enough pizzas for everyone in the team
        current_pizza: List[int] = []
        current_ingredients: Set[str] = set()
        remain_max=sum(l[0] for l in pizzas[:max_team])
        while len(current_pizza) < max_team: 
            best_pizza_id = -1
            best_pizza = set()
            max_ingredients = -1
            # Find the most stacked out pizza
            ID=0
            for z,_pizza in enumerate(pizzas):
                if _pizza[0]<max_ingredients or  pizzas[ID][0]<_pizza[0]:
                    break
                id_pizza=_pizza[1]
                pizza=_pizza[2]

                # Most different ingredients
                special=pizza.difference(current_ingredients)
                diff_ingredients: int = len(special)

                m_diff = diff_ingredients - max_ingredients
                if m_diff>0 or ( m_diff==0 and pizzas[ID][0]>=_pizza[0]):
                    ID=z
                    best_pizza_id = id_pizza
                    best_pizza = pizza
                    max_ingredients = diff_ingredients

            if max_ingredients==0:
                if len(current_pizza)>=2 and teams[len(current_pizza)]>0:
                    break
                ID=len(pizzas)-1
                bust_pizza_id=pizzas[ID][1]
                bust_pizza=pizzas[ID][2]
            # revsere searhc  to find same result with min length..
            if len(current_pizza):
                import bisect
                lst=bisect.bisect_left(keys,max_ingredients,ID)
                lst=len(pizzas)-lst
                # print("Search at here ", lst,z, keys[lst-1:lst+2],diff_ingredients)
                for Z,_p in enumerate(reversed(pizzas[z+1:lst])):
                    p=_p[2]
                    # print("Search _p : ",diff_max_ingredientsingredients,Z, _p[0])
                    if len(special.difference(p))==0:
                        # print("Search end ", keys[lst-2:lst+2],diff_ingredients,Z,keys[lst+Z-2:lst+Z+2])
                        if p.difference(current_ingredients) != special:
                            print("error",p,p.difference(current_ingredients),special)
                            # exit()
                        nZ=lst-1-Z
                        print(z,'-->',nZ,Z)
                        ID=nZ
                        best_pizza_id=_p[1]
                        best_pizza=p
                        max_ingredients=len(pizza.difference(current_ingredients))
                        break
            # Update remaining pizzas
            del pizzas[ID]#=(True,best_pizza_id,best_pizza)
            del keys[-ID-1]
            current_pizza.append(best_pizza_id)
            current_ingredients = current_ingredients.union(best_pizza)
            total_ingredients = total_ingredients.union(best_pizza)
            if len(current_ingredients)==max_top and len(current_pizza)>=2 and teams[len(current_pizza)]>0:
                break
        teams[len(current_pizza)] -= 1
        d: Delivery = Delivery(len(current_pizza), current_pizza)
        deliveries.append(d)

        r+=len(current_ingredients)**2
        print(r, len(current_ingredients),teams)
    print(len(deliveries),len(total_ingredients),r )
    return Output(deliveries)


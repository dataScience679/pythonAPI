#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pulp')


# In[1]:


import pulp
import timeit


# In[ ]:


from flask import Flask, jsonify,app

app = Flask(__name__)

@app.route('/solve_transport_problem', methods=['GET'])
def solve_transport_problem():
    import pulp
    import timeit

    start_time = timeit.default_timer()

    # We create the problem object. We define it as a minimization problem.
    transport_prob = pulp.LpProblem('Transport_Problem', pulp.LpMaximize)

    # Here we define the growth, that are constants in our problem.
    growth_usa = 0.1
    growth_uk = 0.1
    growth_germany = 0.1
    growth_india = 0.1
    growth_france = 0.1
    growth_ksa = 0.1
    growth_israel = 0.1
    growth_uae = 0.1
    growth_gcc = 0.1
    growth_russia =0.1
    growth_world = 0.1
    growth_china = 0.1
    # Here we define the offers and demands, that are constants in our problem.
    impression_usa = 75754358
    impression_uk = 70965631
    impression_germany = 93648476
    impression_india = 443656400
    impression_france = 89833471
    impression_ksa = 140527084
    impression_israel = 84944832
    impression_uae = 92011637
    impression_gcc = 41687147
    impression_russia = 35437563
    impression_world = 7840580
    impression_china = 147543403
    total_impression = 1316160921



    new_impression_usa = (1 + growth_usa) * impression_usa
    new_impression_uk = (1 + growth_uk) * impression_uk
    new_impression_germany = (1 + growth_germany) * impression_germany
    new_impression_india = (1 + growth_india) * impression_india
    new_impression_france = (1 + growth_france) * impression_france
    new_impression_ksa = (1 + growth_ksa) * impression_ksa
    new_impression_israel = (1 + growth_israel) * impression_israel
    new_impression_uae = (1 + growth_uae) * impression_uae
    new_impression_gcc = (1 + growth_gcc) * impression_gcc
    new_impression_russia = (1 + growth_russia) * impression_russia
    new_impression_world = (1 + growth_world) * impression_world
    new_impression_china = (1 + growth_china) * impression_china



    # Here we define the variables. Every Xij for the three warehouses and the three stores.
    usa_budget = pulp.LpVariable("USA_budget", lowBound=0)
    uk_budget = pulp.LpVariable("UK_budget", lowBound=0)
    germany_budget = pulp.LpVariable("Germany_budget", lowBound=0)
    india_budget = pulp.LpVariable("India_budget", lowBound=0)
    france_budget = pulp.LpVariable("France_budget", lowBound=0)
    ksa_budget = pulp.LpVariable("KSA_budget", lowBound=0)
    israel_budget = pulp.LpVariable("Israel_budget", lowBound=0)
    uae_budget = pulp.LpVariable("UAE_budget", lowBound=0)
    gcc_budget = pulp.LpVariable("GCC_budget", lowBound=0)
    russia_budget = pulp.LpVariable("Russia_budget", lowBound=0)
    world_budget = pulp.LpVariable("World_budget", lowBound=0)
    china_budget = pulp.LpVariable("China_budget", lowBound=0)

    cpi_values = [0.00767147, 0.00605734, 0.00515035, 0.00097625, 0.00427715, 0.00262566,
                  0.00416926, 0.00292072, 0.00131023, 0.00991607, 0.00481406, 0.00234354]

    reciprocal_cpi_values = [int(1 / cpi) for cpi in cpi_values]

    # Target function. We want to minimize the sum of the costs.
    transport_prob += (usa_budget * reciprocal_cpi_values[0]) + \
                      (uk_budget * reciprocal_cpi_values[1]) + \
                      (germany_budget * reciprocal_cpi_values[2]) + \
                      (india_budget * reciprocal_cpi_values[3]) + \
                      (france_budget * reciprocal_cpi_values[4]) + \
                      (ksa_budget * reciprocal_cpi_values[5]) + \
                      (israel_budget * reciprocal_cpi_values[6]) + \
                      (uae_budget * reciprocal_cpi_values[7]) + \
                      (gcc_budget * reciprocal_cpi_values[8]) + \
                      (russia_budget * reciprocal_cpi_values[9]) + \
                      (world_budget * reciprocal_cpi_values[10]) + \
                      (china_budget * reciprocal_cpi_values[11])

    # Restrictions:
    transport_prob += usa_budget + uk_budget + germany_budget + india_budget + france_budget + \
                      ksa_budget + israel_budget + uae_budget + gcc_budget + russia_budget + \
                      world_budget + china_budget <= 1.2*4092100  # Specify total_budget

    transport_prob += usa_budget * reciprocal_cpi_values[0] >= new_impression_usa
    transport_prob += uk_budget * reciprocal_cpi_values[1] >= new_impression_uk
    transport_prob += germany_budget * reciprocal_cpi_values[2] >= new_impression_germany
    transport_prob += india_budget * reciprocal_cpi_values[3] >= new_impression_india
    transport_prob += france_budget * reciprocal_cpi_values[4] >= new_impression_france
    transport_prob += ksa_budget * reciprocal_cpi_values[5] >= new_impression_ksa
    transport_prob += israel_budget * reciprocal_cpi_values[6] >= new_impression_israel
    transport_prob += uae_budget * reciprocal_cpi_values[7] >= new_impression_uae
    transport_prob += gcc_budget * reciprocal_cpi_values[8] >= new_impression_gcc
    transport_prob += russia_budget * reciprocal_cpi_values[9] >= new_impression_russia
    transport_prob += world_budget * reciprocal_cpi_values[10] >= new_impression_world
    transport_prob += china_budget * reciprocal_cpi_values[11] >= new_impression_china

    # Solve the Transport Problem
    solution = transport_prob.solve()

    # Extract results
    results = {
        "usa_budget": pulp.value(usa_budget),
        "uk_budget": pulp.value(uk_budget),
        "germany_budget": pulp.value(germany_budget),
        "india_budget": pulp.value(india_budget),
        "france_budget": pulp.value(france_budget),
        "ksa_budget": pulp.value(ksa_budget),
        "israel_budget": pulp.value(israel_budget),
        "uae_budget": pulp.value(uae_budget),
        "gcc_budget": pulp.value(gcc_budget),
        "russia_budget": pulp.value(russia_budget),
        "world_budget": pulp.value(world_budget),
        "china_budget": pulp.value(china_budget),
        "max_impressions_billion": pulp.value(transport_prob.objective) * 1e-9,
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port='8080', use_reloader=False)



# In[ ]:





import clips
from clips import Environment
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Stworzenie środowiska CLIPS
env = Environment()

# Definicja faktów binarnych
env.build('(deffacts binary-facts (customer-age young) (has-discount true))')

# Definicja rozmytych zmiennych wejściowych i wyjściowych
temperature = ctrl.Antecedent(np.arange(0, 101, 1), 'temperature')
satisfaction = ctrl.Consequent(np.arange(0, 101, 1), 'satisfaction')

# Definicja zbiorów rozmytych
temperature.automf(3, names=['cold', 'medium', 'hot'])
satisfaction.automf(3, names=['low', 'medium', 'high'])

# Definicja reguł
rule1 = ctrl.Rule(temperature['cold'], satisfaction['low'])
rule2 = ctrl.Rule(temperature['medium'], satisfaction['medium'])
rule3 = ctrl.Rule(temperature['hot'], satisfaction['high'])

# Tworzenie systemu kontrolnego i symulacji
satisfaction_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
satisfaction_sim = ctrl.ControlSystemSimulation(satisfaction_ctrl)

# Pobranie faktów z bazy
age_fact = env.find_fact('customer-age')
has_discount_fact = env.find_fact('has-discount')

# Przykładowe wartości dla wejść
temperature_input = 45

# Symulacja logiki rozmytej
satisfaction_sim.input['temperature'] = temperature_input
satisfaction_sim.compute()
satisfaction_output = satisfaction_sim.output['satisfaction']

# Dodawanie faktów do środowiska CLIPS
env.assert_string(f'(temperature {temperature_input})')
env.assert_string(f'(satisfaction {satisfaction_output})')

# Definicja reguł w CLIPS
env.build("""
(defrule recommend-product
    (customer-age young)
    (has-discount true)
    (temperature ?t&:(> ?t 30))
    (satisfaction ?s&:(> ?s 50))
=>
    (assert (recommended-product "summer-special")))
""")

# Uruchomienie CLIPS
env.run()

# Sprawdzenie, czy produkt został zarekomendowany
recommended_product = env.find_fact('recommended-product')
if recommended_product:
    product_name = recommended_product.slot_value('product').value()
    print(f'Recommended product: {product_name}')
else:
    print('No product recommended.')

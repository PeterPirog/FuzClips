import subprocess
import re

class ExpertSystem:
    def __init__(self, clips_path=r"C:\Program Files\CLIPS 6.4\CLIPSDOS.exe", show_stdout=False):
        self.clips_interface = CLIPSInterface(clips_path)
        self.show_stdout = show_stdout
        self.facts = []
        self.rules = []

    def add_fact(self, fact_name, value):
        self.facts.append((fact_name, value))

    def add_rule(self, rule_name, condition, action):
        self.rules.append((rule_name, condition, action))

    def run(self):
        input_data = "(deffacts initial-facts\n"
        for fact_name, value in self.facts:
            input_data += f"    ({fact_name} {value})\n"
        input_data += ")\n"

        for rule_name, condition, action in self.rules:
            input_data += f"(defrule {rule_name}\n"
            input_data += f"    {condition}\n"
            input_data += f"    =>\n"
            input_data += f"    {action}\n"
            input_data += ")\n"

        input_data += "(reset)\n(run)\n(facts)\n(exit)\n"

        result = self.clips_interface.run(input_data)

        if self.show_stdout:
            print("Wynik:")
            print(result)

        facts_list = extract_facts(result)
        return facts_list

def extract_facts(result):
    facts_pattern = re.compile(r'f-\d+\s*\((.+?)\)')
    facts = facts_pattern.findall(result)

    # Wyciąganie nazwy faktu i przekształcanie w listę
    facts_list = [fact for fact in facts]
    return facts_list

class CLIPSInterface:
    def __init__(self, executable_path):
        self.executable_path = executable_path

    def run(self, input_data):
        command = [self.executable_path]
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        stdout, stderr = process.communicate(input=input_data)

        return stdout

# Tworzenie instancji ExpertSystem
expert_system = ExpertSystem(show_stdout=True)

# Dodawanie faktów
expert_system.add_fact("is-raining", "true")

# Dodawanie reguł
expert_system.add_rule("take-umbrella", "(is-raining true)", "(assert (take-umbrella true))")
expert_system.add_rule("dont-take-umbrella", "(is-raining false)", "(assert (take-umbrella false))")

# Uruchamianie systemu eksperckiego
result_facts = expert_system.run()

# Wypisanie wywnioskowanych faktów
print("Wywnioskowane fakty:")
print(result_facts)

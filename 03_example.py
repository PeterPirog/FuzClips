import subprocess
import re

class ExpertSystem:
    def __init__(self, clips_path=r"C:\Program Files\CLIPS 6.4\CLIPSDOS.exe", show_stdout=False):
        self.clips_interface = CLIPSInterface(clips_path)
        self.show_stdout = show_stdout
        self.facts = []
        self.rules = []

    def add_fact(self, fact):
        self.facts.append(fact)

    def add_rule(self, rule_name, conditions, conclusions):
        self.rules.append((rule_name, conditions, conclusions))

    def generate_input_data(self):
        input_data = "(deffacts initial-facts\n"
        for fact in self.facts:
            input_data += f"    ({fact})\n"
        input_data += ")\n"

        for rule_name, conditions, conclusions in self.rules:
            input_data += f"(defrule {rule_name}\n"
            for condition in conditions:
                input_data += f"    ({condition})\n"
            input_data += "    =>\n"
            for conclusion in conclusions:
                input_data += f"    (assert ({conclusion}))\n"
            input_data += ")\n"

        input_data += "(reset)\n(run)\n(facts)\n(exit)\n"
        return input_data

    def run_clips(self, input_data):
        return self.clips_interface.run(input_data)

    def run(self):
        input_data = self.generate_input_data()

        result = self.run_clips(input_data)

        if self.show_stdout:
            print("Wynik:")
            print(result)

        facts_list = extract_facts(result)
        activated_rules = self.get_activated_rules(result)
        return facts_list, activated_rules

    def get_activated_rules(self, stdout):
        activated_rules_pattern = re.compile(r'==> Activation: (\w+)')
        activated_rules = activated_rules_pattern.findall(stdout)
        return activated_rules

def extract_facts(result):
    facts_pattern = re.compile(r'f-\d+\s*\((.+?)\)')
    facts = facts_pattern.findall(result)
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
expert_system.add_fact("is-raining true")
expert_system.add_fact("has-umbrella false")

# Dodawanie reguł
expert_system.add_rule("take-umbrella", ["is-raining true", "has-umbrella false"], ["take-umbrella true", "take-sunglasses false"])

# Uruchamianie systemu eksperckiego
result_facts, activated_rules = expert_system.run()

# Wypisanie wywnioskowanych faktów
print("Wywnioskowane fakty:")
print(result_facts)

# Wypisanie aktywowanych reguł
print("Aktywowane reguły:")
print(activated_rules)

import subprocess
import re

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

# Tworzenie interfejsu CLIPS
clips = CLIPSInterface(r"C:\Program Files\CLIPS 6.4\CLIPSDOS.exe")  # Dodaj 'r' przed ścieżką, aby uniknąć problemów z ukośnikami

# Przykładowe dane wejściowe
input_data = '''
(deffacts initial-facts
    (is-raining true))

(defrule take-umbrella
    (is-raining true)
    =>
    (assert (take-umbrella true)))

(defrule dont-take-umbrella
    (is-raining false)
    =>
    (assert (take-umbrella false)))

(reset)
(run)
(facts)
(exit)
'''

# Uruchamianie CLIPS z danymi wejściowymi
result = clips.run(input_data)

# Wypisanie wyników
print("Wynik:")
print(result)

# Wyciąganie faków z wyników
facts_list = extract_facts(result)
print("Wywnioskowane fakty:")
print(facts_list)

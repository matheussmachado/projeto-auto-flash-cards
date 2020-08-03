#!venv/bin/python3

from src.scales.scale3 import automaton

if __name__ == "__main__":
    automaton.run_task()
    if len(automaton.card_list) == 0:
        print('No cards to create.')
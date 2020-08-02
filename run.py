#!venv/bin/python3

from src.scales.scale3 import ac

if __name__ == "__main__":
    ac.run_task()
    if len(ac.card_list) == 0:
        print('No cards to create.')
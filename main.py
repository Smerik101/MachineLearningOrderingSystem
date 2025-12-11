from stocktake import open_stocktake
from ordering import open_ordering
from appstate import AppState
import sys
from preprocessing import pre_processing
from modeltraining import model_training

state = AppState()

def main(state):

    while True:
        entry = int(
            input("Please select action (0=quit, 1=stocktake, 2=ordering)"))
        if entry == 0:
            sys.exit()
        if entry == 1:
            open_stocktake(state)
        if entry == 2:
            open_ordering(state)
        else:
            print("Invalid entry, try again")

pre_processing(state)
model_training(state)
main(state)

import random
from model_interface import QueueLengthController

def intersection_plant(E, S, phase, MAX_ADD=2, MAX_REMOVE=2):
    """
    very simple plant model  that adds or removes random number of
    cars depending on the phase
    phase == 0 => green East-West
    phase == 1 => green North-South
    """
    if phase == 0:
        dE = random.randint(-MAX_REMOVE, 0)
        dS = random.randint(0, MAX_ADD)
    else:
        dE = random.randint(0, MAX_ADD)
        dS = random.randint(-MAX_REMOVE, 0)
    E += dE
    S += dS

    # clamp to [0, Inf]
    E = max(0, E)
    S = max(0, S)

    return E, S

if __name__ == "__main__":
    # initial plant state
    E = 0
    S = 0
    phase = 0

    templatePath = "uppaal/model_template.xml"
    verifytaPath = "$HOME/Documents/stratego/bin/bin-Linux/verifyta"
    controller = QueueLengthController(templatePath)
    
    L = 20 # simulation length
    K = 2  # every K we will do MPC
    cost = 0
    for k in range(L):
        # run plant
        E, S = intersection_plant(E, S, phase)
        cost += E * E + S * S
        # report
        print("Step: {}, E: {} cars, S: {} cars, cost: {}".format(k, E, S, cost))

        if k % K == 0:
            # at each MPC step we want a clean template copy
            # to insert variables
            controller.init_simfile()
            
            # insert current state into simulation template
            state = [E, S]
            controller.insert_state(state)

            # run a verifyta querry
            nextPhase, duration = controller.run(verifytaPath=verifytaPath)
        
            print("  Decison: phases {} to {} for {}s".format(phase, nextPhase, duration))
            phase = nextPhase
        
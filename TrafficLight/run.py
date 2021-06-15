import random
import argparse
import os

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

def run(template_file, query_file, verifyta_path):
    MIN_GREEN = 4

    controller = QueueLengthController(
        templatefile=template_file,
        state_names=["E", "S", "phase"])

    # initial plant state
    E = 0
    S = 0
    phase = 0
    cost = 0

    L = 30 # simulation length
    K = 4  # every K we will do MPC

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
            state = {
                "E": E,
                "S": S,
                "phase": phase
            }
            controller.insert_state(state)

            # to debug errors from verifyta one can save intermediate simulation file
            # controller.debug_copy(templatePath.replace(".xml", "_debug.xml"))

            # run a verifyta querry to simulate optimal strategy
            durations, phase_seq = controller.run(
                queryfile=query_file,
                verifyta_path=verifyta_path)

            # switch phases if optimal solution changes phase
            # after minimum green time, stay otherwise
            next_duration, next_phase = durations[0], phase_seq[0]
            if next_duration == MIN_GREEN and len(phase_seq) > 1:
                next_duration, next_phase = durations[1], phase_seq[1]

            print("  Decison: phases {} to {} for {}s".format(
                phase, next_phase, next_duration))
            phase = next_phase

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--template-file", default="uppaal/model_template.xml", 
        help="Path to Stratego .xml file model template")
    ap.add_argument("-q", "--query-file", default="uppaal/query.q",
        help="Path to Stratego .q query file")
    ap.add_argument("-v", "--verifyta-path", default="verifyta", help=
        "Path to verifyta executable")
    args = ap.parse_args()

    base_path = os.path.dirname(os.path.realpath(__file__)) 
    template_file = os.path.join(base_path, args.template_file)
    query_file = os.path.join(base_path, args.query_file)

    run(template_file, query_file, args.verifyta_path)
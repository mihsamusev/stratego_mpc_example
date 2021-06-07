import os
import argparse

import yaml

import strategoutil as sutil



class MPCSetupRoomHeating(sutil.MPCsetup):
    # Overriding parent method.
    def create_query_file(self, horizon, period, final):
        """
        Create the query file for each step of the room heating model. Current
        content will be overwritten.
        """
        with open(self.queryfile, "w") as f:
            line1 = "strategy opt = minE (D) [<={}*{}]: <> (t=={})\n"
            f.write(line1.format(horizon, period, final))
            f.write("\n")
            line2 = "simulate 1 [<={}+1] {{ {} }} under opt\n"
            f.write(line2.format(period, self.controller.print_var_names()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--template-file", default="heatedroom-online.xml", 
        help="Path to Stratego .xml file model template")
    ap.add_argument("-q", "--query-file", default="heatedroom-online_query.q",
        help="Path to Stratego .q query file")
    ap.add_argument("-m", "--model-config", default="model_config.yaml",
        help="Path to .yml model variables and initial conditions")
    ap.add_argument("-l", "--learning-args", default="verifyta_config.yaml",
        help="Path to .yml verifyta learining arguments")
    ap.add_argument("-v", "--verifyta-path", default="verifyta", 
        help="Path to verifyta executable")
    args = ap.parse_args()

    # Define location of the relevant files and commands.
    base_path = os.path.dirname(os.path.realpath(__file__)) 
    modelTemplatePath = os.path.join(base_path, args.template_file)
    queryFilePath = os.path.join(base_path, args.query_file)
    modelConfigPath = os.path.join(base_path, args.model_config)
    learningConfigPath = os.path.join(base_path, args.learning_args)
    verifytaCommand = args.verifyta_path
    # "/home/trafiklab/uppaal/stratego8_8/bin-Linux/verifyta"

    # Whether to run in debug mode.
    debug = True

    # Get model and learning config dictionaries from files.
    with open(modelConfigPath, "r") as yamlfile:
        model_cfg_dict = yaml.safe_load(yamlfile)
    with open(learningConfigPath, "r") as yamlfile:
        learning_cfg_dict = yaml.safe_load(yamlfile)
    
    # Construct the MPC object.
    controller = MPCSetupRoomHeating(modelTemplatePath, queryfile=queryFilePath,
                                     model_cfg_dict=model_cfg_dict,
                                     learning_args=learning_cfg_dict,
                                     verifytacommand=verifytaCommand, debug=debug, interactive_bash=False)
    
    # Define the MPC parameters.
    period = 15  # Period in time units (minutes).
    horizon = 5  # How many periods to compute strategy for.
    duration = 96  # Duration of experiment in periods.

    controller.run(period, horizon, duration)

import strategoutil as sutil
import yaml


class MPCSetupRoomHeating(sutil.MPCsetup):
    # Overriding parent method.
    def create_query_file(self, queryfile, horizon, period, final, controller):
        """
        Create the query file for each step of the room heating model. Current
        content will be overwritten.
        """
        with open(queryfile, "w") as f:
            line1 = "strategy opt = minE (D) [<={}*{}]: <> (t=={})\n"
            f.write(line1.format(horizon, period, final))
            f.write("\n")
            line2 = "simulate 1 [<={}+1] {{ {} }} under opt\n"
            f.write(line2.format(period, controller.print_var_names()))


if __name__ == "__main__":
    # Define location of the relevant files and commands.
    modelTemplatePath = "heatedroom-online.xml"
    queryFilePath = "heatedroom-online_query.q"
    modelConfigPath = "model_config.yaml"
    learningConfigPath = "verifyta_config.yaml"
    verifytaCommand = "verifyta-stratego-8-7"

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
                                     verifytacommand=verifytaCommand, debug=debug)
    
    # Define the MPC parameters.
    period = 15  # Period in time units (minutes).
    horizon = 5  # How many periods to compute strategy for.
    duration = 96  # Duration of experiment in periods.

    controller.run(period, horizon, duration)

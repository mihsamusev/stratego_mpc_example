import strategoutils
from strategoutils import StrategoController

class QueueLengthController(StrategoController):
    def __init__(self, templatefile):
        super().__init__(templatefile)
        # variables to insert into the simulation *.xml file
        self.stateNames = ["E", "S", "phase"]
         # tag left in model_template.xml
        self.tagRule = "//TAG_{}"

    def insert_state(self, stateValues):
        """
        Uses tag rule to insert state values of [E, S, phase]
        at the appropriate position in the simulation *.xml file
        """
        for name, value in zip(self.stateNames, stateValues):
            tag = self.tagRule.format(name)
            strategoutils.insert_to_model(self.simulationfile,
                tag, str(value))
    
    def run(self, queryfile=None, configfile=None, verifytaPath="verifyta"):
        """
        Builds on top of base class run() function, and does
        post-process verifyta result log to output
        first action and its duration
        """
        resultlog = super().run(queryfile, configfile, verifytaPath)

        tpls = strategoutils.get_output_tuples(resultlog)
        durations_phases = strategoutils.split_duration_action(tpls[0])
        return durations_phases

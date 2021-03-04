from shutil import copyfile
from subprocess import Popen, PIPE
import re
import yaml

def array_to_stratego(arr):
    """converts python array string to C style array
    used in UPPAAL Stratego, 
    NB, does not include ';' in the end!
    """
    arrstr = str(arr)
    arrstr = str.replace(arrstr, "[", "{", 1)
    arrstr = str.replace(arrstr, "]", "}", 1)
    return arrstr

def stratego_to_tuple_list(text):
    """converts stratego simulation output to list of  tuples
    (int, int)
    """
    stringTuples = re.findall(r"\((\d+),(\d+)\)", text)
    intTuples = [(int(t[0]), int(t[1])) for t in stringTuples]
    return intTuples

def insert_to_model(modelfile, tag, inserted):
    """Replaces tag in modelfile by the desired text"""
    with open(modelfile, "r+") as f:
        modeltext = f.read()
        text = modeltext.replace(tag, inserted, 1)
        f.seek(0)
        f.write(text)
        f.truncate()

def get_first_action_duration(tuples, MAX_DURATION=9000):
    """
    get first action and its duration from stratego simulation output
    NB
    naive and doesnt, acount for value getting to zero and back in 0 time
    """
    action = tuples[0][1]
    duration = MAX_DURATION
       
    if len(tuples) == 2:
        action = tuples[1][1]
    elif len(tuples) >= 3:
        if tuples[1][0] != tuples[0][0]:
            action = tuples[0][1]
            duration = tuples[1][0] - tuples[0][0]  
        else:
            action = tuples[1][1]
            duration = tuples[2][0] - tuples[1][0] 

    return action, duration
    
def get_output_tuples(text):
    """
    Assumption that both time and phase are integers and reported
    by verifyta simulate as tuples (time, phase)
    """
    groups = re.findall(r"\[\d+\]:\s((?:\(\d+,\d+\)\s?)+)",text)
    tupleList = []
    for g in groups:
        tupleList.append(stratego_to_tuple_list(g))
    return tupleList

def merge_verifyta_args(configfile):
    """Concatenates and formats a string of verifyta
    arguments given by the .yaml configuration file"""
    args = ""
    with open(configfile, "r") as yamlfile:
        cfg = yaml.safe_load(yamlfile)
        for k, v in cfg.items():
            args += " --" + k + " " + str(v)
    return args

def list_verifyta_args(configfile):
    """Concatenates and formats a string of verifyta
    arguments given by the .yaml configuration file"""
    args = []
    with open(configfile, "r") as yamlfile:
        cfg = yaml.safe_load(yamlfile)
        for k, v in cfg.items():
            args.append("--" + k)
            args.append(str(v))
    return args

def run_stratego(modelfile, queryfile=None, configfile=None, verifytaPath="verifyta"):
    """
    Usage: verifyta.bin [OPTION]... MODEL QUERY
    modelfile .xml
    query .q
    configfile .yaml with entries of the same format as verifyta arguments
    """
    args = ""
    if configfile is not None:
        args = merge_verifyta_args(configfile)
    
    if queryfile is None:
        queryfile = ""

    task = " ".join([verifytaPath, args, modelfile, queryfile])
    
    process = Popen(task, shell=True,stdout=PIPE)
    output, error = process.communicate()
    
    return output.decode("utf-8")

class StrategoController:
    """
    Abstract controller class to interface with UPPAAL Stratego 
    through python
    """
    def __init__(self, templatefile):
        self.templatefile = templatefile
        self.simulationfile = templatefile.strip(".xml") + "_sim.xml"

    def init_simfile(self):
        """
        Make a copy of a template file where data of
        specific variables is inserted
        """
        copyfile(self.templatefile, self.simulationfile)

    def debug_copy(self, debugFilename):
        """
        copy UPPAAL simulationfile.xml file for manual
        debug in Stratego
        """
        copyfile(self.simulationfile, debugFilename)

    def insert_state(self):
        """
        insert  
        """
        pass

    def run(self, queryfile=None, configfile=None, verifytaPath="verifyta"):
        """
        runs verifyta with requested querries and parameters
        that are either part of the *.xml model file or explicitly
        specified  
        """
        output = run_stratego(self.simulationfile, queryfile,
            configfile, verifytaPath)
        return output
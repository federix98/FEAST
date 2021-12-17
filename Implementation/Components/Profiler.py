import time
import sys
import cProfile, pstats, io
from pstats import SortKey

class Profiler():

    def __init__(self, CPUFile = ""):
        print("Constructing profiler")
        self.pr = cProfile.Profile()
        self.folder = "perf_data/"
        self.timestr = ""#time.strftime("%Y%m%d-%H%M%S")
        # Construct

    def start_CPU_Profile(self):
        # ------------ START PROFILING -------------
        self.pr.enable()
        # ------------------------------------------

    def end_CPU_Profile(self, CPUFile, verbose=0):
        self.pr.disable()

        # HARD CODED LOGIC TO GET CUMTIME
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(self.pr, stream=s).sort_stats(sortby)
        ps.print_stats(1)
        if verbose:
            print("_______________________________")
            print(s.getvalue())
        ps.print_stats()
        lst = s.getvalue().split("\n")
        val_index = lst.index([s for s in lst if "cumtime" in s][0]) + 1
        cumtime = lst[val_index].split("    ")[-2]
        if(str(cumtime) == '' or  " " in str(cumtime)):
            if verbose:
                print("INVALID CUMTIME ", str(cumtime), lst)
            cumtime = 0

        text_file = open(CPUFile, "a")
        text_file.write(str(cumtime) + ";")
        text_file.close()

    def start_RT_Profile(self):
        self.t0 = time.time()

    def end_RT_Profile(self, RTFile):
        self.t1 = time.time()
        text_file = open(RTFile, "a")
        text_file.write(str(self.t1-self.t0) + ";")
        text_file.close()

    def start_All_Profile(self):
        self.pr = cProfile.Profile()
        self.start_CPU_Profile()
        self.start_RT_Profile()

    def end_All_Profile(self, RTFile, CPUFile):
        self.end_CPU_Profile(self.folder + self.timestr + str(CPUFile))
        self.end_RT_Profile(self.folder + self.timestr + str(RTFile))

    def reset(self, RTFile, CPUFile):
        CF = open(self.folder + self.timestr + str(CPUFile), "w")
        CF.close()
        RF = open(self.folder + self.timestr + str(RTFile), "w")
        RF.close()
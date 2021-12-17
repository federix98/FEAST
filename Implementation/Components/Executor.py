from Profiler import Profiler

class Executor():

    def __init__(self, planner_connector, out_file = "config.txt", verbose=0):
        self.planner_connector = planner_connector
        self.profiler = Profiler()
        self.profiler.reset("ExecutorRT_.txt", "ExecutorCPU_.txt")
        self.verbose = verbose
        self.out_file = out_file
        self.__start__()

    def __start__(self):
        self.planner_connector.connect()

        while True:
            
            #print("Executor is listening")

            kafka_flag = 0

            # Trick to speedup the Event Driven part
            if hasattr(self.planner_connector, 'tp') and self.planner_connector.tp == "Consumer":
                results = self.planner_connector.consumer
                #print("KafkaConnector detected")
                kafka_flag = 1
            else:
                #print("Socket or DB connector detected")
                results = self.planner_connector.receive()
                if not isinstance(results, list):
                    results = [results]

            for res in results:

                # ------------ START PROFILING -------------
                self.profiler.start_All_Profile()
                # ------------------------------------------

                if res == None:
                    break

                # EVENT DRIVEN SPEEDUP
                if kafka_flag:
                    res = str(res.value, 'utf-8')   

                if self.verbose:
                    print("results", res)

                # Write adaptation results to the file
                text_file = open(self.out_file, "w")
                text_file.write(res)
                text_file.close()

                # ------------ END PROFILING ---------------
                self.profiler.end_All_Profile("ExecutorRT_.txt", "ExecutorCPU_.txt")
                # ------------------------------------------


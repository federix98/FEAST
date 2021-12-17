# FEAST
> A Framework for Evaluating Implementation Architectures of Self-adaptive IoT Systems

This repository is the official implementation of ***FEAST**: A Framework for Evaluating ImplementationArchitectures of Self-adaptive IoT Systems* paper.

## Installation Requirements
1. Install the latest version of JAVA - https://www.java.com/en/download/
2. Install Apache Kafka - https://kafka.apache.org/quickstart
3. Install kafka-python - https://pypi.org/project/kafka-python/
4. Install Keras in Python *(Tested with version 2.2.4)* - https://keras.io
5. Install Tensorflow in Python *(Tested with version 1.15)* - https://www.tensorflow.org/install
6. Install Scikit-learn in Python *(Tested with version 0.22)* - https://scikit-learn.org/

## Project Description
**Implementation** is the folder that contains the implementation of the case study in the document and is organized as follows: 
- *Components*: contains all the basic components and connectors that the specific implementations use. It therefore contains all the basic code of each MAPE-K loop activity, of the various connectors and of the utility classes necessary for the experiment.
- *Layered*: this folder contains the components of the MAPE loop, the CupCarbon sample project and the Machine Learning models of the Layered Implementation (*Socket based strategy*).
- *BB*: this folder contains the components of the MAPE loop, the CupCarbon sample project and the Machine Learning models of the Blackboard Implementation (*Centralized strategy*).
- *EventDriven*: this folder contains the components of the MAPE loop, the CupCarbon sample project and the Machine Learning models of the Event Driven Implementation (*Publish Subscribe based strategy*).
- *results* and *STATS* folders contain some organized results obtained by performing the experiments.

**DataAnalyzer** folder contains all the code that has been developed for the purposes of the analysis and evaluation phase of the framework. In particular, it has the following organization:
- *24h* folder: results obtained by the simulation of the system performed on **Scenario 1** 
- *2h* folder: results obtained by the simulation of the system performed on **Scenario 2** *(see the paper for details of scenarios)*
- *DataLoader.py*: this class contains all the functions able to load the data from the files and generate runtime data structures. This class contains the utility application statement too.
- *UtilityAnalizer.py*: class which contains all the functions to make the analysis and the evaluation
- *evaluation.py*: class to launch in order to perform the analysis and print the data. In this class we can set "RT\_Thresh" (threshold for response time) and "E\_Thresh" (threshold for energy consumption) parameters for the utility function.

**CupCarbon** folder contains the customized source code of CupCarbon to perform the experiment.

## Configuration
To be able to perform the experiments it is necessary to make some configurations first. 
- The communication of the components in the socket based strategy implementation was made through sockets. Please check the availability of the `65431`, `65432`, `65433` ports.
- The communication of the components in the centralized implementation was made through MySQL tables. Create those tables and edit the configuration data in the scripts *\Implementation\BB\BB_\*.py*. 
- The communication of the components in the publish subscriube based strategy implementation was made through Kafka producers and consumers. They use the following topics: *BatchDataTopic*, *CupCarbonEventsTopic*, *PlannerExecutorTopic*. Please create them before running the experiment.

## Running Experiment
To run properly the experiment please do:
- You have to start from the same configuration for each implementaiton, so edit the *config.txt* file so that it is the same for everyone before starting
- Set the verbose flag of each script to the same value (0 or 1) otherwise the response time will be measured differently between scripts
- Clean the MySQL tables if they contain old data
- In the */CupCarbon-master_4.0/src/senscript_functions/Functions.java* edit the ***myf*** function *filename* parameter putting the path of the file which you want to read the adaptation values (config.txt). Take care of putting the correct path for the running of each implementation.
- Launch the customized *CupCarbon* source code and load the NdR_CO project inside the correct implementation folder
- Change the *CupCarbon* parameters in order to put the correct execution scenario
- Launch the MAPE-K scripts of the correct implementaion but the *XX_Monitor.py* one. Make sure that the others are connected.
- Start the *CupCarbon* simulation
- Start the *XX_Monitor.py* script

Let *\_\_IMPLFLD\_\_* the folder of the chosen implementation (Layered, BB or EventDriven). 
The energy results will be in the *\_\_IMPLFLD\_\_\NdR_CO\results\wisen\_simulation.csv* file. 
The response time and CPU time results will be under *\_\_IMPLFLD\_\_\perf\_data* folder.

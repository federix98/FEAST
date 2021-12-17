# DataAnalyzer_MAPE-K_CS
 https://github.com/federix98/MAPE-K_DataEvaluation
## Getting Started
The repository contains all the data generated in the simulation of the NdR case study. Under the "2h" folder we can find the data referring to the 2h scenario, same idea for "24h" folder. We can just run the script in order to analyze and evaluate the data.

## Scripts
We use the following scripts:
* DataLoader.py: this class contains all the functions able to load the data from the files and generate runtime data structures. This class contains the utility application statement too.
* UtilityAnalizer.py: class which contains all the functions to make the analysis and the evaluation
* evaluation.py: class to launch in order to perform the analysis and print the data. In this class we can set "RT\_Thresh" (threshold for response time) and "E\_Thresh" (threshold for energy consumption) parameters for the utility function.


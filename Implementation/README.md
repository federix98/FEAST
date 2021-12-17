# MAPE-K_NdR_ASs
Implementation of the NdR project using 3 different ASs.

## About The Project
This project contains 3 different adaptations of the NdR to the following architectural styles:
- **Layered**
- **Blackboard**
- **Event Driven**

### Project Organization
The project contains 4 folders: 
- *Components*: contains all the basic components and connectors that the specific implementations use. 
- *Layered*: this folder contains the components of the MAPE loop, the CupCarbon sample project and the Machine Learning models of the Layered Implementation.
- *BB*: this folder contains the components of the MAPE loop, the CupCarbon sample project and the Machine Learning models of the Blackboard Implementation.
- *EventDriven*: this folder contains the components of the MAPE loop, the CupCarbon sample project and the Machine Learning models of the Event Driven Implementation.

### Layered Implementation
The communication of the components was made through sockets. 
Please check the availability of the `65431`, `65432`, `65433` ports.

### Blackboard Implementation
The communication of the components was made through sockets and Database (in this case we used MySQL connectors). Create required tables. Also adapt the database connection parameters in the MAPE components definition.

### Event Driven Implementation
The communication of the components was made through Kafka producers and consumers.
Be sure to have the `kafka-python` (https://pypi.org/project/kafka-python/) package installed in your system.
The broker uses the following topics:
- *BatchDataTopic*
- *CupCarbonEventsTopic*
- *PlannerExecutorTopic*

So you have to create these topics or edit the configuration in the Event Driven components definition.

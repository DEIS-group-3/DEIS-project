# DEIS Course Project Description

* Basic idea: 
One of the greatest threats to the continued existence of humans is illnesses, like in the massive effects we have seen this year due to the COVID-19 disease. We imagine that COVID has struck again, this time in Halmstad in the year 2040, when autonomous vehicles drive the streets. You will develop semi-autonomous robots that will travel throughout a city mockup in platoons and navigate through intersection crossings in a safe way, including emergency vehicles. 

* Basic motivation: This topic relates broadly to the School of Information Technology’s focuses on autonomous vehicles in smart cities/platooning and health technology; by considering this project topic, we hope to help prepare HH students to do research and development in designing embedded and intelligent systems related to autonomous vehicles and/or health technology. Additiona expected outcomes are that we will prepare an academic paper together summarizing some of the results of the course (the “research steps”) and a Youtube video that can be used as a demo for th “SafeSmart” research project.

* Groups: Students should try to form groups with a mixture of useful knowledge in embedded systems, intelligent systems, communication, etc, with a similar level of knowledge/expectations for grades. Students will get the chance to form their own groups but the course responsible can reassign group members as required.

* Setup: Each carlike robot will have infrared light sensor arrays pointed downwards to follow tracks, a forward-facing camera to do more complex sensing, and encoders attached to its wheel shafts. Two motors power the robot’s wheels. Processing will be conducted with a microcontroller (Arduino) for low level tasks, and a small computer (Raspberry Pi) running Linux with Wifi for some higher level tasks. Communication will be conducted using a predetermined protocol, running on robot operating system (ROS), which is designed to handle cases with multiple robots sending much information, on our own network, which is not connected to the internet. Groups can choose to add other sensors, actuators, computers, etc. (“eduroam” can be used to download software.)  The robots will run on top of a 1.8 x 2.4 meter table on E1, equipped with “tracks” made from black tape. The students this year will make a city section (with materials like cardboard) to drive around in. There will probably also be some flying robots (toy drones) with a camera.


## Tollgate 1
The main aim of tollgate 1 is to understand the concepts learnt during the labs and the lectures and utilize them into system modeling.

> System modeling constitutes understanding functional and non-functional requirements; connecting requirements to system design.

## Tollgate 2
In this tollgate, students need to present their research step. Each group get a research step topic from one of the main parts of the SafeSmart Project ( general, decision & control, localization, communication, integration + testing). These topics come from future work proposed by researchers in the SafeSmart project. It is also possible for the student themselves to propose a topic but it should be verified that this could result in original/novel research.
The five topics are:
- General: Traffic light. 
- Control: Getting out of the way for an EV.
- Communication: Attacks.
- Localization: Sensor position/angle-invariance.
- Testing: Smart testing. 
We have selected "Decision & Control".
> Decision & control: Robots have to get out of the way when an emergency vehicle needs to pass, e.g., by going to the side of the road or braking suddenly in a platoon.

## Tollgate 3
Basic robot behavior is covered in this tollgate. For this tollgate, we needed to prepare our working environment such as lanes, buildings and working robots like wheeled regular robots and aerial emergency vehicle.
> In particular, Tollgate 3 has basic environment & robot setup as well as basic robot motion, control and communication.
Along with robot and environment setup, we worked on key controlled robot, localization using gps server location information based on shared communication protocol. Robots were moving semi-autonomously as per requirements of this phase.

## Tollgate 4
Tollgate 4 has final demonstartion of rescuing, more complex robot behavior and platooning. It was required to collaborate with other groups to work on shared communication protocol to implement few scenarios such as intersection management, traffic management, Emergency handling, various driving scenarios, etc. In addition, we had to show our research step with practical illustartions.
> Major parts in Tollgate 4 
> - COVID rescue
> - Basic Collaboration with others (with more complex robot behavior)
> - physical implementation of research steps

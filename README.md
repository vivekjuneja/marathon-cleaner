# marathon-cleaner
This utility helps in removing deployed applications running on Marathon that are deemed old by a certain criteria. This is essential for building short-lived ephemeral development and test environments of applications deployed on Marathon. 

We provide disposable Development and Test Environments for developers over Mesos. There is enough tooling and automation that allows Developers to quickly deploy a set of Containerized services on Mesos via Marathon. This ease of creating disposable environment requires basic infrastructure to relinquish used up or unused capacity. One way to solve is to setup a process where any new disposable environment like Test or Development can only last for certain duration of time. Post that, the environemnt must cease to exist, and the capacity is available in the pool for new allocation.

##Purpose
The Marathon Cleaner is used as a means to replenish the resources consumed by Applications deployed on Marathon. For a Mesos Cluster that is used to deploy ephemeral Development and Test Environments, its important to have some policy to remove old applications. One of the constituents of the Policy is the age of the application deployed on Marathon. Applications are deemed 'Old' based on the required definition of Old expressed in 'Hours' or 'Days'. 

##Requirements
In our case, we have a shared infrastructure that is used to deploy different types of environments, including Dev, Staging, Test. This infrastructure is also used by different teams, with diverse projects, mostly web apps or long running services. To ensure this infrastructure has fair usage and high utilization, we intend to provide timed disposable environments. These environments are automatically deleted after a fixed duration. As the environments are disposable, it is possible to recreate them quickly if needed. In some cases, environments may be required to be long lasting, beyond the configured duration. This is usually with the performing load testing for a considerable amount of time to replicate scenario / use-case. In that case, it should be possible to configure such enviroments to be persistent, and be ignored of auto-removal activities. 
We also need service that can be in future be used to provide auto-destroy feature for certain types of application. Additionally, resilience engineering practices like Chaos Monkey style tests could also be carried out with auto-delete service.

##Features Provided
1. Configure the time interval to be used to delete the applications - eg:- Delete Applications that are 1 hour old OR are 3 day old.
2. Prevent some applicatioms from being removed automatically through the use of Marathon application labels. Currently, all applications that NEED NOT be removed must adhere to a common Marathon Application label (Key and Value). 
3. Store the Application Deployment manifest to filesystem before deleting the Application. This is useful to store / archive old deployments. 


##How to Use

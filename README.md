# marathon-cleaner
This utility helps in removing deployed applications running on Marathon that are deemed old by a certain criteria. This is essential for building short-lived ephemeral development and test environments of applications deployed on Marathon. The use case where this utility helps is as following :-

1. We provide disposable Development and Test Environments for developers over Mesos. There is enough tooling and automation that allows Developers to quickly deploy a set of Containerized services on Mesos via Marathon. This ease of creating disposable environment requires basic infrastructure to relinquish used up or unused capacity. One way to solve is to setup a process where any new disposable environment like Test or Development can only last for certain duration of time. Post that, the environemnt must cease to exist, and the capacity is available in the pool for new allocation.
2. 


Removes Old applications deployed on Apache Marathon. This is used to ephemeral applications that are removed after a certain duration 

##Purpose
The Marathon Cleaner is used as a means to replenish the resources consumed by Applications deployed on Marathon. For a Mesos Cluster that is used to deploy ephemeral Development and Test Environments, its important to have some policy to remove old applications. The Marathon Cleaner application looks for all the deployed applications on Marathon, and identifies the Time difference, using which it deletes the application based on the criteria provided.

Currently it supports Hour and Day criteria. 

##How to Use

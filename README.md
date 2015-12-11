# marathon-cleaner
Removes Old applications deployed on Apache Marathon. This is used to ephemeral applications that are removed after a certain duration 

##Purpose
The Marathon Cleaner is used as a means to replenish the resources consumed by Applications deployed on Marathon. For a Mesos Cluster that is used to deploy ephemeral Development and Test Environments, its important to have some policy to remove old applications. The Marathon Cleaner application looks for all the deployed applications on Marathon, and identifies the Time difference, using which it deletes the application based on the criteria provided.

Currently it supports Hour and Day criteria. 

##How to Use

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

Currently, the marathon cleaner appliation only considers Application Groups deployed on Marathon. Applications that are NOT deployed as a Group, but as just Marathon Application are Ignored. The support will be added in the next revision.

##How to Use

```
$ python marathon-app-cleaner.py -h

usage: marathon-app-cleaner.py [-h] [--marathon M] [--days D] [--hours H]
                               [--filterkey FILTERKEY]
                               [--filterkeyval FILTERKEYVAL]

Removes old Applications on Marathon to save Capacity

optional arguments:
  -h, --help            show this help message and exit
  --marathon M          The Marathon endpoint (eg: 10.53.15.219:18080)
  --days D              Number of days old
  --hours H             Number of hours old
  --filterkey FILTERKEY
                        Key for the application label that needs to be
                        filtered out
  --filterkeyval FILTERKEYVAL
                        Value of the Key for application label that needs to
                        be filtered out
```

Example 1:-

```
python marathon-app-cleaner.py --marathon 192.168.33.10:8080 --hours 1 --filterkey ENV --filterkeyval PROD
```

The above parameters allow the marathon cleaner app to connect to Marathon endpoint, and remove applications that are 1 hour Old. It ignores the Application who have a Label with the key as "ENV" with the value as "PROD". 


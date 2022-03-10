# ssh-check
An overdesigned service to check if a set of creds work on an SSH server, and then execute a command if they do.

May CCDC red teamers everywhere rejoice.


### USAGE
Update `./job-addtocheck/services_to_check.json`, then:
```
docker-compose build && docker-compose up
docker-compose up --scale worker-check=10
```  

To add more services, update `services_to_check` and run:
```
docker-compose build job-addtocheck
docker-compose up job-addtocheck
```
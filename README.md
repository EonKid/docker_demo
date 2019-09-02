#Containers

 ##### Create image using this directory's Dockerfile
docker build -tag=eonkid/flask_restapi_demo:1.0 
###### Run "friendlyhello" mapping port 4000 to 80
docker run -p 4000:80 friendlyhello  
###### Same thing, but in detached mode
docker run -d -p 4000:80 friendlyhello         
###### List all running containers
docker container ls                               
###### List all containers, even those not running
docker container ls -a             
###### Gracefully stop the specified container
docker container stop <hash>           
###### Force shutdown of the specified container
docker container kill <hash>         
###### Remove specified container from this machine
docker container rm <hash>        
###### Remove all containers
docker container rm $(docker container ls -a -q)         
###### List all images on this machine
docker image ls -a                             
###### Remove specified image from this machine
docker image rm <image id>            
###### Remove all images from this machine
docker image rm $(docker image ls -a -q)   
###### Log in this CLI session using your Docker credentials
docker login             
###### Tag <image> for upload to registry
docker tag <image> username/repository:tag  
###### Upload tagged image to registry
docker push username/repository:tag            
###### Run image from a registry
docker run username/repository:tag                   




# Services

$ docker swarm init
$ docker stack deploy -c docker-compose.yml learning_docker

#### Get the service ID for the one service in our application:
$ docker service ls

### view all services associated with the getstartedlab stack:
$ docker service ps learning_docker_web

$ docker container ls -q

### To view all tasks of a stack
$ docker stack ps learning_docker

### Take down the app and the swarm
##### Take the app down with docker stack rm:
docker stack rm learning_docker

#### Take down the swarm.
docker swarm leave --force

#### List stacks or apps
docker stack ls
#### Run the specified Compose file                                            
docker stack deploy -c <composefile> <appname>  
#### List running services associated with an app
docker service ls  
#### List tasks associated with an app               
docker service ps <service>  
#### Inspect task or container                
docker inspect <task or container>     
#### List container IDs              
docker container ls -q   
#### Tear down an application                                   
docker stack rm <appname>   
#### Take down a single node swarm from the manager                          
docker swarm leave --force      

# Docker Swarms
##### joining multiple machines into a “Dockerized” cluster called a swarm.

Install Oracle VirtualBox 
https://www.virtualbox.org/wiki/Downloads

#####create a couple of VMs using docker-machine, using the VirtualBox driver:
docker-machine create --driver virtualbox myvm1
docker-machine create --driver virtualbox myvm2

####List the VMs and get their IP addresses
docker-machine ls

$ docker-machine ssh myvm1 "docker swarm init --advertise-addr <myvm1 ip>"
Swarm initialized: current node <node ID> is now a manager.
docker-machine ssh myvm1 "docker swarm init --advertise-addr 192.168.99.100:2376"

To add a worker to this swarm, run the following command:

  docker swarm join \
  --token <token> \
  <myvm ip>:<port>

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
#### myvm2 join your new swarm as a worker:
$ docker-machine ssh myvm2 "docker swarm join \
--token <token> \
<ip>:2377"

docker-machine ssh myvm2 "docker swarm join --token SWMTKN-1-19uuekp39dkbp4dmu7jexcfujhjtt78xoakzo00cj9jwroxp6d-empgyf5wvrgy5qn25ouazq6bz 192.168.99.100:2377"

This node joined a swarm as a worker.

####Run docker node ls on the manager to view the nodes in this swarm:
 docker swarm join --token SWMTKN-1-19uuekp39dkbp4dmu7jexcfujhjtt78xoakzo00cj9jwroxp6d-empgyf5wvrgy5qn25ouazq6bz 192.168.99.100:2376
 docker-machine ssh myvm1 "docker node ls"
 
 #####Leaving a swarm
 docker swarm leave
 
 # Deploy your app on the swarm cluster
 $ docker-machine env myvm1
export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://192.168.99.100:2376"
export DOCKER_CERT_PATH="/Users/sam/.docker/machine/machines/myvm1"
export DOCKER_MACHINE_NAME="myvm1"
# Run this command to configure your shell:
# eval $(docker-machine env myvm1)
$ docker-machine ls

#Note: If your image is stored on a private registry instead of Docker Hub, you need to be logged in using docker login <your-registry> and then you need to add the --with-registry-auth flag to the above command. For example:
docker login registry.example.com

docker stack deploy --with-registry-auth -c docker-compose.yml getstartedlab

#### Deploy using docker stack deploy
docker stack deploy -c docker-compose.yml learning_docker

#####Having connectivity trouble?
Keep in mind that to use the ingress network in the swarm, you need to have the following ports open between the swarm nodes before you enable swarm mode:

    Port 7946 TCP/UDP for container network discovery.
    Port 4789 UDP for the container ingress network.
# Cleanup and reboot
#####Stacks and swarms 
docker stack rm learning_docker

####cheatsheet
docker-machine create --driver virtualbox myvm1 # Create a VM (Mac, Win7, Linux)
docker-machine create -d hyperv --hyperv-virtual-switch "myswitch" myvm1 # Win10
docker-machine env myvm1                # View basic information about your node
docker-machine ssh myvm1 "docker node ls"         # List the nodes in your swarm
docker-machine ssh myvm1 "docker node inspect <node ID>"        # Inspect a node
docker-machine ssh myvm1 "docker swarm join-token -q worker"   # View join token
docker-machine ssh myvm1   # Open an SSH session with the VM; type "exit" to end
docker node ls                # View nodes in swarm (while logged on to manager)
docker-machine ssh myvm2 "docker swarm leave"  # Make the worker leave the swarm
docker-machine ssh myvm1 "docker swarm leave -f" # Make master leave, kill swarm
docker-machine ls # list VMs, asterisk shows which VM this shell is talking to
docker-machine start myvm1            # Start a VM that is currently not running
docker-machine env myvm1      # show environment variables and command for myvm1
eval $(docker-machine env myvm1)         # Mac command to connect shell to myvm1
& "C:\Program Files\Docker\Docker\Resources\bin\docker-machine.exe" env myvm1 | Invoke-Expression   # Windows command to connect shell to myvm1
docker stack deploy -c <file> <app>  # Deploy an app; command shell must be set to talk to manager (myvm1), uses local Compose file
docker-machine scp docker-compose.yml myvm1:~ # Copy file to node's home dir (only required if you use ssh to connect to manager and deploy the app)
docker-machine ssh myvm1 "docker stack deploy -c <file> <app>"   # Deploy an app using ssh (you must have first copied the Compose file to myvm1)
eval $(docker-machine env -u)     # Disconnect shell from VMs, use native docker
docker-machine stop $(docker-machine ls -q)               # Stop all running VMs
docker-machine rm $(docker-machine ls -q) # Delete all VMs and their disk images

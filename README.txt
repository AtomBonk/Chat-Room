||| GENERAL STARTUP INFO |||
1. run: minikube ip
to get YOUR cluster ip in order to connect to it.

go to the chat-client.py file
under main:
change the 1st argument of ChatClient() to YOUR CLUSTER IP 'X.X.X.X' (must have quotes)

2. when applying the whole k8s directory with kubectl, the server pod
will fail until the postgres pod has succesfully initialized.
the server deployment will keep restarting the pod until it can
succesfully connect to the postgres database. this may take 1-2 minutes.


||| KUBERNETES ON WINDOWS WITH DOCKER DRIVER |||

currently if you run kubernetes on windows with the docker driver
the cluster cannot be exposed normally, even if you use an ingress or a nodeport service.
after applying the k8s directory with kubectl (see general 2. above),
in order to connect to the server you will have to execute the command:
minikube service chat-server-service --url

this opens a tunnel to your cluster at the server node-port service.
on your screen it will print which port on the localhost you can connect to.
take the port number and change it in the chat-client.py file.
under main: 
change the 1st argument of ChatClient() to '127.0.0.1' (must have quotes).
change the 2nd argument of ChatClient() to the PORT NUMBER from the tunnel.
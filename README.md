- [HealthChecker](#healthchecker)
- [Quick Start](#quick-start)
  * [Configuration](#configuration)
    + [Cofiguration file](#cofiguration-file)
  * [Building docker Image](#building-docker-image)
  * [Running docker image](#running-docker-image)
  * [Creating a Cloud VM to develop and run the Application](#creating-a-cloud-vm-to-develop-and-run-the-application)
  * [Kubernetes](#kubernetes)

# HealthChecker
HealthChecker is a python3 application that performs health-checks on different url endpoints defined in it's config.yaml file, and sends notifications with the errors found to a notification endpoint. The config.yaml file is validated against a schema to guarantee that it's valid. It exposes a **/healthz** endpoint that can be used to check if it's runnning.


# Quick Start
Make sure you have python3 installed in your machine. In order to install the required libraries you will need **pip3**. 
In Debian distros is enough doing:

```bash
sudo apt-get install python3-pip
```

If you dont have **pip3** the installation instructions can be found [here](https://pip.pypa.io/en/stable/installing/).

Project libraries can be installed with:
```bash
git pull https://github.com/samiracho/HealthChecker.git
cd HealthChecker
pip3 install -r src/resources/requirements.txt
```
You can start the application from the commandline:
```bash
export HK_NOTIFY_TOKEN=your_auth_token
./src/main.py
```
By default it will start a http server in the port 8080 and it will check the configured enpoints each 5 minutes.

## Configuration
Several ENV variables can be set to change the default configuration.

| Name                 | Description                                   | Default value                                      |
| -------------------- | --------------------------------------------- | -------------------------------------------------- |
| **HK_NOTIFY_TOKEN**  | Notification endpoint auth-token.             | none                                               |
| **HK_CONFIG_PATH**   | Path to the config file                       | If not set src/resources/config.yaml               |
| **HK_DEFAULT_PORT**  | Default listening port                        | If not set,  **8080**                              |
| **HK_CHECK_INTERVAL**| Default health-check time interval in seconds | If not set, it will check the endpoints each 5min  |


### Cofiguration file
The endpoints to check have to be defined in a yaml config file that has to follow some format requirements.

> By default the app will use src/resources/config.yaml

> The validation schema can be found in **/src/resources/ValidationSchema.yaml**. It's pretty self explanatory.

Config file example.
```yaml
notificationEndpoint:  
  url: https://notificationendpoint.com/notification  
  method: POST  
  headers: {Authorization: 'Bearer {0}'}  
checks:  
  - service: Google  
      request:  
        method:    GET  
        endpoint:  http://google.com  
        body:      ""  
        verifySSL: False  
      response:  
          codes:   [200, 301, 400]  
          body: "google.com"
```

1. The service.request config will be used to make the health-checks.
2. All the checks in the response category will be performed. 
3. If any of them fails a notification will be sent to the NotificationEndpoint.url with the following format:

```json
{
	"service":"serviceName",
	"description": "Error1 description \n  Error2 description \n ..."
}
```

## Building docker Image

A helper bash script have been included in order to pass the tests and if all pass, build the docker image with the name **healthchecker:latest**

> If you don't have Docker installed you have to follow the Docker Installation docs for your system.

```bash
./build.sh
```

## Running docker image
```bash
docker run healthchecker:latest
```

## Creating a Cloud VM to develop and run the Application
An example script to create a Google Cloud VM with all the required dependencies can be found in `build_env.sh`
It does the following:
1. Creates a VM
2. Installs the required dependencies
> You need to have installed gcloud tools in your machine.

 ## Kubernetes
 A K8s.template.yaml has been included. It does the following:
 1. Creates a configMap with a config.yaml
 2. Creates a secret with the auth token.
 3. Creates a service to expose the deployment.
 4. Creates a deployment with the secret and the configmap mounted.
 5. A livenessProbe points to the application /healthz endpoint
 
 Since the application always reads the config file before doing the health-checks, and the Kubernetes volumes are mounted in read-only mode, it's possible to update the ConfigMap without needing to redeploy.
 The next health-check will use the updated configuration.

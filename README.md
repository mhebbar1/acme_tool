# Acme Cli Tool

This cli tool enables seamless Kubernetes deployment and dependency management, eliminating the need for in-depth Kubernetes knowledge.

This tool currently supports one application ping api and its dependencies.

## Prerequisites

### OS and Tools
This utility has been tested using the following versions.

* MacOS 15.7.3 or higher.
* Docker Desktop 4.57.0 (215387) or higher.
* Homebrew   # Requires super user access to install

Docker Desktop Install Guide for Mac: https://docs.docker.com/desktop/setup/install/mac-install/

### PATH
Update PATH if brew not found in your path
```sh
export PATH=${PATH}:/opt/homebrew/bin:.local/bin
```

### Docker Desktop Configuration
Configure Kubenetes in Docker using `kind` and K8s version 1.32. Specify at least two nodes when creating your cluster.

Once spun up, activate the docker K8s context and confirm your nodes are present:

```sh
kubectl config use-context docker-desktop
kubectl get nodes
NAME                    STATUS   ROLES           AGE    VERSION
desktop-control-plane   Ready    control-plane   5d3h   v1.32.0
desktop-worker          Ready    <none>          5d3h   v1.32.0
```

### Install nginx controller
You will also need to install the nginx controller into your cluster to allow
ingress. You can do this by running:

## Install nginx controller
```sh
make bootstrap-docker-desktop
```

## Clone the Repo

Ask the owner to give you access to the repo.

Clone over ssh

```git clone git@github.com:mhebbar1/acme_tool.git ```

Clone over https:

```git clone https://github.com/mhebbar1/acme_tool.git ```

```sh
cd acme_tool
make install-all
acme --version
  acme, version 0.0.1
```

Add bitnami helm repo
```sh
helm repo add bitnami https://charts.bitnami.com/bitnami
```

## Using the Tool
Commands should be run from the acme tool directory.

```sh acme -h
Usage: acme [OPTIONS] COMMAND [ARGS]...

  Welcome to the Acme CLI

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  delete  Deletes a specified service and its direct dependencies.
  deploy  Deploys a specified service along with any dependencies it...
  logs    Streams the logs from a specified service.
  ls      List namespaces.
```

```sh acme ls -h
Usage: acme ls [OPTIONS]

  List namespaces.

Options:
  --namespace TEXT  namespace to use
  -h, --help        Show this message and exit.

e.g:
# Lists all resources under your username
acme ls
# Lists resources for another user
acme ls --namespace bobsmith
```

```sh acme deploy -h
Usage: acme deploy [OPTIONS]

  Deploys a specified service along with any dependencies it requires.

Options:
  --resources TEXT   Helm resources to override during helm install, key=value
                     format
  --add_env TEXT     Additional env vars to pass to helm install, key=value
                     format
  --add_labels TEXT  Additional labels to pass to helm install, key=value
                     format
  --user TEXT        Username to use for namespace, default is current user
  --new              Boolean, create new namespace
  -h, --help         Show this message and exit.

You can combine one or more options or use the default.

e.g: 
# Deploy with all default configuration in the $user namespace
acme deploy
# Create a new namespace with datastamp for $user and deploy
acme deploy --new
# Deploy with custom resources. requested resources should be less than the limits.
# Default resources: requests.memory=256Mi,requests.cpu=256m,limits.memory=256Mi,limits.cpu=256m
acme deploy --resources requests.memory=300Mi,requests.cpu=250m,limits.memory=512Mi,limits.cpu=500m
# Deploy with added environment vars
acme deploy --add_env FOO=BAR,ENV=DEV,SEARCH_ENGINE="https://www.google.com"
# Deploy with additional app labels
acme deploy --add_labels TOKEN=TEST,APPLICATION=BUGSCRUB
# Deploy in a namespace for bobsmith
acme deploy --user bobsmith
# Create a new namespace with datastamp for user bobsmith 
acme deploy --user bobsmith --new
```

```sh acme delete -h
Usage: acme delete [OPTIONS]

  Deletes a specified service and its direct dependencies.

Options:
  --name_also       including namespace
  --namespace TEXT  namespace to use
  -h, --help        Show this message and exit.


e.g:
# Delete all resources under $user namespace
acme delete
# Delete all resources under $user namespace including namespace itself
acme delete --name_also
# Delete all resources under namespace bobsmith and namespace also
acme delete --namespace bobsmith --name_also
```

```sh acme logs -h
Usage: acme logs [OPTIONS]

  Streams the logs from a specified service.

Options:
  --namespace TEXT  Namespace to use
  --pod_name TEXT   Pod name
  --cont            log tail
  -h, --help        Show this message and exit.

pod_name can be found from `acme ls` command.

e.g:

# Get logs for a given pod in the $user namespace
acme logs --pod_name pod/ping-api-8477794564-24wmc
# Logtail for a pod $user namespace
acme logs --pod_name pod/ping-api-8477794564-24wmc --cont
# Logtail for a pod in a different namespace
acme logs --pod_name pod/ping-api-8477794564-24wmc  --cont --namespace 20260202111749-murthyhebbar
```
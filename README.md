# Acme Cli Tool

This cli tool enables seamless Kubernetes deployment and dependency management, eliminating the need for in-depth Kubernetes knowledge.

## Prerequisites

* MacOS 15.7.3 or higher, or Any Linux flavor that supports Docker Desktop.
* Docker Desktop 4.57.0 (215387) or higher.

## Clone the Repo

Ask the owner to give you access to the repo.

Clone over ssh

``` git@github.com:mhebbar1/acme_tool.git ```

Clone over https:

``` https://github.com/mhebbar1/acme_tool.git ```


```
make install-all
acme --version
  acme, version 0.0.1
```

Configure Kubenetes in Docker using `kind` and K8s version 1.32. Specify at least two nodes when creating your cluster.

Once spun up, activate the docker K8s context and confirm your nodes are present:

```sh
kubectl config use-context docker-desktop
kubectl get nodes
NAME                    STATUS   ROLES           AGE    VERSION
desktop-control-plane   Ready    control-plane   5d3h   v1.32.0
desktop-worker          Ready    <none>          5d3h   v1.32.0
```

You will also need to install the nginx controller into your cluster to allow
ingress. You can do this by running:

## Install nginx controller
```sh
cd acme_tool
make bootstrap-docker-desktop
```

## Using the Tool

``` acme -h
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

``` acme ls -h
Usage: acme ls [OPTIONS]

  List namespaces.

Options:
  --namespace TEXT  namespace to use
  -h, --help        Show this message and exit.
```

``` acme deploy -h
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
```

``` acme delete -h
Usage: acme delete [OPTIONS]

  Deletes a specified service and its direct dependencies.

Options:
  --name_also       including namespace
  --namespace TEXT  namespace to use
  -h, --help        Show this message and exit.

```

``` acme logs -h
Usage: acme logs [OPTIONS]

  Streams the logs from a specified service.

Options:
  --namespace TEXT  Namespace to use
  --pod_name TEXT   Pod name
  --cont            log tail
  -h, --help        Show this message and exit.
```
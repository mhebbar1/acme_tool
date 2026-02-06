"""Deploys a specified service along with any dependencies it requires."""
import os
from datetime import datetime
import click # type: ignore

now = datetime.now()
USER = os.environ.get('USER')

@click.option('--new', is_flag=True, help='Boolean, create new namespace')
@click.option('--user', default=USER,
               help='Username to use for namespace, default is current user')
@click.option('--add_labels', default=None,
               help='Additional labels to pass to helm install, key=value format')
@click.option('--add_env', default=None,
               help='Additional env vars to pass to helm install, key=value format')
@click.option('--resources', default=None,
               help='Helm resources to override during helm install, key=value format')
@click.command()

def deploy(new, user, add_labels, add_env, resources):
    """Deploys a specified service along with any dependencies it requires."""
    #raise NotImplementedError
    if new:
        namespace = f"{now.strftime('%Y%m%d%H%M%S')}-{user}"
    else:
        namespace = user

    print(f"Deploying resources to namespace: {namespace}")
    ns_cmd = f'kubectl create namespace {namespace} --dry-run=client -o yaml | kubectl apply -f -'
    ns_cmd_status = os.system(ns_cmd)
    if ns_cmd_status != 0:
        raise RuntimeError(f"Failed to create namespace '{namespace}'")
    ns_cmd_sw = f'kubectl --context docker-desktop config set-context --current --namespace={namespace}'
    ns_cmd_sw_status = os.system(ns_cmd_sw)
    if ns_cmd_sw_status != 0:
        raise RuntimeError(f"Failed to switch to namespace '{namespace}'")
    print(f"Namespace '{namespace}' is ready.\n")

    # Install Postgres
    cmd1 = f'helm upgrade \
  --kube-context docker-desktop \
  --namespace {namespace} \
  --create-namespace \
  ping-postgres \
  bitnami/postgresql \
  --wait --install \
  -f src/helm/values/ping/postgres.yaml'

    # Install redis
    cmd2 = f'helm upgrade --install \
  --kube-context docker-desktop \
  --namespace {namespace} \
  --create-namespace \
  ping-redis \
  bitnami/redis \
  --wait --install \
  -f src/helm/values/ping/redis.yaml'

    # Prepare connection strings
    redis_url = f'redis://ping-redis-master:6379'
    pg_host = f'ping-postgres-postgresql'
    pg_db = 'postgres'
    pg_user = 'postgres'

    # Install Ping service
    cmd3 = f'helm upgrade \
  --kube-context docker-desktop \
  --namespace {namespace} \
  --create-namespace \
  ping \
  src/helm/application/ \
  --wait --install \
  -f src/helm/values/ping/values.yaml \
  --set image.name=0x7162/ping \
  --set image.tag=latest \
  --set api.additionalEnvVariables.REDIS_CACHE_URL={redis_url} \
  --set api.additionalEnvVariables.POSTGRES_HOST={pg_host} \
  --set api.additionalEnvVariables.POSTGRES_DB={pg_db} \
  --set api.additionalEnvVariables.POSTGRES_USER={pg_user}'

    # Process additional labels
    for arg in (add_labels or "").split(","):
        if arg.strip():
            key, value = arg.split("=")
            if key == "app":
                print("The 'app' label is reserved and cannot be modified.")
            else:
                cmd3 += f" --set api.additionalLabels.{key.strip()}={value.strip()}"

    # Process additional env vars
    for env_arg in (add_env or "").split(","):
        if env_arg.strip():
            key, value = env_arg.split("=")
            cmd3 += f" --set api.additionalEnvVariables.{key.strip()}={value.strip()}"

    # Process helm resource overrides
    for resources_v in (resources or "").split(","):
        if resources_v.strip():
            key, value = resources_v.split("=")
            cmd3 += f" --set api.resources.{key.strip()}={value.strip()}"

    print("\nExecuting deployment commands...\n")
    cmd1_status = os.system(cmd1)
    if cmd1_status == 0:
        print("Postgres deployed successfully.\n")
    else:
        raise RuntimeError("Failed to deploy Postgres service.")
    cmd2_status = os.system(cmd2)
    if cmd2_status == 0:
        print("Redis deployed successfully.\n")
    else:
        raise RuntimeError("Failed to deploy Redis service.")
    cmd3_status = os.system(cmd3)
    if cmd3_status == 0:
        print("Ping service deployed successfully.\n")
    else:
        raise RuntimeError("Failed to deploy Ping service.")

    print("\nDeployment completed successfully.")
    print(f"\nUI is accessible at http://ping.{namespace}.127.0.0.1.nip.io/ping\n")

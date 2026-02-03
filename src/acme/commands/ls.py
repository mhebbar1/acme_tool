"""List namespaces and their resources."""
import os
import subprocess
import click

USER = os.environ.get('USER')
@click.option('--namespace', default=USER, help='namespace to use')
@click.command()

def ls(namespace):
    """List namespaces."""
    print(f"Listing resources for {namespace}")
    print("----------------------------")
    cmd1 = f'kubectl get namespaces --no-headers |grep {namespace} |awk \'{{print $1}}\''
    result = subprocess.run(cmd1, shell=True, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        print(f"No resources found for namespace {namespace}")
    else:
        for ns in result.stdout.splitlines():
            print(f"Resources in namespace: {ns}")
            print("----------------------------")
            cmd2: str = f'kubectl get all -n {ns}'
            os.system(cmd2)
            print("============================\n")

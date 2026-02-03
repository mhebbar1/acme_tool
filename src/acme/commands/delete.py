"""Deletes a specified service and its direct dependencies."""
import os
import click # type: ignore

USER = os.environ.get('USER')
@click.option('--namespace', default=USER, help='namespace to use')
@click.option('--name_also', is_flag=True, help='including namespace')
@click.command()
def delete(namespace, name_also):
    """Deletes a specified service and its direct dependencies."""
    print(f"Deleting resources in namespace {namespace}")
    cmd1 = f'kubectl delete all --all -n {namespace}'
    cmd2 = f'kubectl delete pvc --all -n {namespace}'
    cmd3 = f'kubectl delete namespace {namespace}'
    os.system(cmd1)
    os.system(cmd2)
    if name_also:
        os.system(cmd3)

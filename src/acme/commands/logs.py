"""Streams the logs from a specified service."""
import os
import click # type: ignore

USER = os.environ.get('USER')
@click.option('--cont', is_flag=True, help='log tail')
@click.option('--pod_name', default=None, help='Pod name')
@click.option('--namespace', default=USER, help='Namespace to use')
@click.command()
def logs(pod_name, cont, namespace):
    """Streams the logs from a specified service."""
    cmd1 = f'kubectl logs {pod_name} -n {namespace}'
    if cont:
        cmd1 += " -f"
    os.system(cmd1)

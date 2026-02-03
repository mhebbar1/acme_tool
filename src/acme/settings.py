"""Common settings used across the CLI commands."""
# Standard Library
import os

from pathlib import Path

CLI_ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# ###########################################
# Deployment settings
# ###########################################

SIZES = {
    'small': {
        'resources': {
            'limits': {
                'cpu': '200m',
                'memory': '256Mi',
            },
            'requests': {
                'cpu': '200m',
                'memory': '256Mi',
            },
        },
    },
    'large': {
        'resources': {
            'limits': {
                'cpu': '500m',
                'memory': '512Mi',
            },
            'requests': {
                'cpu': '500m',
                'memory': '512Mi',
            },
        },
    },
}


# ###########################################
# Service settings
# ###########################################

SERVICES = {
    'ping': {
        'image': {
            'name': 'casestudy/ping',
            'tag': 'latest',
        },
        'dependencies': {
            'redis': {
                'chart': 'bitnami/redis',
                'version': '16.13.2',
            },
            'postgres': {
                'chart': 'bitnami/postgresql',
                'version': '16.2.0',
            },
        },
    },
}

# ###########################################
# Logger settings
# ###########################################

LOG_FORMAT_STRING = '%(message)s'
LOG_LEVEL = (os.getenv('DEBUG') and 'DEBUG') or 'INFO'

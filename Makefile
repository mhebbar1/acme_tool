.DEFAULT_GOAL := help
.PHONY: help dev

install-all:
	make install-tools
	make install-requirements
	make install

install-requirements:  ## Install requirements, tries to install to local venv
	uv sync --all-groups --refresh

install: install-requirements  ## Install CLI
	uv tool install -e .

uninstall:  ## Uninstall CLI
	uv tool uninstall acme-cli

install-tools:  ## Install all CLI dependencies (via Brew on Mac)
	sh ./scripts/cli/install_tools.sh

bootstrap-docker-desktop:  ## Bootstrap Docker Desktop with Ingress Nginx
	kubectl apply --context docker-desktop -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.12.2/deploy/static/provider/cloud/deploy.yaml

test:  ## Run pytest
	uv run pytest --cov=src -vvv

coverage-report:  # Output a coverage report
	uv run coverage html

help:  ## Display the list of Makefile commands
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

DOCKER=docker
GROUP=sdnm
PROJECT=clab-cassini-sdnm
VERSION=latest
PORT_NETCONF="830"
PORT_SSH=21
PORT_RESTCONF=8080
NAME=clab-cassini-sdnm

# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

builder: ## Build SDNML cassini image
	@echo 'Building SDNML cassini image' \
	&& $(DOCKER) build -t $(GROUP)/$(PROJECT):$(VERSION) -f Dockerfile .

run: ## RUN SDNML cassini container
	@echo 'Running SDNML cassini container' \
	&& $(DOCKER) run -itd  --privileged --name $(NAME) \
	-p $(PORT_NETCONF):$(PORT_NETCONF) \
	-p $(PORT_SSH):$(PORT_SSH) -p $(PORT_RESTCONF):$(PORT_RESTCONF)  --cap-add=NET_ADMIN \
	--cap-add=SYS_MODULE -v "/lib/modules:/lib/modules" -v "/sys/fs/cgroup:/sys/fs/cgroup:ro" $(GROUP)/$(PROJECT):$(VERSION) 

start: ## Start SDNML cassini container
	@echo 'Starting SDNML cassini container' \
	&& $(DOCKER) start $(NAME)

stop: ## Stop SDNML cassini container
	@echo 'Stoping SDNML cassini container' \
	&& $(DOCKER) stop $(NAME)

del: ## Delete SDNML cassini container
	@echo 'Deleting SDNML cassini container' \
	&& $(DOCKER) rm $(NAME)

del-image: ## Delete SDNML cassini image
	@echo 'Deleting SDNML cassini image' \
	&& $(DOCKER) rmi $(GROUP)/$(PROJECT):$(VERSION)

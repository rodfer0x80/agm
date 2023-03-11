.PHONY: run
run: # start all the good stuff
	scripts/run.sh

.PHONY: clean
clean: # detect OS, install deps
	scripts/clean.sh

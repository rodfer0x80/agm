.PHONY: build
build: # Build python venv with deps
	scripts/build.sh

.PHONY: clean
clean: # Cleanup venv build
	scripts/cleanup.sh

.PHONY: run
run: # Run main script
	scripts/run.py


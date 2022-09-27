.PHONY: build
build: # Build python venv with deps
	scripts/build.sh

.PHONY: clean
clean: # Cleanup venv build
	scripts/cleanup.sh

.PHONY: run
run: # Run main script
	scripts/run.py

.PHONY: debug
debug: # Run main debug script
	scripts/debug.py

.PHONY: test
test: # Run main script
	scripts/test.sh


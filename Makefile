# GNU Makefile that documents and automates common development operations
#              using the GNU make tool (version >= 3.81)
# Development is typically conducted on Linux or Max OS X (with the Xcode
#              command-line tools installed), so this Makefile is designed
#              to work in that environment (and not on Windows).
# USAGE: tax-calculator$ make [TARGET]

.PHONY=help
help:
	@echo "USAGE: make [TARGET]"
	@echo "TARGETS:"
	@echo "help       : show help message"
	@echo "clean      : remove .pyc files and local taxcalc package"
	@echo "package    : build and install local package"
	@echo "cstest     : generate coding-style errors using pycodestyle"
	@echo "pytest     : generate report for and cleanup after pytest"
	@echo "coverage   : generate test coverage report"
	@echo "git-sync   : synchronize local, origin, and upstream Git repos"
	@echo "git-pr N=n : create local pr-n branch containing upstream PR"

.PHONY=clean
clean:
	@find . -name *pyc -exec rm {} \;
	@find . -name *cache -maxdepth 1 -exec rm -r {} \;
	@conda uninstall taxcalc --yes --quiet 2>&1 > /dev/null

.PHONY=package
package:
	@pbrelease taxcalc taxcalc 2.0.0 --local

define pytest-cleanup
find . -name *cache -maxdepth 1 -exec rm -r {} \;
endef

TAXCALC_JSON_FILES := $(shell ls -l ./taxcalc/*json | awk '{print $$9}')

.PHONY=cstest
cstest:
	pycodestyle taxcalc
	@-pycodestyle --ignore=E501,E121 $(TAXCALC_JSON_FILES)

.PHONY=pytest
pytest:
	@cd taxcalc ; pytest -n4 -m ""
	@$(pytest-cleanup)

define coverage-cleanup
rm -f .coverage htmlcov/*
endef

OS := $(shell uname -s)

.PHONY=coverage
coverage:
	@$(coverage-cleanup)
	@coverage run -m pytest -v -m "" > /dev/null
	@coverage html --ignore-errors
ifeq ($(OS), Darwin) # on Mac OS X
	@open htmlcov/index.html
else
	@echo "Open htmlcov/index.html in browser to view report"
endif
	@$(pytest-cleanup)

.PHONY=git-sync
git-sync:
	@./gitsync

.PHONY=git-pr
git-pr:
	@./gitpr $(N)

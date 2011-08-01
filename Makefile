
TEST_DIR = ./test
TEST_FILE_PATTERN = *Test.py


red      = \e[0;31m
RED      = \e[1;31m
blue     = \e[0;34m
BLUE     = \e[1;34m
cyan     = \e[0;36m
CYAN     = \e[1;36m
NO_COLOR = \e[0m

# NOTE: This defeats the whole purpose of Make...
.PHONY : clean build test

default: build

clean:
	@# TODO: how to clean? This does not work
	@#python setup.py uninstall
	@$(RM) -r ./build

install:
	@echo -e '\n$(BLUE) ------------- INSTALL -------------  $(NO_COLOR)\n'
	@python setup.py install


user-install:
	@ # For people without enough system rights for install
	@echo -e '\n$(BLUE) ------------- INSTALL -------------  $(NO_COLOR)\n'
	@python setup.py install --user


build: clean
	@echo -e '\n$(BLUE) -------------- BUILD --------------  $(NO_COLOR)\n'
	@python setup.py build

test: user-install
	@ #TODO: colorize, basics are in place...
	@echo -e '\n$(BLUE) -------------- TEST --------------  $(NO_COLOR)\n'
	@python -m unittest discover -v -s $(TEST_DIR) -p "$(TEST_FILE_PATTERN)" \
		> "$(TEST_DIR)/test.output" 2>&1; \
		cat test/test.output | \
		sed -e s/ERROR:/ERROR/g \
		-e s/FAIL:/FAIL:/g \
		-e s/FAILED/FAILED/g




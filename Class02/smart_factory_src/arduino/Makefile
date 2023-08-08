BOARD:=arduino:avr:uno
SOURCE:=arduino.ino
BINARY:=build/$(subst :,.,$(BOARD))/$(SOURCE).hex

SERIAL=$(shell ./bin/arduino-cli board list | grep -m 1 "$(BOARD)" | awk '{print $$1}')

.PHONY: usage init build flash lint clean

usage:
	@echo ""
	@echo "[!] Smart Factory Arduino control driver build script."
	@echo ""
	@echo "    make usage   : This page (default)"
	@echo "    make init    : One-time setup for CLI build environment"
	@echo "    make build   : Compile Arduino driver"
	@echo "    make flash   : Upload binary into Arduino"
	@echo "    make lint    : Run code formatter"
	@echo "    make clean   : Remove build output"
	@echo ""

init:
ifeq (,$(wildcard ./bin/arduino-cli))
	@curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
	@./bin/arduino-cli config init --overwrite
	@./bin/arduino-cli core install arduino:avr
endif
	@echo "[!] Make sure \"./bin\" is set in your \$$PATH."

build: $(SOURCE)
	@./bin/arduino-cli compile -b $(BOARD) . -e -v

flash:
ifeq (,$(wildcard $(BINARY)))
	@echo "[-] Please run \"make build\" first."
	@exit 1
endif

ifeq ($(SERIAL),)
	@echo "[-] Unable to find Arduino board to flash."
	@exit 1
endif

	@./bin/arduino-cli upload -p $(SERIAL) -b $(BOARD) -t -v -i $(BINARY)

lint:
	@clang-format -i arduino.ino

clean:
	@-rm -rf build

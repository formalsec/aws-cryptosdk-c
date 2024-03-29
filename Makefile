# Helpers
rwildcard=$(foreach d,$(wildcard $(1:=/*)),$(call rwildcard,$d,$2) $(filter $(subst *,%,$2),$d))

LIBC=bin/libc.a
BUILD=_build
PROOFS := $(call rwildcard,proofs,*.c)

TESTS := $(patsubst proofs/%.c,$(BUILD)/tests/%.wat,$(PROOFS))

.PHONY: clean

default: all

all: libc $(TESTS)

libc:
	make -C lib

$(BUILD)/tests/%.wat: proofs/%.c
	@echo "Building $@..."
	@$(MAKE) -C $(dir $<) -j8

clean:
	$(RM) -rf $(BUILD) $(LIBC)

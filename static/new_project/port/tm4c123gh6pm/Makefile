################################################################################
#    Toolchain
#

.PHONY: flash
flash: $(BIN_OUTDIR)$(PROJ_NAME).bin
	@lm4flash -v -E $<

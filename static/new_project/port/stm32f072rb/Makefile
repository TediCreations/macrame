################################################################################
#    Toolchain
#

.PHONY: remoteDebug
remoteDebug:
	@JLinkGDBServer -select USB -device STM32F072RB -endian little -if SWD -speed 4000 -noir -noLocalhostOnly

.PHONY: flash
flash: $(BIN_OUTDIR)flash.jlink
	@JLinkExe -CommanderScript $<

.PHONY: $(BIN_OUTDIR)flash.jlink
$(BIN_OUTDIR)flash.jlink:  $(BIN_OUTDIR)$(PROJ_NAME).bin
	@$(ECHO) "si 1" > $@
	@$(ECHO) "device STM32F072RB" >> $@
	@$(ECHO) "speed 4000" >> $@
	@$(ECHO) "erase" >> $@
	@$(ECHO) "loadbin $<, 0x00" >> $@
	@$(ECHO) "r" >> $@
	@$(ECHO) "g" >> $@
	@$(ECHO) "exit" >> $@

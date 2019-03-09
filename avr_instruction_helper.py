# Create EOL comments with AVR instruction descriptions
# @author: Austin Roach <ahroach@gmail.com>
# @category: Instructions.AVR

# Descriptions from Atmega328p datasheet
_AVR_INSTRUCTIONS = \
 {"add": "Add two registers without carry",
  "adc": "Add two registers with carry",
  "adiw": "Add immediate to word",
  "sub": "Subtract two registers",
  "subi": "Subtract constant from register",
  "sbc": "Subtract two registers with carry",
  "sbci": "Subtract constant from register with carry",
  "sbiw": "Subtract immediate from word",
  "and": "Logical AND registers",
  "andi": "Logical AND register and constant",
  "or": "Logical OR registers",
  "ori": "Logical OR register and constant",
  "eor": "Exclusive or registers",
  "com": "Ones complement",
  "neg": "Twos complement",
  "sbr": "Set bit(s) in register",
  "cbr": "Clear bit(s) in register",
  "inc": "Increment",
  "dec": "Decrement",
  "tst": "Test for zero or minus",
  "clr": "Clear register",
  "ser": "Set register",
  "mul": "Multiply unsigned",
  "muls": "Multiply signed",
  "mulsu": "Multiply signed with unsigned",
  "fmul": "Fractional multiply unsigned",
  "fmuls": "Fractional multiply signed",
  "fmulsu": "Fractional multiply signed with unsigned",
  "rjmp": "Relative jump",
  "ijmp": "Indirect jump to (Z)",
  "jmp": "Direct jump",
  "rcall": "Relative subroutine call",
  "icall": "Indirect call to (Z)",
  "call": "Direct subroutine call",
  "ret": "Subroutine return",
  "reti": "Interrupt return",
  "cpse": "Compare, skip if equal",
  "cp": "Compare",
  "cpc": "Compare with carry",
  "cpi": "Compare Register with immediate",
  "sbrc": "Skip if bit in register cleared",
  "sbrs": "Skip if bit in register set",
  "sbic": "Skip if bit in I/O register cleared",
  "sbis": "Skip if bit in I/O register set",
  "brbs": "Branch if status flag set",
  "brbc": "Branch if status flag cleared",
  "breq": "Branch if equal",
  "brne": "Branch if not equal",
  "brcs": "Branch if carry set",
  "brcc": "Branch if carry cleared",
  "brsh": "Branch if same or higher",
  "brlo": "Branch if lower",
  "brmi": "Branch if minus",
  "brpl": "Branch if plus",
  "brge": "Branch if greater or equal, signed",
  "brlt": "Branch if less than, signed",
  "brhs": "Branch if half carry flag set",
  "brhc": "Branch if half carry flag cleared",
  "brts": "Branch if T flag set",
  "brtc": "Branch if T flag cleared",
  "brvs": "Branch if overflow flag set",
  "brvc": "Branch if overflow flag cleared",
  "brie": "Branch if interrupt enabled",
  "brid": "Branch if interrupt disabled",
  "sbi": "Set bit in I/O register",
  "cbi": "Clear bit in I/O register",
  "lsl": "Logical shift left",
  "lsr": "Logical shift right",
  "rol": "Rotate left through carry",
  "ror": "Rotate right through carry",
  "asr": "Arithmetic shift right",
  "swap": "Swap nibbles",
  "bset": "Set flag",
  "bclr": "Clear flag",
  "bst": "Bit store from register to T",
  "bld": "Bit load from T to register",
  "sec": "Set carry",
  "clc": "Clear carry",
  "sen": "Set negative flag",
  "cln": "Clear negative flag",
  "sez": "Set zero flag",
  "clz": "Clear zero flag",
  "sei": "Global interrupt enable",
  "cli": "Global interrupt disable",
  "ses": "Set signed test flag",
  "cls": "Clear signed test flag",
  "sev": "Set twos-complement overflow",
  "clv": "Clear twos-complement overflow",
  "set": "Set T in SREG",
  "clt": "Clear T in SREG",
  "seh": "Set half carry flag",
  "clh": "Clear half carry flag",
  "mov": "Move between registers",
  "movw": "Copy register word",
  "ldi": "Load immediate",
  "ld": "Load indirect",
  "ld+": "Load indirect and post-increment",
  "-ld": "Load indirect and pre-decrement",
  "ldd": "Load indirect with displacement",
  "lds": "Load direct from SRAM",
  "st": "Store indirect",
  "st+": "Store indirect and post-increment",
  "-st": "Store indirect and pre-decrement",
  "std": "Store indirect with displacement",
  "sts": "Store direct from SRAM",
  "lpm": "Load program memory",
  "lpm+": "Load program memory and post-increment",
  "spm": "Store program memory",
  "in": "In from I/O location",
  "out": "Out to I/O location",
  "push": "Push register on stack",
  "pop": "Pop register from stack",
  "nop": "No operation",
  "sleep": "Sleep",
  "wdr": "Watchdog reset",
  "break": "Break"}

def add_eol_comment(comment, addr):
    listing = currentProgram.getListing()
    codeUnit = listing.getCodeUnitAt(addr)
    codeUnit.setComment(codeUnit.EOL_COMMENT, comment)

def get_mnemonic(thisInstr):
    return thisInstr.getPrototype().getMnemonic(thisInstr.getInstructionContext())

def get_operand(thisInstr, opNum):
    return thisInstr.getDefaultOperandRepresentation(opNum)

def add_instr_desc_comment(currInstr):
        currMnemonic = get_mnemonic(currInstr)
        currAddr = currInstr.getInstructionContext().getAddress()

        # Special case to handle pre-decrement/post-increment variants of ld
        if currMnemonic == "ld":
            secondOperand = get_operand(currInstr, 1)

            # '+' is not stored as a second character in the operand, but
            # rather a separator character after the operand. Not sure
            # how common this is...
            if currInstr.getSeparator(2) == "+":
                currMnemonic = "ld+"
            elif len(secondOperand) == 2 and get_operand(currInstr, 1)[0] == "-":
                currMnemonic = "-ld"

        # Special case to handle pre-decrement/post-increment variants of st
        if currMnemonic == "st":
            firstOperand = get_operand(currInstr, 0)
            if len(firstOperand) == 2:
                if get_operand(currInstr, 0)[1] == "+":
                    currMnemonic = "st+"
                elif get_operand(currInstr, 0)[0] == "-":
                    currMnemonic = "-st"

        # Special case to handle pre-decrement/post-increment variants of st
        if currMnemonic == "lpm":
            firstOperand = get_operand(currInstr, 0)
            if len(firstOperand) == 2:
                if get_operand(currInstr, 0)[1] == "+":
                    currMnemonic = "lpm+"

        # Add a comment for the current mnemonic
        add_eol_comment(_AVR_INSTRUCTIONS[currMnemonic], currAddr)

def loop_over_selection():
    # If no selection, try to add a comment for the current address
    if currentSelection is None:
        currInstr = getInstructionAt(currentAddress)
        if currInstr:
            add_instr_desc_comment(currInstr)
        return

    currAddr = currentSelection.getMinAddress()
    currInstr = getInstructionAt(currAddr)
    if not currInstr:
        # There's no instruction at the current address, so try to find one
        # later in the selection
        currInstr = getInstructionAfter(currAddr)
        if not currInstr:
            # We must not have one at all
            return
        currAddr = currInstr.getInstructionContext().getAddress()


    while currAddr < currentSelection.getMaxAddress():
        # Check to be sure that this instruction is in the selection, to handle
        # non-contiguous selection regions
        if currentSelection.contains(currInstr.getInstructionContext().getAddress()):
            add_instr_desc_comment(currInstr)

        currInstr = currInstr.getNext()
        if not(currInstr):
            # No more instructions in the selection
            break

        currAddr = currInstr.getInstructionContext().getAddress()

if __name__ == "__main__":
    loop_over_selection()


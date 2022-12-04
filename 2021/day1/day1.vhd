LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
USE IEEE.STD_LOGIC_TEXTIO.ALL;
USE STD.TEXTIO.ALL;

ENTITY Day1 IS
END Day1;

ARCHITECTURE AoC OF Day1 IS

TYPE INT_ARRAY IS ARRAY (INTEGER RANGE <>) OF INTEGER;

CONSTANT ClkPeriod         : TIME := 10 ns; -- 100 MHz
CONSTANT CompareSize       : INTEGER := 3;

-- Constant to make sure all the inputs are valid
CONSTANT AllValid          : STD_LOGIC_VECTOR(CompareSize-1 DOWNTO 0) := (OTHERS => '1');

SIGNAL CurrInput           : INTEGER := 0;
SIGNAL LastInput           : INTEGER := 0;
SIGNAL NumBigger           : INTEGER := 0;
SIGNAL RecentInputs        : INT_ARRAY(CompareSize-1 DOWNTO 0) := (OTHERS => 0);
SIGNAL PastInputs          : INT_ARRAY(CompareSize-1 DOWNTO 0) := (OTHERS => 0);
SIGNAL RecentSum           : INTEGER := 0;
SIGNAL PastSum             : INTEGER := 0;
SIGNAL NumBigger2          : INTEGER := 0;

-- Vector to make sure the int arrays have been initialized
SIGNAL ValidInput          : STD_LOGIC_VECTOR(CompareSize-1 DOWNTO 0) := (OTHERS => '0');

-- Counting the number of rows to help tell when we are done reading from the file
SIGNAL RowCount            : STD_LOGIC_VECTOR(31 DOWNTO 0) := (OTHERS => '0');

SIGNAL Clk                 : STD_LOGIC := '0';
SIGNAL Start               : STD_LOGIC := '0';
SIGNAL Stop                : STD_LOGIC := '0';

BEGIN

-- Clock Generation
ClkGen : PROCESS
BEGIN
   Clk                     <= '0';
   WAIT FOR ClkPeriod/2;
   Clk                     <= '1';
   WAIT FOR ClkPeriod/2;
END PROCESS;

-- Enable
Enable : PROCESS
BEGIN
   Start                   <= '0';
   WAIT FOR 10 ns;
   WAIT UNTIL RISING_EDGE(Clk);
   Start                   <= '1';
   WAIT;
END PROCESS;

-- Process to read from a file
ReadInput : PROCESS(Clk)
   FILE InputFile          : text IS "input.txt";
   VARIABLE ThisLine       : LINE;
   VARIABLE Number         : INTEGER;
BEGIN
   IF RISING_EDGE(Clk) THEN
      IF START = '1' THEN
         -- Read a line from the file
         IF(NOT ENDFILE(InputFile)) THEN
            RowCount             <= STD_LOGIC_VECTOR(UNSIGNED(RowCount) + 1);
            READLINE(InputFile, ThisLine);
            
            -- Read in the current Input and move over the current input
            READ(ThisLine, Number);
            CurrInput            <= Number;
            LastInput            <= CurrInput;
            
            -- Part 2
            FOR i IN CompareSize-1 DOWNTO 1 LOOP
               RecentInputs(i)   <= RecentInputs(i-1);
            END LOOP;
            RecentInputs(0)      <= Number;
            
            FOR i IN CompareSize-1 DOWNTO 1 LOOP
               PastInputs(i)     <= PastInputs(i-1);
            END LOOP;
            PastInputs(0)        <= CurrInput;
         ELSE
            Stop                 <= '1';
         END IF;
      ELSE
         -- Initial Values
         Stop                    <= '0';
         CurrInput               <= 0;
         LastInput               <= 0;
         RowCount                <= (OTHERS => '0');
         PastInputs              <= (OTHERS => 0);
         RecentInputs            <= (OTHERS => 0);
      END IF;
   END IF;
END PROCESS;


-- Process to check the relative sizes of the file inputs
Compare : PROCESS(Clk)
BEGIN
   IF RISING_EDGE(Clk) THEN
      -- Check if the last input is greater than 0 to avoid counting
      -- the first number as an increase
      IF (CurrInput > LastInput) AND (LastInput > 0) AND (Stop = '0') THEN
         NumBigger               <= NumBigger + 1;
      END IF;
   END IF;
END PROCESS;

CheckValid : FOR i in CompareSize-1 DOWNTO 0 GENERATE
   ValidInput(i)                 <= '1' WHEN(PastInputs(i) > 0) ELSE '0';
END GENERATE;

-- Part 2 Compare logic
ComparePart2 : PROCESS(Clk)
   VARIABLE RunningSum1 : INTEGER := 0;
   VARIABLE RunningSum2 : INTEGER := 0;
BEGIN
   IF RISING_EDGE(Clk) THEN
      -- Sum up the first 3
      RunningSum1                := 0;
      FOR i IN CompareSize-1 DOWNTO 0 LOOP
         RunningSum1             := RunningSum1 + RecentInputs(i);
      END LOOP;
      
      -- Sum up the previous 3
      RunningSum2                := 0;
      FOR i IN CompareSize-1 DOWNTO 0 LOOP
         RunningSum2             := RunningSum2 + PastInputs(i);
      END LOOP;
      
      -- Compare
      IF (RunningSum1 > RunningSum2) AND (ValidInput = AllValid) AND (Stop = '0') THEN
         NumBigger2              <= NumBigger2 + 1;
      END IF;
   END IF;
END PROCESS;

END AoC;
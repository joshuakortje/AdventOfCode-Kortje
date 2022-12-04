
if {$argc != 0} {
   if {$1 == "-refresh"} {
      # Delete the library for a clean start
      vmap -del Day1
      vdel -all -lib work/Day1
   }
}

# Define and map the library
vlib work/Day1
vmap Day1   work/Day1

# Compile
eval vcom -2008 -work Day1 "day1.vhd"

# Simulate
vsim -gui -novopt Day1.day1 -wlf day1.wlf
log -r /*

run 30 us

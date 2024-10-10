#!/bin/bash

path_to_sender='python3 /home/arabella/work/alarm/arduino_ir/send.py' # move to /bin

light() {
    # This function calls the Python script, passing "0x00" 
    # as the address and "0x46" as the command.
    # Any additional arguments passed to the light function 
    # will be forwarded as additional parameters 
    # (e.g., for specifying the --serial_port if needed).
    $path_to_sender "0x00" "0x46" "$@" || 'echo "An error ocured in ${FUNCNAME[0]}";exit 1'
    echo "${FUNCNAME[0]} successfull"
}

# Set light to 3000K color temperature
light_3000k() {
    $path_to_sender "0x00" "0x0C" "$@" || 'echo "An error ocured in ${FUNCNAME[0]}";exit 1'
    echo "${FUNCNAME[0]} successfull"
}

# Set light to 4000K color temperature
light_4000k() {
    $path_to_sender "0x00" "0x18" "$@" || 'echo "An error ocured in ${FUNCNAME[0]}";exit 1'
    echo "${FUNCNAME[0]} successfull"
}

# Set light to 6000K color temperature
light_6000k() {
    echo "Setting color termerature to 6000K"
    $path_to_sender "0x00" "0x5E" "$@" || 'echo "An error ocured in ${FUNCNAME[0]}";exit 1'
    echo "${FUNCNAME[0]} successfull"
    # Command: 6000K color temperature - 0x5E
}

# Increase color temperature repeatedly
light_increase_k() {
    local repetitions=${1:-10}  # Default to 10 if not specified
    local pause=${2:-0}  # Default to 0 if not specified
    for ((i=0; i<repetitions; i++)); do
        $path_to_sender "0x00" "0x09" || 'echo "An error ocured in ${FUNCNAME[0]}";exit 1'
        sleep $pause  # Adjust the delay as needed
    done
    echo "${FUNCNAME[0]} successfull"
    # Command: Increase color temperature (+K) - 0x09
}

# Decrease color temperature repeatedly
light_decrease_k() {
    local repetitions=${1:-10}  # Default to 10 if not specified
    local pause=${2:-0}  # Default to 0 if not specified
    for ((i=0; i<repetitions; i++)); do
        $path_to_sender "0x00" "0x07" || 'echo "An error ocured in ${FUNCNAME[0]}";exit 1'
        sleep $pause
    done
    echo "${FUNCNAME[0]} successfull"

    # Command: Decrease color temperature (-K) - 0x07
}

# Set brightness to 20%
light_20_percent() {
    $path_to_sender "0x00" "0x1C" "$@" || 'echo "An error ocured in ${FUNCNAME[0]}";exit 1'
    echo "${FUNCNAME[0]} successfull"
    # Command: 20% brightness - 0x1C
}

# Set brightness to 50%
light_50_percent() {
    $path_to_sender "0x00" "0x53" "$@" || 'echo "An error ocured in ${FUNCNAME[0]}";exit 1'
    echo "${FUNCNAME[0]} successfull"
    # Command: 50% brightness - 0x53
}

# Set brightness to 100%
light_100_percent() {
    $path_to_sender "0x00" "0x52" "$@" || 'echo "An error ocured in ${FUNCNAME[0]}";exit 1'
    echo "${FUNCNAME[0]} successfull"
    # Command: 100% brightness - 0x52
}

# Increase brightness
light_increase_brightness() {
    $path_to_sender "0x00" "0x40" --repeats 5 || 'echo "An error ocured in ${FUNCNAME[0]}";exit 1'
    echo "${FUNCNAME[0]} successfull"
    # Command: Increase brightness (+Br) - 0x40
}

# Decrease brightness
light_decrease_brightness() {
    $path_to_sender "0x00" "0x19" --repeats 5 || 'echo "An error ocured in ${FUNCNAME[0]}";exit 1'
    echo "${FUNCNAME[0]} successfull"
    # Command: Decrease brightness (-Br) - 0x19
}

# Set brightness to minimum
light_min_brightness() {
    $path_to_sender "0x00" "0x15" "$@" || 'echo "An error ocured in ${FUNCNAME[0]}";exit 1'
    echo "${FUNCNAME[0]} successfull"
    # Command: Minimum brightness (min Br) - 0x15
}

# Switch to next mode
light_next_mode() {
    $path_to_sender "0x00" "0x45" "$@" || 'echo "An error ocured in ${FUNCNAME[0]}";exit 1'
    echo "${FUNCNAME[0]} successfull"
    # Command: Next mode - 0x45
}

# Set a timer
light_timer() {
    $path_to_sender "0x00" "0x47" "$@" || 'echo "An error ocured in ${FUNCNAME[0]}";exit 1'
    echo "${FUNCNAME[0]} successfull"
    # Command: Timer - 0x47
}

    
alarm() {
    rm -rdf >> /home/arabella/work/alarm_log.txt
    touch /home/arabella/work/alarm_log.txt
    # Check if three arguments are provided
    if [ "$#" -ne 1 ]; then
        echo "Usage: $0 <time>"
        echo "Example time: '08:30 AM'"
        exit 1
    fi

    # Store the time, date, address, and command
    TIME=$1
    _TIME=$TIME
    
    # Create a command to send the IR signals using the previous script
    SOURCE_CMD="source /home/arabella/work/alarm/light.sh;"
    REDIRRECT_CMD=">> /home/arabella/work/alarm_log.txt 2>&1"
    # Schedule the command at the specified time and date using 'at'
    echo "bash -c '$SOURCE_CMD light_min_brightness $REDIRRECT_CMD'" | at $TIME
    for (( i = 0; i < 6; i+=1 )); do
        _TIME=$(date '+%H:%M' --date="$_TIME MSK + 5 minutes")
        echo "bash -c '$SOURCE_CMD light_decrease_k $REDIRRECT_CMD'" | at $_TIME
        echo "bash -c '$SOURCE_CMD light_increase_brightness $REDIRRECT_CMD'" | at $_TIME
    done
    
    # Give feedback that the alarm is set
    echo "Alarm set for $TIME"
}
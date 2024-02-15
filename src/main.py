"""! @file main.py

"""

import pyb
import utime
import micropython
import cqueue

#Allocate memory for debug dump
micropython.alloc_emergency_exception_buf(100)

#Define global variables
global square_toggle
global int_queue

square_toggle = 0
time_since_start = 0
pinC0_value = 0

#Setup constants for ADC conversion
REF_VOLT = 3.3
MAX_ADC = 4096

#Define queue maximum size
QUEUE_SIZE = 10
#Setup queue
int_queue = cqueue.IntQueue(QUEUE_SIZE)


def adc_timer_setup(tim_num,frequency):
    """! @brief Setup for the ADC sampling timer

    This function takes in a timer number and frequency, and performs the necessary
    setup functions to generate a timer.
    This timer is used to run the ADC voltage sampling function at a given frequency.
    """
    adc_tim = pyb.Timer(tim_num, freq=frequency)      
    adc_tim.callback(adc_timer_irq)


def square_timer_setup(tim_num,frequency):
    """! @brief Setup for the square wave generation timer

    This function takes in a timer number and frequency, and performs the necessary
    setup functions to generate a timer.
    This timer is used to run the square wave generation flag function at a given frequency.
    """
    sqr_tim = pyb.Timer(tim_num, freq=frequency)      
    sqr_tim.callback(square_timer_irq)


def adc_timer_irq(tim_num):
    """! @brief Interrupt callback function for sampling voltages

    This function is called by the ADC sampling timer and reads the ADC at a given time.
    This value is then added to the queue to be used outside of the callback function.
    """
    int_queue.put(adc0.read())


def square_timer_irq(tim_num):
    """! @brief Interrupt callback function for setting pin states for square wave generation

    This function is called by the square wave generation timer sets a flag at a given rate.
    The flag is then used by the main loop to determine when it is time to toggle the
    pin that generates the square wave.
    """
    global square_toggle
    square_toggle = 1  


def step_response (square_pin: pyb.Pin, ADC_pin: pyb.ADC):
    """! @brief Loop to generate needed outputs

    Reads flag from square wave timer to toggle pin state at the requested interval.
    Reads from adc data queue and converts to mV values to print over serial.
    Performs no functions between either of these tasks.
    """
    global square_toggle
    global sample_en

    time_since_start = 0

    square_pin.value(0)

    while 1:

        if square_toggle and not square_pin.value(): #If the square wave is low -> high
            square_toggle = 0
            square_pin.value(not square_pin.value())
            time_since_start = 0
        
        elif square_toggle:
            break


        if int_queue.any():
            voltage = (int_queue.get()/MAX_ADC) * REF_VOLT
            print(str(time_since_start) + "," + str(voltage))
            time_since_start += 10


if __name__ == "__main__":

    #Setup pin to read voltages from
    adc0 = pyb.ADC(pyb.Pin.board.PC1)

    #Setup Pin C0
    pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

    #Setup adc timer
    adc_timer_setup(4,100)

    #Setup square wave timer
    square_timer_setup(5,0.2)

    #Begin main loop
    step_response(pinC0, adc0)


"""
ENCODER1_TIMER_NUMBER = 4

ENCODER2_TIMER_NUMBER = 8

if __name__ == "__main__":
    encoder1 = encoder_reader.Encoder(pyb.Pin.board.PB6,pyb.Pin.board.PB7,ENCODER1_TIMER_NUMBER,pyb.Pin.AF2_TIM4)

    encoder2 = encoder_reader.Encoder(pyb.Pin.board.PC6,pyb.Pin.board.PC7,ENCODER2_TIMER_NUMBER,pyb.Pin.AF3_TIM8)

    position1 = 0
    position2 = 0

    while 1:
        position1 = encoder1.read()
        position2 = encoder2.read()
        print( "Encoder1: " + str(position1) + " | Encoder2: " + str(position2) )


        """


"""
import pyb
import time
from motor_driver import MotorDriver as Motor

sleep_time_ms = 10
bright_loop_time_ms = 5000

LED_max_brightness = 100

if __name__ == "__main__":

    en_pin = pyb.Pin.board.PC1
    in1b_pin = pyb.Pin.board.PA1
    in1a_pin = pyb.Pin.board.PA0

    motor = Motor(en_pin, 
                  in1a_pin, 2, 1,
                  in1b_pin, 2, 2,
                  30000)


    motor.set_enable(1)


    try:

        while 1:
        
            motor.set_duty_cycle(10)
            time.sleep(1)
            motor.set_duty_cycle(100)
            time.sleep(1)
            motor.set_duty_cycle(0)
            time.sleep(1)
            motor.set_duty_cycle(-10)
            time.sleep(1)
            motor.set_duty_cycle(-100)
            time.sleep(1)

    except KeyboardInterrupt:
        motor.set_duty_cycle(0)
        motor.set_enable(0)
        print("Program Ended")


"""
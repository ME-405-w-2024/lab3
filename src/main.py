"""! @file main.py

"""

import pyb
import utime
import micropython
import PID_controller
from motor_driver import MotorDriver as Motor
import encoder_reader
import platform

if "MicroPython" not in platform.platform():
    from me405_support import cotask, cqueue

#Allocate memory for debug dump
micropython.alloc_emergency_exception_buf(100)

TASK_DELAY_MS = 10

#Define global variables
global square_toggle
global int_queue

square_toggle = 0
time_since_start = 0
pinC0_value = 0


ENCODER1_TIMER_NUMBER = 4

TIMEOUT_MS = 2000


if __name__ == "__main__":

    # #Begin main loop
    # step_response(pinC0, adc0)
    



    encoder1 = encoder_reader.Encoder(pyb.Pin.board.PB6,pyb.Pin.board.PB7,ENCODER1_TIMER_NUMBER,pyb.Pin.AF2_TIM4)

    #encoder2 = encoder_reader.Encoder(pyb.Pin.board.PC6,pyb.Pin.board.PC7,ENCODER2_TIMER_NUMBER,pyb.Pin.AF3_TIM8)

    


    en_pin = pyb.Pin.board.PC1
    in1b_pin = pyb.Pin.board.PA1
    in1a_pin = pyb.Pin.board.PA0


    motor = Motor(en_pin, 
                  in1a_pin, 2, 1,
                  in1b_pin, 2, 2,
                  30000)

    position1 = 0
    
    motor.set_enable(1)
    motor.set_duty_cycle(0)

    step_target = 16384

    target_range = 500

    p_controller1 = PID_controller.PIDController(Kp=0.005, init_target=step_target)

    done = False



    try:

        while 1:

            if pyb.USB_VCP().any():
                serial_value = pyb.USB_VCP().read()

                recieved_Kp = float(serial_value.decode().strip('\n'))

                #print(recieved_Kp)
                p_controller1.set_Kp(recieved_Kp)

                start_time = utime.ticks_ms()

                done = False

                encoder1.zero()

                current_time_ms_appx = 0

                position_values = []
                time_values = []

                last_time = start_time

                while not done:

                    if (utime.ticks_ms() - last_time) >= TASK_DELAY_MS :

                        current_time_ms_appx += (utime.ticks_ms() - last_time)

                        last_time = utime.ticks_ms()

                        position1 = encoder1.read()

                        control1_value = p_controller1.run(position1)

                        motor.set_duty_cycle(int(control1_value))

                        #print(step_target-position1)
                        
                        position_values.append(position1)

                        time_values.append(current_time_ms_appx)

                    """abs(step_target-position1) < target_range or""" 
                    if (utime.ticks_ms()-start_time) > TIMEOUT_MS:
                        done = True
                        print("Done")


                for idx,value in enumerate(time_values):
                    print(str(value) + "," + str(position_values[idx]))

                
                
    
            motor.set_duty_cycle(0)
            utime.sleep_ms(TASK_DELAY_MS)



            # if int_queue.any():
            #     voltage = (int_queue.get()/MAX_ADC) * REF_VOLT
            #     print(str(time_since_start) + "," + str(voltage))
            #     time_since_start += TASK_DELAY_MS
        
    except KeyboardInterrupt:
        motor.set_duty_cycle(0)
import pyb

  
AUTO_RELOAD_VALUE = 10000


class Encoder:

    def __init__ (self, 
                  inApin: pyb.Pin.board,
                  inBpin: pyb.Pin.board,
                  timer_num: int,
                  af_mode: int
                  ):
        """! 
            Creates an encoder timer that counts
            @param inApin Pyboard pin used to read encoder channel A
            @param inBpin Pyboard pin used to read encoder channel B
            @param timer_num Timer number associated with pin alternate functions
            @param af_mode Alternate function timer to use
        """

        encA_pin = pyb.Pin(inApin, mode=pyb.Pin.AF_PP, af=af_mode)
        encB_pin = pyb.Pin(inBpin, mode=pyb.Pin.AF_PP, af=af_mode)
        self.enc_timer = pyb.Timer(timer_num, prescaler=0, period=AUTO_RELOAD_VALUE-1)
        
        timer_channel = self.enc_timer.channel(1,pyb.Timer.ENC_AB)

        self.zero()
    

    def read(self):

        """! 
            Read the current position
            @return Position since last zero
        """        

        current_count = self.enc_timer.counter()

        count_delta = self.last_count - current_count

        if(abs(count_delta) > AUTO_RELOAD_VALUE/2):

            if(count_delta < 0):
                count_delta += AUTO_RELOAD_VALUE-1

            else:
                count_delta -= AUTO_RELOAD_VALUE-1

        self.last_count = current_count

        self.position += count_delta

        return self.position
    

    def zero(self):

        """! 
            Zeros out the position reading
        """

        self.last_count = 0
        self.position = 0
        self.enc_timer.counter(0)
        


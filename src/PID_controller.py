
class PIDController:

    def __init__(self, Kp, init_target, **kwargs):
        self.Kp = Kp
        self.Ki = kwargs.get('Ki', 0)
        self.Kd = kwargs.get('Kd', 0)
        self.Kf = kwargs.get('Kf', 0)
        self.target_value = init_target


    def set_setpoint():
        #TODO
        pass

    def set_Kp():
        #TODO
        pass

    def set_Ki():
        #TODO
        pass

    def set_Kd():
        #TODO
        pass

    def set_Kf():
        #TODO
        pass

    def run():
        #TODO
        pass
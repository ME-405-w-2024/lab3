
class PIDController:

    def __init__(self, Kp, init_target, **kwargs):
        self.Kp = Kp
        self.Ki = kwargs.get('Ki', 0)
        self.Kd = kwargs.get('Kd', 0)
        self.Kf = kwargs.get('Kf', 0)
        self.target_value = init_target


    def set_setpoint(self, target):
        self.target_value = target

    def set_Kp(self, Kp):
        self.Kp = Kp

    def set_Ki():
        #TODO
        pass

    def set_Kd():
        #TODO
        pass

    def set_Kf():
        #TODO
        pass

    def run(self, current_value):

        #proportional control
        control_value = (current_value - self.target_value) * self.Kp
        
        return control_value
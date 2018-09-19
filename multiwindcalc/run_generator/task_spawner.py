

class TaskSpawner:
    """Base class task spawner"""

    def spawn(self):
        """Create new derivative of luigi.Task for later execution"""
        raise NotImplementedError()

    def branch(self, branch_id=None):
        """Deep copy task input and dependencies so that they can be edited without affecting trunk object"""
        raise NotImplementedError()


class AeroelasticSimulationSpawner:
    """Spawner of aeroelastic simulations of wind turbines including pre-processing dependencies"""

    # Simulation options
    @property
    def output_start_time(self):
        raise NotImplementedError()

    @output_start_time.setter
    def output_start_time(self, time):
        raise NotImplementedError()

    @property
    def simulation_time(self):
        """Total simulation time in seconds"""
        raise NotImplementedError()

    @simulation_time.setter
    def simulation_time(self):
        raise NotImplementedError()

    @property
    def operation_mode(self):
        raise NotImplementedError()

    @operation_mode.setter
    def operation_mode(self, mode):
        """
        Operation mode:
        'normal' - power production run with generator on and rotor free
        'idling' - generator off but rotor free
        'parked' - generator off and rotor fixed
        """
        raise NotImplementedError()

    # Initial Conditions
    @property
    def initial_rotor_speed(self):
        """Rotor speed at start of simulation in rpm"""
        raise NotImplementedError()

    @initial_rotor_speed.setter
    def initial_rotor_speed(self, rotor_speed):
        raise NotImplementedError()

    @property
    def initial_azimuth(self):
        """Rotor azimuth of blade 1 at start of simulation in degrees"""
        raise NotImplementedError

    @initial_azimuth.setter
    def initial_azimuth(self, azimuth):
        raise NotImplementedError()

    @property
    def initial_yaw_angle(self):
        """Nacelle yaw angle at start of simulation in degrees; clockwise from North"""
        raise NotImplementedError()

    @initial_yaw_angle.setter
    def initial_yaw_angle(self, angle):
        raise NotImplementedError()

    @property
    def initial_pitch_angle(self):
        raise NotImplementedError()

    @initial_pitch_angle.setter
    def initial_pitch_angle(self, angle):
        """Sets pitch angle for all blades at start of simulation; in degrees, positive towards feather"""
        raise NotImplementedError()

    # Wind properties
    @property
    def wind_speed(self):
        """Mean wind speed in m/s"""
        raise NotImplementedError()

    @wind_speed.setter
    def wind_speed(self, wind_speed):
        raise NotImplementedError()

    @property
    def turbulence_intensity(self):
        """Turbulence intensity as a fraction (not %): ratio of wind speed standard deviation to mean wind speed"""
        raise NotImplementedError()

    @turbulence_intensity.setter
    def turbulence_intensity(self, turbulence_intensity):
        raise NotImplementedError()

    @property
    def turbulence_seed(self):
        """Random number seed for turbulence generation"""
        raise NotImplementedError()

    @turbulence_seed.setter
    def turbulence_seed(self, seed):
        raise NotImplementedError()

    @property
    def wind_shear(self):
        """Vertical wind shear exponent"""
        raise NotImplementedError()

    @wind_shear.setter
    def wind_shear(self, exponent):
        raise NotImplementedError()

    @property
    def upflow(self):
        """Wind inclination in degrees from the horizontal"""
        raise NotImplementedError()

    @upflow.setter
    def upflow(self, angle):
        raise NotImplementedError()

    # Properties of turbine, for which setting is not supported
    @property
    def number_of_blades(self):
        raise NotImplementedError()

"""Defines the turbsim spawner
"""
from os import path, getcwd, makedirs
import copy

from multiwindcalc.plugins.wind import WindGenerationSpawner

from .tasks import WindGenerationTask


class TurbsimSpawner(WindGenerationSpawner):
    """Spawns TurbSim wind generation tasks"""

    def __init__(self, turbsim_input, outdir):
        self._input = turbsim_input
        self._outdir = outdir

    def spawn(self, _path_, metadata):
        input_hash = self._input.hash()
        wind_input_file = path.join(path.join(self._outdir, input_hash), 'wind.ipt')
        if not path.isdir(path.dirname(wind_input_file)):
            makedirs(path.dirname(wind_input_file))
        self._input.to_file(wind_input_file)
        wind_task = WindGenerationTask('wind ' + input_hash, wind_input_file, _metadata=metadata)
        return wind_task

    def branch(self):
        branched_spawner = copy.copy(self)
        branched_spawner._input = copy.deepcopy(self._input)
        return branched_spawner

    def get_simulation_time(self):
        return self._input['AnalysisTime']

    def set_simulation_time(self, time):
        self._input['AnalysisTime'] = time
        self._input['UsableTime'] = time

    def get_wind_speed(self):
        return float(self._input['URef'])

    def set_wind_speed(self, value):
        self._input['URef'] = value

    def get_turbulence_intensity(self):
        """Turbulence intensity as a fraction (not %): ratio of wind speed standard deviation to mean wind speed"""
        return float(self._input['IECturbc']) / 100

    def set_turbulence_intensity(self, turbulence_intensity):
        self._input['IECturbc'] = turbulence_intensity * 100

    def get_turbulence_seed(self):
        """Random number seed for turbulence generation"""
        return int(self._input['RandSeed1'])

    def set_turbulence_seed(self, seed):
        self._input['RandSeed1'] = seed

    def get_wind_shear(self):
        """Vertical wind shear exponent"""
        exponent = self._input['PLExp']
        return float('NaN') if exponent == 'default' else float(exponent)

    def set_wind_shear(self, exponent):
        self._input['PLExp'] = exponent

    def get_upflow(self):
        """Wind inclination in degrees from the horizontal"""
        return float(self._input['VFlowAng'])

    def set_upflow(self, angle):
        self._input['VFlowAng'] = angle
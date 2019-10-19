from os import path
import copy

from ..tasks import SimulationTask
from ..simulation_inputs import SimulationInput
from .task_spawner import TaskSpawner


class SingleInputFileSpawner(TaskSpawner):
    """Runs bespoke executable taking a single input file as its only command line argument"""

    def __init__(self, simulation_input, file_name):
        """Create a instance of :class:`SingleInputFileSpawner`

        :param simulation_input: Simulation input file write
        :type simulation_input: :class:`SimulationInput`
        :param file_name: Name of input file for simulation, including extension but excluding path
        :type file_name: str
        """
        if not isinstance(simulation_input, SimulationInput):
            raise TypeError("simulation_input must be of type SimulationInput")
        self._simulation_input = simulation_input
        self._file_name = file_name

    def spawn(self, path_, metadata):
        input_file_path = path.join(path_, self._file_name)
        self._simulation_input.to_file(input_file_path)
        return SimulationTask(_id=path_,
                              _input_file_path=input_file_path,
                              _metadata=metadata)

    def branch(self):
        return SingleInputFileSpawner(copy.deepcopy(self._simulation_input), self._file_name)

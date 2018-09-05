from os import path
import numpy as np
from ..component_tests import example_data_folder, create_spawner
from multiwindcalc.run_generator.generate_tasks import generate_tasks_from_spec
from multiwindcalc.run_generator.tasks import SimulationTask, WindGenerationTask
from multiwindcalc.parsers import *


def test_can_create_1d_set_of_aeroelastic_tasks(tmpdir):
    spawner = create_spawner(tmpdir.strpath)
    run_spec = {'wind_speed': list(np.arange(4.0, 15.0, 2.0))}
    root_node = SpecificationNodeParser().parse(run_spec)
    tasks = generate_tasks_from_spec(spawner, root_node)
    assert len(tasks) == 6
    for t in tasks:
        assert isinstance(t, SimulationTask)
        assert len(t.requires()) == 1
        assert isinstance(t.requires()[0], WindGenerationTask)
        assert path.isdir(path.split(t.run_name_with_path)[0])
        assert tmpdir.strpath in t.run_name_with_path
        assert 'wind_speed' in t.metadata


def test_can_create_runs_from_tree_spec(tmpdir):
    spawner = create_spawner(tmpdir.strpath)
    input_path = path.join(example_data_folder, 'iec_fatigue_spec.json')
    spec_model = SpecificationParser(SpecificationFileReader(input_path)).parse()
    runs = generate_tasks_from_spec(spawner, spec_model.root_node)
    assert len(runs) == 12*3*6 + 12*2*6 + 12*3*6
    for t in runs:
        assert isinstance(t, SimulationTask)
        assert len(t.requires()) == 1
        assert isinstance(t.requires()[0], WindGenerationTask)
        assert path.isdir(path.split(t.run_name_with_path)[0])
        assert tmpdir.strpath in t.run_name_with_path
        assert 'wind_speed' in t.metadata
        assert 'turbulence_seed' in t.metadata
        assert 'wind_direction' in t.metadata

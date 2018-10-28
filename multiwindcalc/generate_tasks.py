from multiwindcalc.util import PathBuilder

from multiwindcalc.specification.specification import SpecificationNode

from multiwindcalc.util import TypedProperty

def generate_tasks(task_spawner, run_list):
    """Generate list of luigi.Task for a flat 1D run list"""
    tasks = []
    for run in run_list:
        branch = task_spawner.branch()
        for k, v in run.items():
            setattr(branch, k, v)
        task = branch.spawn()
        task.metadata.update(run)
        tasks.append(task)
    return tasks

def _check_type(task_spawner, name, value):
    if hasattr(type(task_spawner), name):
        attribute = getattr(type(task_spawner), name)
        if isinstance(attribute, TypedProperty):
            expected_type = attribute.type
            if not isinstance(value, expected_type):
                value = expected_type(value)
    return value

def _is_ghost(property_name):
    return property_name[0] == '_'

def _deghost(property_name):
    return property_name[1:]

def generate_tasks_from_spec(task_spawner, node, base_path):
    """Generate list of luigi.Task for a multiwindcalc.SpecificationNode"""
    if not isinstance(node, SpecificationNode):
        raise ValueError('node must be of type ' + SpecificationNode.__name__)
    if not node.is_root:
        value = _check_type(task_spawner, node.property_name, node.property_value)
        if _is_ghost(node.property_name):
            task_spawner.update_meta_property(_deghost(node.property_name))
        else:
            setattr(task_spawner, node.property_name, value)
    if not node.children:   # (leaf)
        task = task_spawner.spawn(str(PathBuilder(base_path).join(node.path)), node.collected_properties)
        return [task]
    else:   # (branch)
        tasks = []
        for child in node.children:
            branch = task_spawner.branch()
            tasks += generate_tasks_from_spec(branch, child, base_path)
        return tasks
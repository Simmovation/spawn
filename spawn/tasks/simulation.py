# spawn
# Copyright (C) 2018, Simmovation Ltd.
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
"""luigi Tasks
"""
from collections import Mapping
import subprocess
import traceback
import os
from os import path
import logging
import luigi
import json

from spawn.runners import ProcessRunner

LOGGER = logging.getLogger(__name__)

class _TaskEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Mapping):
            return dict(obj.items())
        return super().default(obj)

class TaskListParameter(luigi.Parameter):
    """Implementation of :class:`luigi.Parameter` to allow definitions of multiple tasks as dependencies
    """
    def parse(self, input):
        input_dicts = json.loads(input)
        return [luigi.task_register.Register.get_task_cls(i['family'])(**i['params']) for i in input_dicts]
    
    def serialize(self, clss):
        tasks = []
        for c in clss:
            if not isinstance(c, luigi.Task):
                continue
            task = {
                'family': c.get_task_family(),
                'params': {}
            }
            for param_name, _param_obj in c.get_params():
                if hasattr(c, param_name):
                    task['params'][param_name] = getattr(c, param_name)
            tasks.append(task)
        return json.dumps(tasks, cls=_TaskEncoder)

class SimulationTask(luigi.Task):
    """Implementation of :class:`luigi.Task`
    """
    _id = luigi.Parameter()
    _input_file_path = luigi.Parameter()
    _runner_type = luigi.Parameter()
    _metadata = luigi.DictParameter(default={})
    _exe_path = luigi.Parameter()
    _dependencies = TaskListParameter(default=[])
    _working_dir = luigi.Parameter(default=None)

    def run(self):
        """Run this task
        """
        self._create_runner().run()
    
    def complete(self):
        """Determine if this task is complete

        :returns: ``True`` if this task is complete; otherwise ``False``
        :rtype: bool
        """
        return self._create_runner().complete()

    def on_failure(self, exception):
        """Interprets any exceptions raised by the run method.
        
        Attempts to find any logs associated with the runner.

        :returns: A string representation of the error.
        :rtype: str
        """
        runner = self._create_runner()
        all_logs = []
        error_logs = runner.error_logs()
        if error_logs:
            all_logs.append('Error logs:\n\n{}'.format(error_logs))
        logs = runner.logs()
        if logs:
            all_logs.append('Logs:\n\n{}'.format(logs))
        if all_logs:
            return '\n\n'.join(all_logs)
        error_string = traceback.format_exception(type(exception), exception, exception.__traceback__)
        return 'Unhandled exception running task:\n\n{}'.format(''.join(error_string))

    def requires(self):
        """The prerequisites for this task
        """
        return self._dependencies

    @property
    def run_name_with_path(self):
        """Return the run name of this task
        """
        return path.splitext(self._input_file_path)[0]

    @property
    def metadata(self):
        """Metadata for this task
        """
        return self._metadata

    def _create_runner(self):
        if self._runner_type not in self.available_runners:
            raise ValueError('could not find runner for runner_type {} and task type {}'.format(self._runner_type, type(self)))
        return self.available_runners[self._runner_type](self._id, self._input_file_path,
                                                         exe_path=self._exe_path, cwd=self._working_dir)

    @property
    def available_runners(self):
        """Runners available for this task.

        Can be overridden by derived tasks
        """
        return {
            'process': ProcessRunner
        }
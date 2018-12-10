# multiwindcalc
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
""":mod:`multiwindcalc` scheduler for luigi
"""
from luigi import build, configuration

from multiwindcalc import __name__ as APP_NAME
from multiwindcalc.generate_tasks import generate_tasks_from_spec

class LuigiScheduler:
    """Scheduler implementation for Luigi

    Because this is currently the only scheduler implementation it's probable
    that the interface will evolve in time.
    """
    def __init__(self, config):
        """Initialise the :class:`LuigiScheduler`

        :param config: Configuration object
        :type config: :class:`ConfigurationBase`

        Config Values
        =============
        workers             The number of workers (int)
        outdir              The output directory (path-like)
        local               ``True`` if running locally; otherwise, ``False``. (bool)
        port                The port on which the remote scheduler is running, if ``local`` is ``False``. (int)
        """
        self._workers = config.get(APP_NAME, 'workers')
        self._out_dir = config.get(APP_NAME, 'outdir')
        self._local = config.get(APP_NAME, 'local', type=bool)
        self._port = config.get('server', 'port', type=int)

    def run(self, spawner, spec):
        """Run the spec by generating tasks using the spawner
        
        :param spawner: The task spawner
        :type spawner: :class:`TaskSpawner`
        :param spec: The specification
        :type spec: :class:`SpecificationModel`
        """
        tasks = generate_tasks_from_spec(spawner, spec.root_node, self._out_dir)
        build(tasks, local_scheduler=self._local, workers=self._workers, scheduler_port=self._port)

# Copyright 2021 Croix Bleue du Québec

# This file is part of python-devops-sccs.

# python-devops-sccs is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# python-devops-sccs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with python-devops-sccs.  If not, see <https://www.gnu.org/licenses/>.

class Context(object):
    """
    Context permits to communicate with a source code control system for a specific session.
    A session is an abstract concept that can hold nothing or any object type understandable by the plugin which issued it.
    """

    UUID_WATCH_CONTINOUS_DEPLOYMENT_CONFIG="a7d7cba8-1a49-426c-9811-29022aca1a5a"
    UUID_WATCH_CONTINUOUS_DEPLOYMENT_VERSIONS_AVAILABLE="40e9a2d5-fc22-497e-a364-d19115321ba2"
    UUID_WATCH_CONTINUOUS_DEPLOYMENT_ENVIRONMENTS_AVAILABLE="7f7cd008-3350-47b7-80ce-9472e3a649c1"

    def __init__(self, session, plugin, core):
        self.session = session
        self.plugin = plugin
        self._core = core
    
    async def passthrough(self, request, args=None):
        """Passthough

        see plugin.py for function description
        """
        return await self.plugin.passthrough(self.session, request, args)
    
    async def get_repositories(self, args=None):
        """Get a list of repositories
        
        see plugin.py for function description
        """
        return await self.plugin.get_repositories(self.session, args)

    async def get_repository_permissions(self, repository, args=None):
        """Get permissions for a specific repository
        
        see plugin.py for function description
        """
        return await self.plugin.get_repository_permissions(self.session, repository, args)

    async def get_all_repositories_permissions(self, args=None):
        """Get permisions for all accessible repositories
        
        see plugin.py for function description
        """
        return await self.plugin.get_all_repositories_permissions(self.session, args)

    async def get_continuous_deployment_config(self, repository, environments=None, args=None):
        """Get continuous deployment configuration

        see plugin.py for function description
        """
        return await self.plugin.get_continuous_deployment_config(self.session, repository, environments, args)

    def watch_continuous_deployment_config(self, repository, environments=None, args=None, poll_interval=60):
        """Watch for get_continuous_deployment_config"""

        def filtering_by_environment(event):
            if environments and event.value.environment not in environments:
                return False
            return True

        return self._core.scheduler.watch(
            (Context.UUID_WATCH_CONTINOUS_DEPLOYMENT_CONFIG, repository),
            poll_interval,
            self.get_continuous_deployment_config,
            filtering=filtering_by_environment,
            repository=repository,
            args=args
        )

    async def get_continuous_deployment_versions_available(self, repository, args=None):
        """Get continuous deployment versions available

        see plugin.py for function description
        """
        return await self.plugin.get_continuous_deployment_versions_available(self.session, repository, args)

    def watch_continuous_deployment_versions_available(self, repository, args=None, poll_interval=120):
        """watch for get_continuous_deployment_versions_available"""

        return self._core.scheduler.watch(
            (Context.UUID_WATCH_CONTINUOUS_DEPLOYMENT_VERSIONS_AVAILABLE, repository),
            poll_interval,
            self.get_continuous_deployment_versions_available,
            repository=repository,
            args=args
        )

    async def trigger_continuous_deployment(self, repository, environment, version, args=None):
        """Trigger a continuous deployment

        see plugin.py for function description
        """
        result = await self.plugin.trigger_continuous_deployment(self.session, repository, environment, version, args)

        self._core.scheduler.notify(
            (Context.UUID_WATCH_CONTINOUS_DEPLOYMENT_CONFIG, repository)
        )

        return result

    async def get_continuous_deployment_environments_available(self, repository, args=None):
        """List all environments that can be used to run the application

        see plugin.py for function description
        """
        return await self.plugin.get_continuous_deployment_environments_available(self.session, repository, args)

    def watch_continuous_deployment_environments_available(self, repository, args=None, poll_interval=120):
        """watch for get_continuous_deployment_environments_available"""

        return self._core.scheduler.watch(
            (Context.UUID_WATCH_CONTINUOUS_DEPLOYMENT_ENVIRONMENTS_AVAILABLE, repository),
            poll_interval,
            self.get_continuous_deployment_environments_available,
            repository=repository,
            args=args
        )

    async def bridge_repository_to_namespace(self, repository, environment, untrustable=True, args=None):
        """Bridge repository/environment to a kubernetes namespace

        see plugin.py for function description
        """
        return await self.plugin.bridge_repository_to_namespace(self.session, repository, environment, untrustable, args)

    def get_add_repository_contract(self):
        """Get the contract to add a new repository.
        """
        return self._core.provision.get_add_repository_contract()

    async def add_repository(self, repository, template,  template_params, args=None):
        """Add a new repository

        see plugin.py for function description
        """
        return await self.plugin.add_repository(self.session, self._core.provision, repository, template,  template_params, args)

    async def compliance(self, remediation=False, report=False, args=None):
        """Check if all repositories are compliants

        see plugin.py for function description
        """
        return await self.plugin.compliance(self.session, remediation, report, args)

    async def compliance_report(self, args=None):
        """Provides a compliance report about all repositories

        see plugin.py for function description
        """
        return await self.plugin.compliance_report(self.session, args)

    async def compliance_repository(self, repository, remediation=False, report=False, args=None):
        """Check if a repository is compliant

        see plugin.py for function description
        """
        return await self.plugin.compliance_repository(self.session, repository, remediation, report, args)

    async def compliance_report_repository(self, repository, args=None):
        """Provides a compliance report for the repository

        see plugin.py for function description
        """
        return await self.plugin.compliance_report_repository(self.session, repository, args)
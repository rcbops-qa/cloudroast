"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from unittest2.suite import TestSuite

from cafe.drivers.unittest.decorators import tags
from cloudcafe.common.tools.datagen import rand_name
from cloudcafe.compute.common.types import NovaServerStatusTypes


from cloudroast.compute.fixtures import ComputeFixture


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(CreateServerBurnIn("test_create_server"))
    suite.addTest(CreateServerBurnIn("test_can_ping_created_server"))
    return suite


class CreateServerBurnIn(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(CreateServerBurnIn, cls).setUpClass()
        cls.server = cls.server_behaviors.create_active_server().entity
        cls.resources.add(cls.server.id, cls.servers_client.delete_server)

    @tags(type='burn-in', net='no')
    def test_create_server(self):
        self.server_behaviors.wait_for_server_status(
            self.server.id, NovaServerStatusTypes.ACTIVE)

    @tags(type='burn-in', net='yes')
    def test_can_ping_created_server(self):
        server = self.servers_client.get_server(self.server.id).entity
        if self.images_config.primary_image_default_pass is not None:
            password = self.images_config.primary_image_default_pass
        remote_client = self.server_behaviors.get_remote_instance_client(
            server, self.servers_config, password=password)
        self.assertTrue(remote_client.can_authenticate())

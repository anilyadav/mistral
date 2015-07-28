# Copyright 2015 Huawei Technologies Co., Ltd.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from oslo_config import cfg

from mistral.tests import base
from mistral.utils import coordination


class CoordinationTest(base.BaseTest):
    def setUp(self):
        super(CoordinationTest, self).setUp()

    def test_start(self):
        cfg.CONF.set_default(
            'backend_url',
            'zake://',
            'coordination'
        )

        coordinator = coordination.ServiceCoordinator('fake_id')
        coordinator.start()

        self.assertTrue(coordinator.is_active())

    def test_start_without_backend(self):
        cfg.CONF.set_default('backend_url', None, 'coordination')

        coordinator = coordination.ServiceCoordinator()
        coordinator.start()

        self.assertFalse(coordinator.is_active())

    def test_stop_not_active(self):
        cfg.CONF.set_default('backend_url', None, 'coordination')

        coordinator = coordination.ServiceCoordinator()
        coordinator.start()

        coordinator.stop()

        self.assertFalse(coordinator.is_active())

    def test_stop(self):
        cfg.CONF.set_default(
            'backend_url',
            'zake://',
            'coordination'
        )

        coordinator = coordination.ServiceCoordinator()
        coordinator.start()

        coordinator.stop()

        self.assertFalse(coordinator.is_active())

    def test_join_group_not_active(self):
        cfg.CONF.set_default('backend_url', None, 'coordination')

        coordinator = coordination.ServiceCoordinator()
        coordinator.start()

        coordinator.join_group('fake_group')
        members = coordinator.get_members('fake_group')

        self.assertFalse(coordinator.is_active())

        self.assertEqual(0, len(members))

    def test_join_group_and_get_members(self):
        cfg.CONF.set_default(
            'backend_url',
            'zake://',
            'coordination'
        )

        coordinator = coordination.ServiceCoordinator(my_id='fake_id')
        coordinator.start()

        coordinator.join_group('fake_group')
        members = coordinator.get_members('fake_group')

        self.assertEqual(1, len(members))
        self.assertItemsEqual(('fake_id',), members)

    def test_join_group_and_leave_group(self):
        cfg.CONF.set_default(
            'backend_url',
            'zake://',
            'coordination'
        )

        coordinator = coordination.ServiceCoordinator(my_id='fake_id')
        coordinator.start()

        coordinator.join_group('fake_group')
        members_before = coordinator.get_members('fake_group')

        coordinator.leave_group('fake_group')
        members_after = coordinator.get_members('fake_group')

        self.assertEqual(1, len(members_before))
        self.assertEqual(set(['fake_id']), members_before)

        self.assertEqual(0, len(members_after))
        self.assertEqual(set([]), members_after)
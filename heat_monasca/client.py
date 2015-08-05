#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_utils import importutils

from heat.common import exception as heat_exc
from heat.engine.clients import client_plugin
from heat.engine import constraints

client = importutils.try_import('monascaclient.client')
monasca_exc = importutils.try_import('monascaclient.exc')

SERVICE_NAME = 'monasca'


class MonascaClientPlugin(client_plugin.ClientPlugin):
    exceptions_module = [monasca_exc]
    service_types = [MONITORING] = ['monitoring']

    VERSION = '2_0'

    @staticmethod
    def is_available():
        return client is not None

    # Below function is copied from common.client_plugin in liberty
    def _get_client_args(self,
                         service_name,
                         service_type):
        endpoint_type = self._get_client_option(service_name,
                                                'endpoint_type')
        endpoint = self.url_for(service_type=service_type,
                                endpoint_type=endpoint_type)
        args = {
            'auth_url': self.context.auth_url,
            'service_type': service_type,
            'project_id': self.context.tenant_id,
            'token': lambda: self.auth_token,
            'endpoint_type': endpoint_type,
            'os_endpoint': endpoint,
            'cacert': self._get_client_option(service_name, 'ca_file'),
            'cert_file': self._get_client_option(service_name, 'cert_file'),
            'key_file': self._get_client_option(service_name, 'key_file'),
            'insecure': self._get_client_option(service_name, 'insecure')
        }

        return args

    def _create(self):
        args = self._get_client_args(service_name=SERVICE_NAME,
                                     service_type=self.MONITORING)

        return client.Client(
            self.VERSION,
            endpoint=args['os_endpoint'],
            endpoint_type=args['endpoint_type'],
            auth_url=args['auth_url'],
            token=args['token'](),
            project_id=args['project_id'],
            service_type=args['service_type'],
            os_cacert=args['cacert'],
            cert_file=args['cert_file'],
            key_file=args['key_file'],
            insecure=args['insecure']
        )

    def is_not_found(self, ex):
        return isinstance(ex, monasca_exc.NotFound)

    def get_notification(self, notification):
        try:
            return self.client().notifications.get(
                notification_id=notification)['id']
        except monasca_exc.NotFound:
            # Monasca does not support to filter notifications based on the
            # name, as well it does not allow same named notifications
            for n in self.client().notifications.list():
                if n['name'] == notification:
                    return n['id']

        raise heat_exc.EntityNotFound(entity='Monasca Notification',
                                      name=notification)


class MonascaNotificationConstraint(constraints.BaseCustomConstraint):

    expected_exceptions = (heat_exc.EntityNotFound)

    def validate_with_client(self, client, notification):
        client.client_plugin(SERVICE_NAME).get_notification(notification)
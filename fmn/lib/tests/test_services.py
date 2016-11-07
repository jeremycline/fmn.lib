import unittest

from twisted.application.internet import ClientService

from fmn.lib import services


class AmqpServiceTests(unittest.TestCase):

    def test_create_amqp_service(self):
        """
        Basic test to assert create_amqp_service produces a Twisted service.
        """
        amqp_service = services.create_amqp_service('tcp:localhost:5672')
        self.assertTrue(isinstance(amqp_service, ClientService))

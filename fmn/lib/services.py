"""
A module to assist in the creation of Twisted services.
"""
from __future__ import absolute_import, unicode_literals

from pika.adapters import twisted_connection
from twisted.internet import endpoints, protocol, reactor
from twisted.application.internet import ClientService


def create_amqp_service(client_string):
    """
    Creates a Twisted service that is registerable with a Twisted application.

    The service is an AQMP client using the Pika client library. Twisted is
    responsible for maintaining the connection and ensuring it available.
    This service needs to be registered with a Twisted application:

        >>> from twisted.application import service
        >>> application = service.Application('My App')
        >>> amqp_service = create_amqp_service('tcp:localhost:5672')
        >>> amqp_service.setServiceParent(application)

    For more information on using the Twisted application framework, see
    https://twistedmatrix.com/documents/current/core/howto/application.html
    """
    def twisted_protocol_wrapper():
        """
        This works around a problem in the Pika API. The
        `protocol.Factory.forProtocol` function requires a callable with 0
        required arguments, so we use this to wrap the creation of the protocol
        object.

        The upstream issue is https://github.com/pika/pika/pull/780
        """
        return twisted_connection.TwistedProtocolConnection(None)

    amqp_endpoint = endpoints.clientFromString(reactor, client_string)
    amqp_factory = protocol.Factory.forProtocol(twisted_protocol_wrapper)
    amqp_service = ClientService(amqp_endpoint, amqp_factory)
    return amqp_service

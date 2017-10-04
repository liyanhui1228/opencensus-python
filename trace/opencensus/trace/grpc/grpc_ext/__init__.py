# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc

import six


##############  Invocation-Side Interceptor Interfaces & Classes  ##############


class UnaryUnaryClientInterceptor(six.with_metaclass(abc.ABCMeta)):
    """Affords intercepting unary-unary invocations.
    This is an EXPERIMENTAL API and is subject to change without notice."""

    @abc.abstractmethod
    def intercept_unary_unary_call(self, invoker, method, request, **kwargs):
        """Intercepts a synchronous unary-unary invocation.
    Args:
      invoker: The handler to pass control to to continue with
        the invocation. It is the interceptor's responsibility
        to call it if it decides to move the RPC machinery
        forward.  The interceptor can use
        response, call = invoker(method, request, **kwargs)
        to continue with the RPC. invoker can raise RpcError
        to indicate an RPC terminated with non-OK status.
      method: The name of the RPC method.
      request: The request value for the RPC.
    Returns:
      The response value for the RPC and a Call object for the RPC.
    Raises:
      RpcError: Indicating that the RPC terminated with non-OK status. The
        raised RpcError will also be a Call for the RPC affording the RPC's
        metadata, status code, and details.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def intercept_unary_unary_future(self, invoker, method, request, **kwargs):
        """Intercepts an asynchronous unary-unary invocation.
    Args:
      invoker: The handler to pass control to to continue with
        the invocation. It is the interceptor's responsibility
        to call it if it decides to move the RPC machinery
        forward.  The interceptor can use
        future = invoker(method, request, **kwargs)
        to continue with the RPC. invoker returns an object that
        is both a Call for the RPC and a Future. In the event of
        RPC completion, the return Call-Future's result value will
        be the response message of the RPC.
      method: The name of the RPC method.
      request: The request value for the RPC.
    Returns:
        An object that is both a Call for the RPC and a Future. In the event of
        RPC completion, the return Call-Future's result value will be the
        response message of the RPC. Should the event terminate with non-OK
        status, the returned Call-Future's exception value will be an RpcError.
    """
        raise NotImplementedError()


class UnaryStreamClientInterceptor(six.with_metaclass(abc.ABCMeta)):
    """Affords intercepting unary-stream invocations.
    This is an EXPERIMENTAL API and is subject to change without notice."""

    @abc.abstractmethod
    def intercept_unary_stream_call(self, invoker, method, request, **kwargs):
        """Intercepts a unary-stream invocation.
    Args:
      invoker: The handler to pass control to to continue with
        the invocation. It is the interceptor's responsibility
        to call it if it decides to move the RPC machinery
        forward.  The interceptor can use
        response_iterator = invoker(method, request, **kwargs)
        to continue with the RPC. invoker returns an object that
        is both a Call for the RPC and an iterator of response
        values.
      method: The name of the RPC method.
      request: The request value for the RPC.
    Returns:
        An object that is both a Call for the RPC and an iterator of response
        values. Drawing response values from the returned Call-iterator may
        raise RpcError indicating termination of the RPC with non-OK status.
    """
        raise NotImplementedError()


class StreamUnaryClientInterceptor(six.with_metaclass(abc.ABCMeta)):
    """Affords intercepting stream-unary invocations.
    This is an EXPERIMENTAL API and is subject to change without notice."""

    @abc.abstractmethod
    def intercept_stream_unary_call(self, invoker, method, request_iterator,
                                    **kwargs):
        """Intercepts a synchronous stream-unary invocation.
    Args:
      invoker: The handler to pass control to to continue with
        the invocation. It is the interceptor's responsibility
        to call it if it decides to move the RPC machinery
        forward.  The interceptor can use
        reponse, call = (method, request_iterator, **kwargs)
        to continue with the RPC. invoker can raise RpcError
        to indicate an RPC terminated with non-OK status.
      method: The name of the RPC method.
      request_iterator: An iterator that yields request values for the RPC.
    Returns:
      The response value for the RPC and a Call object for the RPC.
    Raises:
      RpcError: Indicating that the RPC terminated with non-OK status. The
        raised RpcError will also be a Call for the RPC affording the RPC's
        metadata, status code, and details.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def intercept_stream_unary_future(self, invoker, method, request_iterator,
                                      **kwargs):
        """Intercepts an asynchronous stream-unary invocation.
    Args:
      invoker: The handler to pass control to to continue with
        the invocation. It is the interceptor's responsibility
        to call it if it decides to move the RPC machinery
        forward.  The interceptor can use
        future = invoker(method, request_iterator, **kwargs)
        to continue with the RPC. invoker returns an object that
        is both a Call for the RPC and a Future. In the event of
        RPC completion, the return Call-Future's result value will
        be the response message of the RPC.
      method: The name of the RPC method.
      request_iterator: An iterator that yields request values for the RPC.
    Returns:
        An object that is both a Call for the RPC and a Future. In the event of
        RPC completion, the return Call-Future's result value will be the
        response message of the RPC. Should the event terminate with non-OK
        status, the returned Call-Future's exception value will be an RpcError.
    """
        raise NotImplementedError()


class StreamStreamClientInterceptor(six.with_metaclass(abc.ABCMeta)):
    """Affords intercepting stream-stream invocations.
    This is an EXPERIMENTAL API and is subject to change without notice."""

    @abc.abstractmethod
    def intercept_stream_stream_call(self, invoker, method, request_iterator,
                                     **kwargs):
        """Intercepts a stream-stream invocation.
      invoker: The handler to pass control to to continue with
        the invocation. It is the interceptor's responsibility
        to call it if it decides to move the RPC machinery
        forward.  The interceptor can use
        response_iterator = invoker(method, request_iterator, **kwargs)
        to continue with the RPC. invoker returns an object that
        is both a Call for the RPC and an iterator of response
        values.
      method: The name of the RPC method.
      request_iterator: An iterator that yields request values for the RPC.
    Returns:
        An object that is both a Call for the RPC and an iterator of response
        values. Drawing response values from the returned Call-iterator may
        raise RpcError indicating termination of the RPC with non-OK status.
    """
        raise NotImplementedError()


##############  Service-Side Interceptor Interfaces & Classes  #################


class UnaryUnaryServerInterceptor(six.with_metaclass(abc.ABCMeta)):
    """Affords intercepting unary-unary RPCs on the service-side.
This is an EXPERIMENTAL API and is subject to change without notice."""

    @abc.abstractmethod
    def intercept_unary_unary_handler(self, handler, method, request,
                                      servicer_context):
        """Intercepts unary-unary RPCs on the service-side.
    Args:
      handler: The handler to continue processing the RPC.
      It takes a request value and a ServicerContext object
      and returns a response value.
      method: The full method name of the RPC.
      request: The request value for the RPC.
      servicer_context: The context of the current RPC.
    Returns:
      The RPC response.
    """
        raise NotImplementedError()


class UnaryStreamServerInterceptor(six.with_metaclass(abc.ABCMeta)):
    """Affords intercepting unary-stream RPCs on the service-side.
    This is an EXPERIMENTAL API and is subject to change without notice."""

    @abc.abstractmethod
    def intercept_unary_stream_handler(self, handler, method, request,
                                       servicer_context):
        """Intercepts unary-stream RPCs on the service-side.
    Args:
      handler: The handler to continue processing the RPC.
      It takes a request value and a ServicerContext object
      and returns an iterator of response values.
      method: The full method name of the RPC.
      request: The request value for the RPC.
      servicer_context: The context of the current RPC.
    Returns:
      An iterator of RPC response values.
    """
        raise NotImplementedError()


class StreamUnaryServerInterceptor(six.with_metaclass(abc.ABCMeta)):
    """Affords intercepting stream-unary RPCs on the service-side.
    This is an EXPERIMENTAL API and is subject to change without notice."""

    @abc.abstractmethod
    def intercept_stream_unary_handler(self, handler, method, request_iterator,
                                       servicer_context):
        """Intercepts stream-unary RPCs on the service-side.
    Args:
      handler: The handler to continue processing the RPC.
      It takes an iterator of request values and
      a ServicerContext object and returns a response value.
      method: The full method name of the RPC.
      request_iterator: An iterator of request values for the RPC.
      servicer_context: The context of the current RPC.
    Returns:
      The RPC response.
    """
        raise NotImplementedError()


class StreamStreamServerInterceptor(six.with_metaclass(abc.ABCMeta)):
    """Affords intercepting stream-stream RPCs on the service-side.
    This is an EXPERIMENTAL API and is subject to change without notice."""

    @abc.abstractmethod
    def intercept_stream_stream_handler(self, handler, method, request_iterator,
                                        servicer_context):
        """Intercepts stream-stream RPCs on the service-side.
    Args:
      handler: The handler to continue processing the RPC.
      It takes a request value and a ServicerContext object
      and returns an iterator of response values.
      method: The full method name of the RPC.
      request_iterator: An iterator of request values for the RPC.
      servicer_context: The context of the current RPC.
    Returns:
      An iterator of RPC response values.
    """
        raise NotImplementedError()


def intercept_channel(channel, *interceptors):
    """Intercepts a channel through a set of interceptors.
  This is an EXPERIMENTAL API and is subject to change without notice.
  Args:
    channel: A Channel.
    interceptors: Zero or more objects of type
      UnaryUnaryClientInterceptor,
      UnaryStreamClientInterceptor,
      StreamUnaryClientInterceptor, or
      StreamStreamClientInterceptor.
      Interceptors are given control in the order they are listed.
  Returns:
    A Channel that intercepts each invocation via the provided interceptors.
  Raises:
    TypeError: If interceptor does not derive from any of
      UnaryUnaryClientInterceptor,
      UnaryStreamClientInterceptor,
      StreamUnaryClientInterceptor, or
      StreamStreamClientInterceptor.
  """
    from grpc import _interceptor  # pylint: disable=cyclic-import
    return _interceptor.intercept_channel(channel, *interceptors)


def intercept_server(
        server,  # pylint: disable=redefined-outer-name
        *interceptors):
    """Creates an intercepted server.
  This is an EXPERIMENTAL API and is subject to change without notice.
  Args:
    server: A Server.
    interceptors: Zero or more objects of type
      UnaryUnaryServerInterceptor,
      UnaryStreamServerInterceptor,
      StreamUnaryServerInterceptor, or
      StreamStreamServerInterceptor.
      Interceptors are given control in the order they are listed.
  Returns:
    A Server that intercepts each received RPC via the provided interceptors.
  Raises:
    TypeError: If interceptor does not derive from any of
      UnaryUnaryServerInterceptor,
      UnaryStreamServerInterceptor,
      StreamUnaryServerInterceptor, or
      StreamStreamServerInterceptor.
  """
    from grpc import _interceptor  # pylint: disable=cyclic-import
    return _interceptor.intercept_server(server, *interceptors)


###################################  __all__  #################################

__all__ = ('UnaryUnaryClientInterceptor', 'UnaryUnaryServerInterceptor',
           'UnaryStreamClientInterceptor', 'UnaryStreamServerInterceptor',
           'StreamUnaryClientInterceptor', 'StreamUnaryServerInterceptor',
           'StreamStreamClientInterceptor', 'StreamStreamServerInterceptor',
           'intercept_server', 'intercept_channel',)

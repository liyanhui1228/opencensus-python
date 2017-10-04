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

import logging
import six
import sys

from opencensus.trace.grpc import grpc_ext
from opencensus.trace.propagation import text_format
from opencensus.trace import execution_context

from opencensus.trace.enums import Enum

log = logging.getLogger(__name__)


class OpenCensusClientInterceptor(grpc_ext.UnaryUnaryClientInterceptor,
                                  grpc_ext.UnaryStreamClientInterceptor,
                                  grpc_ext.StreamUnaryClientInterceptor,
                                  grpc_ext.StreamStreamClientInterceptor):

    def __init__(self, tracer=None):
        if tracer is None:
            tracer = execution_context.get_opencensus_tracer()

        self._tracer = tracer

    def _start_client_span(self, method):
        log.info('Start client span')
        span = self._tracer.start_span(name='[gRPC]{}'.format(str(method)))
        span.add_label(label_key='component', label_value='grpc')
        span.kind = Enum.SpanKind.RPC_CLIENT
        return span

    def intercept_unary_unary_call(self, invoker, method, request, **kwargs):
        span_context = self._tracer.span_context

        print(invoker)
        print(method)
        print(request)
        print(kwargs)

        metadata = getattr(kwargs, 'metadata', ())

        propagator = text_format.TextFormatPropagator()
        headers = propagator.to_carrier(span_context, {})

        metadata = metadata + tuple(six.iteritems(headers))

        with self._start_client_span(method) as span:
            span.name = '[gRPC_unary_unary_sync]{}'.format(str(method))

            try:
                result = invoker(method, metadata)
            except:
                e = sys.exc_info()[0]
                span.add_label('error', str(e))
                raise

        return result

    def intercept_unary_unary_future(self, invoker, method, request, **kwargs):
        span_context = self._tracer.span_context

        propagator = text_format.TextFormatPropagator()
        headers = propagator.to_carrier(span_context, metadata)

        with self._start_client_span(method) as span:
            span.name = '[gRPC_unary_unary_async]{}'.format(str(method))

            try:
                result = invoker(request, metadata)
            except:
                e = sys.exc_info()[0]
                span.add_label('error', str(e))
                raise

        return result

    def intercept_unary_stream_call(self, invoker, method, request, **kwargs):
        span_context = self._tracer.span_context

        propagator = text_format.TextFormatPropagator()
        headers = propagator.to_carrier(span_context, metadata)

        with self._start_client_span(method) as span:
            span.name = '[gRPC_unary_stream]{}'.format(str(method))

            try:
                result = invoker(request, metadata)
            except:
                e = sys.exc_info()[0]
                span.add_label('error', str(e))
                raise

        return result

    def intercept_stream_unary_call(self, invoker, method, request_iterator,
                                    **kawrgs):
        span_context = self._tracer.span_context

        propagator = text_format.TextFormatPropagator()
        headers = propagator.to_carrier(span_context, metadata)

        with self._start_client_span(method) as span:
            span.name = '[gRPC_stream_unary_sync]{}'.format(str(method))

            try:
                result = invoker(request_iterator, metadata)
            except:
                e = sys.exc_info()[0]
                span.add_label('error', str(e))
                raise

        return result

    def intercept_stream_unary_future(self, invoker, method, request_iterator,
                                      **kwargs):
        span_context = self._tracer.span_context

        propagator = text_format.TextFormatPropagator()
        headers = propagator.to_carrier(span_context, metadata)

        with self._start_client_span(method) as span:
            span.name = '[gRPC_stream_unary_async]{}'.format(str(method))

            try:
                result = invoker(request_iterator, metadata)
            except:
                e = sys.exc_info()[0]
                span.add_label('error', str(e))
                raise

        return result

    def intercept_stream_stream_call(self, invoker, method, request_iterator,
                                     **kwargs):
        span_context = self._tracer.span_context

        propagator = text_format.TextFormatPropagator()
        headers = propagator.to_carrier(span_context, metadata)

        with self._start_client_span(method) as span:
            span.name = '[gRPC_stream_stream]{}'.format(str(method))

            try:
                result = invoker(request_iterator, metadata)
            except:
                e = sys.exc_info()[0]
                span.add_label('error', str(e))
                raise

        return result

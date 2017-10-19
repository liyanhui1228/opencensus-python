# Copyright 2017, OpenCensus Authors
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
import grpc
import six
import sys


from opencensus.trace import execution_context
from opencensus.trace import grpc as oc_grpc
from opencensus.trace import labels_helper
from opencensus.trace.enums import Enum
from opencensus.trace.grpc import grpc_ext
from opencensus.trace.propagation import binary_format

log = logging.getLogger(__name__)

LABEL_COMPONENT = 'COMPONENT'
LABEL_ERROR_NAME = 'ERROR_NAME'
LABEL_ERROR_MESSAGE = 'ERROR_MESSAGE'
GRPC_HOST_PORT = 'GRPC_HOST_PORT'
GRPC_METHOD = 'GRPC_METHOD'


class OpenCensusClientInterceptor(grpc_ext.UnaryUnaryClientInterceptor,
                                  grpc_ext.UnaryStreamClientInterceptor,
                                  grpc_ext.StreamUnaryClientInterceptor,
                                  grpc_ext.StreamStreamClientInterceptor):

    def __init__(self, tracer=None, host_port=None):
        if tracer is None:
            tracer = execution_context.get_opencensus_tracer()

        self._tracer = tracer
        self.host_port = host_port
        self._propagator = binary_format.BinaryFormatPropagator()

    def _start_client_span(self, request_type, method):
        log.info('Start client span')
        span = self._tracer.start_span(
            name='[gRPC_client][{}]{}'.format(request_type, str(method)))

        # Add the component grpc to span label
        span.add_label(
            label_key=labels_helper.STACKDRIVER_LABELS.get(LABEL_COMPONENT),
            label_value='grpc')

        # Add the host:port info to span label
        if self.host_port is not None:
            span.add_label(
                label_key=labels_helper.GRPC_LABELS.get(GRPC_HOST_PORT),
                label_value=self.host_port)

        # Add the method to span label
        span.add_label(
            label_key=labels_helper.GRPC_LABELS.get(GRPC_METHOD),
            label_value=str(method))

        span.kind = Enum.SpanKind.RPC_CLIENT
        return span

    def _trace_async_result(self, result):
        if isinstance(result, grpc.Future):
            result.add_done_callback(self._future_done_callback())

        return result

    def _future_done_callback(self):
        def callback(future_response):
            code = future_response.code()

            if code != grpc.StatusCode.OK:
                span.add_label(
                    labels_helper.STACKDRIVER_LABELS.get(LABEL_ERROR_NAME),
                    str(code))

            response = future_response.result()
            self._tracer.end_span()

        return callback

    def intercept_call(self, request_type, invoker, method, request, **kwargs):
        metadata = getattr(kwargs, 'metadata', ())

        with self._start_client_span(request_type, method) as span:
            span_context = self._tracer.span_context
            header = self._propagator.to_header(span_context)
            grpc_trace_metadata = {
                oc_grpc.GRPC_TRACE_KEY: header,
            }
            metadata = metadata + tuple(six.iteritems(grpc_trace_metadata))

            kwargs['metadata'] = metadata

            try:
                result = invoker(method, request, **kwargs)
            except Exception as e:
                span.add_label(
                    labels_helper.STACKDRIVER_LABELS.get(LABEL_ERROR_MESSAGE),
                    str(e))
                span.finish()
                self._tracer.end_trace()
                raise

        return result

    def intercept_future(
            self, request_type, invoker, method, request, **kwargs):
        metadata = getattr(kwargs, 'metadata', ())

        with self._start_client_span(request_type, method) as span:
            span_context = self._tracer.span_context
            header = self._propagator.to_header(span_context)
            grpc_trace_metadata = {
                oc_grpc.GRPC_TRACE_KEY: header,
            }
            metadata = metadata + tuple(six.iteritems(grpc_trace_metadata))

            kwargs['metadata'] = metadata

            try:
                result = invoker(method, request, **kwargs)
            except Exception as e:
                span.add_label(
                    labels_helper.STACKDRIVER_LABELS.get(LABEL_ERROR_MESSAGE),
                    str(e))
                span.finish()
                self._tracer.end_trace()
                raise

        return self._trace_async_result(result)

    def intercept_unary_unary_call(self, invoker, method, request, *args, **kwargs):
        return self.intercept_call(
            oc_grpc.UNARY_UNARY, invoker, method, request, **kwargs)

    def intercept_unary_unary_future(self, invoker, method, request, *args, **kwargs):
        return self.intercept_future(
            oc_grpc.UNARY_UNARY, invoker, method, request, **kwargs)

    def intercept_unary_stream_call(self, invoker, method, request, *args, **kwargs):
        return self.intercept_call(
            oc_grpc.UNARY_STREAM, invoker, method, request, **kwargs)

    def intercept_stream_unary_call(self, invoker, method, request_iterator, *args,
                                    **kwargs):
        return self.intercept_call(
            oc_grpc.STREAM_UNARY, invoker, method, request_iterator, **kwargs)

    def intercept_stream_unary_future(self, invoker, method, request_iterator, *args,
                                      **kwargs):
        return self.intercept_future(
            oc_grpc.STREAM_UNARY, invoker, method, request_iterator, **kwargs)

    def intercept_stream_stream_call(self, invoker, method, request_iterator, *args,
                                     **kwargs):
        return self.intercept_call(
            oc_grpc.STREAM_STREAM, invoker, method, request_iterator, **kwargs)

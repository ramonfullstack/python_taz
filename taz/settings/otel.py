import logging

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (  # noqa
    OTLPSpanExporter
)
from opentelemetry.instrumentation.boto import BotoInstrumentor
from opentelemetry.instrumentation.falcon import FalconInstrumentor
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from simple_settings import settings

logger = logging.getLogger(__name__)

OTEL_EXPORTER_ENABLED = settings.OTEL_EXPORTER_ENABLED
trace_provider = TracerProvider()

if OTEL_EXPORTER_ENABLED:
    logger.debug(
        'OTEL_EXPORTER_ENABLED: true'
    )
    trace_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))

trace.set_tracer_provider(trace_provider)
tracer = trace.get_tracer(__name__, tracer_provider=trace_provider)


INSTRUMENTAIONS = {
    'pymongo': PymongoInstrumentor(),
    'redis': RedisInstrumentor(),
    'grpc': GrpcInstrumentorClient(),
    'falcon': FalconInstrumentor(),
    'boto': BotoInstrumentor(),
    'requests': RequestsInstrumentor()
}


def configure_otel_instrumentation():
    if OTEL_EXPORTER_ENABLED:
        instrumentations_enabled = settings.OTEL_INSTRUMENTATIONS_ENABLED
        for instrument in instrumentations_enabled:
            _instrument = INSTRUMENTAIONS.get(instrument)
            if _instrument:
                _instrument.instrument()


def get_tracer():
    return tracer


def get_current_span() -> trace.Span:
    return trace.get_current_span()


def start_as_current_span(name, kind=trace.SpanKind.INTERNAL, attributes={}):
    ctx = get_current_span().get_span_context()
    link_from_current = trace.Link(ctx)
    return tracer.start_as_current_span(
        name, kind=kind, links=[link_from_current], attributes=attributes,
    )

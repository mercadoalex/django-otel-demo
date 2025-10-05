#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

# OpenTelemetry instrumentation and exporter setup
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

DjangoInstrumentor().instrument()

resource = Resource(attributes={
    SERVICE_NAME: "django-otel-demo"
})

provider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4318/v1/traces"  # Change to your Tempo endpoint
)
span_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(span_processor)

from opentelemetry import trace
trace.set_tracer_provider(provider)

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_django.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

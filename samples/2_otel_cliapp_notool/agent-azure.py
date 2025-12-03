import os

from dotenv import load_dotenv
from openai import AzureOpenAI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.openai import OpenAIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

load_dotenv()

# AWS setting are removed.
# Configure your environment variables for Azure OpenAI:
# - AZURE_OPENAI_API_KEY
# - AZURE_OPENAI_ENDPOINT
# - AZURE_OPENAI_DEPLOYMENT_NAME
# - OPENAI_API_VERSION

provider = TracerProvider()
# otlp_exporter = OTLPSpanExporter(
#     endpoint="http://otel:4318/v1/traces"
# )
# direct exporter to mlflow
otlp_exporter = OTLPSpanExporter(
    endpoint="http://mlflow:5000/v1/traces",
    headers={"x-mlflow-experiment-id": "0"},
)

processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
OpenAIInstrumentor().instrument()
client = AzureOpenAI(
    api_version=os.environ.get("OPENAI_API_VERSION", "2024-05-01-preview"),
)
deployment_name = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
topic = "programming"
prompt = f"Tell me a joke about {topic}"

result = client.chat.completions.create(
    model=deployment_name,
    messages=[{"role": "user", "content": prompt}],
    temperature=0.1,
)
print(result.choices[0].message.content)
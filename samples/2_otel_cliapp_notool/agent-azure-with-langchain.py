import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
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

prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
model = AzureChatOpenAI(
    deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    temperature=0.1,
)
chain = prompt | model
result = chain.invoke({"topic": "programming"})
print(result.content)
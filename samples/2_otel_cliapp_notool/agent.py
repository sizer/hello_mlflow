import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from langchain_aws import ChatBedrockConverse
from langchain_core.prompts import ChatPromptTemplate

AWS_ACCOUNT_ID = os.environ["AWS_ACCOUNT_ID"]
AWS_REGION = os.environ.get("AWS_REGION", "us-west-2")

provider = TracerProvider()
otlp_exporter = OTLPSpanExporter(
    endpoint="http://otel:4318/v1/traces"
)
processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
model = ChatBedrockConverse(
    model=f"arn:aws:bedrock:{AWS_REGION}:{AWS_ACCOUNT_ID}:inference-profile/us.anthropic.claude-haiku-4-5-20251001-v1:0",
    provider="anthoropic",
    region_name=AWS_REGION,
    temperature=0.1,
)
chain = prompt | model
result = chain.invoke({"topic": "programming"})
print(result.content)
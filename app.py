import streamlit as st
import os
import boto3
from datetime import datetime
import json

# Initialize Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")  # Adjust region if needed

st.title("Autonomous Research Agent")

topic = st.text_input("Enter your topic or question:")

def run_bedrock_agent(topic):

    body = {
      "messages": [
        {
          "role": "user",
          "content": f"Summarize the topic. {topic} Then suggest 2 follow-up questions or actions"
        }
      ],
      "max_tokens": 1024,
      "anthropic_version": "bedrock-2023-05-31"
    }

    response = bedrock.invoke_model(
      modelId="anthropic.claude-3-haiku-20240307-v1:0",
      contentType="application/json",
      accept="application/json",
      body=json.dumps(body).encode("utf-8")
    )

    result = json.loads(response['body'].read())
    return result

if st.button("Run Agent"):
    st.write(f"Running agent for: {topic}")

    try:
        summary = run_bedrock_agent(topic)
        st.write(summary["content"][0]["text"])

        # Save summary to S3
        s3 = boto3.client('s3')
        filename = f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        bucket_name = "agentic-ai-summaries"  # Replace with your S3 bucket name

        s3.put_object(
            Bucket=bucket_name,
            Key=filename,
            Body=json.dumps(summary)
        )
        st.success(f"Summary saved to S3 as {filename}")

    except Exception as e:
        st.error(f"Failed to run agent or save summary: {e}")


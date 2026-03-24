# AI Model Text Classification Overview

## Overview

AI Model Text Classification provides pre-trained machine learning models for detecting toxic content and prompt injection attacks in API traffic. The feature includes nine ONNX-optimized models covering toxicity detection (binary and multi-label) and prompt injection/jailbreak detection across up to 15 languages. Administrators deploy these models as gateway resources to filter or analyze text payloads before they reach backend services or LLM endpoints.

## Prerequisites

- Gravitee API Management platform with resource plugin support
- Sufficient gateway memory to load selected model (4.39M to 300M parameters depending on model choice)
- Text payloads in supported languages for the selected model
- For prompt injection detection: LLM-powered APIs or endpoints accepting user-supplied prompts

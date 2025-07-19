import jinja2
import json
import base64
from litellm import completion
from functools import partial
from kydo_seed.config import settings


get_gemini_response = partial(completion, model="gemini/gemini-2.5-flash", api_key=settings.GEMINI_API_KEY)
get_chatgpt_response = partial(completion, model="gpt-4o")



prompt_parts = [
    {
        "role": "user",
        "content": 'Sing me a song.'
    }]

chatgpt_version = get_chatgpt_response(messages=prompt_parts)
print(chatgpt_version)

# --- Data Preparation ---

# 1. Define your inputs
text_prompt = "Compare the logo in the image to the one described in the PDF."
image_path = "path/to/your/logo.png"
pdf_path = "path/to/your/document.pdf"

# 2. Function to encode files
def encode_file(filepath):
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# 3. Build the list of content 'parts'
prompt_parts = [
    {
        "type": "text",
        "text": text_prompt
    },
    {
        "type": "image_url",
        "mime_type": "image/png", # Make sure this matches your image type
        "data": encode_file(image_path)
    },
    {
        "type": "image_url", # Both images and PDFs use the 'image_url' type for data URIs
        "mime_type": "application/pdf",
        "data": encode_file(pdf_path)
    }
]

# --- Template Rendering ---

# 4. Set up Jinja and render the template
env = jinja2.Environment()
# You can also load from a file as shown previously
template_string = """
[
  {
    "role": "user",
    "content": [
      {% for part in parts %}
      {
        "type": "{{ part.type }}",
        {% if part.type == 'text' %}
          "text": {{ part.text | tojson }}
        {% elif part.type == 'image_url' %}
          "image_url": {
            "url": "data:{{ part.mime_type }};base64,{{ part.data }}"
          }
        {% endif %}
      }{% if not loop.last %},{% endif %}
      {% endfor %}
    ]
  }
]
"""
template = env.from_string(template_string)

rendered_json_string = template.render(parts=prompt_parts)
messages_for_api = json.loads(rendered_json_string)


# 5. Make the call with the structured multimodal message
# print(json.dumps(messages_for_api, indent=2)) # Uncomment to inspect the final JSON


response.text
# print(response.choices[0].message.content)





from shortuuid import uuid
import json
from jinja2 import Environment
from pydantic import BaseModel, Field
from typing import Type, TypeVar, Iterable, List
import google.generativeai as genai
from kydo_seed.config import settings
from google.cloud import aiplatform, storage


class Thinking(BaseModel):
    scratch_space: str = Field(description='This space is used for THINKING_OUT_LOUD.')

class Dialectic(Thinking):
    thesis: str
    antithesis: str
    synthesis: str

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel(settings.GEMINI_MODEL_NAME)

', then produce one cycle of the dialectic method: propose a thesis, then state an antithesis, lastly create a synthesis. Respond after one cycle using the provided json schema.'
output_model = Thinking
prompt = 'Which american football team is the best? THINK_OUT_LOUD for a few sentences.'


generation_config = genai.types.GenerationConfig(response_mime_type="application/json", response_schema=output_model)
response = model.generate_content(prompt, generation_config=generation_config)
data = response.candidates[0].content.parts[0].text
output = output_model.model_validate_json(data)
output.scratch_space



class GeminiClient:
    def __init__(self, output_model):
        self.output_model = output_model
        self.env = Environment()
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL_NAME)
        self.generation_config = genai.types.GenerationConfig(
            response_mime_type="application/json",
            response_schema=output_model
        )

    def __call__(self, input_model_instance):
        template = self.env.from_string(input_model_instance.template_string)
        prompt = self.template.render(input_model_instance.model_dump())
        response = self.model.generate_content(prompt, generation_config=self.generation_config)
        data = response.candidates[0].content.parts[0].text
        return self.output_model.model_validate_json(data)


class Thinking(BaseModel):
    scratch_space: str = Field(description='This space is used for THINKING_OUT_LOUD.')

class FreeResponse(Thinking):
    response: str = Field(description="This space is for the response to the user's query")

free_response = GeminiClient(FreeResponse, free_response_prompt_template)


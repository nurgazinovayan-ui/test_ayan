import json
from openai import OpenAI
from app.core.config import get_settings

settings = get_settings()


def generate_content(trend_summary: str) -> dict:
    if not settings.openai_api_key:
        return {
            'concepts': [
                {'concept': 'Behind-the-scenes AI workflow', 'rationale': 'Educational and authentic'},
                {'concept': 'Before/after transformation', 'rationale': 'Visual hook and social proof'},
                {'concept': 'Mini tutorial carousel', 'rationale': 'Saves and shares potential'},
            ],
            'image_prompt': 'A vibrant, modern Instagram visual showing AI creativity, portrait composition, 4:5',
            'caption': 'How we turn trends into content in minutes using AI ✨',
            'hashtags': '#ai #instagrammarketing #contentstrategy'
        }

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = f"""Given this trend summary:\n{trend_summary}\nGenerate JSON with keys: concepts (3 items with concept,rationale), image_prompt, caption, hashtags."""
    response = client.responses.create(
        model=settings.openai_model,
        input=prompt,
        temperature=0.8,
    )
    text = response.output_text
    return json.loads(text)

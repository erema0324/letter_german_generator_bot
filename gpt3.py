import openai
import config

openai.api_key = config.OPENAI_API_KEY

def generate_letter(prompt: str, language: str = None) -> str:
    if language:
        prompt = f"Переведи следующий текст на язык {language}: '{prompt}'.Пожалуйста, учти контекст, сохраняй точность исходного смысла при переводе и обрати внимание на грамматику, стиль и пунктуацию. Без дополнительных комментариев"
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0,
    )

    return response.choices[0].text.strip()

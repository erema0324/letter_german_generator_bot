import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

async def send_prompt_to_chatgpt(prompt: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

async def translate_text(text: str, target_language: str) -> str:
    prompt = f"Переведите следующий текст на {target_language}:\n\n{text}"
    translated_text = await send_prompt_to_chatgpt(prompt)
    return translated_text.strip()

def generate_reply_letter(original_letter: str, reply_intent: str, sender_name: str, receiver_name: str, target_language: str) -> str:
    prompt = f"Напишите ответное письмо на немецком языке на основе следующей информации:\n\nИсходное письмо:\n{original_letter}\n\nОтвет на письмо:\n{reply_intent}\n\nОтправитель: {sender_name}\nПолучатель: {receiver_name}\n"
    reply_letter = send_prompt_to_chatgpt(prompt)
    return reply_letter.strip()


import openai

def generate_response(prompt, api_key):
    openai.api_key = api_key

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=800,
        n=1,
        stop=None,
        temperature=0.4,
    )

    return response.choices[0].text.strip()

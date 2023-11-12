from openai import OpenAI

client = OpenAI(api_key="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")
def parse_client_details(input):
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={ "type": "json_object" },
        seed=1,
        messages=[
            {"role": "system", "content": "Given an input containing information about an entity, please identify and extract the relevant details. Build a JSON response with the following fields: 'name', 'registration_number', 'vat_registration_number', 'address', 'email', 'phone_number', and 'bank_account_number'. If multiple bank account numbers provided, select first one. If any of these fields are missing in the input, include them in the JSON response with empty strings as values. Ensure the response is structured in valid JSON format"},
            {"role": "user", "content": input}
        ]
    )
    result = completion.choices[0].message.content
    return result
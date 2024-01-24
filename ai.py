import os
import json
from openai import OpenAI

model = "gpt-4-1106-preview"

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
def parse_client(input):
    completion = client.chat.completions.create(
        model=model,
        response_format={ "type": "json_object" },
        seed=1,
        messages=[
            {"role": "system", "content": 
                "Given an input containing information about an business entity or private individual, please identify type: business entity or private individual and extract the relevant details. " +
                "Build a JSON response with the following fields:" +
                "For private individual: 'first_name', 'last_name', 'email', 'phone_number' and 'type' with '2' value." +
                "For business entity: 'company_name', 'registration_number', 'vat_number', 'address', 'email', 'phone_number', and 'bank_account' and 'type' with '1' value." + 
                "'vat_number' value starts with `LV` substring"
                "If multiple bank account numbers provided, select first one. " +
                "If any of these fields are missing in the input, include them in the JSON response with empty strings as values. "
                "Ensure the response is structured in valid JSON format"},
            {"role": "user", "content": input}
        ]
    )
    result = json.loads(completion.choices[0].message.content)
    print(result)
    return result

def parse_lines(input):
    completion = client.chat.completions.create(
        model=model,
        response_format={ "type": "json_object" },
        seed=1,
        messages=[
            {"role": "system", "content": 
                "Given an input containing a description of goods or services," +
                "which includes an itemized list with details:"+
                "line item, quantity, and unit price (in this order)"+
                "line item and unit price (in this order), set quantity to 1."
                "Create a JSON response with the following fields:"+
                "For each line item:" +

                "`line_item`" +
                "`quantity`" +
                "`unit_price`" +
                "`subtotal`" +
                "Additionally, include the following overall fields:" +

                "`total`: Grand Total" +
                "Ensure the response captures the breakdown of each item and the specified overall totals."},
            {"role": "user", "content": input}
        ]
    )
    result = json.loads(completion.choices[0].message.content)
    print(result)
    return result
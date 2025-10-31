#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dotenv import load_dotenv
from openai import OpenAI
import os, json, rich

class GPTConnector:
    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initialize the GPTConnector. Loads API key from .env file.
        """
        # Load environment variables from .env
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️ OPENAI_API_KEY not found in .env file")
            return None

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def send_prompt(self, prompt: str) -> dict:
        """
        Sends a prompt to ChatGPT and returns the JSON response.

        :param prompt: The text prompt to send to ChatGPT
        :return: A dictionary containing the model's JSON response
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}  # ensures valid JSON
        )

        message = response.choices[0].message.content

        try:
            if message is None:
                return {"error": "No response from model"}
            return json.loads(message)
        except json.JSONDecodeError:
            return {"raw_response": message}


if __name__ == "__main__":
    connector = GPTConnector(model="gpt-4o-mini")

    prompt = """
    Generate a JSON object describing a random space mission.
    Include: name, destination, crew_size, and launch_year.
    """

    result = connector.send_prompt(prompt)

    rich.print_json(data=result)
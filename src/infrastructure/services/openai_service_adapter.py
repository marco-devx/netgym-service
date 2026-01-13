import os
from openai import OpenAI
from src.domain.ports.services import LLMServicePort
from src.application.dtos.player_response_dto import PlayerResponseDTO
from src.infrastructure.config.settings import get_settings

class OpenAIServiceAdapter(LLMServicePort):
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.openai_api_key
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def generate_player_bio(self, player_data: PlayerResponseDTO) -> str:
        if not self.client:
            return "OpenAI API Key not configured."

        # Convert all DTO data to a readable string format
        stats_summary = player_data.model_dump_json(indent=2)

        prompt = (
            f"Here is the data for a baseball player:\n{stats_summary}\n\n"
            "Based on these statistics, generate a professional and engaging biography. "
            "Highlight their key strengths, role on the field, and overall performance qualities. "
            "Do not strictly list the stats, but weave them into a narrative that describes their playing style and impact. "
            "The tone should be knowledgeable and appreciative of their skills."
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable baseball analyst and writer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=250,
                temperature=0.7 
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating bio: {str(e)}"

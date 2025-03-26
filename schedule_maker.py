from schemas import MasterOpenaiInterface, LLMModelInfo, Message, Schedule, Activity
from user import User
class ScheduleMaker(MasterOpenaiInterface):
    """
    Class for generating a travel cronogram using structured output.
    This class takes the conversation history and a list of activities,
    then uses an LLM to create a structured travel itinerary.
    """
    
    def __init__(self,cheap_models: list[LLMModelInfo] = [], **kwargs):
        main_model = None
        if not main_model and cheap_models:
            main_model = cheap_models[0]
        super().__init__(cheap_models=cheap_models, main_model=main_model)
        if not cheap_models and main_model:
            self.cheap_models = [main_model]
    
    def get_system_message(self) -> dict:
        """Return the system message for cronogram generation"""
        return {
            "role": "system",
            "content": """You are a travel planner assistant that creates detailed chronograms.
            Analyze the conversation history and activities list to create a well-organized daily itinerary.
            Your output must be a valid JSON object with the structure specified in the user's request."""
        }
    
    async def create_cronogram(self, user: User, activities: list[Activity]) -> Schedule:
        """
        Creates a structured travel cronogram based on the user's conversation history
        and selected activities.
        
        Parameters:
        - user: User object containing the conversation history
        - activities: List of Activity objects to include in the cronogram
        
        Returns:
        - A dictionary representing the cronogram
        """
        print("WARNING: activities arent a pydantic object")
        # Prepare activities for inclusion in the prompt
        # activities_text = "\n".join([
        #     f"Activity: {a.name}\nShort description: {a.short_description}\nLong description: {a.long_description}"
        #     for a in activities
        # ])

        activities_text = "\n-----------\n".join([f"{act.name.capitalize()}:\n{act.long_description}" for act in activities]) 
        # Prepare the prompt with the structure definition
        user_prompt = f"""Based on the conversation history and these activities:

{activities_text}

Create a travel cronogram as a JSON object with this structure:
{{
  "title": "string",
  "explanations": "string (e.g., You will visit the Louvre and look for Mona Lisa there, a great painting.)"
  "days": [
    {{
      "day": "number",
      "activities": [
        {{
          "name": "string",
          "duration": "string (e.g., '2 hours')",
          "time": "string (e.g., '09:00 AM')",
          "end_time": "string (e.g., '12:00 AM')",
          "description": "string",
          "notes": "string (optional)"
        }}
      ]
    }}
  ],
  
}}

The cronogram should logically organize activities, respecting timing and travel constraints.
"""
        
        # Combine messages
        messages = [self.get_system_message()]
        # Add conversation history to provide context
        messages.extend(user.dumpHistory())
        # Remove id field which might cause issues
        for message in messages:
            if "id" in message:
                message.pop("id")
        # Add the final user prompt requesting the cronogram
        messages.append({"role": "user", "content": user_prompt})
        
        # Try twice to generate a valid JSON response
        for attempt in range(2):
            try:
                completion = await self.openai.chat.completions.create( #type: ignore
                    model=self.model,
                    messages=messages, #type: ignore
                    response_format={"type": "json_object"}
                )
                
                response_content = completion.choices[0].message.content
                return Schedule.model_validate_json(str(response_content))
            except Exception as e:
                print(f"CRONOGRAM: Error generating cronogram: {e}")
        
        raise Exception("CRONOGRAM: Failed to generate a valid cronogram response")

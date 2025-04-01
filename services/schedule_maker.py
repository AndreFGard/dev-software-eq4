from openai import BaseModel
from schemas import GPTMessage, MasterOpenaiInterface, LLMModelInfo, Message, Schedule, Activity

class ActList(BaseModel):
  activities: list[Activity]

class ActivityMaker(MasterOpenaiInterface):
    """Class that generates activities based on a conversation history and activity history"""
    def __init__(self, cheap_models: list[LLMModelInfo] = [], **kwargs):
        main_model = None
        if not main_model and cheap_models:
          main_model = cheap_models[0]
        super().__init__(cheap_models=cheap_models, main_model=main_model)
        if not cheap_models and main_model:
          self.cheap_models = [main_model]
      
    
    def get_activity_building_prompt(self) -> dict:
        """Return the system message for activity building"""
        return {
            "role": "system",
            "content": """You are an assistant that creates tourism activities based on user messages.
             Break down the last message you receive into a structured json list of activities.
             Describe the details of each activity in the long description. Heres the json schema you will follow:
             {
              "activities": [
                {
                  "long_description": "string (detailed description including important details)",
                  "name": "string (a short, descriptive name for the activity)",
                  "short_description": "string (a brief one-line summary)"
                }
              ]
            }"""
        }


    async def build_activity_from_messages(self,  message: GPTMessage, GPTMessageHistory: list[GPTMessage]) -> list[Activity]:
      system_prompt = self.get_activity_building_prompt()
      user_prompt = f"""Separate the activities described in THIS message: '{message.content}'"""
      
      relevant_hist = [m.model_dump() for m in [GPTMessage(**system_prompt)
                          ] + GPTMessageHistory[-6:] + [
                          GPTMessage(role="user", content=message.content)]]

      for attempt in range(2):
          try:
              completion = await self.openai.chat.completions.create( #type: ignore
                  model=self.model,
                  messages=relevant_hist, #type: ignore
                  response_format={"type": "json_object"}
              )
              
              response_content = completion.choices[0].message.content
              a =  ActList.model_validate_json(str(response_content))
              return a.activities
          except Exception as e:
              print(f"CRONOGRAM: Error generating cronogram: {e}")
      
      raise Exception("CRONOGRAM: Failed to generate a valid cronogram response")



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

        self.activity_maker = ActivityMaker(cheap_models=cheap_models, **kwargs)
    
    def get_cronogram_prompt(self) -> dict:
        """Return the system message for cronogram generation"""
        return {
            "role": "system",
            "content": """You are a travel planner assistant that creates detailed chronograms.
            Analyze the conversation history and activities list to create a well-organized daily itinerary.
            Your output must be a valid JSON object with the structure specified in the user's request."""
        }
    
    async def create_cronogram(self, GPTMessageHistory:list[GPTMessage], activities: list[Activity]) -> Schedule:
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
        messages = [self.get_cronogram_prompt()]
        # Add conversation history to provide context
        messages.extend([gptm.model_dump() for gptm in GPTMessageHistory])
        
        
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

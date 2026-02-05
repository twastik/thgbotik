from google import genai
import os

API_KEY = os.getenv("API_KEY")


class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)
        self.current_mode = "assistant"
        self.system_instructions = {}
        self.loadfrom_file()
   
    def loadfrom_file(self):
        
        instructions_dir = "instructions"
       
        if os.path.exists(instructions_dir):
            for filename in os.listdir(instructions_dir):
                if filename.endswith(".txt"):
                    mode_name = filename[:-4]
                    filepath = os.path.join(instructions_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            self.system_instructions[mode_name] = f.read()
                    except:
                        pass 

        if not self.system_instructions:
         
            pass
   
    def set_mode(self, mode: str):
        
        if mode in self.system_instructions:
            self.current_mode = mode
            return True

        self.current_mode = mode
        return False
   
    def get_available_modes(self):
        
        return list(self.system_instructions.keys())
   
    def ask(self, prompt: str) -> str:
        try:
            config = {
                "system_instruction": self.system_instructions[self.current_mode],
                # "generation_config": {
                #     "max_output_tokens": 2048,  # Коротші відповіді
                #     "temperature": 0.7,  # Менше випадковості
                # },
                # "safety_settings": [
                #     {
                #         "category": "HARM_CATEGORY_HARASSMENT",
                #         "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                #     }
                # ]
            }
           
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=config
            )
           
            if response.text:
                return response.text
            return "Отримано порожню відповідь."
           
        except Exception as e:
            if "429" in str(e):
                return "Ліміт вичерпано. Почекай 30 секунд."
            return f"Помилка API: {str(e)}"


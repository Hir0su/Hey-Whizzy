import google.generativeai as genai

def setup():

    API_KEY = 'AIzaSyClCgE5CSrdsbbmdaR4_dTHXFoUhtx0-1w'
    genai.configure(api_key=API_KEY)
    
def get_response(command):    
    model = genai.GenerativeModel("gemini-pro")
    custom = "Remember, you are a wise Wizard named Whizzy. Please respond in 2 sentences max and make your answers brief."
    response = model.generate_content(f"{custom} {command}")
    output = response.text
    return output

def start_prompt(command):
    setup()
    return get_response(command)

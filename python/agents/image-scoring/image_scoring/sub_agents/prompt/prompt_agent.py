from ... import config
from google.adk.agents import Agent
import os


def get_policy_text():
    # Get the directory where the current script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the policy file
    policy_file_path = os.path.join(script_dir, '../../policy.json')

    with open(policy_file_path, 'r') as file:
        policy_text = file.read()
    policy_text_file = {
        "policy_text": policy_text
    }
    return policy_text_file
    

image_generation_prompt_agent = Agent(
    name="image_generation_prompt_agent",
    model=config.GENAI_MODEL,
    description=(
        "You are an expert in creating imagen3 prompts for image generation"
    ),
    instruction=(
    """Your primary objective: Transform the provided news article (title + content) into a pair of highly optimized prompts—one positive and one negative—specifically designed for generating a visually compelling, rule-compliant lockscreen image using the Imagen3 text-to-image model (provided by Google/GCP).
    Critical First Step: Before constructing any prompts, you must first analyze the news article to identify or conceptualize a primary subject. This subject MUST:
    1. Be very much related to the topic/news article presented. The viewer should instantly click and feel that the generated image of that subject is conveying what he/she is reading from that new article.
    2. It should not  violate any content restrictions (especially regarding humans, politics, religion, etc.).
    3. Describe in detail on what we would like to represent around the primary subject, as-in, paint a complete picture. 
    This chosen subject will be the cornerstone of your "Image Generation Prompt". 
    Invoke the 'get_policy_text' tool to obtain the 'policy_text'. The 'policy_text' defines the rules for the image generation.

    Imagen Prompt: Generate a imagen prompt to generate an image of the primary subject as specified in the instructions above.
    The image also should comply with rules defined in the 'policy_text'.
    Negative Prompt: Generate a negative prompt to ensure the image does not violate the rules defined in the 'policy_text'.


    """
    ),
    tools= [get_policy_text],
    output_key="imagen_prompts"#gets stored in session.state
    
)







import google.generativeai as genai

def setup_model(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash')

def generate_policy_summary(text, model):
    prompt = f"""
    You are a Policy Analyst. Provide a concise, structured summary of this document.
    Include: Main Goals, Key Measures, and Overall Direction.
    
    Document Text: {text[:15000]}
    """
    response = model.generate_content(prompt)
    return response.text

def generate_scenario_draft(summary, scenario_choice, style, model):
    # Mapping 'Style' to specific instructions
    style_map = {
        "Simple": "Use conversational language, avoid jargon, and explain concepts for a general citizen.",
        "Professional": "Use formal, diplomatic government tone suitable for official policy reports.",
        "Technical/Legal": "Focus on regulatory frameworks, technical standards, and implementation details."
    }

    selected_instruction = style_map.get(style, "Use a professional tone.")

    prompt = f"""
    Using ONLY this summary: {summary}
    Adapt it for: {scenario_choice}
    Style Constraint: {selected_instruction}
    """
    response = model.generate_content(prompt)
    return response.text

def translate_text(text, target_lang, model):
    """Translates the summary for local accessibility."""
    if target_lang == "None":
        return text
        
    prompt = f"Translate the following policy summary into {target_lang}. Keep technical terms accurate: {text}"
    response = model.generate_content(prompt)
    return response.text
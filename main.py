import gradio as gr
import requests
import os
from dotenv import load_dotenv
import gradio as gr
import google.generativeai as genai
load_dotenv()
genai.configure(api_key=os.getenv('API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash') 

def generate_product_ideas(industry, product_type, target_audience, features, constraints):
    prompt = f"Generate innovative product ideas for the {industry} industry. The product should be a {product_type} targeting {target_audience}. It should have the following features: {features}. Consider these constraints: {constraints}."
    response = model.generate_content(prompt)
    print(response.text)
    return response.text
  
   
    

with gr.Blocks() as interface:
    gr.Markdown("## Product Idea Generator")
    with gr.Row():
        industry = gr.Dropdown(["Technology", "Health", "Finance", "Education", ...], label="Industry")
        product_type = gr.Dropdown(["Hardware", "SaaS", "Mobile App", ...], label="Product Type")
    target_audience = gr.Textbox(label="Target Audience")
    features = gr.Textbox(label="Desired Features")
    constraints = gr.Textbox(label="Constraints")
    submit_button = gr.Button("Generate Ideas")
    output_text = gr.Textbox(label="Product Ideas")

    submit_button.click(generate_product_ideas, inputs=[industry, product_type, target_audience, features, constraints], outputs=output_text)

interface.launch()

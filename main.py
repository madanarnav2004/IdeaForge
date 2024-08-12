import gradio as gr
import requests
import os
from dotenv import load_dotenv
import gradio as gr
import google.generativeai as genai
import json
load_dotenv()
genai.configure(api_key=os.getenv('API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash') 
PRODUCT_HUNT_BASE_URL = "https://api.producthunt.com/v2/api/graphql"

def fetch_product_hunt_posts(industry, product_type):
    """Fetches the top 10 Product Hunt posts matching the given industry and product type."""

    developer_token = os.getenv("PRODUCT_HUNT_DEVELOPER_TOKEN")

    

    query = """
    query {
      posts(first: 30, order: VOTES) { # Fetch 30 posts
        edges {
          node {
            id
            name
            tagline
            votesCount
            website
            commentsCount
          }
        }
      }
    }
    """

    headers = {"Authorization": f"Bearer {developer_token}"}
    response = requests.post(
        PRODUCT_HUNT_BASE_URL,
        json={"query": query},  
        headers=headers
    )
    response.raise_for_status()

    try:
        data = response.json()
        print(json.dumps(data, indent=2))  

        posts = [edge["node"] for edge in data["data"]["posts"]["edges"]]

        # Filter by industry and product type (case-insensitive)
        filtered_posts = [
            post 
            for post in posts 
            if industry.lower() in post["tagline"].lower() 
            and product_type.lower() in post["tagline"].lower()
        ]

        # Limit to top 3 filtered posts
        top_filtered_posts = filtered_posts[:3]

        return top_filtered_posts 

    except KeyError:
        print("Unexpected API response format.")
        return []
def generate_product_ideas(industry, product_type, target_audience, features, constraints):
  
    product_hunt_posts = fetch_product_hunt_posts(industry, product_type)

    top_products = ", ".join([post["name"] for post in product_hunt_posts[:3]])
    summary = f"Top products in the {industry} {product_type} category include: {top_products}"

    prompt = f"""
    Generate innovative product ideas with these details:

    Industry: {industry}
    Product Type: {product_type}
    Target Audience: {target_audience}
    Desired Features: {features if features else "N/A"}
    Constraints: {constraints if constraints else "N/A"}

    Market Analysis (Product Hunt):
    {summary}

    Provide a concise list of product ideas, each with a brief description.
    """

    response = model.generate_content(prompt)
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

interface.launch(share=True)

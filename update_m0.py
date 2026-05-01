import os
import re

file_path = "M0/M0_LN1.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add The Shift to Generative AI section
gen_ai_section = """
# The Shift to Generative AI

Before diving into the tools, it's essential to understand the paradigm shift we are experiencing. Traditional machine learning models, often referred to as discriminative models, focus on predicting outputs by learning the conditional probability of some expected output given an input. They are adept at tasks like classification or regression. Generative Artificial Intelligence (GenAI), on the other hand, seeks to learn and replicate complex data distributions to synthesize entirely new and original data, mirroring human-like outputs. 

According to *Generative AI Foundations in Python*, state-of-the-art generative models can behave as collaborators capable of synthetic understanding and generating sophisticated responses. The rapid growth of generative approaches fundamentally reshapes how we interact with technology. Whether you are synthesizing images with Diffusion models or generating text with Large Language Models (LLMs) based on the Transformer architecture, these models require immense computational power. This is where tools like Google Colab become indispensable for modern AI development.
"""

content = re.sub(r'(# Google Colab in AD698)', gen_ai_section + r'\n\n\1', content)

# Enhance What is Google Colab section
colab_enhancement = """## What is Google Colab?
As highlighted in *Generative AI Foundations in Python*, Jupyter notebooks enable live code execution, visualization, and explanatory text, suitable for prototyping and data analysis. Google Colab is a cloud-based version of Jupyter Notebook specifically designed for machine learning prototyping. It provides free GPU resources and integrates directly with Google Drive for file storage and sharing, making it the perfect environment to handle the computational complexity of deep generative models.
"""

content = re.sub(r'## What is Google Colab\?.*?(?=## Why Use Google Colab\?)', colab_enhancement + '\n', content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated {file_path}")

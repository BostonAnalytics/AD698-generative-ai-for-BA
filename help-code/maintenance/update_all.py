import os
import re
import glob

# Content map from the book for each module
book_content_map = {
    "M0": """
# Generative AI Foundations: Colab and Tensors

Before diving into the tools, it's essential to understand the paradigm shift we are experiencing. Traditional machine learning models, often referred to as discriminative models, focus on predicting outputs by learning the conditional probability of some expected output given an input. They are adept at tasks like classification or regression. Generative Artificial Intelligence (GenAI), on the other hand, seeks to learn and replicate complex data distributions to synthesize entirely new and original data, mirroring human-like outputs. 

According to *Generative AI Foundations in Python*, state-of-the-art generative models can behave as collaborators capable of synthetic understanding and generating sophisticated responses. The rapid growth of generative approaches fundamentally reshapes how we interact with technology. Whether you are synthesizing images with Diffusion models or generating text with Large Language Models (LLMs) based on the Transformer architecture, these models require immense computational power. This is where tools like Google Colab become indispensable for modern AI development. Jupyter notebooks enable live code execution, visualization, and explanatory text, suitable for prototyping and data analysis. Google Colab is a cloud-based version of Jupyter Notebook specifically designed for machine learning prototyping. It provides free GPU resources and integrates directly with Google Drive for file storage and sharing, making it the perfect environment to handle the computational complexity of deep generative models.
""",
    "M1": """
# Foundations of NLP and Early Generative Systems

In *Generative AI Foundations in Python*, the evolution of NLP is traced from simple count-based methods to the advanced neural networks we see today. Before the widespread use of neural networks (NNs) in language processing, NLP was largely grounded in methods that counted words. Two particularly notable techniques were count vectors and Term Frequency-Inverse Document Frequency (TF-IDF). These count-based methods were successful for tasks such as searching and categorizing, but they could not capture the semantic relationships between words, meaning they could not interpret the nuanced meanings of words in context. 

This challenge paved the way for exploring NNs, offering a deeper and more nuanced way to understand and represent text. In 2003, Yoshua Bengio's team introduced the Neural Network Language Model (NNLM), designed to predict the next word in a sequence based on prior words using hidden layers that learned word embeddings. These embeddings are compact vector representations capturing the core semantic meanings of words. This marked a monumental shift in the field's capability to understand and process language.
""",
    "M2": """
# Distributed Representations and Continuous Vector Spaces

Following the inception of the NNLM, NLP research was propelled toward crafting high-quality word vector representations. As detailed in *Generative AI Foundations in Python*, this period saw the emergence of Word2Vec and GloVe. These methods applied distributed representation to craft high-quality word vector representations. Distributed representation portrays items such as words not as unique identifiers but as sets of continuous values or vectors. In these vectors, each value corresponds to a specific feature or characteristic of the item. 

Word2Vec uses NNs to predict surrounding words for each target word, ascertaining weights that form a vector in a continuous vector space—a mathematical space wherein each point represents a possible value a vector can take. GloVe analyzes global co-occurrence statistics to learn vector representations that capture the relationships between words. Both Word2Vec and GloVe excel at encapsulating relevant semantic information about words to represent an efficient encoding—a compact way of representing information that captures the essential features necessary for a task while reducing the dimensionality and complexity of the data.
""",
    "M3": """
# Sequence Models and the Emergence of the Transformer

According to *Generative AI Foundations in Python*, modeling long-range dependencies required more sophisticated network architectures, leading to the use of RNNs. Recurrent Neural Networks process data sequences by iterating through each element while maintaining a dynamic internal state. This was further improved by Long Short-Term Memory (LSTM) networks, which applied a unique gating architecture to control the flow of information, maintaining and accessing information over long sequences without suffering from the vanishing gradient problem.

Concurrently, Convolutional Neural Networks (CNNs) were adapted for NLP to extract hierarchical features using convolutional layers over local n-gram windows. However, the true paradigm shift occurred in 2017 with the introduction of the Transformer architecture by Vaswani et al. The Transformer applied a self-attention mechanism, allowing each element in the input sequence to focus on distinct parts of the sequence, capturing dependencies regardless of their positions. This sequence-to-sequence learning model became the foundation for all modern generative language models.
""",
    "M4": """
# Transformers, Self-Attention, and Prompt Engineering

At the core of the transformer architecture lies the self-attention mechanism. As described in *Generative AI Foundations in Python*, this mechanism captures complex relationships among different elements within an ordered data sequence. The principle of attention enables a model to focus on certain pivotal aspects of the input data while potentially disregarding less significant parts. 

The transformer bifurcates into two main segments: the encoder and the decoder. The encoder discerns relationships between different positions in the input sequence, while the decoder focuses on generating outputs, employing masked self-attention to prevent consideration of future outputs. To retain sequence order, the model adopts positional encoding, ensuring it preserves the initial order of data. Multi-head attention allows the model to channel attention toward multiple data points simultaneously, capturing a wider range of information from the same input words. This architecture powers the prompt-based generative tasks we rely on today.
""",
    "M5": """
# RAG Foundations and Domain Adaptation

Generative models, while powerful, often lack specific domain knowledge or access to up-to-date information. As outlined in *Generative AI Foundations in Python*, adapting a general-purpose LLM without extensive fine-tuning is achievable through prompt engineering and Retrieval-Augmented Generation (RAG). 

RAG provides techniques to ground the model's responses in factual data by retrieving relevant documents and including them in the context of the prompt. This addresses one of the primary limitations of generative models—hallucination—where models generate factually inaccurate information. By augmenting the model's inputs with additional information that is known to be factual, RAG ensures that the synthesized content is accurate, contextually relevant, and grounded in reality.
""",
    "M7": """
# Moving from Prototype to Production

Transitioning a generative AI prototype to a production-ready deployment involves careful consideration of model size, computational complexity, and robust evaluation. *Generative AI Foundations in Python* highlights the process of setting up a robust Python environment using Docker, CI/CD pipelines, and proper monitoring. 

Choosing the right pretrained generative model requires evaluating trade-offs between precision, speed, and resource constraints. It is also essential to have a strategy for evaluating model outputs. For example, using models like CLIP to evaluate the semantic alignment between text and images provides a quantitative measure of fidelity. Beyond metrics, production deployment must emphasize responsible AI practices, addressing transparency, explainability, and the mitigation of inherent biases.
""",
    "M8": """
# Fine-Tuning, BERT, and Ethical Considerations

The evolution of Transformers led to models like BERT (Bidirectional Encoder Representations from Transformers), which analyze sentences bidirectionally to capture deep semantic and syntactic nuances. While foundation models are versatile, fine-tuning them for specific tasks further enhances their capabilities. *Generative AI Foundations in Python* examines how Parameter-Efficient Fine-Tuning (PEFT) and Low-Rank Adaptation (LoRA) facilitate approachable continued training for specific tasks without the computational overhead of full fine-tuning.

However, deploying these models requires rigorous ethical oversight. Generative models inevitably learn societal biases embedded in the training data and are susceptible to toxicity and accidental memorization of sensitive information. A human-centered AI governance strategy, combining technical improvements, robust guidelines, and ethical reflections, is essential to ensure fairness, accountability, and the responsible adoption of these transformative technologies.
"""
}

def process_file(filepath, module_num):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add fig-alt to images
    def replace_image(match):
        alt = match.group(1)
        path = match.group(2)
        options = match.group(3) or ''
        
        if 'fig-alt' not in options:
            if options:
                if options.endswith('}'):
                    options = options[:-1] + ' fig-alt=\"' + (alt if alt else 'Image description') + '\"}'
            else:
                options = '{fig-alt=\"' + (alt if alt else 'Image description') + '\"}'
        return f'![{alt}]({path}){options}'

    new_content = re.sub(r'!\[(.*?)\]\((.*?)\)(\{.*?\})?', replace_image, content)
    
    # 2. Add Book Content if not already present
    book_content = book_content_map.get(module_num)
    if book_content and "Generative AI Foundations" not in new_content:
        # Find the first heading and insert before it, or right after the YAML frontmatter
        yaml_end = new_content.find('---', 3)
        if yaml_end != -1:
            insertion_point = yaml_end + 3
            new_content = new_content[:insertion_point] + "\n\n" + book_content.strip() + "\n\n" + new_content[insertion_point:]

    # 3. Incorporate an image from the module's figures if available
    # We will pick the first image in M{num}_lecture01_figures or M{num}_lecture02_figures and add it at the end of the book content
    figures_dirs = glob.glob(f"{module_num}_lecture*_figures")
    if figures_dirs:
        for fig_dir in figures_dirs:
            images = glob.glob(f"{fig_dir}/*.png") + glob.glob(f"{fig_dir}/*.jpeg") + glob.glob(f"{fig_dir}/*.jpg")
            if images:
                image_path = images[0].replace('\\', '/')
                # Check if image is already in the document
                if image_path not in new_content:
                    image_md = f'\n\n![Related Figure from {fig_dir}](./{image_path}){{fig-alt="Related figure from {fig_dir}" width=80% fig-align="center"}}\n\n'
                    # insert after the book content
                    if book_content:
                        book_content_idx = new_content.find(book_content.strip())
                        if book_content_idx != -1:
                            insert_idx = book_content_idx + len(book_content.strip())
                            new_content = new_content[:insert_idx] + image_md + new_content[insert_idx:]
                break

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Processed {filepath}')

modules = ["M0", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"]

for module in modules:
    qmd_files = glob.glob(f"{module}/*_LN*.qmd")
    for qmd in qmd_files:
        # Ignore M6 and some M8 as discussed
        if "M06" in qmd or "M08_LN2" in qmd or "M08_LN4" in qmd:
            continue
        process_file(qmd, module)

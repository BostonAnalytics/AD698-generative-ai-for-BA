$ErrorActionPreference = 'Stop'

# Map each LN file (by basename) to its topic-specific categories
$categoryMap = @{
    'M0_LN1'   = "['M0:', 'Colab', 'GPU', 'Tensors', 'Lecture Notes']"
    'M0_LN2'   = "['M0:', 'Mathematics', 'Neural Networks', 'SGD', 'Lecture Notes']"
    'M0_LN3'   = "['M0:', 'Linear Models', 'MLP', 'Deep Learning', 'Lecture Notes']"
    'M01_LN1'  = "['M01:', 'Neural Networks', 'NLP', 'History of AI', 'Lecture Notes']"
    'M01_LN2'  = "['M01:', 'Language Models', 'Probability', 'Generative AI', 'Lecture Notes']"
    'M02_LN1'  = "['M02:', 'Mathematics', 'Language Modeling', 'Foundations', 'Lecture Notes']"
    'M02_LN2'  = "['M02:', 'Text Representation', 'Structured Text', 'NLP', 'Lecture Notes']"
    'M03_LN1'  = "['M03:', 'Prompt Engineering', 'System Design', 'LLM', 'Lecture Notes']"
    'M03_LN2'  = "['M03:', 'Tokenization', 'Embeddings', 'Semantic Search', 'Lecture Notes']"
    'M04_LN1'  = "['M04:', 'Transformers', 'Attention', 'Context Windows', 'Lecture Notes']"
    'M04_LN2'  = "['M04:', 'Fine-Tuning', 'Training', 'Transfer Learning', 'Lecture Notes']"
    'M05_LN1'  = "['M05:', 'RAG', 'Retrieval', 'Vector Search', 'Lecture Notes']"
    'M05_LN2'  = "['M05:', 'RAG', 'Generation', 'Evaluation', 'Lecture Notes']"
    'M06_LN1'  = "['M06:', 'Agentic AI', 'Autonomous Systems', 'AI Agents', 'Lecture Notes']"
    'M06_LN2'  = "['M06:', 'Agentic AI', 'LangChain', 'Implementation', 'Lecture Notes']"
    'M07_LN1'  = "['M07:', 'Business Analytics', 'Dashboards', 'Applied AI', 'Lecture Notes']"
    'M07_LN2'  = "['M07:', 'Business Analytics', 'Applied AI', 'Lecture Notes']"
    'M08_LN1'  = "['M08:', 'Neural Networks', 'Classification', 'Regression', 'Lecture Notes']"
    'M08_LN2'  = "['M08:', 'Neural Networks', 'Deep Learning', 'Lecture Notes']"
    'M08_LN3'  = "['M08:', 'BERT', 'Transformers', 'PyTorch', 'Lecture Notes']"
    'M08_LN4'  = "['M08:', 'Applied AI', 'Deep Learning', 'Lecture Notes']"
}

$updated = 0
foreach ($key in $categoryMap.Keys) {
    $files = Get-ChildItem -Recurse -File -Filter "$key.qmd" | Where-Object { $_.FullName -match '\\M[0-8]\\' }
    foreach ($f in $files) {
        $raw = Get-Content -Raw -Path $f.FullName
        $newCat = $categoryMap[$key]
        # Replace the categories line
        $newRaw = $raw -replace '(?m)^categories:\s*\[.*\]\s*$', "categories: $newCat"
        if ($newRaw -ne $raw) {
            [System.IO.File]::WriteAllText($f.FullName, $newRaw, [System.Text.UTF8Encoding]::new($false))
            $updated++
            Write-Output "Updated: $($f.Name)"
        }
    }
}
Write-Output "Total updated: $updated"

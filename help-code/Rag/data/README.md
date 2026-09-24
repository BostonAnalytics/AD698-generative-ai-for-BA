# Tesla sample for presentation rendering

`tesla_10k_render_sample.json` contains four excerpts from the local Tesla 10-K
file `20240129_10-K_edgar_data_1318605_0001628280-24-002390.txt` in
`data/SEC-10K-2024`. Accession: `0001628280-24-002390`.

The filing date is January 29, 2024; its fiscal year is 2023. `filing_year`
therefore means 2024, not the fiscal year. Each excerpt retains its Item number,
source filename, accession, and dates. Text was extracted with BeautifulSoup
using the `lxml` parser, removing header/script/style tags and collapsing
whitespace. The excerpts are contiguous selections, not generated summaries.

The sample covers battery supply risk, production ramp risk, the customer
network, and the energy segment. These short selections are deliberately chosen
for teaching and are not representative evaluation data or a multi-year corpus.

`M5/M05_P2.qmd` loads this small tracked file during rendering. It demonstrates
chunking, TF-IDF retrieval, prompt formatting, a cited extractive answer, and
precision/recall against explicitly identified relevant excerpts. No downloads,
embedding-model inference, or model API calls are required by these demos.
Run the parent folder's notebooks for the full RAG and RAGAS workflows.

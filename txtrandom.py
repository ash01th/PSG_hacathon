from utils import extract_text 
from utils import extract_text_from_pdf
from utils import count_tokens
from utils import optional_embedding
from utils import split_text_into_chunks
from utils import create_embeddings
from utils import store_embeddings_in_chromadb
from utils import get_relevant_data
from llm_completion import get_response_from_llama

text = extract_text("NarasimhaKarumanchi-DSA.pdf")
print("embedding_needed:", optional_embedding(text))
chunks = split_text_into_chunks(text, "NarasimhaKarumanchi-DSA.pdf")
print(len(chunks))

embeddings = []
for i, chunk in enumerate(chunks[:5]):
    print(f"Creating embedding for chunk {i + 1}")
    embedding = create_embeddings(chunk, "n/a")
    embeddings.append(embedding)


print(len(embeddings))
nums=[str(i) for i in range(len(embeddings))]
store_embeddings_in_chromadb(text=chunks[:5],embeddings=embeddings,file_name=nums)
chunk1=get_relevant_data("fetch me details about narasimha karumanchi")

msg=[
    {"role":"system",
     "content":"""You are an AI assistant specializing in providing accurate, context-based responses. Your role is to analyze the provided context and answer user queries with precision and reliability.
Task Instructions:

Context Analysis


Carefully examine the provided context
Identify key information relevant to the query
Note any temporal or situational constraints in the context


Response Framework


Begin with a direct answer to the query
Support your response with specific quotes or references from the context
Maintain factual accuracy and avoid speculation


Response Requirements


Base your answer exclusively on the provided context
Do not incorporate external knowledge
If information is missing or unclear in the context, acknowledge these gaps
Present information in order of relevance to the query


Accuracy Guidelines


Use exact quotes when citing specific facts or figures
Maintain the original meaning and nuance of the context
Acknowledge any ambiguity in the context
Preserve the temporal context of the information


Output Format


Structure your response in clear paragraphs
Use quotation marks for direct citations
Begin with the most relevant information
End with any necessary caveats or limitations

If the context is insufficient to answer the query:

State clearly that the information is not present in the context
Specify what aspects of the query cannot be answered
Identify what additional information would be needed to provide a complete answer

Response Format:
[Direct answer to the query, supported by context]
[Additional relevant details from context]
[Any necessary caveats or limitations]"""},
{"role":"user","content":f"""the context for the query is {chunk1}  fetch me details in regards to the query 'fetch me details about narasimha karumanchi' """}
]
print(get_response_from_llama(msg))
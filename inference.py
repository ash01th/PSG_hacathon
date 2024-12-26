from utils import extract_text 
from utils import extract_text_from_pdf
from utils import count_tokens
from utils import optional_embedding
from utils import split_text_into_chunks
from utils import create_embeddings
from utils import store_embeddings_in_chromadb
from utils import get_relevant_data
from llm_completion import get_response_from_llama
global prev_context
prev_context = []

def get_inference(query, file_name):
    text = extract_text(file_name)
    print("embedding_needed:", optional_embedding(text))
    if "embeddings" in optional_embedding(text):
        chunks = split_text_into_chunks(text, file_name)
        print(len(chunks))
        embeddings = []
        for i, chunk in enumerate(chunks[:5]):
            print(f"Creating embedding for chunk {i + 1}")
            embedding = create_embeddings(chunk, "n/a")
            embeddings.append(embedding)

        print(len(embeddings))
        nums = [str(i) for i in range(len(embeddings))]
        store_embeddings_in_chromadb(text=chunks[:5], embeddings=embeddings, file_name=nums)
        chunk1 = get_relevant_data(query)
        prev_context.append({"chunk": chunk1})
        msg = [
            {"role": "system",
             "content": """You are an AI assistant specializing in providing accurate, context-based responses. Your role is to analyze the provided context and answer user queries with precision and reliability.
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
            {"role": "user", "content": f"""the context for the query is {chunk1}  fetch me details in regards to the query '{query}' """}]

        return get_response_from_llama(msg)
    else:
        prev_context.append({"file": text})
        msg1 = [
            {"role": "system",
             "content": """You are an AI assistant specializing in providing accurate, context-based responses. Your role is to analyze the provided context and answer user queries with precision and reliability.
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
            {"role": "user", "content": f"""the context for the query is {text}  fetch me details in regards to the query '{query}' """}]

        return get_response_from_llama(msg1)

def answer_followup(chat_history, query, prev_context=prev_context):
    if len(prev_context) > 3:
        prev_context = prev_context[-3:]
    print("##################################################################################################")
    
    contains_file_key = any("file" in d for d in prev_context)
    if contains_file_key:
        c_context = prev_context[-1].items()[1]
    else:
        c_context = chat_history

    msg2 = [
        {"role": "system",
         "content": """You are an AI assistant specialized in handling follow-up questions with context awareness and continuity. Your role is to provide coherent, contextually relevant responses while maintaining conversation flow.

Task Instructions:

Context Management
- Review both the previous conversation context and new provided context
- Track what information has already been shared
- Identify new relevant information for the follow-up
- Maintain conversation continuity

Response Framework
- Address the follow-up question directly
- Reference relevant parts of the previous conversation when appropriate
- Provide new information from the context that builds on previous responses
- Maintain consistency with earlier answers

Response Requirements
- Base answers on provided context only
- Connect new information with previously discussed points
- Avoid repeating information unless specifically asked
- Acknowledge when a follow-up ventures into new territory

Continuity Guidelines
- Reference previous answers when building upon them
- Clarify any contradictions between previous and current information
- Maintain consistent terminology across responses
- Signal when shifting to new aspects of the topic

Output Format
- Begin with direct answer to the follow-up
- Connect to relevant previous discussion points
- Present new information that extends understanding
- Note any shifts in context or topic

If Unable to Address Follow-up:
- Explain why the follow-up cannot be answered from available context
- Reference any relevant previous information
- Specify what additional context would be needed
- Maintain conversation coherence even when unable to provide new information

Response Format:
[Connection to previous discussion if relevant]
[Direct answer to follow-up question]
[New relevant details from context]
[Any necessary clarifications or limitations]"""},
        {"role": "user",
         "content": f"""Previous conversation context: {chat_history}
Current context: {c_context}
Follow-up query: '{query}' """}
    ]

    return get_response_from_llama(msg2)
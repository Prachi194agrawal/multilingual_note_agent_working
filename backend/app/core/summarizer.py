# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains.summarize import load_summarize_chain
# from langchain.llms import DeepSeek
# from typing import Dict, List

# def extract_action_items(text: str) -> List[str]:
#     """
#     Extract action items from the transcript using LLM.
    
#     Args:
#         text: The transcript text
        
#     Returns:
#         List of action items
#     """
#     llm = DeepSeek()
#     prompt = f"""
#     Extract all action items from the following meeting transcript. 
#     An action item is a specific task that needs to be completed.
#     Format each action item as a separate line starting with "- ".
#     If there are no action items, return "No action items found."
    
#     Transcript:
#     {text}
    
#     Action Items:
#     """
    
#     response = llm(prompt)
    
#     # Process the response to extract action items
#     action_items = []
#     for line in response.strip().split('\n'):
#         if line.startswith('- '):
#             action_items.append(line[2:])
    
#     return action_items

# def summarize_transcript(text: str) -> Dict[str, any]:
#     """
#     Summarize a meeting transcript using LangChain + DeepSeek.
    
#     Args:
#         text: The transcript text
        
#     Returns:
#         Dictionary containing summary and action items
#     """
#     # Split text into chunks if it's too long
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=4000,
#         chunk_overlap=200
#     )
    
#     texts = text_splitter.split_text(text)
    
#     # Initialize LLM
#     llm = DeepSeek()
    
#     # Summarization chain
#     chain = load_summarize_chain(llm, chain_type="map_reduce")
    
#     # Generate summary
#     summary = chain.run(texts)
    
#     # Extract action items
#     action_items = extract_action_items(text)
    
#     return {
#         "summary": summary,
#         "action_items": action_items
#     }



from typing import Dict, List
import re

def extract_action_items(text: str) -> List[str]:
    """
    Extract action items from the transcript using simple keyword-based approach
    
    Args:
        text: The transcript text
        
    Returns:
        List of action items
    """
    # Simple rule-based extraction
    lines = text.split('.')
    action_items = []
    
    # Keywords that often indicate action items
    keywords = ["need to", "should", "have to", "will", "must", "going to", "plan to", 
                "action item", "task", "todo", "action", "deadline", "by friday", 
                "by monday", "next week", "prepare", "schedule", "update", "create"]
    
    for line in lines:
        line = line.strip()
        if any(keyword in line.lower() for keyword in keywords):
            if len(line) > 10:  # Avoid very short lines
                action_items.append(line)
    
    # If no action items found with keywords, extract sentences that might be tasks
    if not action_items:
        for line in lines:
            line = line.strip()
            words = line.split()
            if len(words) > 3 and words[0].lower() in ["prepare", "create", "develop", "implement", 
                                                     "review", "schedule", "send", "follow", "update", "complete"]:
                action_items.append(line)
    
    return action_items[:5]  # Limit to top 5 action items

def summarize_transcript(text: str) -> Dict[str, any]:
    """
    Summarize a meeting transcript using simple extractive approach.
    
    Args:
        text: The transcript text
        
    Returns:
        Dictionary containing summary and action items
    """
    # Simple extractive summarization
    sentences = re.split(r'[.!?]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return {
            "summary": "No text to summarize.",
            "action_items": []
        }
    
    # Start with the first sentence (often contains context)
    summary_sentences = [sentences[0]] if sentences else []
    
    # Look for important sentences based on keywords
    important_terms = ["key", "important", "conclusion", "summary", "decided", "agreed", "plan", 
                      "result", "outcome", "goal", "objective", "priority"]
    
    for sentence in sentences[1:]:  # Skip the first sentence as we already included it
        if any(term in sentence.lower() for term in important_terms):
            if sentence not in summary_sentences:
                summary_sentences.append(sentence)
    
    # If we don't have enough sentences, add more based on length (longer sentences often have more info)
    if len(summary_sentences) < 3 and len(sentences) > 1:
        # Sort remaining sentences by length
        remaining = [s for s in sentences if s not in summary_sentences]
        remaining.sort(key=len, reverse=True)
        summary_sentences.extend(remaining[:3 - len(summary_sentences)])
    
    # Combine sentences into summary
    summary = ". ".join(summary_sentences)
    if not summary.endswith('.'):
        summary += '.'
    
    # Extract action items
    action_items = extract_action_items(text)
    
    return {
        "summary": summary,
        "action_items": action_items
    }
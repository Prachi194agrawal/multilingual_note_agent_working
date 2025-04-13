# import os
# import whisper
# from typing import Tuple

# # Load Whisper model once at module level for better performance
# model = whisper.load_model("base")

# def transcribe_audio(audio_path: str) -> Tuple[str, str]:
#     """
#     Transcribe audio file using Whisper and detect language.
    
#     Args:
#         audio_path: Path to the audio file
        
#     Returns:
#         A tuple containing (transcript, detected_language)
#     """
#     # Check if file exists
#     if not os.path.exists(audio_path):
#         raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
#     # Process with Whisper
#     result = model.transcribe(audio_path)
    
#     transcript = result["text"]
#     language = result["language"]
    
#     return transcript, language



import os
import random
from typing import Tuple

def detect_language(text):
    """
    Simple mock language detection.
    In a real implementation, you would use a language detection library.
    """
    # This is a simplified mock implementation
    # In a real app, you'd use a language detection library
    english_words = ["the", "and", "is", "in", "it", "to", "of", "for", "with", "on"]
    mandarin_words = ["的", "是", "不", "我", "有", "个", "他", "这", "们", "在"]
    cantonese_words = ["呢", "咁", "嘅", "係", "喺", "唔", "咗", "佢", "啲", "同"]
    
    text_lower = text.lower()
    
    # Count word occurrences
    english_count = sum(1 for word in english_words if word in text_lower)
    mandarin_count = sum(1 for word in mandarin_words if word in text_lower)
    cantonese_count = sum(1 for word in cantonese_words if word in text_lower)
    
    # Determine language based on highest count
    if english_count > mandarin_count and english_count > cantonese_count:
        return "en"
    elif mandarin_count > english_count and mandarin_count > cantonese_count:
        return "zh"
    elif cantonese_count > english_count and cantonese_count > mandarin_count:
        return "yue"
    else:
        # Default to English if uncertain
        return "en"

def transcribe_audio(audio_path: str) -> Tuple[str, str]:
    """
    Mock implementation of audio transcription.
    In a real implementation, you would use a speech recognition service.
    
    Args:
        audio_path: Path to the audio file
        
    Returns:
        A tuple containing (transcript, detected_language)
    """
    # Check if file exists
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Get file extension
    _, file_extension = os.path.splitext(audio_path)
    
    # Mock transcript based on file size
    file_size = os.path.getsize(audio_path)
    file_name = os.path.basename(audio_path)
    
    # Create a mock transcript
    mock_transcripts = {
        "en": [
            "Today we discussed the quarterly results. Sales have increased by 15% compared to last quarter.",
            "John will prepare the presentation for next week's meeting. Sarah will contact the clients.",
            "We need to focus on improving our customer service experience. The team agreed to implement new support tools.",
            "Action items from this meeting: 1. Update the website by Friday. 2. Schedule team training for next month.",
            "The project deadline is extended to May 15th. Everyone should update their tasks in the project management tool."
        ],
        "zh": [
            "今天我们讨论了季度业绩。与上季度相比，销售额增长了15％。",
            "约翰将为下周的会议准备演示文稿。莎拉将与客户联系。",
            "我们需要专注于改善客户服务体验。团队同意实施新的支持工具。",
            "会议行动项目：1.在星期五之前更新网站。2.安排下个月的团队培训。",
            "项目截止日期延长至5月15日。每个人都应该在项目管理工具中更新他们的任务。"
        ],
        "yue": [
            "今日我哋討論咗季度業績。同上季度比較，銷售額增長咗15％。",
            "約翰將為下星期嘅會議準備演示文稿。莎拉將同客戶聯繫。",
            "我哋需要專注於改善客戶服務體驗。團隊同意實施新嘅支持工具。",
            "會議行動項目：1.喺星期五之前更新網站。2.安排下個月嘅團隊培訓。",
            "項目截止日期延長至5月15日。每個人都應該喺項目管理工具中更新佢哋嘅任務。"
        ]
    }
    
    # Decide mock language based on filename or random selection
    if "english" in file_name.lower() or "en" in file_name.lower():
        language = "en"
    elif "mandarin" in file_name.lower() or "zh" in file_name.lower():
        language = "zh"
    elif "cantonese" in file_name.lower() or "yue" in file_name.lower():
        language = "yue"
    else:
        # Random selection with bias towards English
        language = random.choices(["en", "zh", "yue"], weights=[0.6, 0.2, 0.2])[0]
    
    # Select a random transcript in the chosen language
    transcript = " ".join(random.sample(mock_transcripts[language], 
                          k=min(3, len(mock_transcripts[language]))))
    
    return transcript, language
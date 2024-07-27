import streamlit as st
import requests

def get_transcript_from_api(video_id):
    api_url = f"https://youtube-transcriber-api-iot.vercel.app/v1/transcripts?id={video_id}" # your host
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            transcript_data = response.json()
            if 'transcripts' in transcript_data:
                return transcript_data['transcripts']
            else:
                return "Transcript data not available."
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"

def format_transcript(transcripts, max_length=80):
    paragraphs = []
    current_paragraph = []

    for entry in transcripts:
        text = entry['text']
        if len(" ".join(current_paragraph)) + len(text) > max_length:
            paragraphs.append(" ".join(current_paragraph))
            current_paragraph = [text]
        else:
            current_paragraph.append(text)

    if current_paragraph:
        paragraphs.append(" ".join(current_paragraph))

    formatted_transcript = "\n\n".join(paragraphs)
    return formatted_transcript

st.title("YouTube Transcript Extractor")
st.write("Enter the URL of a YouTube video to extract and format its transcript.")

url = st.text_input("YouTube Video URL", "https://www.youtube.com/watch?v=XPTscnVqYwY")
if url:
    # Extract the video ID from the URL
    try:
        if "v=" in url:
            video_id = url.split("v=")[-1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[-1]
        else:
            st.error("Invalid YouTube URL.")
            video_id = None

        if video_id:
            transcripts = get_transcript_from_api(video_id)
            if transcripts:
                formatted_transcript = format_transcript(transcripts)
                st.subheader("Formatted Transcript")
                st.write(formatted_transcript)
            else:
                st.error("Unable to retrieve transcript. Please check the video URL or try a different video.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

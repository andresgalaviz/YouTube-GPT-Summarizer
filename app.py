from flask import Flask, request, jsonify, render_template
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import os
import openai
import re

app = Flask(__name__)
openai.api_key = os.environ.get("API_KEY")


def extract_video_id(url):
    pattern = r"(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/(?:watch\?v=)?([\w-]+)(?:[^\s]+)?"
    match = re.match(pattern, url)
    if match:
        return match.group(1)
    return None


def get_video_title(video_id) -> str | None:
    try:
        yt = YouTube(
            f"https://www.youtube.com/watch?v={video_id}",
            allow_oauth_cache=True,
        )
        vid_info = yt.vid_info
        title = yt.title
        return title
    except Exception as e:
        print(e)
        return None


def split_transcript(transcript_text, max_tokens=4000):
    words = transcript_text.split()
    chunks = []
    chunk = []
    chunk_size = 0
    for word in words:
        if chunk_size + len(word) >= max_tokens:
            chunks.append(chunk)
            chunk = []
            chunk_size = 0

        chunk.append(word)
        chunk_size += len(word)

    if chunk:
        chunks.append(chunk)

    return chunks


def summarize_chunks(title, chunks):
    summaries = []

    for chunk in chunks:
        chunk_text = " ".join(chunk)
        summary = summarize_transcript(title, chunk_text)
        summaries.append(summary)

    return " ".join(summaries)


def summarize_transcript(title, transcript_text):
    print("Summarizing transcript...")
    prompt = f"Transcript from video titled {title}: {transcript_text}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a youtube transcript summarizer. You will be given a transcript from a youtube video. Summarize the transcript in a way that is easy to understand.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return response["choices"][0]["message"]["content"].strip()


@app.route("/get_summary", methods=["POST"])
def get_summary():
    video_url = request.get_json()["url"]
    video_id = extract_video_id(video_url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"})
    title = get_video_title(video_id)

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        return jsonify({"error": str(e)})

    transcript_text = " ".join([entry["text"] for entry in transcript])
    transcript_chunks = split_transcript(transcript_text, max_tokens=4000)
    summary = summarize_chunks(title, transcript_chunks)

    return jsonify({"title": title, "summary": summary})


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)

import os
import re
import glob
import subprocess

# List of YouTube URLs provided by the user
URLS = [
    "https://www.youtube.com/watch?v=489KJG-vjeM&authuser=2",
    "https://www.youtube.com/watch?v=Uim1hoY_oi0&authuser=2",
    "https://www.youtube.com/watch?v=BIfjNfVjS-0&authuser=2",
    "https://www.youtube.com/watch?v=aTcoRUoyBsE&authuser=2",
    "https://www.youtube.com/watch?v=j7rPtDoieps&authuser=2",
    "https://www.youtube.com/watch?v=YhkjxAMxt5k&authuser=2",
    "https://www.youtube.com/watch?v=R0wwmzziS5Y&authuser=2",
    "https://www.youtube.com/watch?v=yXnKNUvMUTs&authuser=2"
]

YT_DLP_PATH = "/Users/ttoloza/Library/Python/3.13/bin/yt-dlp"

def clean_text(text):
    # Remove HTML/XML tags
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def clean_vtt_content(vtt_text):
    # Split by blank lines to get blocks
    blocks = vtt_text.replace('\r\n', '\n').split('\n\n')
    
    all_words = []
    
    for block in blocks:
        lines = block.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Skip WebVTT header, metadata, number blocks, or timestamp lines
            if line.startswith('WEBVTT') or '-->' in line or line.isdigit() or line.startswith('Note:') or line.startswith('Kind:') or line.startswith('Language:'):
                continue
            
            cleaned = clean_text(line)
            if not cleaned:
                continue
            
            # Split into words
            words = cleaned.split()
            if not words:
                continue
            
            # Find overlap between all_words suffix and words prefix
            max_overlap = 0
            for i in range(1, min(len(all_words), len(words)) + 1):
                suffix = all_words[-i:]
                prefix = words[:i]
                if [w.lower() for w in suffix] == [w.lower() for w in prefix]:
                    max_overlap = i
            
            # Add non-overlapping words
            all_words.extend(words[max_overlap:])
    
    # Format into list items/paragraphs of ~80 words for readability
    paragraphs = []
    chunk_size = 80
    for i in range(0, len(all_words), chunk_size):
        paragraph = " ".join(all_words[i:i+chunk_size])
        if paragraph:
            paragraphs.append("- " + paragraph)
            
    return "\n".join(paragraphs)

def main():
    if not os.path.exists("cookies.txt"):
        print("Error: cookies.txt not found. Please export your YouTube cookies and place them in this folder.")
        print("See the instructions on how to export cookies in the response.")
        return

    print("Starting transcription process for 8 videos...")
    
    # Set up environment variables including Homebrew node path
    env = os.environ.copy()
    env["PATH"] = f"/opt/homebrew/bin:{env.get('PATH', '')}"
    
    # Base arguments for yt-dlp to solve JS challenges correctly
    yt_dlp_base_args = [
        YT_DLP_PATH,
        "--cookies", "cookies.txt",
        "--js-runtimes", "node:/opt/homebrew/bin/node",
        "--remote-components", "ejs:github"
    ]
    
    for idx, url in enumerate(URLS, 1):
        print(f"\nProcessing video {idx}/8: {url}")
        
        # 1. Get the video title
        try:
            cmd_title = yt_dlp_base_args + ["--get-filename", "-o", "%(title)s", url]
            res_title = subprocess.run(
                cmd_title,
                capture_output=True,
                text=True,
                check=True,
                env=env
            )
            title = res_title.stdout.strip()
            # Replace characters that might be invalid in file names
            title_clean = re.sub(r'[\\/*?:"<>|]', "", title)
            filename = f"{idx:02d}_{title_clean}.md"
            print(f"Video title: {title}")
        except Exception as e:
            print(f"Error getting title for {url}: {e}")
            filename = f"{idx:02d}_video.md"
            title = f"Video {idx}"

        # 2. Download subtitles as WebVTT using yt-dlp
        temp_base = f"temp_sub_{idx}"
        try:
            print("Downloading subtitles...")
            cmd_download = yt_dlp_base_args + [
                "--write-subs",
                "--write-auto-subs",
                "--sub-lang", "es",
                "--skip-download",
                "-o", temp_base,
                url
            ]
            subprocess.run(cmd_download, check=True, env=env)
            
            # Find the downloaded VTT file (might be es, es-419, etc.)
            vtt_files = glob.glob(f"{temp_base}.*.vtt")
            if not vtt_files:
                print(f"Warning: No subtitles found for {url}.")
                continue
                
            vtt_file = vtt_files[0]
            print(f"Downloaded subtitles file: {vtt_file}")
            
            # Read and clean VTT content
            with open(vtt_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            clean_transcript = clean_vtt_content(content)
            
            # 3. Write to output file matching the project markdown rule
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# Transcripcion: {title}\n\n")
                f.write(f"## Metadata\n\n")
                f.write(f"- Video URL: {url}\n\n")
                f.write(f"## Contenido\n\n")
                f.write(clean_transcript)
                f.write("\n")
                
            print(f"Saved transcription to {filename}")
            
            # Clean up temp file
            os.remove(vtt_file)
            
        except Exception as e:
            print(f"Error processing subtitles for {url}: {e}")

if __name__ == "__main__":
    main()

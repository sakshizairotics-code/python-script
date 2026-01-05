# Quote Videos (Phase-1 Starter Kit)

This starter project generates **vertical (9:16) quote videos** where each video shows **one quote (1–4 lines)** on screen for **30 seconds**.

- ✅ Super simple (solid background + centered text)
- ✅ Controlled via Excel/CSV
- ✅ Produces MP4 files ready for Shorts/Reels/TikTok

---

## Folder Structure

```
quote_videos_phase1/
  input/
    quotes.csv
    fonts/
      YourFont.ttf   <-- you add your font here
    bg/              (not used in phase-1; for phase-2)
  output/
  make_videos.py
  requirements.txt
```

---

## Step-by-step Setup (Windows)

### 1) Install Python
Install **Python 3.10+** and tick:
- ✅ **Add Python to PATH**

Verify:
```bash
python --version
```

### 2) Install FFmpeg (required)
MoviePy needs FFmpeg.

**Option A (Chocolatey):**
```bash
choco install ffmpeg -y
```

**Option B (Manual):**
1. Download FFmpeg build for Windows  
2. Add the `bin` folder to your Windows PATH  
3. Verify:
```bash
ffmpeg -version
```

If this command works, you’re ready.

### 3) Create virtual environment + install libraries
Open CMD/PowerShell inside this folder, then run:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Add a Font (IMPORTANT)

This project needs a `.ttf` font file.

1. Put a font file inside:
```
input/fonts/YourFont.ttf
```

2. In `input/quotes.csv`, set:
```
font_file = input/fonts/YourFont.ttf
```

**Where to get fonts?**
- Any `.ttf` you already have (Poppins/Inter/Roboto etc.)
- Download from Google Fonts (then use the `.ttf`)

---

## Prepare Quotes in Excel → Export CSV

Edit `input/quotes.csv` (you can open in Excel and save as CSV).

### Required columns:
- `output_name` → output mp4 name (without extension)
- `text` → quote text (1–4 lines; script auto-wraps)
- `duration` → set `30` for 30 seconds
- `bg_color` → hex like `#111827`
- `text_color` → `white` or `#FFFFFF`
- `font_file` → path to `.ttf`
- `font_size` → try 56–72
- `align` → `center` / `left` / `right`

---

## Run

With venv activated:

```bash
python make_videos.py
```

Videos will be created in:
```
output/
```

---

## Troubleshooting

### ❌ “ffmpeg not found”
Run:
```bash
ffmpeg -version
```
If it fails, FFmpeg is not installed or not in PATH.

### ❌ “Font not found”
Check:
- file exists at `input/fonts/YourFont.ttf`
- CSV points to exactly that path (case-sensitive on Linux)

### Text is too big / too small
Change `font_size` in CSV:
- 56 (small)
- 64 (default)
- 72 (large)

---

## Code Explanation (High level)

### `make_videos.py` does 3 main jobs:

1. **Read CSV**
   - Loads `input/quotes.csv` using pandas
   - Iterates each row (each row = one video)

2. **Render one image frame**
   - Creates a 1080x1920 background using Pillow
   - Wraps quote text so it fits width
   - Centers the text vertically and horizontally
   - Adds a small shadow for readability

3. **Convert frame into a 30-sec MP4**
   - MoviePy makes a static clip from the image
   - Uses FFmpeg to export `H.264` MP4

---

## Next Changes (Phase-2 ideas)

When Phase-1 is working, we can upgrade to:

1. **Background images / videos**
   - `bg_type = image/video`
   - `bg_path = input/bg/xxx.jpg`

2. **Music**
   - add `music_path`, `music_volume`
   - fade in/out

3. **Animations**
   - zoom-in / fade-in text
   - subtle movement for better retention

4. **Auto split long quotes**
   - one quote becomes 2–3 slides inside same 30 sec

5. **Batch rendering speed**
   - parallel export
   - caching fonts
   - faster preset tuning

---

If you want, share your final CSV format (columns you prefer),
and I’ll update Phase-2 structure to match it exactly.

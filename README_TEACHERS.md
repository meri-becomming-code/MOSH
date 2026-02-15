# Math to Canvas - For Exhausted Teachers 😴☕

## The Problem
You have handwritten solutions, worksheets, or equations. Students need them in Canvas. You're too tired to type LaTeX.

## The Solution
**Gemini does it for you.** One command. Done.

---

## ⚡ Quick Start (5 Minutes Setup, Then Forever Easy)

### Step 1: One-Time Setup (School IT can do this)
```powershell
# Install Python tools (copy/paste this, press Enter)
pip install google-generativeai pillow pdf2image

# Get Gemini API key from: https://aistudio.google.com/app/apikey
# Set it once:
set GEMINI_API_KEY=your_key_here
```

### Step 2: Every Time You Need to Convert
```powershell
# Put your PDF in a folder, then run:
python gemini_math_converter.py --pdf "Chapter_3_Solutions.pdf"

# Wait 2 minutes. Done. Gemini converted everything.
```

### Step 3: Paste into Canvas
Open `canvas_math_output.html`, copy all, paste in Canvas HTML editor. Save. **Done.**

**Time**: 2 minutes loading + 2 minutes to paste = **4 minutes total**  
**Manual typing**: 3+ hours

---

## What Gemini Does For You

✅ Reads your handwritten solutions  
✅ Converts to Canvas LaTeX format  
✅ Preserves problem numbers and steps  
✅ Makes equations accessible (screen readers work)  
✅ Makes equations searchable (students can copy/paste)  

**You do**: Drop file, run command, paste result  
**Gemini does**: Everything else

---

## Three Simple Commands (That's It!)

### Convert a PDF
```powershell
python gemini_math_converter.py --pdf "solutions.pdf"
```

### Convert photos from your phone
```powershell
# Put photos in a folder, then:
python gemini_math_converter.py --folder "whiteboard_photos/"
```

### Convert one equation image
```powershell
python gemini_math_converter.py --image "equation.png"
```

**Output**: Always `canvas_math_output.html` (ready to paste in Canvas)

---

## Real Example

**Monday Morning**:
1. You have a 10-page PDF of answer keys (handwritten)
2. Open PowerShell in your folder
3. Type: `python gemini_math_converter.py --pdf "Unit_4_Answers.pdf"`
4. Wait 2-3 minutes while Gemini works
5. Open `canvas_math_output.html`
6. Copy everything
7. Canvas → New Page → HTML view → Paste → Save
8. **Done!** Go get coffee ☕

**Time**: 5 minutes of your time (computer does the rest)

---

## Cost

**Option 1**: Gemini API Pay-as-you-go
- ~$0.001 per image (basically free)
- Semester cost: < $5

**Option 2**: Gemini Subscription
- $20/month per teacher
- **OR** $20/month for department (one shared key)

**Time saved**: 10+ hours per semester  
**Worth it?** Absolutely.

---

## Troubleshooting (2 Common Issues)

### "No API key"
```powershell
# Get key from: https://aistudio.google.com/app/apikey
set GEMINI_API_KEY=paste_your_key_here
```

### "pdf2image not installed"
```powershell
pip install pdf2image
# Also download: https://github.com/oschwartz10612/poppler-windows/releases
# Extract and add to PATH (or ask IT)
```

---

## Getting School to Pay for It

**Pitch to admin**:
> "For $20/month, our entire math department saves 50+ hours per semester converting materials to accessible Canvas format. That's $20 for 50 hours of work. ROI is 250:1."

**Result**: They'll say yes.

---

## That's It!

**Setup once** → **Run one command** → **Paste** → **Done**

No typing. No LaTeX. No exhaustion.

**Gemini does the work. You get the credit.** ⭐

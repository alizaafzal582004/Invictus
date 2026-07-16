# AI Push-Up Counter - Hunter System

Ek AI-powered push-up counter jo real-time mein aapke reps count karta hai with a futuristic Solo Leveling inspired UI.

## Features

- 🎥 **Real-time webcam tracking**
- 💪 **Automatic rep counting**
- 🎖️ **Rank system (E to S)**
- ⚔️ **Solo Leveling inspired UI**
- 📱 **Mobile responsive**

## Vercel Deployment

### Prerequisites
1. [Vercel account](https://vercel.com) banao
2. [Vercel CLI](https://vercel.com/cli) install karo:
   ```bash
   npm i -g vercel
   ```

### Deploy karne ke steps:

1. **Repository setup:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Push-up counter app"
   ```

2. **GitHub pe push karo (optional but recommended):**
   - GitHub pe new repository banao
   - Local repo ko GitHub se connect karo:
   ```bash
   git remote add origin https://github.com/yourusername/pushup-counter.git
   git branch -M main
   git push -u origin main
   ```

3. **Vercel deploy:**

   **Option A: Vercel CLI se:**
   ```bash
   vercel
   ```
   
   **Option B: Vercel Dashboard se:**
   - [vercel.com](https://vercel.com) pe jao
   - "New Project" click karo
   - GitHub repository select karo
   - Deploy karo!

4. **Environment setup:**
   - Vercel automatically Python runtime detect kar lega
   - `vercel.json` file already configured hai

### Important Notes:

- **Camera access:** Vercel pe deployed app sirf HTTPS se camera access kar sakta hai
- **Performance:** Serverless functions ke limitations ke wajah se processing thoda slow ho sakta hai
- **Model:** YOLO model remove kiya hai size limitations ke wajah se. Simple computer vision use kiya hai.

## Local Development

```bash
# Virtual environment banao
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Dependencies install karo
pip install -r requirements.txt

# App run karo
python api/app.py
```

## Project Structure

```
pushup_counter/
├── api/
│   └── app.py          # Flask backend for Vercel
├── templates/
│   └── index.html      # Frontend UI
├── vercel.json         # Vercel configuration
├── requirements.txt    # Python dependencies
├── app.py             # Original Streamlit app (backup)
└── README.md          # Ye file
```

## Usage Instructions

1. Website open karo
2. "START TRAINING" button press karo
3. Camera permission allow karo
4. Side profile mein khade ho jao (sideways to camera)
5. Push-ups start karo!
6. Real-time mein reps count honge

## Tips for Better Detection

- 📹 **Camera position:** Side angle se khade ho
- 💡 **Lighting:** Acchi lighting mein exercise karo
- 👕 **Clothing:** Contrasting colors pehno
- 🏠 **Background:** Plain background better hai

## Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Python Flask
- **Computer Vision:** OpenCV
- **Deployment:** Vercel
- **Design:** Solo Leveling inspired UI

---

**Made with ⚔️ by Hunter System**
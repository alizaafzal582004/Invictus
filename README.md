<div align="center">

# ⚔️ HUNTER PUSH-UP SYSTEM
### AI-Powered Real-Time Fitness Quest Tracker
**Every rep is XP. Every day skipped is a level lost.**

*"In a world where everyone can level up, only the ones who show up every single day become Hunters."*

[![Live Demo](https://img.shields.io/badge/🔴_LIVE_DEMO-Try_it_Now-00E5FF?style=for-the-badge)](https://either-keep-up-or-get-left-behind.streamlit.app/)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Pose_Estimation-7B2FFF?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-FF3B3B?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-4361FF?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-FFD700?style=for-the-badge)

</div>

---

## 📸

<div align="center">

<img width="1600" height="813" alt="App Screenshot" src="https://github.com/user-attachments/assets/482be19a-91f7-45d7-9f59-557f9efd28fb" />

*Real-time pose detection · Live rep counting · Daily Quest sync*

</div>

---

## 🎯 

> *"In the world of Solo Leveling, the weakest hunter became the strongest not through talent — but by refusing to skip a single day of training, even when no one was watching."*

Most fitness apps just count reps. **This one makes you accountable to a system that never lets you slack.**

Inspired by that exact mechanic, this app turns a simple push-up into a daily quest with real consequences:

- Show up every day → your **Flame 🔥** grows, your **Shadow Army 👥** expands, your daily target **levels up**.
- Skip a day → you lose a shadow. No excuses, no undo, no cheating the streak.

It's not just a rep counter — it's a **discipline engine**, built end-to-end with real-time computer vision, custom pose-based rep detection logic, a persistent progression system, and a production deployment pipeline solving real-world WebRTC/cloud infrastructure challenges.

> *"Either keep up, or get left behind."*

---

## 👩‍💻What This Project Demonstrates

This project was built solo, from a rough idea to a live, publicly deployed product — the same arc as taking a feature from concept to production in a real engineering team.

`Computer Vision` `Real-Time Inference Pipelines` `Algorithm Design` `Full-Stack Python` `Cloud Deployment Debugging` `WebRTC / Networking` `State Management` `Product Thinking` `UI/UX Design`

**In short:** I didn't just wire together a tutorial. I diagnosed and fixed dependency conflicts on a production server, engineered a custom counting algorithm resilient to real-world noise, designed a stateful system that behaves correctly across days without supervision, and shipped it live — end to end, alone.

---

## ✨ Features

| | |
|---|---|
| 🎥 **Live Hunter Mode** | Real-time push-up detection using your browser camera (powered by WebRTC) |
| 📁 **Upload Video** | Upload a recorded push-up video and get an automatic rep count with an annotated output video |
| 🏠 **Daily Quest Dashboard** | Track today's push-up target, progress bar, and completion status at a glance |
| 🔥 **Flame Streak** | A daily streak counter that grows only through consistency — no shortcuts |
| 👥 **Shadow Army** | Earn a shadow for every day you hit your target, lose one the day you don't |
| 📅 **Weekly Progression** | Complete 7/7 days in a week and your daily target levels up by +5 reps |
| 🎖️ **Hunter Rank System** | Climb from E-Rank to S-Rank Hunter as your Flame Streak grows |
| 💾 **Persistent Progress** | Your progress is saved automatically and picked up the moment you return — even if you skip days |

---

## 💡 Why This Project Stands Out

This isn't a tutorial clone — every layer was built and debugged from scratch:

- **Custom rep-detection algorithm**: elbow-angle tracking with confidence filtering, frame confirmation, and cooldown logic to eliminate false positives from pose jitter
- **Production deployment engineering**: solved real Streamlit Cloud constraints — Debian package conflicts, headless OpenCV builds, and outbound-UDP-blocked networks requiring a TURN-over-TCP relay configuration
- **Stateful progression system**: a day-rollover engine that correctly back-fills missed days (even multiple skipped days) and applies streak/penalty logic without the user ever opening the app
- **Performance tuning for constrained hardware**: frame resizing and frame-skipping to keep real-time inference usable on a free-tier cloud CPU with no GPU

---

## 🛠️ Tech Stack

| Component            | Technology                          |
|-----------------------|--------------------------------------|
| Pose Detection         | YOLOv8n-Pose (Ultralytics)          |
| Computer Vision        | OpenCV                              |
| Web Interface           | Streamlit                           |
| Live Camera Streaming    | streamlit-webrtc                    |
| Connectivity (NAT/Firewall) | TURN server (Metered.ca)        |

---

## 🚀 Getting Started (Run Locally)

### 1. Clone the repository
```bash
git clone https://github.com/alizaafzal582004/Invictus.git
cd Invictus
```

### 2. Create a virtual environment
```bash
py -3.11 -m venv venv
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 📖 How It Works

1. **Pose Estimation:** Each video frame is passed through a lightweight YOLOv8-Pose model to detect body keypoints (shoulders, elbows, wrists).
2. **Angle Calculation:** The elbow angle (shoulder–elbow–wrist) is calculated every frame.
3. **Rep Counting:** A push-up is counted when the arm angle transitions from a confirmed "down" position (< 105°) to a confirmed "up" position (> 145°).
4. **Daily Quest Sync:** Every counted rep is automatically synced to your Daily Quest progress.
5. **Day Rollover Logic:** When you open the app on a new day, the system checks whether the previous day's target was met and updates your Flame Streak and Shadow Army accordingly — even accounting for days you didn't open the app.

---

## 📂 Project Structure

```
Invictus/
├── app.py                  # Main Streamlit application
├── progress_manager.py     # Daily quest, streak, and shadow tracking logic
├── progress.json           # Local persistent progress data (auto-generated)
├── requirements.txt        # Python dependencies
├── packages.txt             # System-level dependencies (for cloud deployment)
├── yolov8n-pose.pt          # YOLOv8 pose estimation model weights
└── README.md                 # Project documentation
```

---

## ⚠️ Notes

- For best detection accuracy, position yourself **side-on** to the camera with your full arm (shoulder to wrist) visible in frame.
- Live camera mode requires camera permission in your browser.
- On the deployed version, live camera connections route through a TURN relay server, so the connection may take a few seconds to establish.

---

## 🚀 Try the Live Demo

Experience the AI-powered push-up tracking system in your browser.

**🔗 Live App:** https://either-keep-up-or-get-left-behind.streamlit.app/

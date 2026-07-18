import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import time
import threading
import av
from ultralytics import YOLO
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
from progress_manager import get_today_progress, add_pushups, get_rank_title, QUOTE

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Push-Up Counter | Hunter System", page_icon="⚔️", layout="wide")

# ---------------- SOLO LEVELING INSPIRED THEME ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    .stApp {
        background: radial-gradient(circle at top, #0a0e27 0%, #05070f 60%, #000000 100%);
        font-family: 'Orbitron', sans-serif;
    }

    .main-title {
        font-size: 48px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #7B2FFF, #4361FF, #00E5FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(123, 47, 255, 0.6);
        letter-spacing: 3px;
        margin-bottom: 0px;
        animation: glow-pulse 2.5s ease-in-out infinite;
    }

    @keyframes glow-pulse {
        0%, 100% { filter: drop-shadow(0 0 10px #7B2FFF); }
        50% { filter: drop-shadow(0 0 25px #00E5FF); }
    }

    .sub-title {
        text-align: center;
        color: #8A8FB9;
        font-size: 16px;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 30px;
    }

    .system-box {
        background: rgba(15, 20, 45, 0.6);
        border: 1px solid #4361FF;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(67, 97, 255, 0.4), inset 0 0 20px rgba(67, 97, 255, 0.1);
        margin-bottom: 15px;
    }

    .system-title {
        color: #00E5FF;
        font-weight: 700;
        letter-spacing: 2px;
        font-size: 14px;
        text-transform: uppercase;
        margin-bottom: 8px;
        border-bottom: 1px solid rgba(0, 229, 255, 0.3);
        padding-bottom: 6px;
    }

    .stat-value {
        font-size: 36px;
        font-weight: 900;
        color: #FFFFFF;
        text-shadow: 0 0 15px #4361FF;
    }

    .rank-badge {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 20px;
        font-weight: 900;
        font-size: 20px;
        letter-spacing: 2px;
        background: linear-gradient(135deg, #7B2FFF, #00E5FF);
        color: #05070f;
        box-shadow: 0 0 20px rgba(123, 47, 255, 0.7);
    }

    .flame-box {
        text-align: center;
        font-size: 60px;
        text-shadow: 0 0 25px #FF6A00, 0 0 45px #FF3B00;
        animation: flicker 1.5s infinite alternate;
    }

    @keyframes flicker {
        0% { text-shadow: 0 0 20px #FF6A00, 0 0 35px #FF3B00; }
        100% { text-shadow: 0 0 35px #FFD700, 0 0 55px #FF3B00; }
    }

    .quote-box {
        text-align: center;
        font-style: italic;
        color: #00E5FF;
        font-size: 18px;
        letter-spacing: 1px;
        padding: 15px;
        border-top: 1px solid rgba(0,229,255,0.3);
        border-bottom: 1px solid rgba(0,229,255,0.3);
        margin: 20px 0px;
        text-shadow: 0 0 10px rgba(0,229,255,0.5);
    }

    .stButton button {
        background: linear-gradient(135deg, #4361FF, #7B2FFF);
        color: white;
        border: none;
        border-radius: 8px;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(123, 47, 255, 0.5);
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        transform: translateY(-3px) scale(1.03);
        box-shadow: 0 8px 25px rgba(0, 229, 255, 0.7);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0e27 0%, #14183a 100%);
        border-right: 1px solid #4361FF;
    }

    .stMarkdown, p, label {
        color: #C5C8E8 !important;
    }

    .stAlert {
        background: rgba(15, 20, 45, 0.8) !important;
        border: 1px solid #4361FF !important;
        border-radius: 10px !important;
    }

    .stProgress > div > div {
        background: linear-gradient(90deg, #4361FF, #00E5FF) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">⚔️ HUNTER PUSH-UP SYSTEM ⚔️</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">// Arise. Train. Level Up. //</div>', unsafe_allow_html=True)

# ---------------- LOAD MODEL (cached) ----------------
@st.cache_resource
def load_model():
    return YOLO('yolov8n-pose.pt')

model = load_model()

# ---------------- KEYPOINT INDICES ----------------
LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST = 5, 7, 9
RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST = 6, 8, 10

# ---------------- ANGLE FUNCTION ----------------
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def get_angle_if_confident(kpts, confs, a_idx, b_idx, c_idx, min_conf=0.4):
    if confs[a_idx] < min_conf or confs[b_idx] < min_conf or confs[c_idx] < min_conf:
        return None
    return calculate_angle(kpts[a_idx], kpts[b_idx], kpts[c_idx])

# ---------------- RANK SYSTEM ----------------
def get_rank(count):
    if count >= 50:
        return "S", "#FFD700"
    elif count >= 30:
        return "A", "#FF3B3B"
    elif count >= 20:
        return "B", "#7B2FFF"
    elif count >= 10:
        return "C", "#4361FF"
    elif count >= 5:
        return "D", "#00E5FF"
    else:
        return "E", "#8A8FB9"

# ---------------- FRAME PROCESSING (elbow-angle based, confirmed & debounced) ----------------
UP_THRESHOLD = 145
DOWN_THRESHOLD = 105
CONFIRM_FRAMES = 1
COOLDOWN = 0.3

def process_frame(frame, counter, stage, last_count_time, up_frames, down_frames):
    results = model(frame, verbose=False)
    annotated_frame = results[0].plot()
    angle = None

    try:
        kpts = results[0].keypoints.xy[0].cpu().numpy()
        confs = results[0].keypoints.conf[0].cpu().numpy()

        left_arm = get_angle_if_confident(kpts, confs, LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST, min_conf=0.4)
        right_arm = get_angle_if_confident(kpts, confs, RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST, min_conf=0.4)
        arm_angles = [a for a in [left_arm, right_arm] if a is not None]

        if arm_angles:
            angle = sum(arm_angles) / len(arm_angles)
            current_time = time.time()

            if angle < DOWN_THRESHOLD:
                down_frames += 1
                up_frames = 0
                if down_frames >= CONFIRM_FRAMES:
                    stage = "down"

            elif angle > UP_THRESHOLD:
                up_frames += 1
                down_frames = 0
                if up_frames >= CONFIRM_FRAMES and stage == "down":
                    if current_time - last_count_time > COOLDOWN:
                        counter += 1
                        last_count_time = current_time
                    stage = "up"
            else:
                pass

            cv2.putText(annotated_frame, f'ANGLE: {int(angle)}', (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 255), 3)
            cv2.putText(annotated_frame, f'STAGE: {stage.upper() if stage else "READY"}', (20, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 229, 0), 3)
        else:
            cv2.putText(annotated_frame, 'ARM NOT DETECTED', (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    except Exception:
        pass

    cv2.putText(annotated_frame, f'REPS: {counter}', (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 100), 3)

    return annotated_frame, counter, stage, angle, last_count_time, up_frames, down_frames


# ---------------- WEBRTC VIDEO PROCESSOR (browser camera, works when deployed online) ----------------
class PushupProcessor(VideoProcessorBase):
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.last_count_time = 0
        self.up_frames = 0
        self.down_frames = 0
        self.angle = None
        self.synced_count = 0
        self.lock = threading.Lock()

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        annotated, counter, stage, angle, last_count_time, up_frames, down_frames = process_frame(
            img, self.counter, self.stage, self.last_count_time, self.up_frames, self.down_frames
        )

        with self.lock:
            self.counter = counter
            self.stage = stage
            self.last_count_time = last_count_time
            self.up_frames = up_frames
            self.down_frames = down_frames
            self.angle = angle

            if self.counter > self.synced_count:
                add_pushups(self.counter - self.synced_count)
                self.synced_count = self.counter

        return av.VideoFrame.from_ndarray(annotated, format="bgr24")


# TURN-over-TCP forced (Streamlit Cloud blocks outbound UDP, so STUN/UDP TURN gets stuck)
RTC_CONFIGURATION = RTCConfiguration(
    {
        "iceServers": [
            {
                "urls": ["turn:openrelay.metered.ca:443?transport=tcp"],
                "username": "openrelayproject",
                "credential": "openrelayproject",
            },
            {
                "urls": ["turns:openrelay.metered.ca:443?transport=tcp"],
                "username": "openrelayproject",
                "credential": "openrelayproject",
            },
        ],
        "iceTransportPolicy": "relay",
    }
)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown('<div class="system-title">⚙️ SYSTEM CONTROL</div>', unsafe_allow_html=True)
mode = st.sidebar.radio("Select Quest Mode:", ["🏠 Daily Quest Dashboard", "📁 Upload Video", "🎥 Live Hunter Mode"])
st.sidebar.markdown("---")
st.sidebar.info("💡 Tip: Side-on ho to sabse accurate. Poora arm frame mein visible ho.")

# ================= MODE 0: DAILY QUEST DASHBOARD =================
if mode == "🏠 Daily Quest Dashboard":
    data = get_today_progress()

    target = data["target"]
    today_count = data["today_count"]
    flame = data["flame"]
    shadows = data["shadows"]
    week_completed = data["week_completed_days"]
    rank_title = get_rank_title(flame)

    progress_pct = min(today_count / target, 1.0) if target > 0 else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f'<div class="system-box"><div class="system-title">🎯 TODAY\'S QUEST</div>'
            f'<div class="stat-value">{today_count} / {target}</div>'
            f'<div style="color:#8A8FB9; margin-top:5px;">Push-ups completed today</div></div>',
            unsafe_allow_html=True
        )
        st.progress(progress_pct)
        if today_count >= target:
            st.success("✅ Quest Complete! Come back tomorrow for the next one.")
        else:
            st.warning(f"⚠️ {target - today_count} push-ups left to complete today's quest!")

    with col2:
        st.markdown(
            f'<div class="system-box"><div class="flame-box">🔥</div>'
            f'<div style="text-align:center;"><div class="system-title" style="text-align:center; border:none;">FLAME STREAK</div>'
            f'<div class="stat-value" style="text-align:center;">{flame} days</div></div></div>',
            unsafe_allow_html=True
        )

    with col3:
        shadow_icons = "👤" * min(shadows, 10) if shadows > 0 else "—"
        st.markdown(
            f'<div class="system-box"><div class="system-title">👥 SHADOW ARMY</div>'
            f'<div class="stat-value">{shadows}</div>'
            f'<div style="margin-top:8px;">{shadow_icons}</div></div>',
            unsafe_allow_html=True
        )

    col4, col5 = st.columns(2)
    with col4:
        st.markdown(
            f'<div class="system-box"><div class="system-title">🎖️ HUNTER RANK</div>'
            f'<span class="rank-badge">{rank_title}</span></div>',
            unsafe_allow_html=True
        )
    with col5:
        st.markdown(
            f'<div class="system-box"><div class="system-title">📅 WEEKLY PROGRESS</div>'
            f'<div class="stat-value">{week_completed} / 7 days</div>'
            f'<div style="color:#8A8FB9; margin-top:5px;">Complete all 7 to level up target by +5</div></div>',
            unsafe_allow_html=True
        )

    st.markdown(f'<div class="quote-box">"{QUOTE}"</div>', unsafe_allow_html=True)
    st.info("👉 Go to **Upload Video** or **Live Hunter Mode** in the sidebar to start doing push-ups. Your reps will automatically count toward today's quest.")

# ================= MODE 1: VIDEO UPLOAD =================
elif mode == "📁 Upload Video":
    st.markdown('<div class="system-box"><div class="system-title">📼 QUEST LOG — VIDEO ANALYSIS</div>Apni push-up video upload karo aur system tumhare reps scan karega.</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Quest Recording", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tfile.write(uploaded_file.read())
        video_path = tfile.name

        st.video(video_path)

        if st.button("⚔️ START QUEST ANALYSIS"):
            cap = cv2.VideoCapture(video_path)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS) or 25
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            out_path = os.path.join(tempfile.gettempdir(), "output_pushup.mp4")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

            counter, stage = 0, None
            last_count_time = 0
            up_frames, down_frames = 0, 0
            last_shown_count = -1
            synced_count = 0

            progress_bar = st.progress(0)
            col1, col2 = st.columns([3, 1])
            frame_placeholder = col1.empty()
            with col2:
                count_placeholder = st.empty()
            levelup_placeholder = st.empty()

            frame_num = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                annotated_frame, counter, stage, angle, last_count_time, up_frames, down_frames = process_frame(
                    frame, counter, stage, last_count_time, up_frames, down_frames
                )
                out.write(annotated_frame)

                if counter > synced_count:
                    add_pushups(counter - synced_count)
                    synced_count = counter

                frame_num += 1
                if total_frames > 0:
                    progress_bar.progress(min(frame_num / total_frames, 1.0))

                if frame_num % 3 == 0:
                    frame_placeholder.image(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
                    count_placeholder.markdown(
                        f'<div class="system-box"><div class="system-title">💪 REPS</div>'
                        f'<div class="stat-value">{counter}</div></div>', unsafe_allow_html=True)

                    if counter != last_shown_count and counter > 0:
                        levelup_placeholder.success(f"⚡ Rep #{counter} counted! Added to today's quest.")
                        last_shown_count = counter

            cap.release()
            out.release()

            st.balloons()
            st.success(f"✅ QUEST COMPLETE — Total Reps: {counter} (added to Daily Quest)")
            st.video(out_path)

            with open(out_path, "rb") as f:
                st.download_button("⬇️ Download Battle Recording", f, file_name="pushup_result.mp4")

# ================= MODE 2: LIVE WEBCAM (browser-based, works online) =================
elif mode == "🎥 Live Hunter Mode":
    st.markdown('<div class="system-box"><div class="system-title">🎥 LIVE HUNTER TRACKING</div>Apne browser ka camera allow karo. Reps automatically Daily Quest mein add hongi. (Connection thoda time le sakta hai — TURN relay use ho raha hai.)</div>', unsafe_allow_html=True)

    ctx = webrtc_streamer(
        key="pushup-detection",
        video_processor_factory=PushupProcessor,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

    stats_placeholder = st.empty()

    if ctx.video_processor:
        while ctx.state.playing:
            with ctx.video_processor.lock:
                counter = ctx.video_processor.counter
                stage = ctx.video_processor.stage
                angle = ctx.video_processor.angle

            data = get_today_progress()
            stats_placeholder.markdown(
                f'<div class="system-box"><div class="system-title">💪 SESSION REPS</div>'
                f'<div class="stat-value">{counter}</div></div>'
                f'<div class="system-box"><div class="system-title">🎯 TODAY\'S QUEST</div>'
                f'<div class="stat-value">{data["today_count"]} / {data["target"]}</div></div>'
                f'<div class="system-box"><div class="system-title">📊 LIVE DEBUG</div>'
                f'<b>Angle:</b> {int(angle) if angle else "N/A"} &nbsp; <b>Stage:</b> {stage}</div>',
                unsafe_allow_html=True
            )
            time.sleep(0.5)
import os
from datetime import datetime

import streamlit as st
from PIL import Image
from ultralytics import YOLO


# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(
    page_title="SteelDefect AI",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background: #f5f8fc;
}

.block-container {
    max-width: 900px;
    padding-top: 25px;
    padding-bottom: 60px;
}

header {
    visibility: hidden;
}

.main-title {
    text-align: center;
    font-size: 34px;
    font-weight: 800;
    color: #102a43;
    margin-bottom: 3px;
}

.main-title span {
    color: #1473e6;
}

.subtitle {
    text-align: center;
    color: #718096;
    font-size: 14px;
    margin-bottom: 25px;
}

.hero {
    background: linear-gradient(135deg, #082443, #17518b);
    border-radius: 22px;
    padding: 30px;
    color: white;
    margin-bottom: 22px;
}

.hero-title {
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero-text {
    font-size: 15px;
    line-height: 1.6;
    color: #e6f0ff;
}

.card {
    background: white;
    border: 1px solid #dce5ef;
    border-radius: 18px;
    padding: 22px;
    margin-top: 15px;
    margin-bottom: 15px;
    box-shadow: 0 5px 18px rgba(20, 45, 80, 0.07);
}

.section-title {
    color: #102a43;
    font-size: 22px;
    font-weight: 800;
    margin-top: 25px;
    margin-bottom: 12px;
}

.small-title {
    color: #102a43;
    font-size: 17px;
    font-weight: 800;
    margin-top: 20px;
    margin-bottom: 10px;
}

.info-text {
    color: #52657a;
    font-size: 14px;
    line-height: 1.6;
}

.stat-card {
    background: white;
    border: 1px solid #dce5ef;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(20, 45, 80, 0.06);
}

.stat-label {
    color: #718096;
    font-size: 13px;
    margin-bottom: 5px;
}

.stat-value {
    color: #102a43;
    font-size: 27px;
    font-weight: 800;
}

.defect-card {
    background: white;
    border: 1px solid #dce5ef;
    border-radius: 15px;
    padding: 17px;
    margin-top: 10px;
    box-shadow: 0 3px 12px rgba(20, 45, 80, 0.05);
}

.defect-name {
    color: #102a43;
    font-size: 16px;
    font-weight: 800;
}

.defect-confidence {
    color: #1473e6;
    font-size: 13px;
    margin-top: 5px;
}

.detail-card {
    background: white;
    border: 1px solid #dce5ef;
    border-radius: 18px;
    padding: 20px;
    margin-top: 14px;
    box-shadow: 0 4px 14px rgba(20, 45, 80, 0.06);
}

.detail-title {
    color: #102a43;
    font-size: 17px;
    font-weight: 800;
    margin-bottom: 15px;
}

.detail-row {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    padding: 8px 0;
    border-bottom: 1px solid #edf2f7;
    font-size: 13px;
}

.detail-label {
    color: #718096;
    font-weight: 600;
}

.detail-value {
    color: #102a43;
    font-weight: 700;
    text-align: right;
}

.success-box {
    background: #e8f7ee;
    border: 1px solid #b9e5c9;
    border-radius: 14px;
    padding: 15px;
    color: #176b3a;
    margin-top: 15px;
}

.warning-box {
    background: #fff8df;
    border: 1px solid #f0df9b;
    border-radius: 14px;
    padding: 15px;
    color: #765d00;
    margin-top: 15px;
}

.empty-box {
    background: #edf6ff;
    border: 1px solid #c9e1f7;
    border-radius: 14px;
    padding: 18px;
    color: #24527a;
    margin-top: 15px;
}

.support-box {
    background: white;
    border: 1px solid #dce5ef;
    border-radius: 18px;
    padding: 20px;
    margin-top: 20px;
}

.footer-space {
    height: 20px;
}

div.stButton > button {
    width: 100%;
    min-height: 46px;
    border-radius: 12px;
    font-weight: 700;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# MODEL
# ============================================================

MODEL_PATH = os.path.join(os.path.dirname(__file__), "best.pt")


@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return YOLO(MODEL_PATH)


model = load_model()


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "history" not in st.session_state:
    st.session_state.history = []


# ============================================================
# TOP HEADER
# ============================================================

st.markdown(
    """
<div class="main-title">
    Steel<span>Defect</span>AI
</div>
<div class="subtitle">
    Smart inspection for better quality
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# NAVIGATION
# ============================================================

nav1, nav2, nav3, nav4 = st.columns(4)

with nav1:
    if st.button("🏠 Home", key="home_btn"):
        st.session_state.page = "Home"
        st.rerun()

with nav2:
    if st.button("📊 Results", key="results_btn"):
        st.session_state.page = "Results"
        st.rerun()

with nav3:
    if st.button("🔎 Defects", key="defects_btn"):
        st.session_state.page = "Defects"
        st.rerun()

with nav4:
    if st.button("⚙️ Settings", key="settings_btn"):
        st.session_state.page = "Settings"
        st.rerun()


# ============================================================
# MODEL ERROR
# ============================================================

if model is None:
    st.error(
        "best.pt was not found. Put best.pt in the same folder as app.py."
    )
    st.stop()


# ============================================================
# DETECTION FUNCTION
# ============================================================

def detect_image(image, confidence):
    result = model.predict(
        source=image,
        conf=confidence,
        imgsz=640,
        verbose=False,
    )[0]

    plotted = result.plot()

    plotted_image = Image.fromarray(plotted[:, :, ::-1])

    detections = []

    for box in result.boxes:
        class_id = int(box.cls[0])
        score = float(box.conf[0])

        x1, y1, x2, y2 = [int(v) for v in box.xyxy[0]]

        name = model.names[class_id]

        detections.append(
            {
                "name": name,
                "confidence": score,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "width": x2 - x1,
                "height": y2 - y1,
            }
        )

    return plotted_image, detections


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "Home":

    st.markdown(
        """
<div class="hero">

<div class="hero-title">
Detect Steel Surface Defects
</div>

<div class="hero-text">
Upload or capture an image to identify steel surface defects
and their locations using advanced YOLO11 AI.
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📷 Scan Image", key="scan_home"):
            st.session_state.page = "Scan"
            st.rerun()

    with col2:
        if st.button("🖼️ Gallery", key="gallery_home"):
            st.session_state.page = "Scan"
            st.rerun()

    st.markdown(
        '<div class="section-title">AI Inspection</div>',
        unsafe_allow_html=True,
    )

    a, b, c = st.columns(3)

    with a:
        st.markdown(
            """
<div class="stat-card">
<div style="font-size:30px;">⚡</div>
<b>Fast Detection</b>
<div class="info-text">Quick AI analysis</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with b:
        st.markdown(
            """
<div class="stat-card">
<div style="font-size:30px;">🎯</div>
<b>Smart Analysis</b>
<div class="info-text">YOLO11 detection</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with c:
        st.markdown(
            """
<div class="stat-card">
<div style="font-size:30px;">📍</div>
<b>Defect Location</b>
<div class="info-text">Bounding box position</div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-title">Supported Defects</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="support-box">

<b>Crazing</b> &nbsp; • &nbsp;
<b>Inclusion</b> &nbsp; • &nbsp;
<b>Patches</b>

<br><br>

<b>Pitted surface</b> &nbsp; • &nbsp;
<b>Rolled-in scale</b> &nbsp; • &nbsp;
<b>Scratches</b>

</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# SCAN PAGE
# ============================================================

elif st.session_state.page == "Scan":

    st.markdown(
        '<div class="section-title">Scan Steel Surface</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="info-text">Take a photo or upload a steel surface image.</div>',
        unsafe_allow_html=True,
    )

    camera_image = st.camera_input(
        "Camera",
        key="camera_input",
    )

    uploaded_image = st.file_uploader(
        "Choose image from gallery",
        type=["jpg", "jpeg", "png"],
        key="upload_input",
    )

    selected_image = camera_image if camera_image else uploaded_image

    if selected_image:

        image = Image.open(selected_image).convert("RGB")

        st.image(
            image,
            caption="Selected steel surface",
            use_container_width=True,
        )

        confidence = st.slider(
            "Confidence Threshold",
            min_value=0.05,
            max_value=0.90,
            value=0.25,
            step=0.05,
        )

        if st.button(
            "🔍 Analyze Image",
            type="primary",
            key="analyze_button",
        ):

            with st.spinner("Analyzing image with YOLO11..."):

                output_image, detections = detect_image(
                    image,
                    confidence,
                )

            result_data = {
                "input": image,
                "output": output_image,
                "detections": detections,
                "time": datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                ),
            }

            st.session_state.last_result = result_data

            st.session_state.history.insert(
                0,
                result_data,
            )

            st.session_state.page = "Results"

            st.rerun()


# ============================================================
# RESULTS PAGE
# ============================================================

elif st.session_state.page == "Results":

    st.markdown(
        '<div class="section-title">Detection Results</div>',
        unsafe_allow_html=True,
    )

    result = st.session_state.last_result

    if result is None:

        st.markdown(
            """
<div class="warning-box">
<b>No detection result found.</b>
<br><br>
Go to Scan, upload an image, and press Analyze Image.
</div>
""",
            unsafe_allow_html=True,
        )

    else:

        detections = result["detections"]

        # -----------------------------
        # DETECTION IMAGE
        # -----------------------------

        st.image(
            result["output"],
            caption="AI Detection Result",
            use_container_width=True,
        )

        # -----------------------------
        # STATS
        # -----------------------------

        total = len(detections)

        if detections:
            highest = max(
                d["confidence"]
                for d in detections
            )
        else:
            highest = 0.0

        stat1, stat2 = st.columns(2)

        with stat1:
            st.markdown(
                f"""
<div class="stat-card">
<div class="stat-label">Total Detections</div>
<div class="stat-value">{total}</div>
</div>
""",
                unsafe_allow_html=True,
            )

        with stat2:
            st.markdown(
                f"""
<div class="stat-card">
<div class="stat-label">Highest Confidence</div>
<div class="stat-value">{highest * 100:.1f}%</div>
</div>
""",
                unsafe_allow_html=True,
            )

        # -----------------------------
        # NO DEFECT
        # -----------------------------

        if not detections:

            st.markdown(
                '<div class="section-title">Detected Defects</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                """
<div class="empty-box">
No defect found above the selected confidence threshold.
</div>
""",
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="section-title">Detailed Analysis</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                """
<div class="empty-box">
No detailed defect information available.
</div>
""",
                unsafe_allow_html=True,
            )

        else:

            # -----------------------------
            # DEFECT SUMMARY
            # -----------------------------

            st.markdown(
                '<div class="section-title">Detected Defects</div>',
                unsafe_allow_html=True,
            )

            grouped = {}

            for detection in detections:

                name = detection["name"]

                if name not in grouped:
                    grouped[name] = []

                grouped[name].append(
                    detection["confidence"]
                )

            sorted_groups = sorted(
                grouped.items(),
                key=lambda item: max(item[1]),
                reverse=True,
            )

            for name, scores in sorted_groups:

                best_score = max(scores)
                count = len(scores)

                st.markdown(
                    f"""
<div class="defect-card">

<div class="defect-name">
{name}
</div>

<div class="defect-confidence">
Confidence: {best_score * 100:.1f}%
&nbsp;&nbsp; • &nbsp;&nbsp;
{count} detection(s)
</div>

</div>
""",
                    unsafe_allow_html=True,
                )

            # -----------------------------
            # DETAILED ANALYSIS
            # -----------------------------

            st.markdown(
                '<div class="section-title">Detailed Analysis</div>',
                unsafe_allow_html=True,
            )

            for index, detection in enumerate(
                sorted(
                    detections,
                    key=lambda x: x["confidence"],
                    reverse=True,
                ),
                start=1,
            ):

                name = detection["name"]
                confidence_value = detection["confidence"]

                x1 = detection["x1"]
                y1 = detection["y1"]
                x2 = detection["x2"]
                y2 = detection["y2"]

                width = detection["width"]
                height = detection["height"]

                st.markdown(
                    f"""
<div class="detail-card">

<div class="detail-title">
🔍 Defect {index}: {name}
</div>

<div class="detail-row">
<span class="detail-label">Confidence</span>
<span class="detail-value">
{confidence_value * 100:.1f}%
</span>
</div>

<div class="detail-row">
<span class="detail-label">Location</span>
<span class="detail-value">
X: {x1}, Y: {y1}
</span>
</div>

<div class="detail-row">
<span class="detail-label">Size</span>
<span class="detail-value">
{width} × {height} pixels
</span>
</div>

<div class="detail-row">
<span class="detail-label">Bounding Box</span>
<span class="detail-value">
[{x1}, {y1}, {x2}, {y2}]
</span>
</div>

</div>
""",
                    unsafe_allow_html=True,
                )

        # -----------------------------
        # BUTTONS
        # -----------------------------

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            if st.button(
                "📷 Scan Another Image",
                key="scan_again",
                type="primary",
            ):
                st.session_state.page = "Scan"
                st.rerun()

        with c2:
            if st.button(
                "🏠 Back Home",
                key="back_home",
            ):
                st.session_state.page = "Home"
                st.rerun()


# ============================================================
# DEFECT INFO PAGE
# ============================================================

elif st.session_state.page == "Defects":

    st.markdown(
        '<div class="section-title">Defect Types</div>',
        unsafe_allow_html=True,
    )

    defect_info = {
        "Crazing": "Fine crack-like lines appearing on the steel surface.",
        "Inclusion": "Foreign material or impurity embedded in the steel.",
        "Patches": "Localized irregular patch-like surface defect.",
        "Pitted surface": "Small pits or cavity-like defects on the surface.",
        "Rolled-in scale": "Scale material pressed into the steel surface during rolling.",
        "Scratches": "Long narrow linear marks or grooves on the surface.",
    }

    for name, description in defect_info.items():

        st.markdown(
            f"""
<div class="defect-card">

<div class="defect-name">
{name}
</div>

<div class="info-text">
{description}
</div>

</div>
""",
            unsafe_allow_html=True,
        )


# ============================================================
# SETTINGS PAGE
# ============================================================

elif st.session_state.page == "Settings":

    st.markdown(
        '<div class="section-title">Settings</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="card">

<b>Detection Model</b>

<div class="info-text">
YOLO11 trained on the NEU-DET steel surface defect dataset.
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="card">

<b>Supported Classes</b>

<div class="info-text">
Crazing • Inclusion • Patches • Pitted surface •
Rolled-in scale • Scratches
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="card">

<b>Application</b>

<div class="info-text">
SteelDefect AI<br>
AI-powered steel surface inspection
</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer-space"></div>
<div style="text-align:center;color:#8a9bad;font-size:12px;">
SteelDefect AI • Smart inspection for better quality
</div>
""",
    unsafe_allow_html=True,
)
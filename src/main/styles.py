# 定义网页界面的全局视觉样式
import streamlit as st

APP_CSS = """
<style>
:root {
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --background: #f5f7fb;
    --card: #ffffff;
    --text: #1f2937;
    --muted: #6b7280;
    --border: #e5e7eb;
    --success: #16a34a;
    --warning: #d97706;
    --danger: #dc2626;
}

.stApp {
    background:
        linear-gradient(rgba(37, 99, 235, 0.028) 1px, transparent 1px),
        linear-gradient(90deg, rgba(37, 99, 235, 0.028) 1px, transparent 1px),
        radial-gradient(circle at 8% 4%, rgba(37, 99, 235, 0.20), transparent 27rem),
        radial-gradient(circle at 94% 12%, rgba(14, 165, 233, 0.18), transparent 30rem),
        radial-gradient(circle at 52% 108%, rgba(99, 102, 241, 0.12), transparent 36rem),
        linear-gradient(145deg, #f2f7ff 0%, #fbfdff 46%, #edf8ff 100%);
    background-size: 44px 44px, 44px 44px, auto, auto, auto, auto;
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.app-header {
    position: relative;
    overflow: hidden;
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;
    color: white;
    border-radius: 22px;
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 52%, #0ea5e9 100%);
    box-shadow: 0 18px 45px rgba(37, 99, 235, 0.22);
}

.app-header::after {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    right: -80px;
    top: -120px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.12);
}

.app-header h1 {
    position: relative;
    margin: 0 0 0.4rem 0;
    color: white;
    font-size: 2.2rem;
    letter-spacing: -0.03em;
}

.app-header p {
    position: relative;
    margin: 0;
    color: rgba(255, 255, 255, 0.88);
    font-size: 1rem;
}

.eyebrow {
    position: relative;
    margin-bottom: 0.55rem;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.75);
}

.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-top: 1rem;
}

.format-chip {
    padding: 0.28rem 0.62rem;
    border: 1px solid rgba(255, 255, 255, 0.32);
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.13);
    font-size: 0.76rem;
    font-weight: 650;
}

.light-chips .format-chip {
    color: #1e3a8a;
    border-color: #bfdbfe;
    background: #eff6ff;
}

.panel-title {
    margin-bottom: 0.2rem;
    color: var(--text);
    font-size: 1.12rem;
    font-weight: 750;
}

.panel-subtitle {
    margin-bottom: 1rem;
    color: var(--muted);
    font-size: 0.86rem;
    line-height: 1.55;
}

.step-label {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    margin: 0.4rem 0 0.6rem 0;
    color: var(--primary-dark);
    font-size: 0.82rem;
    font-weight: 750;
}

.empty-state {
    display: flex;
    min-height: 430px;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    text-align: center;
    border: 1px dashed rgba(147, 197, 253, 0.95);
    border-radius: 18px;
    background:
        radial-gradient(circle at 50% 20%, rgba(219, 234, 254, 0.72), transparent 16rem),
        linear-gradient(145deg, rgba(255, 255, 255, 0.94), rgba(239, 246, 255, 0.82));
    box-shadow: 0 18px 42px rgba(59, 130, 246, 0.09);
}

.empty-state .empty-icon {
    margin-bottom: 0.9rem;
    font-size: 3.4rem;
}

.empty-state h3 {
    margin: 0 0 0.4rem 0;
    color: var(--text);
}

.empty-state p {
    max-width: 360px;
    margin: 0;
    color: var(--muted);
    line-height: 1.6;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid rgba(203, 213, 225, 0.82);
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.88);
    box-shadow: 0 12px 34px rgba(30, 64, 175, 0.09);
    backdrop-filter: blur(18px);
}

[data-testid="stFileUploaderDropzone"] {
    padding: 1rem;
    border: 1.5px dashed #93c5fd;
    border-radius: 14px;
    background: #f8fbff;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--primary);
    background: #eff6ff;
}

.stButton > button,
.stDownloadButton > button {
    min-height: 2.8rem;
    border-radius: 11px;
    font-weight: 700;
}

.stButton > button[kind="primary"],
.stDownloadButton > button[kind="primary"] {
    border: none;
    background: linear-gradient(135deg, var(--primary-dark), var(--primary));
    box-shadow: 0 8px 18px rgba(37, 99, 235, 0.22);
}

[data-testid="stMetric"] {
    min-height: 108px;
    padding: 1rem;
    border: 1px solid var(--border);
    border-radius: 14px;
    background: var(--card);
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
}

[data-testid="stMetricLabel"] {
    color: var(--muted);
}

[data-testid="stMetricValue"] {
    color: var(--text);
    font-weight: 780;
}

.result-heading {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.55rem;
    margin-bottom: 0.2rem;
    color: var(--text);
    font-size: 1.02rem;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    padding: 0.22rem 0.55rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 750;
}

.status-success {
    color: #166534;
    background: #dcfce7;
}

.status-warning {
    color: #92400e;
    background: #fef3c7;
}

.status-failed {
    color: #991b1b;
    background: #fee2e2;
}

.output-caption {
    margin-bottom: 0.9rem;
    color: var(--muted);
    font-size: 0.82rem;
}

.tip-card {
    padding: 0.85rem 0.95rem;
    border-left: 4px solid #60a5fa;
    border-radius: 10px;
    background: #eff6ff;
    color: #1e3a8a;
    font-size: 0.84rem;
    line-height: 1.55;
}

@media (max-width: 700px) {
    .app-header {
        padding: 1.5rem;
        border-radius: 17px;
    }

    .app-header h1 {
        font-size: 1.65rem;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}
/* 科技感动效 */
.stApp {
    isolation: isolate;
    overflow-x: hidden;
}

.stApp::before {
    content: "";
    position: fixed;
    inset: -20%;
    z-index: -2;
    pointer-events: none;
    background:
        radial-gradient(circle at 18% 22%, rgba(37, 99, 235, 0.26), transparent 24%),
        radial-gradient(circle at 82% 18%, rgba(14, 165, 233, 0.22), transparent 25%),
        radial-gradient(circle at 52% 88%, rgba(99, 102, 241, 0.18), transparent 30%);
    filter: blur(46px);
    animation: auroraDrift 16s ease-in-out infinite alternate;
}

.stApp::after {
    content: "";
    position: fixed;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    background-image:
        linear-gradient(rgba(37, 99, 235, 0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(37, 99, 235, 0.045) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.72), transparent 78%);
    -webkit-mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.72), transparent 78%);
    animation: gridDrift 24s linear infinite;
}

.app-header {
    background-size: 180% 180%;
    animation: headerFlow 10s ease infinite;
    border: 1px solid rgba(255, 255, 255, 0.22);
}

.app-header::before {
    content: "";
    position: absolute;
    top: -20%;
    left: -40%;
    width: 34%;
    height: 140%;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255, 255, 255, 0.34),
        transparent
    );
    transform: skewX(-18deg);
    animation: headerSheen 6.5s ease-in-out infinite;
}

.app-header::after {
    animation: orbFloat 7s ease-in-out infinite;
}

.app-header h1 {
    text-shadow: 0 4px 18px rgba(15, 23, 42, 0.18);
}

.format-chip {
    transition: transform 180ms ease, box-shadow 180ms ease, background 180ms ease;
}

.format-chip:hover {
    transform: translateY(-2px);
    background: rgba(255, 255, 255, 0.22);
    box-shadow: 0 6px 16px rgba(15, 23, 42, 0.15);
}

.light-chips .format-chip:hover {
    background: #dbeafe;
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.14);
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    transition: transform 220ms ease, box-shadow 220ms ease, border-color 220ms ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-3px);
    border-color: rgba(96, 165, 250, 0.72);
    box-shadow: 0 18px 44px rgba(37, 99, 235, 0.14);
}

[data-testid="stFileUploaderDropzone"] {
    transition: transform 200ms ease, box-shadow 200ms ease, border-color 200ms ease;
}

[data-testid="stFileUploaderDropzone"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(37, 99, 235, 0.13);
}

.stButton > button,
.stDownloadButton > button {
    position: relative;
    overflow: hidden;
    transition: transform 180ms ease, box-shadow 180ms ease, filter 180ms ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-2px);
    filter: brightness(1.03);
}

.stButton > button[kind="primary"]:hover,
.stDownloadButton > button[kind="primary"]:hover {
    box-shadow: 0 12px 25px rgba(37, 99, 235, 0.32);
}

.empty-icon {
    filter: drop-shadow(0 10px 18px rgba(37, 99, 235, 0.16));
    animation: emptyFloat 3.6s ease-in-out infinite;
}

@keyframes auroraDrift {
    0% {
        transform: translate3d(-2%, -1%, 0) scale(1);
    }
    100% {
        transform: translate3d(3%, 2%, 0) scale(1.08);
    }
}

@keyframes gridDrift {
    from {
        background-position: 0 0, 0 0;
    }
    to {
        background-position: 48px 48px, 48px 48px;
    }
}

@keyframes headerFlow {
    0%, 100% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
}

@keyframes headerSheen {
    0%, 65% {
        left: -40%;
    }
    100% {
        left: 130%;
    }
}

@keyframes orbFloat {
    0%, 100% {
        transform: translate3d(0, 0, 0) scale(1);
    }
    50% {
        transform: translate3d(-16px, 18px, 0) scale(1.08);
    }
}

@keyframes emptyFloat {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-8px);
    }
}

@media (prefers-reduced-motion: reduce) {
    .stApp::before,
    .stApp::after,
    .app-header,
    .app-header::before,
    .app-header::after,
    .empty-icon {
        animation: none !important;
    }

    .format-chip,
    div[data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stFileUploaderDropzone"],
    .stButton > button,
    .stDownloadButton > button {
        transition: none !important;
    }
}
/* 强科技感动效 */
.block-container {
    position: relative;
}

.block-container::before {
    content: "";
    position: fixed;
    top: -22%;
    left: 0;
    right: 0;
    height: 190px;
    z-index: 0;
    pointer-events: none;
    background: linear-gradient(
        180deg,
        transparent 0%,
        rgba(56, 189, 248, 0.02) 35%,
        rgba(37, 99, 235, 0.16) 50%,
        rgba(56, 189, 248, 0.02) 65%,
        transparent 100%
    );
    filter: blur(1px);
    animation: pageScan 7s linear infinite;
}

.block-container > * {
    position: relative;
    z-index: 1;
}

.app-header {
    border: 1px solid rgba(255, 255, 255, 0.34);
    box-shadow:
        0 22px 58px rgba(37, 99, 235, 0.28),
        0 0 0 1px rgba(125, 211, 252, 0.16),
        inset 0 1px 0 rgba(255, 255, 255, 0.22);
}

.app-header::before {
    width: 28%;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255, 255, 255, 0.58),
        transparent
    );
    animation-duration: 4.8s;
}

.app-header::after {
    box-shadow:
        0 0 0 1px rgba(255, 255, 255, 0.18),
        0 0 55px rgba(125, 211, 252, 0.38);
    animation: orbPulse 5.5s ease-in-out infinite;
}

.app-header h1 {
    text-shadow:
        0 4px 18px rgba(15, 23, 42, 0.22),
        0 0 28px rgba(191, 219, 254, 0.24);
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    position: relative;
    box-shadow:
        0 12px 34px rgba(30, 64, 175, 0.10),
        0 0 0 1px rgba(147, 197, 253, 0.08);
    animation: panelPulse 5.5s ease-in-out infinite;
}

div[data-testid="stVerticalBlockBorderWrapper"]::after {
    content: "";
    position: absolute;
    top: 0;
    left: 24px;
    right: 24px;
    height: 2px;
    border-radius: 999px;
    pointer-events: none;
    opacity: 0.72;
    background: linear-gradient(
        90deg,
        transparent,
        #60a5fa,
        #22d3ee,
        #818cf8,
        transparent
    );
    background-size: 220% 100%;
    animation: cardBorderFlow 4.2s linear infinite;
}

[data-testid="stFileUploaderDropzone"] {
    box-shadow:
        inset 0 0 28px rgba(37, 99, 235, 0.045),
        0 0 0 rgba(37, 99, 235, 0);
    animation: uploadPulse 3.2s ease-in-out infinite;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #3b82f6;
    box-shadow:
        inset 0 0 34px rgba(37, 99, 235, 0.09),
        0 14px 32px rgba(37, 99, 235, 0.18),
        0 0 28px rgba(59, 130, 246, 0.15);
}

.stButton > button[kind="primary"],
.stDownloadButton > button[kind="primary"] {
    background: linear-gradient(
        110deg,
        #1d4ed8 0%,
        #2563eb 32%,
        #0ea5e9 55%,
        #2563eb 78%,
        #1d4ed8 100%
    );
    background-size: 220% 100%;
    animation: buttonFlow 5.5s ease infinite;
    box-shadow:
        0 10px 24px rgba(37, 99, 235, 0.26),
        inset 0 1px 0 rgba(255, 255, 255, 0.25);
}

.stButton > button[kind="primary"]:hover,
.stDownloadButton > button[kind="primary"]:hover {
    box-shadow:
        0 15px 34px rgba(37, 99, 235, 0.38),
        0 0 28px rgba(14, 165, 233, 0.26),
        inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.empty-state .empty-icon {
    position: relative;
    animation: emptyFloat 3.2s ease-in-out infinite;
}

.empty-state .empty-icon::before,
.empty-state .empty-icon::after {
    content: "";
    position: absolute;
    inset: -18px;
    border: 1px solid rgba(59, 130, 246, 0.34);
    border-radius: 50%;
    pointer-events: none;
    animation: ringPulse 2.8s ease-out infinite;
}

.empty-state .empty-icon::after {
    inset: -30px;
    border-color: rgba(14, 165, 233, 0.18);
    animation-delay: 0.9s;
}

@keyframes pageScan {
    0% {
        transform: translateY(-220px);
        opacity: 0;
    }
    18% {
        opacity: 0.85;
    }
    82% {
        opacity: 0.65;
    }
    100% {
        transform: translateY(115vh);
        opacity: 0;
    }
}

@keyframes panelPulse {
    0%, 100% {
        box-shadow:
            0 12px 34px rgba(30, 64, 175, 0.10),
            0 0 0 1px rgba(147, 197, 253, 0.08);
    }
    50% {
        box-shadow:
            0 17px 42px rgba(37, 99, 235, 0.16),
            0 0 0 1px rgba(96, 165, 250, 0.19);
    }
}

@keyframes cardBorderFlow {
    from {
        background-position: 0% 50%;
    }
    to {
        background-position: 220% 50%;
    }
}

@keyframes uploadPulse {
    0%, 100% {
        border-color: rgba(147, 197, 253, 0.88);
        box-shadow:
            inset 0 0 28px rgba(37, 99, 235, 0.045),
            0 0 0 rgba(37, 99, 235, 0);
    }
    50% {
        border-color: rgba(59, 130, 246, 0.96);
        box-shadow:
            inset 0 0 36px rgba(37, 99, 235, 0.075),
            0 0 22px rgba(59, 130, 246, 0.10);
    }
}

@keyframes buttonFlow {
    0%, 100% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
}

@keyframes orbPulse {
    0%, 100% {
        transform: translate3d(0, 0, 0) scale(1);
        opacity: 0.82;
    }
    50% {
        transform: translate3d(-18px, 20px, 0) scale(1.16);
        opacity: 1;
    }
}

@keyframes ringPulse {
    0% {
        transform: scale(0.72);
        opacity: 0;
    }
    25% {
        opacity: 0.75;
    }
    100% {
        transform: scale(1.25);
        opacity: 0;
    }
}

@media (prefers-reduced-motion: reduce) {
    .block-container::before,
    div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="stVerticalBlockBorderWrapper"]::after,
    [data-testid="stFileUploaderDropzone"],
    .stButton > button[kind="primary"],
    .stDownloadButton > button[kind="primary"],
    .empty-state .empty-icon::before,
    .empty-state .empty-icon::after {
        animation: none !important;
    }
}
</style>
"""


def applyStyles() -> None:
    """把全局 CSS 注入当前 Streamlit 页面。"""
    st.markdown(APP_CSS, unsafe_allow_html=True)
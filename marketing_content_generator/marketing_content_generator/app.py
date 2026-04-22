#!/usr/bin/env python3
"""
Marketing Content Generator
Run: python app.py
Then open: http://localhost:5000
Requires: pip install flask groq python-dotenv
Set: GROQ_API_KEY environment variable
"""

from flask import Flask, request, jsonify, Response, stream_with_context
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Marketing Content Generator</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  --bg:         #0f0f12;
  --bg2:        #16161a;
  --bg3:        #1e1e24;
  --bg4:        #26262e;
  --border:     rgba(255,255,255,0.06);
  --border2:    rgba(255,255,255,0.11);
  --text:       #ececec;
  --text2:      #8a8a9a;
  --text3:      #4a4a5a;
  --accent:     #7c5cbf;
  --accent2:    #9b7de0;
  --accent-bg:  rgba(124,92,191,0.13);
  --green:      #3ecf8e;
  --radius:     13px;
  --sidebar-w:  255px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', sans-serif;
  background: var(--bg);
  color: var(--text);
  height: 100vh;
  display: flex;
  overflow: hidden;
}

/* ── SIDEBAR ── */
#sidebar {
  width: var(--sidebar-w);
  min-width: var(--sidebar-w);
  background: var(--bg2);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  height: 100vh;
  transition: width 0.22s ease, min-width 0.22s ease;
  overflow: hidden;
}
#sidebar.collapsed { width: 54px; min-width: 54px; }

.sidebar-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 13px 13px;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}

.logo {
  display: flex;
  align-items: center;
  gap: 9px;
  font-size: 13.5px;
  font-weight: 700;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  letter-spacing: -0.2px;
}

.logo-icon {
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  flex-shrink: 0;
  box-shadow: 0 0 14px rgba(124,92,191,0.35);
}

.sidebar-toggle {
  width: 26px; height: 26px;
  background: none;
  border: 1px solid var(--border);
  border-radius: 7px;
  color: var(--text3);
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.15s;
  flex-shrink: 0;
}
.sidebar-toggle:hover { border-color: var(--border2); color: var(--text2); }

.new-chat-btn {
  margin: 10px 9px 6px;
  padding: 9px 13px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  border: none;
  border-radius: 10px;
  color: white;
  font-family: 'Inter', sans-serif;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 7px;
  transition: all 0.15s;
  white-space: nowrap;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 4px 14px rgba(124,92,191,0.3);
}
.new-chat-btn:hover { opacity: 0.88; transform: translateY(-1px); }

.sidebar-nav {
  padding: 6px 8px;
  display: flex;
  flex-direction: column;
  gap: 1px;
  flex-shrink: 0;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 8px 9px;
  border-radius: 8px;
  border: none;
  background: none;
  color: var(--text2);
  font-family: 'Inter', sans-serif;
  font-size: 12.5px;
  cursor: pointer;
  transition: all 0.14s;
  white-space: nowrap;
  overflow: hidden;
  width: 100%;
  text-align: left;
  font-weight: 500;
}
.nav-btn:hover { background: var(--bg3); color: var(--text); }
.nav-btn.active { background: var(--accent-bg); color: var(--accent2); }
.nav-btn svg { flex-shrink: 0; }

.sidebar-section-title {
  font-size: 9.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--text3);
  padding: 14px 17px 5px;
  white-space: nowrap;
  flex-shrink: 0;
}

.conv-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 8px 10px;
}
.conv-list::-webkit-scrollbar { width: 3px; }
.conv-list::-webkit-scrollbar-thumb { background: var(--bg4); border-radius: 2px; }

.conv-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 9px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.13s;
  color: var(--text2);
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  font-weight: 500;
}
.conv-item:hover { background: var(--bg3); color: var(--text); }
.conv-item.active { background: var(--bg4); color: var(--text); }
.conv-item-text { overflow: hidden; text-overflow: ellipsis; flex: 1; }

.sidebar-bottom {
  padding: 9px 8px;
  border-top: 1px solid var(--border);
  flex-shrink: 0;
}

.user-row {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 8px 9px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.13s;
}
.user-row:hover { background: var(--bg3); }

.avatar {
  width: 30px; height: 30px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.user-info { overflow: hidden; flex: 1; }
.user-name { font-size: 12.5px; font-weight: 600; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-plan { font-size: 10px; color: var(--text3); margin-top: 1px; }

/* ── MAIN ── */
#main {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  min-width: 0;
}

/* ── TOPBAR ── */
#topbar {
  height: 50px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 18px;
  flex-shrink: 0;
  background: var(--bg);
}

.topbar-left { display: flex; align-items: center; gap: 8px; }

.topbar-model {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 9px;
  padding: 6px 11px;
  font-size: 12px;
  color: var(--text2);
  cursor: pointer;
  transition: all 0.14s;
  position: relative;
  font-weight: 500;
}
.topbar-model:hover { border-color: var(--border2); color: var(--text); }
.model-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--green); flex-shrink: 0; }

.model-dropdown {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  background: var(--bg3);
  border: 1px solid var(--border2);
  border-radius: 11px;
  padding: 5px;
  min-width: 210px;
  z-index: 100;
  display: none;
  box-shadow: 0 14px 36px rgba(0,0,0,0.6);
}
.model-dropdown.open { display: block; animation: fadeIn 0.11s ease; }

.model-opt {
  padding: 9px 11px;
  border-radius: 7px;
  font-size: 12px;
  color: var(--text2);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.11s;
  font-weight: 500;
}
.model-opt:hover { background: var(--bg4); color: var(--text); }
.model-opt.selected { color: var(--accent2); }
.model-opt-badge {
  margin-left: auto;
  font-size: 10px;
  background: var(--accent-bg);
  color: var(--accent2);
  padding: 2px 7px;
  border-radius: 10px;
  font-weight: 600;
}

.topbar-right { display: flex; align-items: center; gap: 5px; }
.icon-btn {
  width: 32px; height: 32px;
  background: none;
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text2);
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.14s;
  font-size: 13px;
}
.icon-btn:hover { border-color: var(--border2); color: var(--text); background: var(--bg3); }

/* ── MESSAGES AREA ── */
#messages-area {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
}
#messages-area::-webkit-scrollbar { width: 4px; }
#messages-area::-webkit-scrollbar-thumb { background: var(--bg4); border-radius: 2px; }

/* ── HOME VIEW ── */
#home-view {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 24px 60px;
}

.home-logo {
  width: 58px; height: 58px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  border-radius: 18px;
  display: flex; align-items: center; justify-content: center;
  font-size: 26px;
  margin-bottom: 22px;
  box-shadow: 0 0 0 0 rgba(124,92,191,0);
  animation: pulseGlow 3s ease-in-out infinite;
}

@keyframes pulseGlow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(124,92,191,0); }
  50% { box-shadow: 0 0 0 10px rgba(124,92,191,0.12); }
}

.home-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 9px;
  text-align: center;
  letter-spacing: -0.6px;
  line-height: 1.2;
}
.home-title .name { 
  background: linear-gradient(135deg, var(--accent2), #c084fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.home-sub {
  font-size: 13.5px;
  color: var(--text2);
  margin-bottom: 34px;
  text-align: center;
  font-weight: 400;
  max-width: 400px;
  line-height: 1.6;
}

/* ── PILLS ── */
.pills {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 30px;
  max-width: 620px;
}
.pill {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 8px 15px;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 20px;
  font-size: 12.5px;
  color: var(--text2);
  cursor: pointer;
  transition: all 0.16s;
  user-select: none;
  font-weight: 500;
}
.pill:hover {
  border-color: rgba(124,92,191,0.4);
  color: var(--text);
  background: var(--bg4);
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(124,92,191,0.12);
}
.pill span { font-size: 14px; }

/* ── QUICK STATS ── */
.stats-row {
  display: flex;
  gap: 12px;
  margin-bottom: 22px;
}
.stat-card {
  flex: 1;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px 16px;
  text-align: center;
  min-width: 100px;
}
.stat-num {
  font-size: 20px;
  font-weight: 700;
  color: var(--accent2);
  margin-bottom: 3px;
  font-variant-numeric: tabular-nums;
}
.stat-label {
  font-size: 11px;
  color: var(--text3);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

/* ── CHAT VIEW ── */
#chat-view {
  display: none;
  padding: 24px 0 10px;
  min-height: 100%;
}

.msg-row { margin-bottom: 18px; }

.msg-wrap {
  max-width: 700px;
  margin: 0 auto;
  padding: 0 22px;
  animation: msgIn 0.18s ease;
}
@keyframes msgIn {
  from { opacity: 0; transform: translateY(5px); }
  to   { opacity: 1; transform: translateY(0); }
}

.msg-user .msg-wrap { display: flex; justify-content: flex-end; }
.msg-assistant .msg-wrap { display: flex; justify-content: flex-start; }

.msg-bubble-user {
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  border-radius: 16px 16px 3px 16px;
  padding: 12px 17px;
  max-width: 72%;
  font-size: 14px;
  line-height: 1.65;
  color: white;
  font-weight: 400;
  box-shadow: 0 4px 14px rgba(124,92,191,0.25);
}

.msg-ai-wrap {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  max-width: 92%;
}

.ai-avatar {
  width: 32px; height: 32px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  display: flex; align-items: center; justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
  margin-top: 1px;
  box-shadow: 0 0 10px rgba(124,92,191,0.3);
}

.msg-bubble-ai {
  font-size: 14px;
  line-height: 1.78;
  color: var(--text);
  padding-top: 3px;
  flex: 1;
}

.msg-bubble-ai p { margin-bottom: 10px; }
.msg-bubble-ai p:last-child { margin-bottom: 0; }
.msg-bubble-ai code {
  font-family: 'JetBrains Mono', monospace;
  background: var(--bg3);
  border: 1px solid var(--border);
  padding: 2px 6px;
  border-radius: 5px;
  font-size: 12.5px;
  color: var(--accent2);
}
.msg-bubble-ai pre {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 11px;
  padding: 14px 16px;
  overflow-x: auto;
  margin: 10px 0;
}
.msg-bubble-ai pre code {
  background: none; border: none; padding: 0;
  font-size: 12.5px; color: var(--text);
}
.msg-bubble-ai strong { color: var(--text); font-weight: 600; }
.msg-bubble-ai h1 { font-size: 18px; font-weight: 700; margin: 16px 0 8px; color: var(--text); }
.msg-bubble-ai h2 { font-size: 16px; font-weight: 700; margin: 14px 0 7px; color: var(--text); }
.msg-bubble-ai h3 { font-size: 14.5px; font-weight: 600; margin: 12px 0 6px; color: var(--text); }
.msg-bubble-ai ul, .msg-bubble-ai ol { padding-left: 20px; margin-bottom: 10px; }
.msg-bubble-ai li { margin-bottom: 4px; }
.msg-bubble-ai blockquote {
  border-left: 3px solid var(--accent);
  padding-left: 14px;
  margin: 10px 0;
  color: var(--text2);
  font-style: italic;
}

.ai-actions {
  display: flex;
  gap: 4px;
  margin-top: 9px;
}
.ai-action-btn {
  background: none;
  border: 1px solid var(--border);
  border-radius: 7px;
  color: var(--text3);
  padding: 5px 10px;
  font-size: 11px;
  cursor: pointer;
  display: flex; align-items: center; gap: 5px;
  transition: all 0.13s;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
}
.ai-action-btn:hover { border-color: var(--border2); color: var(--text2); background: var(--bg3); }

/* Typing cursor */
.typing-cursor {
  display: inline-block;
  width: 2px; height: 15px;
  background: var(--accent2);
  margin-left: 2px;
  vertical-align: middle;
  animation: blink 0.75s ease infinite;
  border-radius: 1px;
}
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

/* Thinking dots */
.thinking {
  display: flex;
  gap: 5px;
  padding: 4px 0;
  align-items: center;
}
.thinking-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--text3);
  animation: thinkBounce 1.2s ease-in-out infinite;
}
.thinking-dot:nth-child(2) { animation-delay: 0.16s; }
.thinking-dot:nth-child(3) { animation-delay: 0.32s; }
@keyframes thinkBounce {
  0%, 80%, 100% { transform: scale(0.65); opacity: 0.35; }
  40% { transform: scale(1); opacity: 1; }
}

/* ── INPUT BAR ── */
#input-bar {
  padding: 10px 18px 14px;
  flex-shrink: 0;
  border-top: 1px solid var(--border);
  background: var(--bg);
}

.input-box {
  max-width: 700px;
  margin: 0 auto;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 15px;
  transition: border-color 0.2s, box-shadow 0.2s;
  overflow: hidden;
}
.input-box:focus-within {
  border-color: rgba(124,92,191,0.45);
  box-shadow: 0 0 0 3px rgba(124,92,191,0.08);
}

.input-textarea-wrap { padding: 13px 15px 0; }

#user-input {
  width: 100%;
  background: none;
  border: none;
  outline: none;
  resize: none;
  color: var(--text);
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  line-height: 1.6;
  min-height: 26px;
  max-height: 180px;
  overflow-y: auto;
}
#user-input::placeholder { color: var(--text3); }
#user-input::-webkit-scrollbar { width: 3px; }

.input-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 11px 10px;
}

.input-left { display: flex; align-items: center; gap: 3px; }
.input-right { display: flex; align-items: center; gap: 6px; }

.input-icon-btn {
  width: 29px; height: 29px;
  background: none;
  border: none;
  border-radius: 7px;
  color: var(--text3);
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px;
  transition: all 0.13s;
}
.input-icon-btn:hover { background: var(--bg3); color: var(--text2); }

.char-count {
  font-size: 11px;
  color: var(--text3);
  font-family: 'JetBrains Mono', monospace;
}

.send-btn {
  width: 34px; height: 34px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  border: none;
  border-radius: 10px;
  color: white;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px;
  transition: all 0.15s;
  flex-shrink: 0;
  box-shadow: 0 3px 10px rgba(124,92,191,0.35);
}
.send-btn:hover { opacity: 0.88; transform: scale(1.05); }
.send-btn:disabled { background: var(--bg4); color: var(--text3); cursor: not-allowed; transform: none; box-shadow: none; }

.input-hint {
  text-align: center;
  font-size: 10.5px;
  color: var(--text3);
  margin-top: 8px;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

/* ── FILE ATTACHMENTS ── */
.attach-preview {
  max-width: 700px;
  margin: 0 auto 7px;
  display: flex;
  gap: 7px;
  flex-wrap: wrap;
}
.attach-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 5px 10px;
  font-size: 11.5px;
  color: var(--text2);
  font-weight: 500;
}
.attach-chip button {
  background: none; border: none;
  color: var(--text3); cursor: pointer;
  font-size: 14px; line-height: 1; padding: 0;
}

/* ── TOAST ── */
.toast {
  position: fixed;
  bottom: 22px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--bg3);
  border: 1px solid var(--border2);
  border-radius: 10px;
  padding: 9px 16px;
  font-size: 12.5px;
  color: var(--text);
  z-index: 999;
  animation: toastIn 0.18s ease;
  pointer-events: none;
  font-weight: 500;
  box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}
@keyframes toastIn {
  from { opacity: 0; transform: translateX(-50%) translateY(7px); }
  to   { opacity: 1; transform: translateX(-50%) translateY(0); }
}

/* ── ANIMATIONS ── */
@keyframes fadeIn { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: translateY(0); } }

/* ── DIVIDER ── */
.date-divider {
  text-align: center;
  font-size: 11px;
  color: var(--text3);
  margin: 16px 0;
  position: relative;
  font-weight: 500;
}
.date-divider::before, .date-divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 38%;
  height: 1px;
  background: var(--border);
}
.date-divider::before { left: 4%; }
.date-divider::after  { right: 4%; }
</style>
</head>
<body>

<!-- SIDEBAR -->
<aside id="sidebar">
  <div class="sidebar-top">
    <div class="logo" id="logo-text">
      <div class="logo-icon">✦</div>
      <span>MCG</span>
    </div>
    <button class="sidebar-toggle" id="toggle-sidebar">
      <svg width="11" height="9" viewBox="0 0 11 9" fill="none"><rect width="11" height="1.4" rx="0.7" fill="currentColor"/><rect y="3.8" width="11" height="1.4" rx="0.7" fill="currentColor"/><rect y="7.6" width="11" height="1.4" rx="0.7" fill="currentColor"/></svg>
    </button>
  </div>

  <button class="new-chat-btn" onclick="newChat()">
    <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M6.5 1v11M1 6.5h11" stroke="white" stroke-width="1.8" stroke-linecap="round"/></svg>
    <span class="label-text">New Session</span>
  </button>

  <div class="sidebar-nav">
    <button class="nav-btn active" onclick="newChat()">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 2h10v8H8L6 12V10H2V2z" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/></svg>
      <span class="label-text">Content</span>
    </button>
    <button class="nav-btn">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><circle cx="6" cy="6" r="4" stroke="currentColor" stroke-width="1.3"/><path d="M10 10l3 3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>
      <span class="label-text">Search</span>
    </button>
    <button class="nav-btn">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><rect x="1.5" y="1.5" width="11" height="11" rx="2" stroke="currentColor" stroke-width="1.3"/><path d="M4.5 7h5M4.5 4.5h5M4.5 9.5h3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
      <span class="label-text">Templates</span>
    </button>
    <button class="nav-btn">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11z" stroke="currentColor" stroke-width="1.3"/><path d="M7 4.5v4l2.5 1.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
      <span class="label-text">History</span>
    </button>
  </div>

  <div class="sidebar-section-title label-text">Recent</div>
  <div class="conv-list" id="conv-list"></div>

  <div class="sidebar-bottom">
    <div class="user-row">
      <div class="avatar">A</div>
      <div class="user-info label-text">
        <div class="user-name">Adarsh</div>
        <div class="user-plan">Pro Plan · <span style="color:var(--accent2)">Active</span></div>
      </div>
    </div>
  </div>
</aside>

<!-- MAIN -->
<main id="main">

  <!-- Topbar -->
  <div id="topbar">
    <div class="topbar-left">
      <div class="topbar-model" id="model-btn" onclick="toggleModelDropdown()">
        <div class="model-dot"></div>
        <span id="model-label">Llama 3.3 70B</span>
        <svg width="9" height="6" viewBox="0 0 9 6" fill="none"><path d="M1 1l3.5 4L8 1" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>
        <div class="model-dropdown" id="model-dropdown">
          <div class="model-opt selected" onclick="selectModel('llama-3.3-70b-versatile','Llama 3.3 70B',this)">
            <div class="model-dot"></div> Llama 3.3 70B <span class="model-opt-badge">Smart</span>
          </div>
          <div class="model-opt" onclick="selectModel('llama-3.1-8b-instant','Llama 3.1 8B',this)">
            <div class="model-dot"></div> Llama 3.1 8B <span class="model-opt-badge">Fast</span>
          </div>
          <div class="model-opt" onclick="selectModel('mixtral-8x7b-32768','Mixtral 8x7B',this)">
            <div class="model-dot"></div> Mixtral 8x7B <span class="model-opt-badge">Creative</span>
          </div>
          <div class="model-opt" onclick="selectModel('gemma2-9b-it','Gemma 2 9B',this)">
            <div class="model-dot"></div> Gemma 2 9B <span class="model-opt-badge">Balanced</span>
          </div>
        </div>
      </div>
    </div>
    <div class="topbar-right">
      <button class="icon-btn" title="Export" onclick="exportChat()">
        <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M6.5 1v8M3.5 6l3 3 3-3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/><path d="M1 10v1.5a.5.5 0 00.5.5h10a.5.5 0 00.5-.5V10" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>
      </button>
      <button class="icon-btn" title="Settings">
        <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><circle cx="6.5" cy="6.5" r="2" stroke="currentColor" stroke-width="1.3"/><path d="M6.5 1v1.2M6.5 10.8V12M12 6.5h-1.2M2.2 6.5H1M10.3 2.7l-.85.85M3.55 9.45l-.85.85M10.3 10.3l-.85-.85M3.55 3.55l-.85-.85" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>
      </button>
    </div>
  </div>

  <!-- Messages / Home -->
  <div id="messages-area">

    <!-- HOME VIEW -->
    <div id="home-view">
      <div class="home-logo">✦</div>
      <h1 class="home-title"><span class="name">Marketing Content</span> Generator</h1>
      <p class="home-sub">Create compelling copy, campaigns, and content powered by AI — faster than ever.</p>

      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-num" id="stat-sessions">0</div>
          <div class="stat-label">Sessions</div>
        </div>
        <div class="stat-card">
          <div class="stat-num" id="stat-messages">0</div>
          <div class="stat-label">Messages</div>
        </div>
        <div class="stat-card">
          <div class="stat-num">∞</div>
          <div class="stat-label">Ideas</div>
        </div>
      </div>

      <div class="pills">
        <div class="pill" onclick="fillPrompt('Write a compelling product description for ')"><span>🛍️</span> Product Copy</div>
        <div class="pill" onclick="fillPrompt('Write an engaging social media post about ')"><span>📱</span> Social Media</div>
        <div class="pill" onclick="fillPrompt('Create an email marketing campaign for ')"><span>📧</span> Email Campaign</div>
        <div class="pill" onclick="fillPrompt('Write a blog post about ')"><span>✍️</span> Blog Post</div>
        <div class="pill" onclick="fillPrompt('Generate 5 catchy ad headlines for ')"><span>🎯</span> Ad Headlines</div>
        <div class="pill" onclick="fillPrompt('Write a brand tagline and brand story for ')"><span>💡</span> Brand Story</div>
      </div>
    </div>

    <!-- CHAT VIEW -->
    <div id="chat-view"></div>
  </div>

  <!-- Input Bar -->
  <div id="input-bar">
    <div class="attach-preview" id="attach-preview"></div>
    <div class="input-box">
      <div class="input-textarea-wrap">
        <textarea id="user-input" rows="1"
          placeholder="Describe the content you want to generate..."
          onkeydown="handleKey(event)"
          oninput="autoResize(this); updateCount()"></textarea>
      </div>
      <div class="input-footer">
        <div class="input-left">
          <button class="input-icon-btn" title="Attach file" onclick="document.getElementById('file-input').click()">
            <svg width="15" height="15" viewBox="0 0 15 15" fill="none"><path d="M3 8.5V5a4 4 0 018 0v7a2.5 2.5 0 01-5 0V6a1 1 0 012 0v5.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>
          </button>
          <button class="input-icon-btn" title="Voice input">
            <svg width="15" height="15" viewBox="0 0 15 15" fill="none"><rect x="5" y="1" width="5" height="8" rx="2.5" stroke="currentColor" stroke-width="1.3"/><path d="M2.5 7.5a5 5 0 0010 0M7.5 12.5v2" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>
          </button>
          <input type="file" id="file-input" style="display:none" onchange="handleFile(this)">
        </div>
        <div class="input-right">
          <span class="char-count" id="char-count"></span>
          <button class="send-btn" id="send-btn" onclick="sendMessage()" title="Send (Enter)">
            <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M11.5 6.5L1 1.5l2.5 5-2.5 5 10.5-5z" fill="white"/></svg>
          </button>
        </div>
      </div>
    </div>
    <div class="input-hint">AI can make mistakes — always review your marketing content before publishing.</div>
  </div>
</main>

<script>
// ── State ──
let conversations = [];
let currentMessages = [];
let currentModel = 'llama-3.3-70b-versatile';
let attachedFiles = [];
let isStreaming = false;
let totalMessages = 0;

// ── Init ──
function init() {
  renderConvList();
  updateStats();
}

function updateStats() {
  document.getElementById('stat-sessions').textContent = conversations.length;
  document.getElementById('stat-messages').textContent = totalMessages;
}

// ── Sidebar ──
document.getElementById('toggle-sidebar').addEventListener('click', () => {
  document.getElementById('sidebar').classList.toggle('collapsed');
});

function renderConvList() {
  const list = document.getElementById('conv-list');
  if (!conversations.length) {
    list.innerHTML = '<div style="padding:8px 10px;font-size:11.5px;color:var(--text3);font-weight:500">No sessions yet</div>';
    return;
  }
  list.innerHTML = conversations.map((c, i) => `
    <div class="conv-item ${i === 0 ? 'active' : ''}" onclick="loadConv(${i})">
      <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2 2h8v6H7L5 10V8H2V2z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/></svg>
      <span class="conv-item-text">${c.title}</span>
    </div>
  `).join('');
}

function loadConv(i) {
  currentMessages = [...conversations[i].messages];
  showChatView();
  renderMessages();
}

// ── Model ──
function toggleModelDropdown() {
  document.getElementById('model-dropdown').classList.toggle('open');
}
document.addEventListener('click', e => {
  if (!e.target.closest('#model-btn'))
    document.getElementById('model-dropdown').classList.remove('open');
});
function selectModel(id, label, el) {
  currentModel = id;
  document.getElementById('model-label').textContent = label;
  document.querySelectorAll('.model-opt').forEach(o => o.classList.remove('selected'));
  el.classList.add('selected');
  event.stopPropagation();
  document.getElementById('model-dropdown').classList.remove('open');
}

// ── Input ──
function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 180) + 'px';
}
function updateCount() {
  const len = document.getElementById('user-input').value.length;
  document.getElementById('char-count').textContent = len > 80 ? len : '';
}
function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
}
function fillPrompt(text) {
  const el = document.getElementById('user-input');
  el.value = text;
  el.focus();
  autoResize(el);
  el.setSelectionRange(el.value.length, el.value.length);
}

// ── File ──
function handleFile(input) {
  const file = input.files[0];
  if (!file) return;
  attachedFiles.push(file);
  renderAttachments();
  input.value = '';
}
function renderAttachments() {
  document.getElementById('attach-preview').innerHTML = attachedFiles.map((f, i) => `
    <div class="attach-chip">📎 ${f.name}<button onclick="removeAttach(${i})">×</button></div>
  `).join('');
}
function removeAttach(i) { attachedFiles.splice(i, 1); renderAttachments(); }

// ── Views ──
function showHomeView() {
  document.getElementById('home-view').style.display = 'flex';
  document.getElementById('chat-view').style.display = 'none';
}
function showChatView() {
  document.getElementById('home-view').style.display = 'none';
  document.getElementById('chat-view').style.display = 'block';
}

// ── New chat ──
function newChat() {
  if (currentMessages.length) {
    const title = currentMessages[0].content.slice(0, 40) + (currentMessages[0].content.length > 40 ? '…' : '');
    conversations.unshift({ title, messages: [...currentMessages] });
    renderConvList();
    updateStats();
  }
  currentMessages = [];
  attachedFiles = [];
  renderAttachments();
  showHomeView();
  document.getElementById('user-input').value = '';
  document.getElementById('user-input').style.height = 'auto';
}

// ── Export ──
function exportChat() {
  if (!currentMessages.length) { showToast('No content to export'); return; }
  const text = currentMessages.map(m => `[${m.role.toUpperCase()}]\n${m.content}`).join('\n\n---\n\n');
  const blob = new Blob([text], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'marketing-content.txt';
  a.click();
  showToast('Content exported!');
}

// ── Render messages ──
function renderMessages() {
  const cv = document.getElementById('chat-view');
  cv.innerHTML = currentMessages.map((m, i) => buildMessageHTML(m, i)).join('');
  scrollBottom();
}

function buildMessageHTML(msg, idx) {
  if (msg.role === 'user') {
    return `<div class="msg-row msg-user">
      <div class="msg-wrap"><div class="msg-bubble-user">${escapeHtml(msg.content)}</div></div>
    </div>`;
  }
  return `<div class="msg-row msg-assistant" id="msg-${idx}">
    <div class="msg-wrap">
      <div class="msg-ai-wrap">
        <div class="ai-avatar">✦</div>
        <div style="flex:1;min-width:0">
          <div class="msg-bubble-ai" id="bubble-content-${idx}">${formatMarkdown(msg.content)}</div>
          <div class="ai-actions">
            <button class="ai-action-btn" onclick="copyMsg(${idx})">
              <svg width="10" height="10" viewBox="0 0 10 10" fill="none"><rect x="3" y="3" width="6" height="6" rx="1.2" stroke="currentColor" stroke-width="1.2"/><path d="M2 7H1.5A.5.5 0 011 6.5V1.5A.5.5 0 011.5 1h5A.5.5 0 017 1.5V2" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
              Copy
            </button>
            <button class="ai-action-btn" onclick="regenMsg(${idx})">
              <svg width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M1.5 5a3.5 3.5 0 106.5-1.8" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/><path d="M6.5 1.5L8 3.2l-1.8 1" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              Regenerate
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>`;
}

function escapeHtml(t) {
  return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\n/g,'<br>');
}

function formatMarkdown(text) {
  if (!text) return '';
  return text
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/```(\w*)\n?([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    .replace(/`([^`\n]+)`/g, '<code>$1</code>')
    .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/^&gt; (.+)$/gm, '<blockquote>$1</blockquote>')
    .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
    .replace(/^[-*] (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>[\s\S]*?<\/li>)/g, '<ul>$1</ul>')
    .replace(/\n\n+/g, '</p><p>')
    .replace(/\n/g, '<br>')
    .replace(/^(?!<[hupbol])(.+)$/gm, (m) => m ? `<p>${m}</p>` : m)
    .replace(/<p><\/p>/g, '');
}

function copyMsg(idx) {
  navigator.clipboard.writeText(currentMessages[idx].content).then(() => showToast('Copied to clipboard ✓'));
}

function regenMsg(idx) {
  if (isStreaming) return;
  // Remove all messages from idx onwards, then resend
  currentMessages = currentMessages.slice(0, idx);
  renderMessages();
  // Re-trigger send with last user message
  const lastUser = [...currentMessages].reverse().find(m => m.role === 'user');
  if (lastUser) sendMessageWith(lastUser.content);
}

function scrollBottom() {
  const ma = document.getElementById('messages-area');
  requestAnimationFrame(() => { ma.scrollTop = ma.scrollHeight; });
}

// ── Send ──
async function sendMessage() {
  const input = document.getElementById('user-input');
  const text = input.value.trim();
  if (!text || isStreaming) return;
  input.value = '';
  input.style.height = 'auto';
  attachedFiles = [];
  renderAttachments();
  await sendMessageWith(text);
}

async function sendMessageWith(text) {
  if (isStreaming) return;

  currentMessages.push({ role: 'user', content: text });
  totalMessages++;
  showChatView();
  renderMessages();

  // Thinking bubble
  const thinkingId = 'think-' + Date.now();
  document.getElementById('chat-view').insertAdjacentHTML('beforeend', `
    <div class="msg-row msg-assistant" id="${thinkingId}">
      <div class="msg-wrap">
        <div class="msg-ai-wrap">
          <div class="ai-avatar">✦</div>
          <div class="msg-bubble-ai">
            <div class="thinking">
              <div class="thinking-dot"></div>
              <div class="thinking-dot"></div>
              <div class="thinking-dot"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `);
  scrollBottom();
  isStreaming = true;
  document.getElementById('send-btn').disabled = true;

  const idx = currentMessages.length;
  currentMessages.push({ role: 'assistant', content: '' });

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: currentMessages.slice(0, idx), model: currentModel }),
    });

    const thinkEl = document.getElementById(thinkingId);
    if (thinkEl) thinkEl.remove();

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(errText);
    }

    // Insert AI bubble
    document.getElementById('chat-view').insertAdjacentHTML('beforeend', `
      <div class="msg-row msg-assistant" id="msg-${idx}">
        <div class="msg-wrap">
          <div class="msg-ai-wrap">
            <div class="ai-avatar">✦</div>
            <div style="flex:1;min-width:0">
              <div class="msg-bubble-ai" id="bubble-content-${idx}"><span class="typing-cursor"></span></div>
            </div>
          </div>
        </div>
      </div>
    `);
    scrollBottom();

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let full = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      for (const line of chunk.split('\n')) {
        const l = line.trim();
        if (!l.startsWith('data: ')) continue;
        const raw = l.slice(6).trim();
        if (raw === '[DONE]') continue;
        try {
          const j = JSON.parse(raw);
          if (j.error) throw new Error(j.error);
          if (j.text) {
            full += j.text;
            currentMessages[idx].content = full;
            const bubble = document.getElementById(`bubble-content-${idx}`);
            if (bubble) {
              bubble.innerHTML = formatMarkdown(full) + '<span class="typing-cursor"></span>';
              scrollBottom();
            }
          }
        } catch (pe) {
          if (pe.message && pe.message !== 'JSON') throw pe;
        }
      }
    }

    totalMessages++;
    updateStats();

    // Final render with actions
    const msgEl = document.getElementById(`msg-${idx}`);
    if (msgEl) msgEl.outerHTML = buildMessageHTML({ role: 'assistant', content: full }, idx);

  } catch (err) {
    const thinkEl = document.getElementById(thinkingId);
    if (thinkEl) thinkEl.remove();
    const errContent = `⚠️ Error: ${err.message}`;
    currentMessages[idx].content = errContent;
    document.getElementById('chat-view').insertAdjacentHTML('beforeend',
      buildMessageHTML({ role: 'assistant', content: errContent }, idx));
  } finally {
    isStreaming = false;
    document.getElementById('send-btn').disabled = false;
    scrollBottom();
  }
}

// ── Toast ──
function showToast(msg) {
  const t = document.createElement('div');
  t.className = 'toast';
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 2200);
}

init();
</script>
</body>
</html>"""


@app.route("/")
def index():
    return HTML


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])
    model = data.get("model", "llama-3.3-70b-versatile")

    # Supported Groq models — fall back to default if unknown sent
    VALID_MODELS = {
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
    }
    if model not in VALID_MODELS:
        model = "llama-3.3-70b-versatile"

    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        return jsonify({"error": "GROQ_API_KEY is not set. Please set it in your environment."}), 500

    # Inject real current date/time so model never guesses
    from datetime import datetime
    import pytz

    now = datetime.now(pytz.timezone("Asia/Kolkata"))  # IST for Bhopal, India
    current_datetime_str = now.strftime("%A, %d %B %Y, %I:%M %p IST")

    # Add a system prompt tailored for marketing
    system_prompt = (
        f"Today's date and time is: {current_datetime_str}. "
        "Always use this as the current date when asked. Never say you don't know the current date. "
        "You are a world-class marketing content specialist and copywriter. "
        "You write compelling, persuasive, and creative marketing content including "
        "ad copy, social media posts, email campaigns, product descriptions, brand stories, "
        "blog posts, and more. Adapt your tone to the brand's needs. "
        "Always be creative, concise, and conversion-focused."
    )

    groq_messages = [{"role": "system", "content": system_prompt}] + messages

    def generate():
        try:
            from groq import Groq
            client = Groq(api_key=api_key)

            stream = client.chat.completions.create(
                model=model,
                messages=groq_messages,
                max_tokens=2048,
                temperature=0.8,
                stream=True,
            )

            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    text = delta.content
                    yield f"data: {json.dumps({'text': text})}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

    return Response(
        stream_with_context(generate()),
        content_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


if __name__ == "__main__":
    print("\n✦  Marketing Content Generator")
    print("─" * 38)

    if not os.environ.get("GROQ_API_KEY"):
        print("⚠  Set your GROQ_API_KEY first:")
        print("   export GROQ_API_KEY=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\n")
    else:
        print("✓  GROQ_API_KEY loaded\n")

    print("▶  Install: pip install flask groq python-dotenv pytz")
    print("▶  Run:     python app.py")
    print("▶  Open:    http://localhost:5000\n")

    app.run(debug=False, port=5000, threaded=True)
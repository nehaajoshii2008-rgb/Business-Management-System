# 🌐 ISBMS Online Cloud Server Deployment Guide

Your ISBMS application is 100% production-ready for online server hosting!

---

## ⚡ Method 1: Instant Public Live URL (Right Now)

We have created an automated launcher script:
📄 [`Launch_Public_Online_Server.bat`](file:///c:/Users/Admin/OneDrive/Documents/ISBMS/Launch_Public_Online_Server.bat)

### How to use:
1. Double-click `Launch_Public_Online_Server.bat`.
2. It generates an instant **live public HTTPS URL** (e.g. `https://isbms-shop.loca.lt`).
3. Anyone anywhere in the world can open this link on their mobile phone or PC!

---

## ☁️ Method 2: Permanent 24/7 Free Cloud Server (Render.com)

Your codebase contains pre-configured production files:
- [render.yaml](file:///c:/Users/Admin/OneDrive/Documents/ISBMS/render.yaml)
- [Procfile](file:///c:/Users/Admin/OneDrive/Documents/ISBMS/Procfile)
- [requirements.txt](file:///c:/Users/Admin/OneDrive/Documents/ISBMS/requirements.txt)

### Steps to publish free online 24/7:
1. **Push your code to GitHub**:
   Upload your ISBMS project folder to your GitHub account repository.

2. **Connect to Render**:
   - Go to **[Render.com](https://render.com/)** and sign up (Free).
   - Click **New +** ➔ Select **Blueprint**.
   - Connect your GitHub repository.

3. **Automatic Deployment**:
   - Render will read [render.yaml](file:///c:/Users/Admin/OneDrive/Documents/ISBMS/render.yaml) and automatically build your database, static assets, and Python WSGI server.
   - Within 2 minutes, Render gives you a **permanent 24/7 free web link** (e.g. `https://isbms-pos.onrender.com`) with a free SSL certificate!

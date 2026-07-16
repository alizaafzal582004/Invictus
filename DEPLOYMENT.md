# 🚀 Vercel Deployment Guide

## Option 1: GitHub + Vercel Dashboard (Easiest)

### Step 1: GitHub pe upload karo

1. [GitHub.com](https://github.com) pe jao aur login karo
2. "New repository" click karo
3. Repository name: `pushup-counter` (ya koi bhi naam)
4. Public/Private select karo
5. "Create repository" click karo

### Step 2: Code upload karo

GitHub pe naya repository banane ke baad ye commands run karo:

```bash
git remote add origin https://github.com/YOUR_USERNAME/pushup-counter.git
git branch -M main
git push -u origin main
```

### Step 3: Vercel se connect karo

1. [vercel.com](https://vercel.com) pe jao
2. GitHub se login karo
3. "New Project" click karo  
4. Apna `pushup-counter` repository select karo
5. "Deploy" button click karo

**Bas! 🎉 Aapka app live hai!**

---

## Option 2: Vercel CLI (Advanced)

### Step 1: Node.js install karo
[nodejs.org](https://nodejs.org) se Node.js download karo

### Step 2: Vercel CLI install karo
```bash
npm i -g vercel
```

### Step 3: Deploy karo
```bash
vercel login
vercel
```

---

## 🔥 Deployment ke baad:

1. **URL milega:** `https://your-project-name.vercel.app`
2. **Camera permission:** HTTPS pe camera automatic kaam karega
3. **Updates:** GitHub pe push karo, Vercel automatic redeploy kar dega

## 📱 Testing:

1. Browser mein URL open karo
2. "START TRAINING" click karo
3. Camera permission allow karo
4. Push-ups start karo!

## ⚠️ Common Issues:

**Problem:** Camera access nahi mil rahi
**Solution:** Sirf HTTPS pe camera kaam karta hai, Vercel automatic HTTPS provide karta hai

**Problem:** Slow processing
**Solution:** Serverless functions limitation hai, local testing ke liye `python api/app.py` run karo

**Problem:** Pose detection accurate nahi hai  
**Solution:** Original Streamlit app (app.py) use karo local testing ke liye - YOLO model better hai

---

**🎯 Ready to deploy? GitHub upload karo aur Vercel se connect karo!**
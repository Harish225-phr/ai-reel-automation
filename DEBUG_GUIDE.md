🔍 **FRONTEND-BACKEND CONNECTION DEBUG GUIDE**

## 🚨 **ISSUE: Frontend hitting server nahi ho raha**

---

## **STEP 1: Check Backend Server Status**

### Terminal mein check karo:

```powershell
# Check if backend is running on port 5000
netstat -ano | findstr :5000

# Output example:
# TCP    127.0.0.1:5000    0.0.0.0:0    LISTENING    1234
# ^^^^^^ Good! Server is running

# Agar nothing, server nahi chal raha!
```

### Health check karo:

```powershell
# Test if server responds
curl -UseBasicParsing http://localhost:5000/health

# Expected output:
# {"status": "ok", "service": "ai-reel-generator"}
```

---

## **STEP 2: Check Frontend Console**

### Browser mein:

1. **F12 दबाoo** (Developer tools)
2. **Console tab** खोलो
3. **Generate button** click करो
4. **Messages देखो:**

```
[Frontend] API Base URL: http://localhost:5000
[Frontend] Sending request to: http://localhost:5000/api/generate-reel
[Frontend] Payload: {prompt: "...", language: "en"}
[Frontend] Response status: 200
[Frontend] Response OK: true
```

**ये messages visible हैं?**
- ✅ YES → Frontend भेज रहा है
- ❌ NO → Generate button काम नहीं कर रहा

---

## **STEP 3: Check Backend Console**

### Backend terminal mein:

```
[API] Received request from frontend!
[API] URL: http://127.0.0.1:5000/api/generate-reel
[API] Method: POST
[API] Request body: {'prompt': '...', 'language': 'en'}
```

**ये messages दिख रहे हैं?**
- ✅ YES → Backend receive कर रहा है ✅
- ❌ NO → Frontend connect नहीं हो पा रहा

---

## **COMMON ISSUES & FIXES:**

### **Issue 1: Backend server running नहीं है**

**Check:**
```powershell
netstat -ano | findstr :5000
# Empty output = Not running
```

**Fix:**
```powershell
cd d:\Python\ai-reel-automation
.venv\Scripts\Activate.ps1
python api_server.py
# Wait for: "Listening on http://localhost:5000"
```

---

### **Issue 2: Port is busy/wrong**

**Check which process using port:**
```powershell
Get-Process | Where-Object {$_.ProcessName -like "*python*"}
```

**Kill it:**
```powershell
taskkill /PID <pid> /F
Start-Sleep 2
python api_server.py
```

---

### **Issue 3: CORS error in browser console**

**Error message:**
```
Access to XMLHttpRequest at 'http://localhost:5000/api/generate-reel' 
from origin 'http://localhost:8080' has been blocked by CORS policy
```

**Fix:**
CORS already enabled in api_server.py, but verify:

```python
from flask_cors import CORS
CORS(app)  # ✅ Should be there
```

If not, add it after `app = Flask(__name__)`

---

### **Issue 4: Frontend API URL is wrong**

**Check .env.local:**
```
cat Frontend\reel-genius\.env.local
```

**Should contain:**
```
VITE_API_URL=http://localhost:5000
```

If wrong, update it!

---

## **COMPLETE DEBUG WORKFLOW:**

### **Terminal 1 - Backend with debugging:**

```powershell
cd d:\Python\ai-reel-automation
.venv\Scripts\Activate.ps1
python api_server.py

# Watch for:
# "Listening on http://localhost:5000"
# [API] Received request... (when you click generate)
```

### **Terminal 2 - Frontend:**

```powershell
cd Frontend\reel-genius
npm run dev

# Watch for:
# "Local: http://localhost:8080/"
```

### **Browser (http://localhost:8080):**

1. **F12** → Console tab
2. Watch for `[Frontend]` messages
3. Type a prompt
4. **Click "Generate Reel"**
5. **Check both:**
   - Browser console for `[Frontend]` logs
   - Backend terminal for `[API]` logs

---

## **EXPECTED FLOW:**

```
Browser Console:
  [Frontend] API Base URL: http://localhost:5000
  [Frontend] Sending request to: http://localhost:5000/api/generate-reel
  [Frontend] Response status: 200

Backend Terminal:
  [API] Received request from frontend!
  [API] Request body: {...}
  [PARSE] Parsing prompt...
  [SCRIPT] Generating script...
  ... (processing continues)
```

---

## **QUICK TESTING:**

### **Test backend directly:**

```powershell
$payload = @{
    prompt = "test prompt"
    language = "en"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:5000/api/generate-reel `
  -Method POST `
  -Body $payload `
  -ContentType "application/json" `
  -UseBasicParsing
```

---

## **IF STILL NOT WORKING:**

1. **Kill everything:**
   ```powershell
   Get-Process | Where-Object {$_.ProcessName -like "*python*" -or $_.ProcessName -like "*node*"} | Stop-Process -Force
   ```

2. **Start fresh:**
   ```powershell
   # Terminal 1
   cd d:\Python\ai-reel-automation
   python api_server.py
   
   # Terminal 2
   cd Frontend\reel-genius
   npm run dev
   ```

3. **Screenshot browser console & backend terminal**
4. Share with debug info

---

## **DEBUG CHECKLIST:**

- [ ] Backend server running? (port 5000)
- [ ] Frontend dev server running? (port 8080)
- [ ] Browser console shows `[Frontend]` logs?
- [ ] Backend terminal shows `[API]` logs?
- [ ] No CORS errors in browser?
- [ ] API URL correct: `http://localhost:5000`?
- [ ] API keys set? (`$env:PIXABAY_API_KEY=...`)

✅ All checked? Should work!

---

**Ab check kar aur batao kya dekha terminal mein! 👀**

# Instagram Auto-Upload Setup Guide

## 🎯 Quick Summary

Your AI Reel Generator अब **directly Instagram पर upload** कर सकता है - automatically! 

```
Generate Reel → Auto Upload to Instagram → Auto Post
```

---

## 📋 Requirements

✅ Instagram Business Account (Convert personal → Business)
✅ Meta App (developer.facebook.com पर बना)
✅ Business Account ID
✅ Long-lived Access Token

---

## 🚀 Step-by-Step Setup

### Step 1: Instagram Business Account बनाएं

1. Instagram खोलो
2. Settings → Account type and tools
3. Select "Switch to professional account"
4. Choose "Creator" or "Business"
5. Complete setup

### Step 2: Meta App बनाएं

1. जाओ: https://developers.facebook.com
2. Click "My Apps" → "Create App"
3. Choose "Business" type
4. Fill details:
   - **App Name**: "AI Reel Auto Uploader"
   - **App Purpose**: "Business"
5. Click "Create App"

### Step 3: Instagram Graph API Add करो

App में:
1. Click "Add Product"
2. Search "Instagram Graph API"
3. Click "Set up"
4. Select your Instagram Business Account

### Step 4: Access Token प्राप्त करो

```
Tools → Graph API Explorer
```

1. App selects करो: "AI Reel Auto Uploader"
2. Select "Instagram Graph API"
3. Click "Get User Access Token"
4. Permissions देने के लिए "instagram_business_content_publish" select करो
5. Token generate करो

**⚠️ यह token short-lived है!** Long-lived version चाहिए:

Long-lived Token के लिए:
```
लाईव >> Permissions >> instagram_manage_messages
```

या API से generate करो:
```
GET https://graph.instagram.com/v19.0/me/accounts
  ?fields=instagram_business_account
  &access_token=SHORT_LIVED_TOKEN
```

फिर:
```
GET https://graph.instagram.com/oauth/access_token
  ?grant_type=fb_exchange_token
  &client_id=YOUR_APP_ID
  &client_secret=YOUR_APP_SECRET
  &fb_exchange_token=SHORT_LIVED_TOKEN
```

### Step 5: Business Account ID खोजो

1. जाओ: https://graph.instagram.com/v19.0/me?fields=id,name
2. अपना short-lived token paste करो
3. Response में `id` field = **Business Account ID**

---

## 📝 Usage Examples

### Frontend से Upload करो

```javascript
// Configure Instagram first
fetch('http://localhost:5000/api/instagram/config', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    "business_account_id": "YOUR_BUSINESS_ACCOUNT_ID",
    "access_token": "YOUR_LONG_LIVED_ACCESS_TOKEN"
  })
})
.then(res => res.json())
.then(data => console.log('Configured!', data))

// Upload reel
fetch('http://localhost:5000/api/instagram/upload', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    "video_id": "reel_20260402_120000",
    "caption": "Amazing spiritual reel! 🕉️✨\n\n#yoga #meditation #spirituality",
    "hashtags": ["#reels", "#shorts", "#trending"]
  })
})
.then(res => res.json())
.then(data => {
  console.log('Posted!', data.url)
  // data.url = Instagram reel link
})
```

### Schedule multiple reels

```javascript
fetch('http://localhost:5000/api/instagram/schedule', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    "uploads": [
      {
        "video_id": "reel_20260402_120000",
        "caption": "Morning motivation 🌅",
        "schedule_at": "2026-04-02T08:00:00",
        "hashtags": ["#motivation", "#morning"]
      },
      {
        "video_id": "reel_20260402_121000",
        "caption": "Evening vibes 🌙",
        "schedule_at": "2026-04-02T18:00:00",
        "hashtags": ["#vibes", "#evening"]
      }
    ]
  })
})
.then(res => res.json())
.then(data => console.log('Scheduled!', data))
```

### Check Account Status

```javascript
fetch('http://localhost:5000/api/instagram/status')
  .then(res => res.json())
  .then(data => {
    if (data.status === 'configured') {
      console.log(`Connected to @${data.username}`)
    }
  })
```

---

## 🛠️ Python Usage

```python
from instagram_uploader import InstagramUploader
from datetime import datetime, timedelta

# Initialize
uploader = InstagramUploader(
    business_account_id="YOUR_ID",
    access_token="YOUR_TOKEN"
)

# Upload immediately
result = uploader.upload_reel(
    video_path="output/reel_20260402_120000.mp4",
    caption="Check out this amazing reel! 🎬✨",
    hashtags=['#reels', '#viral']
)

print(f"Reel posted: {result['url']}")

# Schedule for later
tomorrow_8am = datetime.now() + timedelta(days=1)
tomorrow_8am = tomorrow_8am.replace(hour=8, minute=0, second=0)

result = uploader.upload_reel(
    video_path="output/reel_20260402_121000.mp4",
    caption="Scheduled reel! 🚀",
    schedule_at=tomorrow_8am
)

print(f"Scheduled at: {result['publish_time']}")
```

---

## ⚡ API Endpoints

### POST `/api/instagram/config`
Configure credentials
```json
{
  "business_account_id": "...",
  "access_token": "..."
}
```

### POST `/api/instagram/upload`
Upload reel
```json
{
  "video_id": "reel_...",
  "caption": "...",
  "hashtags": ["#tag1", "#tag2"],
  "schedule_at": "2026-04-02T14:00:00" (optional)
}
```

### POST `/api/instagram/schedule`
Schedule multiple
```json
{
  "uploads": [
    {
      "video_id": "...",
      "caption": "...",
      "schedule_at": "...",
      "hashtags": [...]
    }
  ]
}
```

### GET `/api/instagram/account`
Get account info

### GET `/api/instagram/insights?metric=impressions`
Get insights (metrics: impressions, reach, profile_views)

### GET `/api/instagram/status`
Check if configured

---

## 📱 Flow

```
User generates reel
    ↓
Frontend shows "Share to Instagram" button
    ↓
Click → Enter caption + hashtags
    ↓
Choose: Post now or schedule
    ↓
Call `/api/instagram/upload`
    ↓
✅ Reel appears on Instagram!
    ↓
Link + stats shown to user
```

---

## ⚠️ Important Notes

1. **Token Expiry**: Long-lived tokens expire after ~60 days
   - Re-generate before expiry
   - Or use refresh token mechanism

2. **Rate Limits**: Instagram allows ~200-500 posts per day
   - Don't spam posts too fast
   - Add delays between uploads in scheduler

3. **Content Policy**: Ensure videos follow Instagram Content Policy
   - No copyright music (already handled)
   - No explicit content
   - Proper credits

4. **Business Account**: Required for Graph API
   - Creator account doesn't work with API
   - Personal → Business is free

---

## 🐛 Troubleshooting

### "Invalid credentials" error
- Verify Access Token is valid
- Check Business Account ID
- Regenerate token from Meta App

### "Video upload failed"
- Ensure video is MP4 format
- Check file size < 4GB
- Verify video codec is H.264

### "Permission denied"
- Check token has `instagram_business_content_publish` permission
- Ensure Instagram account is connected to Meta App

### "Scheduled post not showing"
- Verify date/time is in future
- Instagram may have different timezone
- Check scheduled posts in Instagram Settings

---

## 🎉 Success!

Once set up, you can:

✅ Generate reels with one click
✅ Auto-upload to Instagram
✅ Schedule posts in advance
✅ Add captions + hashtags
✅ Track insights & analytics

**That's it!** Your AI reel generator is now **Instagram-ready**! 🚀


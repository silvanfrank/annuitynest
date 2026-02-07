# Deploying Annuity Nest on Coolify

This guide outlines how to deploy the Annuity Nest MVP using Coolify.

## 1. Prepare the Repository

Ensure your repository is pushed to GitHub/GitLab.

**Prerequisites:**
- Coolify instance running
- Domain name pointed to your Coolify server IP

---

## 2. Coolify Configuration

### 2.1. Create New Application
1. **Login** to your Coolify instance.
2. **Create New Resource:** Application → **Public Repository** (or Private if using private repo).
3. **Repository Settings:**
   - **URL:** `https://github.com/silvanfrank/annuitynest` (or your repo URL)
   - **Branch:** `main`
   - **Build Pack:** **Dockerfile**

### 2.2. Build Settings
Navigate to **General** tab:

**Base Directory:**
```
/
```
(Leave empty or set to `/` as the Dockerfile is in the root)

**Dockerfile Location:**
```
/Dockerfile
```

**Port Exposes:**
```
5000
```

**Port Mappings:**
```
5000:5000
```

### 2.3. Environment Variables
Go to **Environment Variables** tab and add:

| Key | Value | Description |
|-----|-------|-------------|
| `SECRET_KEY` | `generate_a_secure_random_key` | Flask session secret key |
| `FLASK_DEBUG` | `False` | Disable debug mode for production |
| `PORT` | `5000` | Port to run the application on |

### 2.4. Domain Configuration
**Domain Settings:**
- **Protocol:** `https`
- **Domain:** `annuity.yourdomain.com` (Replace with your actual domain)
- **Wildcard:** No

**DNS Setup (Required):**
Add an A record in your DNS provider:
```
annuity.yourdomain.com → [Your Coolify Server IP]
```

### 2.5. Deploy
1. Click **Deploy**
2. Watch the build logs. It will pip install dependencies and start Gunicorn.
3. Wait for the container to start.

---

## 3. Verification

### 3.1. Health Check
Once deployed, verify the API is running:

```bash
curl https://annuity.yourdomain.com/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "calculator_loaded": true
}
```

### 3.2. Manual Test
Visit `https://annuity.yourdomain.com` in your browser. You should see the Annuity Nest form. Try generating a quote.

---

## 4. Troubleshooting

### Issue: Calculator not initializing
**Symptom:** `/health` returns `calculator_loaded: false` or 500 errors.
**Cause:** Excel files missing or corrupt.
**Solution:**
- Ensure `excel files/` directory is committed to the repository.
- Check logs: `AnnuityCalculator initialized successfully` should appear on startup.

### Issue: "Dockerfile not found"
**Solution:** Ensure **Base Directory** is `/` and **Dockerfile Location** is `/Dockerfile`.

### Issue: 502 Bad Gateway
**Solution:**
- Verify **Port Exposes** is set to `5000`.
- Check logs to see if Gunicorn started successfully.
- Ensure `init_calculator()` does not crash the app on startup.

---

## 5. Deployment Status Template

```
🚀 Annuity Nest Deployment
━━━━━━━━━━━━━━━━━━━━━━━━
✅ Build: Success
✅ Health Check: Passing
✅ Domain: annuity.yourdomain.com
✅ SSL: Active
━━━━━━━━━━━━━━━━━━━━━━━━
Ready for Production: YES
```

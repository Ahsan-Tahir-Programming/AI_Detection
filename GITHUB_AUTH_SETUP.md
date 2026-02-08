# GitHub Authentication Fix

## Problem ❌

You're getting permission denied because Git was caching credentials from a different GitHub account (SikandarNiaz).

## Solution ✅

### Option 1: Use GitHub Personal Access Token (BEST)

#### Step 1: Create Personal Access Token on GitHub

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name it: "AI Detection Project"
4. Select scopes:
   - ✅ repo (full control)
   - ✅ workflow
5. Generate token
6. **Copy the token** (you'll only see it once!)

#### Step 2: Configure Git to Use Token

```bash
# Set the remote to use token format
git remote set-url origin https://YOUR_GITHUB_USERNAME:YOUR_TOKEN@github.com/Ahsan-Tahir-Programming/AI_Detection.git

# Replace:
# YOUR_GITHUB_USERNAME = Ahsan-Tahir-Programming
# YOUR_TOKEN = the token you just copied
```

**Example:**

```bash
git remote set-url origin https://Ahsan-Tahir-Programming:ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx@github.com/Ahsan-Tahir-Programming/AI_Detection.git
```

#### Step 3: Try Push Again

```bash
git push -u origin master:main
```

---

### Option 2: Use Git Credential Manager

```bash
# Clear old credentials
git credential-manager unconfigure

# Reconfigure
git credential-manager configure

# Try pushing
git push -u origin master:main
```

When prompted, authenticate with your GitHub account in the browser window that opens.

---

### Option 3: SSH Key (Advanced but Most Secure)

#### Step 1: Generate SSH Key

```bash
ssh-keygen -t ed25519 -C "your_github_email@example.com"
# Press Enter for default location
# Enter a passphrase (optional)
```

#### Step 2: Add to GitHub

1. Copy public key: `type $env:USERPROFILE\.ssh\id_ed25519.pub`
2. Go to: https://github.com/settings/keys
3. Click "New SSH key"
4. Paste the key, save

#### Step 3: Update Remote to SSH

```bash
git remote set-url origin git@github.com:Ahsan-Tahir-Programming/AI_Detection.git
```

#### Step 4: Push

```bash
git push -u origin master:main
```

---

## Quick Fix - Copy-Paste These Commands

### Using Personal Access Token (RECOMMENDED):

```powershell
# 1. Go to project
cd "c:\ahsan\ahsan-work\personnel github projects\python\Ai_Detection"

# 2. Update remote with your GitHub token
# REPLACE: YOUR_TOKEN with token from https://github.com/settings/tokens
git remote set-url origin https://Ahsan-Tahir-Programming:YOUR_TOKEN@github.com/Ahsan-Tahir-Programming/AI_Detection.git

# 3. Test connection
git ls-remote origin

# 4. Push to GitHub
git push -u origin master:main

# 5. Push dev branch
git checkout dev
git push -u origin dev
```

---

## How to Get Your Personal Access Token

1. Open: https://github.com/settings/tokens/new
2. Token name: `AI Detection Project`
3. Expiration: `90 days` (or 1 year)
4. Scopes to select:
   - ☑️ repo - Full control of private repositories
   - ☑️ workflow - Update GitHub Action and workflow
5. Click "Generate token"
6. **COPY the token immediately** - You won't see it again!

---

## Your Current Credentials

```
GitHub Account: Huzam229 (huzamkhan99@gmail.com)
Repository: github.com/Ahsan-Tahir-Programming/AI_Detection
Branches: master → main (push), dev
```

---

## Troubleshooting

### Issue: "Permission denied" still

**Solution:**

- Double-check token is valid
- Verify you have access to the repository
- Token might have expired (create new one)

### Issue: "fatal: unable to access"

**Solution:**

- Check internet connection
- Try with SSH instead of HTTPS
- Clear credentials: `git credential-manager unconfigure`

### Issue: "Everything up-to-date"

**Solution:**

- Good! It means nothing new to push
- Check GitHub website to verify your branch appears

---

## After Success

Your GitHub should have:

```
✅ main branch (from local master)
✅ dev branch (from local dev)
✅ All commits visible
✅ Ready for Vercel/Render deployment
```

---

## Next: Setup Automatic Deployment

Once pushed successfully:

### Frontend: Vercel

```bash
goto vercel.com
→ Import Project
→ Select AI_Detection repo
→ Select 'main' branch
→ Auto-deploy enabled!
```

### Backend: Render

```bash
goto render.com
→ New Web Service
→ Select AI_Detection repo
→ Select 'main' branch
→ Auto-deploy enabled!
```

---

**Need help?** Run this and share output:

```bash
git remote -v
git branch -a
git config user.name
git config user.email
```

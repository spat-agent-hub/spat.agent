#!/bin/bash

# --- CONFIGURATION ---
PROJECT_NAME="spat-agent-hub"
GITHUB_BRANCH="main"

echo "🚀 Starting Deployment for $PROJECT_NAME..."

# 1. Validation: Check for .env
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found! Create one before deploying."
    exit 1
fi

# 2. Sync with GitHub
echo "📦 Staging changes for GitHub..."
git add .
read -p "📝 Enter commit message: " commit_msg
git commit -m "$commit_msg"

echo "📤 Pushing to GitHub ($GITHUB_BRANCH)..."
git push origin $GITHUB_BRANCH

# 3. Vercel Deployment
echo "🌐 Triggering Vercel Build..."

# If you haven't linked the project yet, this will link it non-interactively
vercel link --yes

# Deploy to production and pull the latest environment variables
vercel deploy --prod --yes

echo "--------------------------------------------------"
echo "✅ SUCCESS: Your 100k \$SPAT Agent is live!"
echo "🔗 Vercel URL: https://$PROJECT_NAME.vercel.app"
echo "🔗 Dashboard: Run 'streamlit run dashboard.py' locally"
echo "--------------------------------------------------"

# LinkedIn Auto Poster (free: GitHub Actions + Gemini + LinkedIn API)

Posts to your own LinkedIn profile on a schedule (default: Mon/Wed/Fri, 9:00 AM Pakistan time).
A GitHub Action runs `post.py`, which asks Gemini to write a post from `topics.json` and publishes it through LinkedIn's official API.

## Files

| File | Purpose |
|---|---|
| `post.py` | Generates the post and publishes it |
| `topics.json` | Your topic list (edit freely) |
| `.github/workflows/post.yml` | The schedule |

## One-time setup

### 1. Gemini API key (free)
1. Go to https://aistudio.google.com and sign in.
2. Click **Get API key** and create one. Copy it.

### 2. LinkedIn access token
1. Go to https://www.linkedin.com/developers/apps and **Create app**. LinkedIn requires a Company Page to link; create a simple one if you don't have one.
2. In the app, open the **Products** tab and request **Share on LinkedIn** and **Sign In with LinkedIn using OpenID Connect**.
3. Open the **Auth** tab and note your Client ID and Client Secret. Add a redirect URL such as `https://www.linkedin.com/developers/tools/oauth/redirect`.
4. Open https://www.linkedin.com/developers/tools/oauth, choose your app, tick the scopes `openid`, `profile` and `w_member_social`, and generate a token. Copy the **access token**.
5. Tokens expire after about 60 days. Put a reminder in your calendar to generate a new one and update the GitHub secret.

### 3. Put the project on GitHub
1. Create a new **private** repository.
2. Upload everything in this folder, keeping the `.github/workflows/post.yml` path exactly.

### 4. Add secrets
Repository **Settings > Secrets and variables > Actions > New repository secret**:

| Secret name | Value |
|---|---|
| `GEMINI_API_KEY` | your Gemini key |
| `LINKEDIN_ACCESS_TOKEN` | your LinkedIn token |
| `LINKEDIN_PERSON_ID` | optional. Leave it out and the script looks it up itself |

### 5. Make the posts sound like you
Open `post.py` and edit `PERSONA` (your profession, audience, tone). Edit `topics.json` with topics you actually want to post about.

## Test before going live
1. Go to the **Actions** tab, choose **LinkedIn Auto Post**, click **Run workflow**.
2. Leave **dry_run** ticked. The post is generated and printed in the logs but NOT published.
3. Happy with it? Run again with dry_run unticked to publish one real post.
4. After that, the schedule runs by itself.

## Customising
- **Schedule:** edit the `cron` line in `post.yml`. It is in UTC, so 04:00 UTC is 9:00 AM Pakistan time.
- **Different Gemini model:** set the `GEMINI_MODEL` environment variable in `post.yml`.
- **Review before posting:** keep using dry runs for the first few weeks, and read what the model writes before you let it publish unattended.

## Notes
- This uses LinkedIn's official API for posting to your own profile. It does not like, comment or connect; automating those breaks LinkedIn's rules and can get your account restricted.
- GitHub may pause scheduled workflows in repositories with no activity for 60 days. If posts stop, open the Actions tab and re-enable the workflow.
- Free-tier limits and token rules change. Check the current Gemini and LinkedIn terms when you sign up.

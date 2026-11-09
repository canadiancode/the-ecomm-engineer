#!/usr/bin/env python3
"""PreToolUse hook: block any publish call unless the live Pipeline Status for
that Video ID is exactly "Approved".

Gated: Upload-Post MCP posting tools, and any Bash command that touches
upload-post.com. Fails closed: any error, a missing Video ID, or missing
credentials blocks the call (exit 2).

Video ID: a V### found in the tool input, or else the contents of
.claude/state/publish-target (written by /publish). If both exist they must match.

Sheet access (read-only), first one found:
  TEE_SA_KEY_FILE                 path to a Google service-account JSON key
  GOOGLE_APPLICATION_CREDENTIALS  same, if it is a service-account key
The Sheet must be shared (Viewer) with that service account's email.
Only Python 3 stdlib plus the `openssl` CLI (for signing) are needed.
"""
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request

SHEET_ID = "1HVSdkA4jfSirk1lTcrUO5qfzVbmHvXsUbULw7Mudsc4"
PIPELINE_RANGE = "Pipeline!A2:N"  # A = Video ID, N = Status
REQUIRED_STATUS = "Approved"

POSTING_TOOLS = {"upload_video", "upload_photos", "upload_text", "upload_document", "edit_scheduled"}
# Unknown future Upload-Post tools whose name sounds like posting are gated too.
POSTING_WORDS = ("upload", "publish", "post", "schedule")
SAFE_TOOLS = {
    "get_status", "get_job_status", "get_history", "get_media", "list_scheduled", "cancel_scheduled",
    "get_analytics", "get_total_impressions", "get_post_analytics", "get_platform_metrics",
    "get_account_info", "list_users", "get_facebook_pages", "get_linkedin_pages", "get_pinterest_boards",
    "get_google_business_locations", "get_reddit_detailed_posts", "get_post_comments",
    "list_dm_conversations", "get_ffmpeg_job", "get_ffmpeg_consumption", "submit_ffmpeg_job",
    "download_ffmpeg_result", "get_queue_settings", "preview_queue", "create_media_upload",
    "complete_media_upload", "get_media_upload", "delete_media_upload", "generate_jwt", "validate_jwt",
}
VIDEO_ID_RE = re.compile(r"\bV\d{3,4}\b")


def block(reason):
    print(f"BLOCKED by require-approved hook: {reason}", file=sys.stderr)
    sys.exit(2)


def needs_gate(tool_name, tool_input):
    if tool_name == "Bash":
        cmd = str(tool_input.get("command", ""))
        return "upload-post.com" in cmd.lower() or "upload_post_api_key" in cmd.lower()
    if re.search(r"upload.?post", tool_name, re.I):
        short = tool_name.rsplit("__", 1)[-1]
        if short in POSTING_TOOLS:
            return True
        if short in SAFE_TOOLS:
            return False
        return any(w in short.lower() for w in POSTING_WORDS)
    return False


def find_video_id(tool_input):
    ids = set(VIDEO_ID_RE.findall(json.dumps(tool_input)))
    if len(ids) > 1:
        block(f"more than one Video ID in the call ({', '.join(sorted(ids))}). Publish one video at a time.")
    from_input = ids.pop() if ids else None

    project = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    target_file = os.path.join(project, ".claude", "state", "publish-target")
    from_file = None
    if os.path.isfile(target_file):
        with open(target_file) as f:
            m = VIDEO_ID_RE.search(f.read())
            from_file = m.group(0) if m else None

    if from_input and from_file and from_input != from_file:
        block(f"Video ID in the call ({from_input}) doesn't match .claude/state/publish-target ({from_file}).")
    vid = from_input or from_file
    if not vid:
        block("no Video ID found. /publish must write the ID (e.g. V002) to .claude/state/publish-target first.")
    return vid


def b64url(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def access_token():
    key_path = os.environ.get("TEE_SA_KEY_FILE") or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not key_path or not os.path.isfile(key_path):
        block("no Google service-account key found (set TEE_SA_KEY_FILE). Can't verify the Sheet, so publishing stays blocked.")
    with open(key_path) as f:
        key = json.load(f)
    if key.get("type") != "service_account":
        block(f"{key_path} is not a service-account key.")

    now = int(time.time())
    header = b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    claims = b64url(json.dumps({
        "iss": key["client_email"],
        "scope": "https://www.googleapis.com/auth/spreadsheets.readonly",
        "aud": key.get("token_uri", "https://oauth2.googleapis.com/token"),
        "iat": now,
        "exp": now + 600,
    }).encode())
    signing_input = f"{header}.{claims}".encode()

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".pem") as pem:
        pem.write(key["private_key"])
        pem_path = pem.name
    try:
        os.chmod(pem_path, 0o600)
        sig = subprocess.run(
            ["openssl", "dgst", "-sha256", "-sign", pem_path],
            input=signing_input, capture_output=True, check=True, timeout=15,
        ).stdout
    finally:
        os.unlink(pem_path)

    body = urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": f"{header}.{claims}.{b64url(sig)}",
    }).encode()
    req = urllib.request.Request(key.get("token_uri", "https://oauth2.googleapis.com/token"), data=body)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)["access_token"]


def pipeline_status(video_id):
    url = (f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/"
           f"{urllib.parse.quote(PIPELINE_RANGE)}?valueRenderOption=FORMATTED_VALUE")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {access_token()}"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        rows = json.load(resp).get("values", [])
    matches = [r for r in rows if r and r[0].strip() == video_id]
    if not matches:
        block(f"{video_id} isn't in the Pipeline tab.")
    if len(matches) > 1:
        block(f"{video_id} appears {len(matches)} times in the Pipeline tab. Fix the duplicate first.")
    row = matches[0]
    return row[13].strip() if len(row) > 13 else ""


def main():
    try:
        event = json.load(sys.stdin)
    except Exception:
        block("couldn't read the hook input.")
    tool_name = event.get("tool_name", "")
    tool_input = event.get("tool_input") or {}
    if not needs_gate(tool_name, tool_input):
        sys.exit(0)

    video_id = find_video_id(tool_input)
    try:
        status = pipeline_status(video_id)
    except SystemExit:
        raise
    except Exception as e:  # network, auth, parsing: fail closed
        block(f"couldn't read the Pipeline status for {video_id} ({type(e).__name__}: {e}).")

    if status != REQUIRED_STATUS:
        block(f"Pipeline Status for {video_id} is '{status or 'blank'}', not '{REQUIRED_STATUS}'. Only Kevin can approve it in the Sheet.")
    sys.exit(0)


if __name__ == "__main__":
    main()

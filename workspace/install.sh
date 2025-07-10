uv venv 
source .venv/bin/activate 
uv pip sync requirements.txt 
npm install @slack/bolt dotenv 
# node claude_hands2.js
// app.js
const { App } = require('@slack/bolt');
const { spawn } = require('child_process');

// dotenvで環境変数を読み込み
require('dotenv').config();

// Boltアプリを初期化
const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  socketMode: true, // Socket Modeを有効化
  appToken: process.env.SLACK_APP_TOKEN, // App-Level Token
});

// メンションイベントをリッスン
app.event('app_mention', async ({ event }) => {
  console.log('メンションを受信:', event);
  
  try {
    // メンションされたメッセージからプロンプトを取得
    const prompt = event.text;
    const parent_user_id = event.parent_user_id;
    const client_msg_id = event.client_msg_id;
    const thread_ts = event.thread_ts;
    
    // 現在の日時でログファイル名を生成
    const now = new Date();
    const timestamp = now.toISOString().replace(/[:.]/g, '-').slice(0, 19); // YYYY-MM-DDTHH-MM-SS
    const logFileName = `./log/claude_hands_${timestamp}.log`;
    const command = `uv run agent.py "次のメンション内容にslackで返信して、${prompt} メンションされたメッセージの情報[ parent_user_id:${parent_user_id},client_msg_id:${client_msg_id},thread_ts:${thread_ts}]" > ${logFileName}`;
    
    console.log('バックグラウンドで実行:', command);
    
    const child = spawn('sh', ['-c', command], {
      detached: true,  // プロセスを切り離し
      stdio: 'ignore'  // 出力を無視
    });
    
    // プロセスを切り離してバックグラウンド実行
    child.unref();
    
    console.log(`プロセス起動完了。出力は ${logFileName} に保存されます。`);
    
  } catch (error) {
    console.error('処理エラー:', error);
  }
});

// Botを起動
(async () => {
  try {
    await app.start();
    console.log('⚡️ Socket Mode Botが起動しました！');
  } catch (error) {
    console.error('Bot起動エラー:', error);
  }
})();
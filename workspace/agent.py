import anyio
import sys
import traceback
from claude_code_sdk import query, ClaudeCodeOptions, Message
from claude_code_sdk.types import *

async def generate_code(prompt: str):
    messages: list[Message] = []

    try:
        options = ClaudeCodeOptions(
            # max_turns=50,
            allowed_tools=["Read", "Write", "Bash"],
            permission_mode="bypassPermissions"  # すべての権限をバイパス
        )

        count, turns = 1, 1
        async for message in query(
            prompt=prompt,
            options=options
        ):
            print(f'\n\n [c={count}]@[t={turns}]', type(message))
            messages.append(message)
            
            if isinstance(message, SystemMessage): 
                print('--- SystemMessage --- ')     

            if isinstance(message, AssistantMessage): 
                print('--- AssistantMessage --- ')     

            if isinstance(message, ResultMessage): 
                print('--- ResultMessage --- ')     

            if isinstance(message, UserMessage):   
                print('--- UserMessage --- ')     
                turns += 1
                count = 1

            count += 1
            print(message)
            print("---")
            
    except Exception as e:
        print(f"\n❌ エラーが発生しました:")
        print(f"エラータイプ: {type(e).__name__}")
        print(f"エラーメッセージ: {str(e)}")
        print(f"\n📋 詳細なスタックトレース:")
        traceback.print_exc()
        print(f"\n🔧 実行していたプロンプト: {prompt}")
        raise  # エラーを再発生させて終了コードを1にする

def main():
    try:
        if len(sys.argv) < 2:
            print("使用方法: uv run agent.py \"<プロンプト>\"")
            print("例: uv run agent.py \"適当なポエムを書いてslackに投稿して\"")
            sys.exit(1)
        
        # コマンドライン引数からプロンプトを取得
        prompt = " ".join(sys.argv[1:])
        
        print(f"実行するプロンプト: {prompt}")
        anyio.run(generate_code, prompt)
        print("\n✅ 正常に完了しました")
        
    except KeyboardInterrupt:
        print("\n⚠️ ユーザーによって中断されました (Ctrl+C)")
        sys.exit(1)
    except SystemExit:
        # sys.exit()の場合はそのまま終了
        raise
    except Exception as e:
        print(f"\n💥 予期しないエラーで終了しました:")
        print(f"エラータイプ: {type(e).__name__}")
        print(f"エラーメッセージ: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
import autogen
import json
from pathlib import Path
import os

# Groqの設定
config_list_groq = [
    {
        "model": "mixtral-8x7b-32768",
        "api_key": os.getenv("GROQ_API_KEY"),
        "base_url": "https://api.groq.com/",  # Groq APIのベースURL
        "api_type": "openai",  # OpenAI互換のAPIを使用
    }
]

config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json"
)

llm_config = {
   "config_list": config_list
}

print(f"llm_config: {llm_config}")

# 以下は変更なし
# user_proxy = autogen.UserProxyAgent(
#     name="User_proxy",
#     system_message="A human admin.",
#     code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
#     human_input_mode="TERMINATE",
# )

agent_a = autogen.AssistantAgent(
   name="programmer", 
   system_message="私はプログラミングのスペシャリストです。",
#    llm_config=config_list_groq[0],
   llm_config=llm_config
)
agent_b = autogen.AssistantAgent(
   name="system_manager",
   system_message="私はシステム設計のスペシャリストです。", 
#    llm_config=config_list_groq[0],
   llm_config=llm_config
)
agent_c = autogen.AssistantAgent(
   name="concerner",
   system_message="私は、懸念事項を指摘する提案者です。",
#    llm_config=config_list_groq[0],
   llm_config=llm_config
)

groupchat = autogen.GroupChat(
   agents=[agent_a, agent_b, agent_c], messages=[], max_round=10
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)  # llm_configを使用

# your_prompt = "NVIDIAの株価の５年間（~2024/04）の推移をプロットし、画像として保存しましょう。"
your_prompt = "自分自身の自己紹介をしてください。またあなたのLLMのモデル名を教えてください。"

manager.initiate_chat(
    manager, 
    message=your_prompt
)

all_messages = manager.chat_messages[agent_a]

current_file_path = Path(__file__).resolve()
parent_directory = current_file_path.parent
save_file = parent_directory / "conversation.json"
with open(save_file, "w") as f:
   json.dump(all_messages, f, indent=2, ensure_ascii=False)
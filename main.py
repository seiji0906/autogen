
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")
assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding", "use_docker": False}) # IMPORTANT: set to True to run code in docker, recommended
# user_proxy.initiate_chat(assistant, message="autogenでllm_configに登録するLLMに、OpenAIのGPT4だけではなく、Claude3opus、AzureOpenAIのGPT4を登録する方法を調査する。実際に実行する必要はありません。")

your_prompt = ""
user_proxy.initiate_chat(assistant, message=your_prompt)

# 以下にUserProxyなしでエージェントがグループチャットを行うプログラムを記述
# https://microsoft.github.io/autogen/docs/topics/groupchat/customized_speaker_selection
# UserProxyを無効にする設定方法がまだわかっていない
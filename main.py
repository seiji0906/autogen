# # https://microsoft.github.io/autogen/docs/topics/groupchat/customized_speaker_selection


import autogen
import json
from pathlib import Path


# OAI_CONFIG_LIST
config_list_gpt = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json"
)

llm_config = {
   "config_list": config_list_gpt,
   "seed": 10,  # キャッシュの作成に使用
   "temperature": 0.7,
}

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
    human_input_mode="TERMINATE",
)

agent_a = autogen.AssistantAgent(
#    name="ceo",
   name="programmer",
#    system_message="私はDTSのCEOです。CEOは企業の全体的な戦略を決定し、その実行を監督します。主に、会社の方向性や政策の設定、重要な経営判断、リソースの配分など、企業の成長と成功に直接関連する多岐にわたる責任を担います。また、他の経営陣や取締役会と連携し、企業のビジョンと目標を定め、その達成に向けてチームを導く役割も果たします。",
   system_message="私はプログラミングのスペシャリストです。",
   llm_config=llm_config,
)
agent_b = autogen.AssistantAgent(
#    name="cto",
   name="system_manager",
#    system_message="私はDTSのCTOです。CTOは新しい技術の研究、開発、導入を監督し、企業の技術的なニーズと目標を満たすためのプロジェクトやチームを管理します。",
   system_message="私はシステム設計のスペシャリストです。",
   llm_config=llm_config,
)
agent_c = autogen.AssistantAgent(
#    name="cmo",
   name="concerner",
#    system_message="私はDTSのCMOです。CMOは、他の経営層と密接に連携し、企業の総合的なビジネス戦略にマーケティングの観点を融合させることが求められます。デジタルマーケティング、SNSの活用、データ駆動型マーケティングなど、最新のマーケティング技術や戦略に精通している必要があります。",
   system_message="私は、懸念事項を指摘する提案者です。",
   llm_config=llm_config,
)
# agent_d = autogen.AssistantAgent(
#    name="employee",
#    system_message="私はDTSの社員です。CTO、CMO、CEOの指示に忠実に従います。",
#    llm_config=llm_config,
# )

# max_roundで会話回数を制限しています
groupchat = autogen.GroupChat(
   agents=[user_proxy, agent_a, agent_b, agent_c], messages=[], max_round=10
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

your_prompt = "NVIDIAの株価の５年間（~2024/04）の推移をプロットし、画像として保存しましょう。"

manager.initiate_chat(
    manager, 
    # message="株式会社DTSという会社がどのような事業を行っているか調査し、DTSが生成AIという技術に対してどのように向き合い、事業を展開していくべきかを話し合ってください。"
    message=your_prompt
)

# agent指定はどれでも同じで、全ての会話記録が順番通りに入る
all_messages = manager.chat_messages[agent_a]

# 現在のファイルの絶対パスを取得
current_file_path = Path(__file__).resolve()
# 一つ上の階層のフォルダを取得
parent_directory = current_file_path.parent
save_file = parent_directory / "conversation.json"
# all_messagesの内容をjsonファイルに上書き保存
with open(save_file, "w") as f:
   json.dump(all_messages, f, indent=2, ensure_ascii=False)

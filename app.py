import random
import streamlit as st


# プレイヤーのステータス管理
class Player:

    def __init__(self, name):
        self.name = name
        self.position = 0
        self.money = 100000  # 初期資金：10万円
        self.job = "無職"
        self.married = False


# イベント定義
EVENTS = {
    1: ("初任給支給！", 50000, None),
    3: ("ビジネス本を読んで勉強した。", -5000, "会社員"),
    5: ("宝くじが当たった！", 200000, None),
    7: ("素敵な出会いがあった！結婚します。", 0, "結婚"),
    10: ("YouTubeチャンネルを開設した。", -20000, "YouTuber"),
    12: ("家賃の更新月だった。", -60000, None),
    15: ("給料日！ボーナスも入った。", 150000, None),
    18: ("財布を落としてしまった…", -10000, None),
    22: ("株への投資が大成功！", 300000, None),
    25: ("高級レストランで贅沢な食事をした。", -30000, None),
    28: ("怪我をして入院してしまった。", -50000, None),
}

# 画面のタイトル
st.title("🎲 Web版・人生すごろくゲーム")

# ゲーム状態の初期化（ブラウザのリロード対策）
if "player" not in st.session_state:
    st.session_state.player = None
if "logs" not in st.session_state:
    st.session_state.logs = []
if "turn" not in st.session_state:
    st.session_state.turn = 1

GOAL = 30

# --- 1. プレイヤー登録画面 ---
if st.session_state.player is None:
    name_input = st.text_input("プレイヤーの名前を入力してください:", "プレイヤー1")
    if st.button("ゲームを始める🚀"):
        st.session_state.player = Player(name_input)
        st.session_state.logs.append(
            f"ゲームスタート！ゴールは {GOAL} マス先です。"
        )
        st.rerun()

# --- 2. ゲーム本編画面 ---
else:
    p = st.session_state.player

    # ステータス表示
    st.header(f"【{p.name} のステータス】")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("位置", f"{p.position} / {GOAL} マス")
    col2.metric("職業", p.job)
    col3.metric("結婚", "既婚" if p.married else "未婚")
    col4.metric("所持金", f"{p.money:,}円")

    st.divider()

    # ゴール判定
    if p.position >= GOAL:
        st.balloons()
        st.success("🏁 ゴールに到達しました！ゲーム終了です！")

        if p.money > 100000:
            st.subheader(
                f"✨ 最終資産 {p.money:,}円！ 大富豪の素晴らしい人生でしたね！"
            )
        else:
            st.subheader(
                f"😢 最終資産 {p.money:,}円… ちょっと苦しい人生でしたが、次は頑張りましょう！"
            )

        if st.button("もう一度遊ぶ 🔄"):
            st.session_state.player = None
            st.session_state.logs = []
            st.session_state.turn = 1
            st.rerun()
    else:
        # ルーレットを回すボタン
        st.subheader(f"ーー ターン {st.session_state.turn} ーー")
        if st.button("🎲 ルーレットを回す"):
            spin = random.randint(1, 6)
            p.position += spin
            st.session_state.turn += 1

            log_text = f"【ターン {st.session_state.turn-1}】🎲 ルーレットの結果: 【 {spin} 】"

            if p.position >= GOAL:
                p.position = GOAL
                log_text += " -> 🎉 ゴールイン！"
            else:
                log_text += f" -> 🏃 {spin} マス進み、{p.position} マス目に着きました。"

                # イベント処理
                if p.position in EVENTS:
                    text, money_change, special = EVENTS[p.position]
                    log_text += f" ｜ イベント: {text}"

                    if money_change != 0:
                        p.money += money_change
                        sign = "＋" if money_change > 0 else "－"
                        log_text += (
                            f" ({sign}{abs(money_change):,}円の変動)"
                        )

                    if special == "結婚" and not p.married:
                        p.married = True
                        log_text += " 💍 ご結婚おめでとうございます！"
                    elif special in ["会社員", "YouTuber"]:
                        p.job = special
                        log_text += f" 💼 転職しました！"
                else:
                    log_text += (
                        " ｜ イベント: 特に何も起きず、平穏な日々を過ごした。"
                    )

            # ログの先頭に追加して新しい順に表示
            st.session_state.logs.insert(0, log_text)
            st.rerun()

    # ゲーム進行ログの表示
    if st.session_state.logs:
        st.subheader("📜 出来事の記録")
        for log in st.session_state.logs:
            st.write(log)

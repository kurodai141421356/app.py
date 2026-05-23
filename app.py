import random
import streamlit as st


class Player:

    def __init__(self, name):
        self.name = name
        self.position = 0
        self.money = 100000  # 初期資金：10万円
        self.job = "無職"
        self.married = False


# 全29マス分のイベントを定義（100%イベントが発生します！）
EVENTS = {
    1: ("初任給支給！生活が安定してきた。", 50000, None),
    2: ("スマホの画面がバキバキに割れた…修理代発生。", -15000, None),
    3: ("ビジネス本を読んで猛勉強！", -5000, "会社員"),
    4: ("コンビニのクジで特賞の高級肉が当たった！", 10000, None),
    5: ("宝くじが当選！一攫千金！", 200000, None),
    6: ("サブスクの解約を忘れていて引き落とされた。", -8000, None),
    7: ("運命の出会い！電撃結婚！", 0, "結婚"),
    8: ("歯が激しく痛み出し、親知らずを抜歯した。", -12000, None),
    9: ("フリマアプリで不用品が高く売れた。", 25000, None),
    10: ("動画編集を学び、一発逆転を狙う！", -20000, "YouTuber"),
    11: ("街頭インタビューを受け、謝礼をもらった。", 5000, None),
    12: ("家賃の更新月。手痛い出費…", -60000, None),
    13: ("実家からお米と仕送り仕送り金が届いた！", 30000, None),
    14: ("友人にお金を貸したが返ってこない予感がする…", -20000, None),
    15: ("給料日！さらにボーナスも支給！", 150000, None),
    16: ("SNSの投稿がプチ炎上。心が傷ついた。", 0, None),
    17: ("なんと仮想通貨が高騰！利確に成功！", 100000, None),
    18: ("道でお財布を落としてしまった…絶望。", -15000, None),
    19: ("お年玉（または臨時ボーナス）をもらった！", 20000, None),
    20: ("怪しいセミナーに勧誘されたが、断って本を買った。", -3000, None),
    21: ("ふるさと納税の返礼品で贅沢グルメを堪能。", -10000, None),
    22: ("株への投資が大成功！大儲け！", 300000, None),
    23: ("深夜のネットショッピングで爆買いしてしまった。", -40000, None),
    24: ("ギックリ腰になり、整体通いが確定した。", -18000, None),
    25: ("高級レストランで贅沢すぎるディナー。", -30000, None),
    26: ("昔買った限定スニーカーが超高値で売れた！", 80000, None),
    27: ("身に覚えのない有料サイトの請求に騙された…", -50000, None),
    28: ("不運にも怪我をしてしまい、緊急入院。", -50000, None),
    29: ("人生最後の勝負！競馬で万馬券を当てた！", 150000, None),
}

st.title("🎲 激動の人生すごろくゲーム")

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

        if p.money > 200000:
            st.subheader(
                f"👑 最終資産 {p.money:,}円！ 大富豪の素晴らしい人生でしたね！"
            )
        elif p.money > 100000:
            st.subheader(
                f"😊 最終資産 {p.money:,}円！ まずまず幸せな人生でした。"
            )
        else:
            st.subheader(
                f"😢 最終資産 {p.money:,}円… 苦しい破産寸前の人生でした。次は頑張りましょう！"
            )

        if st.button("もう一度遊ぶ 🔄"):
            st.session_state.player = None
            st.session_state.logs = []
            st.session_state.turn = 1
            st.rerun()
    else:
        st.subheader(f"ーー ターン {st.session_state.turn} ーー")
        if st.button("🎲 ルーレットを回す"):
            spin = random.randint(1, 6)
            p.position += spin
            st.session_state.turn += 1

            log_text = f"【ターン {st.session_state.turn-1}】🎲 ルーレット: 【 {spin} 】"

            if p.position >= GOAL:
                p.position = GOAL
                log_text += " -> 🎉 ゴールイン！"
            else:
                log_text += f" -> 🏃 {p.position} マス目に進んだ！"

                # 必ずイベントが発生
                if p.position in EVENTS:
                    text, money_change, special = EVENTS[p.position]
                    log_text += f" ｜ 📢 イベント: {text}"

                    # 【追加ルール】職業によるボーナス変動
                    if money_change > 0 and p.job == "YouTuber":
                        money_change = int(money_change * 1.5)
                        log_text += " (★YouTuber特典で収入1.5倍！)"
                    elif money_change > 0 and p.job == "会社員":
                        money_change += 10000
                        log_text += " (★会社員手当で+1万円！)"

                    # 【追加ルール】既婚時のイベント補正
                    if p.married and p.position == 12:
                        money_change -= 30000
                        log_text += " (★家族が増えたため家賃がさらに上乗せ…)"
                    elif p.married and p.position == 25:
                        money_change = int(money_change * 2)
                        log_text += " (★夫婦二人分のディナーで出費2倍！)"

                    # 所持金の変動処理
                    if money_change != 0:
                        p.money += money_change
                        sign = "＋" if money_change > 0 else "－"
                        log_text += (
                            f" 💰 {sign}{abs(money_change):,}円の変動！"
                        )

                    # 特殊イベント処理
                    if special == "結婚":
                        if not p.married:
                            p.married = True
                            log_text += " 💍 ご結婚おめでとうございます！"
                        else:
                            p.money += 50000
                            log_text += " 🎉 既に結婚しているので、結婚記念日の祝金5万円を貰った！"
                    elif special in ["会社員", "YouTuber"]:
                        p.job = special
                        log_text += f" 💼 転職成功！"

            st.session_state.logs.insert(0, log_text)
            st.rerun()

    if st.session_state.logs:
        st.subheader("📜 激動の人生ログ")
        for log in st.session_state.logs:
            st.write(log)

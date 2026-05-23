import random
import streamlit as st


class Player:

    def __init__(self, name):
        self.name = name
        self.position = 0
        self.money = 100000  # 初期資金：10万円
        self.job = "無職"
        self.married = False
        self.is_gameover = False  # ゲームオーバーフラグ


# 全49マス分のイベントを定義（50マス目がゴール）
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
    13: ("実家からお米と仕送り金が届いた！", 30000, None),
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
    # --- ここから30マス以降の追加イベント ---
    30: ("【試練】謎の投資話に乗って大失敗…！", -150000, None),
    31: ("引っ越しを決意。敷金・礼金で大出費。", -120000, None),
    32: ("会社のプロジェクトが大成功！特別報奨金！", 100000, None),
    33: ("自動車の車検代の請求がきた。", -80000, None),
    34: ("親戚の結婚式が重なり、ご祝儀貧乏になる。", -60000, None),
    35: ("【チャンス】起業に挑戦。大出資を受ける！", 250000, "社長"),
    36: ("オフィスのデスクチェアを高級品に買い替えた。", -40000, None),
    37: ("人間ドックで再検査になり、通院費がかさんだ。", -30000, None),
    38: ("趣味のコレクションに熱が入り、爆買い。", -70000, None),
    39: ("空き巣の被害に遭ってしまった…！", -100000, None),
    40: ("国からの給付金が振り込まれた！", 100000, None),
    41: ("エアコンと冷蔵庫が同時に壊れて買い替え。", -150000, None),
    42: ("税金の督促状が届き、一括で納付した。", -120000, None),
    43: ("偶然買った古い絵画にプレミア価値がついた！", 200000, None),
    44: ("詐欺メールのURLをうっかりクリックして被害に…", -180000, None),
    45: ("遺産を相続することになった！", 300000, None),
    46: ("高級時計の購入欲に負けてしまった。", -250000, None),
    47: ("海外旅行に行って贅沢三昧の贅沢三昧をした。", -200000, None),
    48: ("【破滅の罠】カジノで全財産を賭けた大勝負に負けた…", -400000, None),
    49: ("ゴールの手前で全力疾走！靴が破れた。", -5000, None),
}

st.title("☠️ サバイバル人生すごろくゲーム")

if "player" not in st.session_state:
    st.session_state.player = None
if "logs" not in st.session_state:
    st.session_state.logs = []
if "turn" not in st.session_state:
    st.session_state.turn = 1

GOAL = 50

# --- 1. プレイヤー登録画面 ---
if st.session_state.player is None:
    name_input = st.text_input("プレイヤーの名前を入力してください:", "プレイヤー1")
    if st.button("ゲームを始める🚀"):
        st.session_state.player = Player(name_input)
        st.session_state.logs.append(
            f"ゲームスタート！ゴールは {GOAL} マス先です。破産に気をつけて！"
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

    # 所持金がマイナスなら赤文字で警告
    if p.money < 0:
        col4.metric("所持金", f"{p.money:,}円", delta="破産状態", delta_color="inverse")
    else:
        col4.metric("所持金", f"{p.money:,}円")

    st.divider()

    # --- A. ゲームオーバー判定 ---
    if p.is_gameover:
        st.error("💀 ゲームオーバー 💀")
        st.subheader(f"【自己破産】{p.name}は借金 {abs(p.money):,}円 を抱えて破産しました…")

        if st.button("もう一度挑戦する 🔄"):
            st.session_state.player = None
            st.session_state.logs = []
            st.session_state.turn = 1
            st.rerun()

    # --- B. ゴール判定 ---
    elif p.position >= GOAL:
        st.balloons()
        st.success("🏁 無事に破産せずゴールに到達しました！ゲームクリア！")

        if p.money > 500000:
            st.subheader(
                f"👑 最終資産 {p.money:,}円！ 伝説の大富豪として歴史に名を残しました！"
            )
        elif p.money > 100000:
            st.subheader(
                f"😊 最終資産 {p.money:,}円！ 堅実で幸せな人生でした。"
            )
        else:
            st.subheader(
                f"😰 最終資産 {p.money:,}円… ギリギリ破産を免れた命がけの人生でした。"
            )

        if st.button("もう一度遊ぶ 🔄"):
            st.session_state.player = None
            st.session_state.logs = []
            st.session_state.turn = 1
            st.rerun()

    # --- C. 通常のターン処理 ---
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

                # イベント処理
                if p.position in EVENTS:
                    text, money_change, special = EVENTS[p.position]
                    log_text += f" ｜ 📢 イベント: {text}"

                    # 職業によるボーナス変動
                    if money_change > 0 and p.job == "YouTuber":
                        money_change = int(money_change * 1.5)
                        log_text += " (★YouTuber特典で収入1.5倍！)"
                    elif money_change > 0 and p.job == "会社員":
                        money_change += 10000
                        log_text += " (★会社員手当で+1万円！)"
                    elif money_change > 0 and p.job == "社長":
                        money_change = int(money_change * 2)
                        log_text += " (★社長の特権！ビジネス収入2倍！)"

                    # 既婚時のイベント補正
                    if p.married and p.position in [12, 31]:
                        money_change -= 30000
                        log_text += " (★家族分の家賃・引っ越し代が上乗せ…)"
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
                    elif special in ["会社員", "YouTuber", "社長"]:
                        p.job = special
                        log_text += f" 💼 転職成功！職業が【{special}】になった！"
                else:
                    log_text += " ｜ 平穏な日々を過ごした。"

            # ターン終了時に所持金チェック（ゲームオーバー判定）
            if p.money < 0:
                p.is_gameover = True
                log_text += " 💀 所持金がマイナスになり、自己破産しました！"

            st.session_state.logs.insert(0, log_text)
            st.rerun()

    if st.session_state.logs:
        st.subheader("📜 激動の人生ログ")
        for log in st.session_state.logs:
            st.write(log)

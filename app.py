import random
import time

class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.money = 100000  # 初期資金：10万円
        self.job = "無職"
        self.married = False

def print_status(player):
    print(f"\n--- 【{player.name}のステータス】 ---")
    print(f"位置: {player.position}マス目 | 職業: {player.job} | 結婚: {'既婚' if player.married else '未婚'}")
    print(f"所持金: {player.money:,}円")
    print("-" * 30)

def get_event(pos, player):
    # マス目に応じた人生イベントの定義
    events = {
        1: ("初任給支給！", 50000, None),
        3: ("ビジネス本を読んで勉強した。", -5,000, "会社員"),
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
    
    if pos in events:
        text, money_change, special = events[pos]
        print(f"【イベント】: {text}")
        
        if money_change != 0:
            if money_change > 0:
                print(f"💰 ＋{money_change:,}円 を獲得しました！")
            else:
                print(f"💸 －{abs(money_change):,}円 を支払いました。")
            player.money += money_change
            
        if special == "結婚" and not player.married:
            player.married = True
            print("💍 ご結婚おめでとうございます！")
        elif special in ["会社員", "YouTuber"]:
            player.job = special
            print(f"💼 転職しました！ 新しい職業：{special}")
    else:
        print("【イベント】: 特に何も起きず、平穏な日々を過ごした。")

def play_game():
    print("====== 🎲 テキスト版・人生すごろくゲーム 🎲 ======")
    name = input("プレイヤーの名前を入力してください: ")
    if not name:
        name = "プレイヤー1"
        
    player = Player(name)
    goal = 30
    turn = 1
    
    print(f"\nゲームスタート！ゴールは {goal} マス先です。")
    
    while player.position < goal:
        print(f"\n====== 【ターン {turn}】 ======")
        print_status(player)
        
        input("👉 【Enter】キーを押してルーレットを回してください...")
        
        # 1〜6のサイコロを振る
        spin = random.randint(1, 6)
        print(f"🎲 ルーレットの結果: 【 {spin} 】")
        
        player.position += spin
        if player.position >= goal:
            player.position = goal
            print(f"\n🎉 ついにゴールに到達しました！")
            break
            
        print(f"🏃 {spin} マス進み、{player.position} マス目に着きました。")
        get_event(player.position, player)
        
        turn += 1
        time.sleep(0.5)
        
    print("\n====== 🏁 ゲーム終了（結果発表） ======")
    print_status(player)
    if player.money > 100000:
        print(f"✨ 最終資産 {player.money:,}円！ 大富豪の素晴らしい人生でしたね！")
    else:
        print(f"😢 最終資産 {player.money:,}円… ちょっと苦しい人生でしたが、次は頑張りましょう！")

if __name__ == '__main__':
    play_game()

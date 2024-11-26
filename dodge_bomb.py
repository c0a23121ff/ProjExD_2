import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650

#押下キーと移動量の対応関係を表す辞書DELTAを定義する
DELTA = {pg.K_UP: (0, -5), pg.K_DOWN: (0, 5),
        pg.K_LEFT: (-5, 0), pg.K_RIGHT: (5, 0),}



os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct : pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRectかばくだんRect
    戻り値:左右の壁にぶつかっているか、上下の壁にぶつかっているかを表すbool値のタプル
    画面内に収まっている場合はTrue、画面外に出ている場合はFalseを返す
    """
    yoko = True
    tate = True
    if rct.left < 0 or WIDTH < rct.right: #横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #縦方向判定
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    #画面をブラックアウトさせる
    bo = pg.Surface((WIDTH, HEIGHT)) #黒いSurfaceを生成
    pg.draw.rect(bo, (0, 0, 0), [0, 0, WIDTH, HEIGHT]) #画面を真っ黒にする
    bo.set_alpha(128) #透明度を指定
    screen.blit(bo, [0, 0]) #画面にブラックアウトを描画
    #Game Overの文字を描画
    font = pg.font.Font(None, 100) #フォントを生成
    text = font.render("Game Over", True, (255, 255, 255)) #テキストを生成
    screen.blit(text, [WIDTH//2-200, HEIGHT//2-50]) #テキストを描画
    #gameoverの文字の両脇に画像を配置
    #画像を描画
    nk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    screen.blit(nk_img, [WIDTH//2-200-50, HEIGHT//2-50])
    screen.blit(nk_img, [WIDTH//2+190, HEIGHT//2-50])

    pg.display.update() #画面を更新
    time.sleep(5) #5秒待つ
    return

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾の画像と速度を初期化する
    戻り値:爆弾の画像リストと速度リスト
    """
    bb_imgs = [] #爆弾の画像リスト
    accs = [a for a in range(1,11)] #速度リスト
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r)) #爆弾用のSurfaceを生成
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r) #赤い丸を描画
        bb_img.set_colorkey((0, 0, 0)) #四隅の黒色を透明化
        bb_imgs.append(bb_img)
    return bb_imgs, accs

#押下キーに対する移動量の合計値タプルをキー，rotozoomしたSurfaceを値とした辞書を準備する
def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    引数:押下キーに対する移動量の合計値タプル
    戻り値:rotozoomしたSurface
    """
    # kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    if sum_mv == (0, 0):
        pass
    if sum_mv == (0, -5):
        kk_img = pg.transform.flip(pg.image.load("fig/3.png"), False, True)
    return kk_img
    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    vx, vy = +5, +5
    bb_imgs, bb_accs = init_bb_imgs()
    
    bb_img = pg.Surface((20, 20)) # 爆弾用のSurfaceを生成
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) # 赤い丸を描画
    bb_rct = bb_img.get_rect() # 爆弾rectを取得
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) # 爆弾の初期位置
    bb_img.set_colorkey((0, 0, 0)) # 四隅の黒色を透明化
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            print("GAME OVER")
            gameover(screen)
            return #ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv = DELTA[pg.K_UP]
        # if key_lst[pg.K_DOWN]:
        #     sum_mv = DELTA[pg.K_DOWN]
        # if key_lst[pg.K_LEFT]:
        #     sum_mv = DELTA[pg.K_LEFT]
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv = DELTA[pg.K_RIGHT]
        kk_rct.move_ip(sum_mv)
        #こうかとんが画面外なら、元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip([-sum_mv[0], -sum_mv[1]])
        screen.blit(kk_img, kk_rct)
        bb_img = bb_imgs[min(tmr//500, 9)]
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_rct.width, bb_rct.height = bb_img.get_size()
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko: #左右の壁にぶつかったら反転
            vx *= -1
        if not tate: #上下の壁にぶつかったら反転
            vy *= -1
        screen.blit(bb_img, bb_rct)
        kk_img = get_kk_img((0,0))
        kk_img = get_kk_img(tuple(sum_mv))
        pg.display.update()
        tmr += 1 #タイマーを1増やす
        clock.tick(50) #フレームレートを指定


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

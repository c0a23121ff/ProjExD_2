import os
import random
import sys
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

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0

    bb_img = pg.Surface((20, 20)) # 爆弾用のSurfaceを生成
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) # 赤い丸を描画
    bb_rct = bb_img.get_rect() # 爆弾rectを取得
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) # 爆弾の初期位置
    bb_img.set_colorkey((0, 0, 0)) # 四隅の黒色を透明化
    vx, vy = +5, +5

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            print("GAME OVER")
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
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko: #左右の壁にぶつかったら反転
            vx *= -1
        if not tate: #上下の壁にぶつかったら反転
            vy *= -1
        screen.blit(bb_img, bb_rct)
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

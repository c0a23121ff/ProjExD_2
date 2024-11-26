import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650

#押下キーと移動量の対応関係を表す辞書DELTAを定義する
DELTA = {pg.K_UP: (0, -5), pg.K_DOWN: (0, 5),
        pg.K_LEFT: (-5, 0), pg.K_RIGHT: (5, 0),}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
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
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

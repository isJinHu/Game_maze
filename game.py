import cfg
import sys
import pygame
from modules.misc import *
from modules.mazes import *
from modules.Sprites import *

'''主函数'''

cfg.FPS = 100


def main(cfg):
    # 初始化
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('Maze')
    font = pygame.font.SysFont('ComicSansMS', 15)
    modes = {'start': 'game_start', 'switch': 'game_switch', 'end': 'game_end'}
    # 开始界面
    choice = Interface(screen, cfg, modes['start'])
    # start or restart
    while True:
        if not choice:
            pygame.quit()
            sys.exit(-1)
        # 设置界面
        arithmetic = setting(screen, cfg)
        # 记录关卡数
        num_levels = 0
        # 记录最少用了多少步通关
        best_scores = 'None'
        # 寻路功能
        path_finding = {"lost your way ?": None, "too lazy ?": None}
        path_n = 0
        # 关卡循环切换
        while True:
            num_levels += 1
            clock = pygame.time.Clock()
            screen = pygame.display.set_mode(cfg.SCREENSIZE)
            # --随机生成关卡地图
            maze_now = RandomMaze(cfg.MAZESIZE, cfg.BLOCKSIZE, cfg.BORDERSIZE)
            # --生成hero
            hero_now = Hero(cfg.HEROPICPATH, cfg.STARTPOINT, cfg.BLOCKSIZE, cfg.BORDERSIZE)
            # --统计步数
            num_steps = 0
            # --关卡内主循环
            while True:
                dt = clock.tick(cfg.FPS)
                screen.fill((255, 255, 255))
                is_move = False
                # ----显示一些信息
                Label_co(screen, font, 'LEVELDONE: %d' % num_levels, (255, 0, 0), (10, 10))
                Label_co(screen, font, 'BESTSCORE: %s' % best_scores, (255, 0, 0), (cfg.SCREENSIZE[0] // 4 + 10, 10))
                Label_co(screen, font, 'USEDSTEPS: %s' % num_steps, (255, 0, 0), (cfg.SCREENSIZE[0] // 2 + 10, 10))
                Label_co(screen, font, 'S: your starting point    D: your destination', (255, 0, 0), (10, 600))
                text_render = font.render(path_finding[path_n], True, (255, 0, 0))
                rect = text_render.get_rect()
                rect.left, rect.top = cfg.SCREENSIZE[0] - cfg.SCREENSIZE[0] // 4 + 10, 10
                pos = screen.blit(text_render, rect)
                # ----↑↓←→控制hero
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(-1)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            is_move = hero_now.move('up', maze_now)
                        elif event.key == pygame.K_DOWN:
                            is_move = hero_now.move('down', maze_now)
                        elif event.key == pygame.K_LEFT:
                            is_move = hero_now.move('left', maze_now)
                        elif event.key == pygame.K_RIGHT:
                            is_move = hero_now.move('right', maze_now)
                num_steps += int(is_move)
                hero_now.draw(screen)
                maze_now.draw(screen)
                # ----判断游戏是否胜利
                if (hero_now.coordinate[0] == cfg.DESTINATION[0]) and (hero_now.coordinate[1] == cfg.DESTINATION[1]):
                    break
                pygame.display.update()
            # --更新最优成绩
            if best_scores == 'None':
                best_scores = num_steps
            else:
                if best_scores > num_steps:
                    best_scores = num_steps
            # --关卡切换
            choice = Interface(screen, cfg, modes['switch'])
            if not choice:
                break
        choice = Interface(screen, cfg, modes['end'])


if __name__ == '__main__':
    main(cfg)

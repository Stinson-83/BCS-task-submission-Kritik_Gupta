import pygame,sys,random
from collections import deque
import matplotlib.pyplot as plt
import pickle
import os
import pandas as pd

class Maze:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.maze = [list(line.strip()) for line in f.readlines()]
        self.height = len(self.maze)
        self.width = len(self.maze[0])

    def draw(self, screen, wall_surface):
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == 'X':
                    screen.blit(wall_surface, (x * 50, y * 50))

    def find_valid_spawn_points(self):
        valid = []
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == ' ': 
                    valid.append((x, y))
        return valid

    def bfs(self, start, end):
        queue = deque([start])
        visited = {start}
        parent = {}

        directions = [(-1,0),(0,-1),(0,1),(1,0)]

        while queue:
            current = queue.popleft()
            if current == end:
                break
            for dx, dy in directions:
                new = (current[0] + dx, current[1] + dy)
                if 0 <= new[0] < self.width and 0 <= new[1] < self.height:
                    if self.maze[new[1]][new[0]] != 'X' and new not in visited:
                        visited.add(new)
                        queue.append(new)
                        parent[new] = current

        path = []
        current = end
        while current != start:
            if current not in parent:
                return [] 
            path.append(current)
            current = parent[current]
        path.append(start)
        path.reverse()
        return path


class Character:
    def __init__(self, color, pos):
        self.surface = pygame.Surface((50, 50))
        self.surface.fill(color)
        self.pos = pos

    def draw(self, screen):
        screen.blit(self.surface, (self.pos[0]*50, self.pos[1]*50))


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((750, 500))
        pygame.display.set_caption("The Goblet of Fire")
        self.clock = pygame.time.Clock()

        self.background = pygame.Surface((750, 500))
        self.background.fill('Grey')

        self.wall = pygame.Surface((50, 50))
        self.wall.fill('darkgreen')

        self.maze = Maze("C:\\Users\\Administrator\\Downloads\\V1.txt")
        self.valid_cells = self.maze.find_valid_spawn_points()
        spawns = random.sample(self.valid_cells, 3)
        self.harry = Character('blue', spawns[0])
        self.death_eater = Character('red', spawns[1])
        self.cup = Character('indigo', spawns[2])
        self.turn="harry"
        self.frame_counter = 0
        self.move_interval = 1

        self.totalepisodes=18000
        try:
            with open("qtable.pkl", "rb") as f:
                self.qtable = pickle.load(f)
                print("qtable,loaded")
        except FileNotFoundError:
            self.qtable = {}
            print("qtable not loaded")
        self.rewards_per_episode = []
        self.successes = []
        self.actions=[(0,1),(0,-1),(1,0),(-1,0)]
        self.epsilon=1.0
        self.alpha=0.5
        self.gamma=0.9
        self.min_epsilon=0.05
        self.epsilon_decay=0.9996
        self.training = True

    def qlearning(self):
        dx = self.death_eater.pos[0] - self.harry.pos[0]
        dy = self.death_eater.pos[1] - self.harry.pos[1]
        cx = self.cup.pos[0]
        cy = self.cup.pos[1]
        state = (self.harry.pos, (dx, dy), (cx, cy))

        if state not in self.qtable:
            self.qtable[state]=[0,0,0,0]

        if random.random()<self.epsilon:
            action_index=random.randint(0,3)
        else:
            action_index=self.qtable[state].index(max(self.qtable[state]))

        action=self.actions[action_index]

        new_x=self.harry.pos[0]+action[0]
        new_y=self.harry.pos[1]+action[1]
        new_pos=(new_x,new_y)

        while new_pos not in self.valid_cells:
            self.qtable[state][action_index]=-4
            if random.random()<self.epsilon:
                action_index=random.randint(0,3)
            else:
                action_index=self.qtable[state].index(max(self.qtable[state]))

            action=self.actions[action_index]

            new_x=self.harry.pos[0]+action[0]
            new_y=self.harry.pos[1]+action[1]
            new_pos=(new_x,new_y)
       
        if new_pos == self.cup.pos:
            reward = 200
            
        elif new_pos == self.death_eater.pos:
            reward = -300
            
        else:
            old_dist = abs(self.harry.pos[0] - cx) + abs(self.harry.pos[1] - cy)
            new_dist = abs(new_pos[0] - cx) + abs(new_pos[1] - cy)
            new_de_dist = abs(new_pos[0] - self.death_eater.pos[0]) + abs(new_pos[1] - self.death_eater.pos[1])
            progress = max(-3, min( 3, old_dist - new_dist))   # -3 … +3
            danger   = -3 / max(new_de_dist,1)                 # 0 … -3
            reward   = progress*4 + danger                     # -15 … +12

                
        new_dx = self.death_eater.pos[0] - new_pos[0]
        new_dy = self.death_eater.pos[1] - new_pos[1]
        new_state = (new_pos,(new_dx, new_dy),(cx,cy))

        if new_state not in self.qtable:
            self.qtable[new_state] = [0, 0, 0, 0]
        
        old_value=self.qtable[state][action_index]
        future_value=max(self.qtable[new_state])
        new_value=old_value + self.alpha*(reward+self.gamma*future_value - old_value)
        self.qtable[state][action_index]=new_value

        self.harry.pos=new_pos

        return reward

    def run(self):
        self.count=0
        for episode in range(self.totalepisodes):
            harry_pos, death_eater_pos, cup_pos = random.sample(self.valid_cells, 3)
            self.harry.pos = harry_pos
            self.death_eater.pos = death_eater_pos
            self.cup.pos = cup_pos

            total_reward = 0

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                self.frame_counter+=1
                if self.frame_counter % self.move_interval == 0:
                    if self.turn == "death_eater":
                        self.update()
                        self.turn = "harry"
                    elif self.turn == "harry":
                        total_reward += self.qlearning()
                        self.turn = "death_eater"
                # self.draw()
                # self.clock.tick(100)
                if self.check_terminal():
                    break

            self.rewards_per_episode.append(total_reward)

            if episode % 100 == 0:
                print(f"Episode {episode} | Total reward: {total_reward} | Epsilon: {self.epsilon:.3f}")

            if self.epsilon > self.min_epsilon:
                self.epsilon *= self.epsilon_decay
            
            self.alpha = max(0.1, self.alpha * 0.9995)

        print(self.count)

        with open("qtable.pkl", "wb") as f:
            pickle.dump(self.qtable, f)
        print("Q-table saved to:", os.path.abspath("qtable.pkl"))

        rewards_series = pd.Series(self.rewards_per_episode)


        rolling_mean = rewards_series.rolling(window=200).mean()


        plt.figure(figsize=(10, 5))
        plt.plot(rolling_mean, label="Rolling Mean Reward (window=200)", color='blue')
        plt.xlabel("Episode")
        plt.ylabel("Average Reward")
        plt.title("Rolling Average of Episode Rewards")
        plt.legend()
        plt.grid(True)
        plt.show()

        window_size = 200  
        rolling_success = pd.Series(self.successes).rolling(window=window_size).mean()

        plt.figure(figsize=(10, 5))
        plt.plot(rolling_success, label=f"Rolling Success Rate (window={window_size})", color="green")
        plt.xlabel("Episode")
        plt.ylabel("Success Rate")
        plt.title("Agent Success Rate Over Time")
        plt.legend()
        plt.show()

    def update(self):
        if self.frame_counter % self.move_interval == 0:
            path = self.maze.bfs(self.death_eater.pos, self.harry.pos)
            if len(path) > 1:
                self.death_eater.pos = path[1]

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.maze.draw(self.screen, self.wall)
        self.harry.draw(self.screen)
        self.death_eater.draw(self.screen)
        self.cup.draw(self.screen)
        pygame.display.update()

    def check_terminal(self):
        if self.harry.pos == self.cup.pos:
            self.successes.append(1)
            self.count+=1
            return True
        if self.harry.pos == self.death_eater.pos:
            self.successes.append(0)
            return True
        return False

Game().run()

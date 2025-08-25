import tkinter as tk
import random
import time
import math

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TRACK_WIDTH = 400
TRACK_LEFT = (WINDOW_WIDTH - TRACK_WIDTH) // 2
TRACK_RIGHT = TRACK_LEFT + TRACK_WIDTH
CAR_WIDTH = 40
CAR_HEIGHT = 80
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 80
LANE_COUNT = 3
LANE_WIDTH = TRACK_WIDTH // LANE_COUNT
FPS = 60
ENEMY_SPAWN_INTERVAL = 1500  # ms
OBSTACLE_SPAWN_INTERVAL = 3500  # ms
FUEL_SPAWN_INTERVAL = 7000  # ms
SPEED_INCREMENT_INTERVAL = 10000  # ms
FUEL_DECREASE_INTERVAL = 400  # ms
FUEL_DECREASE_AMOUNT = 2
FUEL_PICKUP_AMOUNT = 30
MAX_FUEL = 100
BOSS_LEVEL = 5  # Level at which the boss appears
FINAL_BOSS_LEVEL = 10  # Level for the final boss

class Car:
    def __init__(self, canvas, x, y, color="blue"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.color = color
        # Draw a more detailed car: body, windows, wheels, lights, spoiler, mirrors, exhaust
        self.body = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill=self.color, outline="black", width=2
        )
        # Windows
        self.window = self.canvas.create_rectangle(
            self.x + 8, self.y + 12, self.x + self.width - 8, self.y + 35,
            fill="lightblue", outline="gray", width=1
        )
        # Wheels (with hubcaps)
        self.wheel1 = self.canvas.create_oval(
            self.x + 2, self.y + 8, self.x + 14, self.y + 22,
            fill="black", outline="gray"
        )
        self.hubcap1 = self.canvas.create_oval(
            self.x + 6, self.y + 12, self.x + 10, self.y + 18,
            fill="silver", outline=""
        )
        self.wheel2 = self.canvas.create_oval(
            self.x + self.width - 14, self.y + 8, self.x + self.width - 2, self.y + 22,
            fill="black", outline="gray"
        )
        self.hubcap2 = self.canvas.create_oval(
            self.x + self.width - 10, self.y + 12, self.x + self.width - 6, self.y + 18,
            fill="silver", outline=""
        )
        self.wheel3 = self.canvas.create_oval(
            self.x + 2, self.y + self.height - 22, self.x + 14, self.y + self.height - 8,
            fill="black", outline="gray"
        )
        self.hubcap3 = self.canvas.create_oval(
            self.x + 6, self.y + self.height - 18, self.x + 10, self.y + self.height - 12,
            fill="silver", outline=""
        )
        self.wheel4 = self.canvas.create_oval(
            self.x + self.width - 14, self.y + self.height - 22, self.x + self.width - 2, self.y + self.height - 8,
            fill="black", outline="gray"
        )
        self.hubcap4 = self.canvas.create_oval(
            self.x + self.width - 10, self.y + self.height - 18, self.x + self.width - 6, self.y + self.height - 12,
            fill="silver", outline=""
        )
        # Headlights
        self.headlight1 = self.canvas.create_oval(
            self.x + 8, self.y, self.x + 16, self.y + 8,
            fill="yellow", outline=""
        )
        self.headlight2 = self.canvas.create_oval(
            self.x + self.width - 16, self.y, self.x + self.width - 8, self.y + 8,
            fill="yellow", outline=""
        )
        # Taillights
        self.taillight1 = self.canvas.create_oval(
            self.x + 8, self.y + self.height - 8, self.x + 16, self.y + self.height,
            fill="red", outline=""
        )
        self.taillight2 = self.canvas.create_oval(
            self.x + self.width - 16, self.y + self.height - 8, self.x + self.width - 8, self.y + self.height,
            fill="red", outline=""
        )
        # Spoiler
        self.spoiler = self.canvas.create_rectangle(
            self.x + 6, self.y + self.height - 14, self.x + self.width - 6, self.y + self.height - 10,
            fill="black", outline="gray"
        )
        # Side mirrors
        self.mirror1 = self.canvas.create_rectangle(
            self.x - 4, self.y + 20, self.x, self.y + 30,
            fill="gray", outline=""
        )
        self.mirror2 = self.canvas.create_rectangle(
            self.x + self.width, self.y + 20, self.x + self.width + 4, self.y + 30,
            fill="gray", outline=""
        )
        # Exhaust pipes
        self.exhaust1 = self.canvas.create_rectangle(
            self.x + 10, self.y + self.height, self.x + 16, self.y + self.height + 6,
            fill="gray", outline=""
        )
        self.exhaust2 = self.canvas.create_rectangle(
            self.x + self.width - 16, self.y + self.height, self.x + self.width - 10, self.y + self.height + 6,
            fill="gray", outline=""
        )

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        for part in [self.body, self.window, self.wheel1, self.wheel2, self.wheel3, self.wheel4,
                     self.hubcap1, self.hubcap2, self.hubcap3, self.hubcap4,
                     self.headlight1, self.headlight2, self.taillight1, self.taillight2,
                     self.spoiler, self.mirror1, self.mirror2, self.exhaust1, self.exhaust2]:
            self.canvas.move(part, dx, dy)

    def get_bbox(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def destroy(self):
        for part in [self.body, self.window, self.wheel1, self.wheel2, self.wheel3, self.wheel4,
                     self.hubcap1, self.hubcap2, self.hubcap3, self.hubcap4,
                     self.headlight1, self.headlight2, self.taillight1, self.taillight2,
                     self.spoiler, self.mirror1, self.mirror2, self.exhaust1, self.exhaust2]:
            self.canvas.delete(part)

class EnemyCar(Car):
    def __init__(self, canvas, lane, y, color=None):
        if color is None:
            color = random.choice(["red", "green", "orange", "cyan", "magenta"])
        x = TRACK_LEFT + lane * LANE_WIDTH + (LANE_WIDTH - CAR_WIDTH) // 2
        super().__init__(canvas, x, y, color)
        # Add a racing stripe for enemies
        self.stripe = self.canvas.create_rectangle(
            self.x + self.width // 2 - 4, self.y + 10,
            self.x + self.width // 2 + 4, self.y + self.height - 10,
            fill="white", outline=""
        )
        # Add a roof number
        self.roof_number = self.canvas.create_text(
            self.x + self.width // 2, self.y + 20,
            text=str(random.randint(1, 99)), font=("Arial", 10, "bold"), fill="black"
        )
        # Add a small flag
        self.flag = self.canvas.create_polygon(
            self.x + self.width - 8, self.y + 8,
            self.x + self.width - 2, self.y + 12,
            self.x + self.width - 8, self.y + 16,
            fill="white", outline="black"
        )

    def move(self, dx, dy):
        super().move(dx, dy)
        self.canvas.move(self.stripe, dx, dy)
        self.canvas.move(self.roof_number, dx, dy)
        self.canvas.move(self.flag, dx, dy)

    def destroy(self):
        super().destroy()
        self.canvas.delete(self.stripe)
        self.canvas.delete(self.roof_number)
        self.canvas.delete(self.flag)

class PlayerCar(Car):
    def __init__(self, canvas, lane, y):
        super().__init__(canvas, TRACK_LEFT + lane * LANE_WIDTH + (LANE_WIDTH - CAR_WIDTH) // 2, y, color="blue")
        # Add a racing number
        self.number = self.canvas.create_text(
            self.x + self.width // 2, self.y + self.height // 2,
            text="7", font=("Arial", 16, "bold"), fill="white"
        )
        # Add a custom logo
        self.logo = self.canvas.create_oval(
            self.x + self.width // 2 - 8, self.y + 40, self.x + self.width // 2 + 8, self.y + 56,
            fill="gold", outline="black"
        )
        # Add a speed trail effect (hidden by default)
        self.trail = []
        for i in range(3):
            oval = self.canvas.create_oval(
                self.x + self.width // 2 - 6, self.y + self.height + 8 + i * 8,
                self.x + self.width // 2 + 6, self.y + self.height + 18 + i * 8,
                fill="lightblue", outline="", state="hidden"
            )
            self.trail.append(oval)

    def move(self, dx, dy):
        super().move(dx, dy)
        self.canvas.move(self.number, dx, dy)
        self.canvas.move(self.logo, dx, dy)
        for oval in self.trail:
            self.canvas.move(oval, dx, dy)

    def show_trail(self, show=True):
        for oval in self.trail:
            self.canvas.itemconfig(oval, state="normal" if show else "hidden")

    def destroy(self):
        super().destroy()
        self.canvas.delete(self.number)
        self.canvas.delete(self.logo)
        for oval in self.trail:
            self.canvas.delete(oval)

class Obstacle:
    def __init__(self, canvas, lane, y):
        self.canvas = canvas
        self.x = TRACK_LEFT + lane * LANE_WIDTH + (LANE_WIDTH - ENEMY_WIDTH) // 2
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT // 2
        # Draw a detailed obstacle (barrier with stripes and hazard sign)
        self.body = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill="gray", outline="black", width=2
        )
        self.stripes = []
        for i in range(3):
            stripe = self.canvas.create_rectangle(
                self.x + i * (self.width // 3), self.y,
                self.x + (i + 1) * (self.width // 3) - 2, self.y + self.height,
                fill="orange" if i % 2 == 0 else "white", outline=""
            )
            self.stripes.append(stripe)
        # Hazard sign
        self.hazard = self.canvas.create_polygon(
            self.x + self.width // 2 - 10, self.y + self.height // 2 - 8,
            self.x + self.width // 2 + 10, self.y + self.height // 2 - 8,
            self.x + self.width // 2, self.y + self.height // 2 + 8,
            fill="yellow", outline="black"
        )
        self.hazard_text = self.canvas.create_text(
            self.x + self.width // 2, self.y + self.height // 2,
            text="!", font=("Arial", 12, "bold"), fill="red"
        )

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.canvas.move(self.body, dx, dy)
        for stripe in self.stripes:
            self.canvas.move(stripe, dx, dy)
        self.canvas.move(self.hazard, dx, dy)
        self.canvas.move(self.hazard_text, dx, dy)

    def get_bbox(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def destroy(self):
        self.canvas.delete(self.body)
        for stripe in self.stripes:
            self.canvas.delete(stripe)
        self.canvas.delete(self.hazard)
        self.canvas.delete(self.hazard_text)

class FuelPickup:
    def __init__(self, canvas, lane, y):
        self.canvas = canvas
        self.x = TRACK_LEFT + lane * LANE_WIDTH + (LANE_WIDTH - 30) // 2
        self.y = y
        self.width = 30
        self.height = 40
        # Draw a detailed fuel can with handle and spout
        self.body = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill="yellow", outline="black", width=2
        )
        self.cap = self.canvas.create_rectangle(
            self.x + 10, self.y - 6, self.x + 20, self.y,
            fill="gray", outline="black"
        )
        self.handle = self.canvas.create_oval(
            self.x + 5, self.y - 10, self.x + 25, self.y - 2,
            fill="gray", outline="black"
        )
        self.spout = self.canvas.create_rectangle(
            self.x + 13, self.y - 12, self.x + 17, self.y - 6,
            fill="gray", outline="black"
        )
        self.label = self.canvas.create_text(
            self.x + self.width // 2, self.y + self.height // 2,
            text="F", font=("Arial", 16, "bold"), fill="red"
        )

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.canvas.move(self.body, dx, dy)
        self.canvas.move(self.cap, dx, dy)
        self.canvas.move(self.handle, dx, dy)
        self.canvas.move(self.spout, dx, dy)
        self.canvas.move(self.label, dx, dy)

    def get_bbox(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def destroy(self):
        self.canvas.delete(self.body)
        self.canvas.delete(self.cap)
        self.canvas.delete(self.handle)
        self.canvas.delete(self.spout)
        self.canvas.delete(self.label)

# Bosses remain visually distinct and more detailed
class BossCar(Car):
    def __init__(self, canvas, y, speed):
        x = TRACK_LEFT
        super().__init__(canvas, x, y, color="darkred")
        self.width = TRACK_WIDTH
        self.height = CAR_HEIGHT * 1.5
        self.speed = speed
        # Boss body (overrides base car)
        self.body = self.canvas.create_rectangle(
            x, y, x + self.width, y + self.height, fill="darkred", outline="gold", width=4
        )
        # Boss windows
        self.window = self.canvas.create_rectangle(
            x + 40, y + 30, x + self.width - 40, y + 60,
            fill="black", outline="gray", width=2
        )
        # Boss headlights
        self.headlight1 = self.canvas.create_oval(
            x + 30, y, x + 60, y + 20, fill="yellow", outline=""
        )
        self.headlight2 = self.canvas.create_oval(
            x + self.width - 60, y, x + self.width - 30, y + 20, fill="yellow", outline=""
        )
        # Boss taillights
        self.taillight1 = self.canvas.create_oval(
            x + 30, y + self.height - 20, x + 60, y + self.height, fill="red", outline=""
        )
        self.taillight2 = self.canvas.create_oval(
            x + self.width - 60, y + self.height - 20, x + self.width - 30, y + self.height, fill="red", outline=""
        )
        # Boss wheels
        self.wheel1 = self.canvas.create_oval(
            x + 10, y + 10, x + 40, y + self.height - 10, fill="black", outline="gray"
        )
        self.wheel2 = self.canvas.create_oval(
            x + self.width - 40, y + 10, x + self.width - 10, y + self.height - 10, fill="black", outline="gray"
        )
        # Boss spoiler
        self.spoiler = self.canvas.create_rectangle(
            x + 20, y + self.height - 18, x + self.width - 20, y + self.height - 10,
            fill="black", outline="gold"
        )
        # Boss exhausts
        self.exhaust1 = self.canvas.create_rectangle(
            x + 40, y + self.height, x + 60, y + self.height + 10,
            fill="gray", outline=""
        )
        self.exhaust2 = self.canvas.create_rectangle(
            x + self.width - 60, y + self.height, x + self.width - 40, y + self.height + 10,
            fill="gray", outline=""
        )
        # Boss armor plates
        self.armor = []
        for i in range(4):
            plate = self.canvas.create_rectangle(
                x + 60 + i * 80, y + 10, x + 100 + i * 80, y + 30,
                fill="darkgoldenrod", outline="black"
            )
            self.armor.append(plate)
        self.move_direction = 1  # 1: right, -1: left
        self.move_counter = 0
        self.health = 15

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        for part in [self.body, self.window, self.headlight1, self.headlight2,
                     self.taillight1, self.taillight2, self.wheel1, self.wheel2,
                     self.spoiler, self.exhaust1, self.exhaust2]:
            self.canvas.move(part, dx, dy)
        for plate in self.armor:
            self.canvas.move(plate, dx, dy)

    def update(self):
        if self.move_counter % 30 == 0:
            self.move_direction *= -1
        dx = self.move_direction * 10
        if self.x + dx < TRACK_LEFT:
            dx = TRACK_LEFT - self.x
            self.move_direction = 1
        elif self.x + dx + self.width > TRACK_RIGHT:
            dx = TRACK_RIGHT - (self.x + self.width)
            self.move_direction = -1
        self.move(dx, self.speed)
        self.move_counter += 1

    def get_bbox(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def hit(self):
        self.health -= 1
        self.canvas.itemconfig(self.body, outline="white" if self.health % 2 == 0 else "gold")
        if self.health <= 0:
            self.destroy()
            return True
        return False

    def destroy(self):
        for part in [self.body, self.window, self.headlight1, self.headlight2,
                     self.taillight1, self.taillight2, self.wheel1, self.wheel2,
                     self.spoiler, self.exhaust1, self.exhaust2]:
            self.canvas.delete(part)
        for plate in self.armor:
            self.canvas.delete(plate)

class FinalBossCar(Car):
    def __init__(self, canvas, y, speed):
        x = TRACK_LEFT
        super().__init__(canvas, x, y, color="purple")
        self.width = TRACK_WIDTH
        self.height = CAR_HEIGHT * 2
        self.speed = speed
        # Final boss body (overrides base car)
        self.body = self.canvas.create_rectangle(
            x, y, x + self.width, y + self.height, fill="purple", outline="yellow", width=6
        )
        # Final boss windows
        self.window = self.canvas.create_rectangle(
            x + 60, y + 40, x + self.width - 60, y + 90,
            fill="black", outline="gray", width=2
        )
        # Final boss headlights
        self.headlight1 = self.canvas.create_oval(
            x + 50, y, x + 90, y + 30, fill="yellow", outline=""
        )
        self.headlight2 = self.canvas.create_oval(
            x + self.width - 90, y, x + self.width - 50, y + 30, fill="yellow", outline=""
        )
        # Final boss taillights
        self.taillight1 = self.canvas.create_oval(
            x + 50, y + self.height - 30, x + 90, y + self.height, fill="red", outline=""
        )
        self.taillight2 = self.canvas.create_oval(
            x + self.width - 90, y + self.height - 30, x + self.width - 50, y + self.height, fill="red", outline=""
        )
        # Final boss wheels
        self.wheel1 = self.canvas.create_oval(
            x + 20, y + 20, x + 70, y + self.height - 20, fill="black", outline="gray"
        )
        self.wheel2 = self.canvas.create_oval(
            x + self.width - 70, y + 20, x + self.width - 20, y + self.height - 20, fill="black", outline="gray"
        )
        # Final boss spoiler
        self.spoiler = self.canvas.create_rectangle(
            x + 40, y + self.height - 24, x + self.width - 40, y + self.height - 12,
            fill="black", outline="yellow"
        )
        # Final boss exhausts
        self.exhaust1 = self.canvas.create_rectangle(
            x + 60, y + self.height, x + 90, y + self.height + 14,
            fill="gray", outline=""
        )
        self.exhaust2 = self.canvas.create_rectangle(
            x + self.width - 90, y + self.height, x + self.width - 60, y + self.height + 14,
            fill="gray", outline=""
        )
        # Final boss armor plates
        self.armor = []
        for i in range(5):
            plate = self.canvas.create_rectangle(
                x + 80 + i * 100, y + 20, x + 120 + i * 100, y + 50,
                fill="gold", outline="black"
            )
            self.armor.append(plate)
        self.move_direction = 1
        self.move_counter = 0
        self.health = 30
        self.laser_active = False
        self.laser = None
        self.laser_cooldown = 0
        # Final boss deploys mines
        self.mines = []
        self.mine_cooldown = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        for part in [self.body, self.window, self.headlight1, self.headlight2,
                     self.taillight1, self.taillight2, self.wheel1, self.wheel2,
                     self.spoiler, self.exhaust1, self.exhaust2]:
            self.canvas.move(part, dx, dy)
        for plate in self.armor:
            self.canvas.move(plate, dx, dy)
        if self.laser:
            self.canvas.move(self.laser, dx, dy)
        for mine in self.mines:
            self.canvas.move(mine, dx, dy)

    def update(self):
        if self.move_counter % 20 == 0:
            self.move_direction *= -1
        dx = self.move_direction * 18
        if self.x + dx < TRACK_LEFT:
            dx = TRACK_LEFT - self.x
            self.move_direction = 1
        elif self.x + dx + self.width > TRACK_RIGHT:
            dx = TRACK_RIGHT - (self.x + self.width)
            self.move_direction = -1
        self.move(dx, self.speed)
        self.move_counter += 1
        # Laser attack
        if self.laser_cooldown <= 0 and not self.laser_active and random.random() < 0.03:
            self.fire_laser()
            self.laser_cooldown = 120  # frames
        if self.laser_active:
            self.update_laser()
        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1
        # Deploy mines
        if self.mine_cooldown <= 0 and random.random() < 0.04:
            self.deploy_mine()
            self.mine_cooldown = 90
        if self.mine_cooldown > 0:
            self.mine_cooldown -= 1

    def fire_laser(self):
        lx = TRACK_LEFT + TRACK_WIDTH // 2 - 10
        ly = self.y + self.height
        self.laser = self.canvas.create_rectangle(
            lx, ly, lx + 20, WINDOW_HEIGHT, fill="red", outline=""
        )
        self.laser_active = True

    def update_laser(self):
        if self.laser_active:
            if self.move_counter % 30 == 0:
                self.canvas.delete(self.laser)
                self.laser = None
                self.laser_active = False

    def deploy_mine(self):
        mx = random.randint(TRACK_LEFT + 20, TRACK_RIGHT - 20)
        my = self.y + self.height + 10
        mine = self.canvas.create_oval(
            mx - 10, my - 10, mx + 10, my + 10, fill="black", outline="red", width=2
        )
        self.mines.append(mine)

    def get_mine_bboxes(self):
        bboxes = []
        for mine in self.mines:
            bbox = self.canvas.bbox(mine)
            if bbox:
                bboxes.append(bbox)
        return bboxes

    def clear_mines(self):
        for mine in self.mines:
            self.canvas.delete(mine)
        self.mines.clear()

    def get_bbox(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def get_laser_bbox(self):
        if self.laser_active:
            lx = TRACK_LEFT + TRACK_WIDTH // 2 - 10
            return (lx, self.y + self.height, lx + 20, WINDOW_HEIGHT)
        return None

    def hit(self):
        self.health -= 1
        self.canvas.itemconfig(self.body, outline="white" if self.health % 2 == 0 else "yellow")
        if self.health <= 0:
            self.destroy()
            return True
        return False

    def destroy(self):
        for part in [self.body, self.window, self.headlight1, self.headlight2,
                     self.taillight1, self.taillight2, self.wheel1, self.wheel2,
                     self.spoiler, self.exhaust1, self.exhaust2]:
            self.canvas.delete(part)
        for plate in self.armor:
            self.canvas.delete(plate)
        if self.laser:
            self.canvas.delete(self.laser)
        self.clear_mines()

# ... rest of your classes ...

# **Chess Game**
Welcome to Chess Game, a strategic implementation of the classic chess game. This project was developed to enhance and test my skills in **object-oriented programming (OOP)** and **game development** using **Python** and **PyGame**.

## **Features**
- Fully object-oriented design to ensure clean, modular, and reusable code.
- Supports **player vs. player** chess matches.
- Implements **special moves** such as **castling**, **en passant**, and **pawn promotion**.
- Graphical interface using **PyGame** for smooth and interactive gameplay.
- Turn-based mechanics with move validation.

## **Purpose**
The primary goal of this project was to apply and solidify my understanding of **OOP principles**, such as:

- **Encapsulation**
- **Inheritance**
- **Polymorphism**
- **Abstraction**

## **Technologies Used**
- **Language:** Python  
- **Libraries/Frameworks:** PyGame, PyAutoGUI  

## **Code Snippet**
### **Game Class - Core Game Logic**
```python
class Game(object):
    def __init__(self):
        self.player1 = Player(0)
        self.player2 = Player(1)
        self.player2.enemy = self.player1
        self.player1.enemy = self.player2

    def is_over(self):
        movables = self.available()
        if movables == "t":
            return "Tie"
        p1_movements, p2_movements = 0, 0
        for l in range(8):
            for c in range(8):
                for x in movables[0]:
                    if x.valid_move([l, c]) and x.is_legal_move([l, c]):
                        p1_movements += 1
                for y in movables[1]:
                    if y.valid_move([l, c]) and y.is_legal_move([l, c]):
                        p2_movements += 1
        if self.player1.is_checked() and p1_movements == 0:
            return self.player2.name
        elif self.player2.is_checked() and p2_movements == 0:
            return self.player1.name
        if p1_movements == p2_movements == 0:
            return "Tie"
        return None
```

### **Tool Class - Handling Chess Pieces**
```python
class Tool(object):
    def __init__(self, name, color, pos, player):
        self.player = player
        self.name = name
        self.team = color
        self.position = pos
        self.icon = None
        self.x, self.y = 0, 0
        self.two_move, self.just_now = False, False

    def move(self, pos):
        self.position = pos
        self.eat(pos)
        self.x = 14 + self.position[1] * 94
        self.y = 14 + self.position[0] * 94
```

### **GameView - GUI using PyGame**
```python
def show_state():
    screen.fill((117, 117, 117))
    screen.blit(board_img, (board_x, board_y))
    for t in game.player1.tools + game.player2.tools:
        if t.position is not None:
            screen.blit(t.icon, (t.x, t.y))
    pg.display.update()
```

## **Future Enhancements**
- Add AI player for **single-player mode**.
- Implement **timed moves** for competitive play.
- Support **online multiplayer** through socket programming.
- Track **player statistics** and game history.

## **Contributing**
Contributions are welcome! If you have ideas or improvements, feel free to **open an issue** or **submit a pull request**.

## **License**
This project is a **learning-based** project and is shared as-is. Feel free to use or modify the code for **personal or educational purposes**. No formal license is applied.


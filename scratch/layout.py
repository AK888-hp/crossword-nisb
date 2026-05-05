import json
import random

words = [
    "SEMICONDUCTOR",
    "BANDWIDTH",
    "OSCILLATION",
    "CMOS",
    "POWER",
    "INDUCTOR",
    "AMPLITUDE",
    "RESISTOR",
    "ATTENUATION",
    "VOLTAGE",
    "ANALOG",
    "TRANSISTOR"
]

clues = {
    "SEMICONDUCTOR": "Material with conductivity between an insulator and most metals",
    "BANDWIDTH": "Range of frequencies within a given band",
    "OSCILLATION": "Repetitive variation, typically in time",
    "CMOS": "Complementary metal-oxide-semiconductor",
    "POWER": "Rate of doing work",
    "INDUCTOR": "Passive two-terminal electrical component that stores energy in a magnetic field",
    "AMPLITUDE": "Maximum extent of a vibration or oscillation",
    "RESISTOR": "Passive two-terminal electrical component that implements electrical resistance",
    "ATTENUATION": "Gradual loss of flux intensity through a medium",
    "VOLTAGE": "Electric potential difference",
    "ANALOG": "Relating to a mechanism that represents data by measurement of a continuous physical variable",
    "TRANSISTOR": "Semiconductor device used to amplify or switch electrical signals and power"
}

# A simple grid generation approach for testing
def generate_grid(words):
    grid = {} # (x,y) -> char
    placements = []
    
    # Sort by length descending
    words = sorted(words, key=len, reverse=True)
    
    def can_place(word, x, y, dx, dy):
        for i, char in enumerate(word):
            nx, ny = x + dx*i, y + dy*i
            if (nx, ny) in grid and grid[(nx, ny)] != char:
                return False
            # check neighbors to avoid adjacent letters
            if (nx, ny) not in grid:
                n1 = (nx + dy, ny + dx)
                n2 = (nx - dy, ny - dx)
                if n1 in grid or n2 in grid:
                    return False
        # check start and end
        if (x-dx, y-dy) in grid or (x+dx*len(word), y+dy*len(word)) in grid:
            return False
        return True

    def place_word(word, x, y, dx, dy):
        for i, char in enumerate(word):
            nx, ny = x + dx*i, y + dy*i
            grid[(nx, ny)] = char
        placements.append({
            "word": word,
            "clue": clues[word],
            "direction": "across" if dx == 1 else "down",
            "x": x,
            "y": y
        })

    # Place first word
    place_word(words[0], 0, 0, 1, 0)
    
    # Place remaining
    for word in words[1:]:
        placed = False
        for c_idx, char in enumerate(word):
            if placed: break
            # Find matching char in grid
            for (gx, gy), gchar in grid.items():
                if char == gchar:
                    # try placing vertically
                    start_x = gx
                    start_y = gy - c_idx
                    if can_place(word, start_x, start_y, 0, 1):
                        place_word(word, start_x, start_y, 0, 1)
                        placed = True
                        break
                    # try placing horizontally
                    start_x = gx - c_idx
                    start_y = gy
                    if can_place(word, start_x, start_y, 1, 0):
                        place_word(word, start_x, start_y, 1, 0)
                        placed = True
                        break
        if not placed:
            print(f"Could not place {word}")

    return placements

placements = generate_grid(words)

# Normalize coordinates
min_x = min(p['x'] for p in placements)
min_y = min(p['y'] for p in placements)
for p in placements:
    p['x'] -= min_x
    p['y'] -= min_y

max_x = max(p['x'] + (len(p['word']) if p['direction'] == 'across' else 1) for p in placements)
max_y = max(p['y'] + (len(p['word']) if p['direction'] == 'down' else 1) for p in placements)

out = {
    "grid": {
        "width": max_x + 1,
        "height": max_y + 1
    },
    "words": placements
}

print(json.dumps(out, indent=2))

#!/usr/bin/env python3
"""Draw the front page of Wednesday 18 November 2026 world news as a 1024x1024 PNG.

Stdlib only: an embedded 5x7 bitmap font and a hand-rolled PNG encoder, so
the program runs in the grader's bare sandbox with nothing installed.
Deterministic: no randomness, no timestamps, no network, no file reads.
Writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

The font covers capitals, digits and punctuation; all text is uppercased
before drawing, so every letter renders.
"""
import os
import struct
import zlib

W, H = 1024, 1024

# --- colours ---
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (30, 58, 95)
GREY = (110, 108, 100)
LIGHT = (232, 226, 210)

# --- 5x7 bitmap font: each glyph is 7 rows of 5 pixels, '#' = ink ---
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "#.#.#", "##..#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "-": (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    "/": ("....#", "....#", "...#.", "...#.", "..#..", ".#...", "#...."),
    "(": ("...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"),
    ")": ("##...", "..#..", "...#.", "...#.", "...#.", "..#..", "##..."),
    "%": ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "&": (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "+": (".....", "..#..", "..#..", ".###.", "..#..", "..#..", "....."),
    "=": (".....", ".....", ".###.", ".....", ".###.", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.buf = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i], self.buf[i + 1], self.buf[i + 2] = c

    def fill_rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.px(xx, yy, c)

    def hline(self, x, y, w, c, t=1):
        self.fill_rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.fill_rect(x, y, t, h, c)

    def rect(self, x, y, w, h, c, t=1):
        self.hline(x, y, w, c, t)
        self.hline(x, y + h - t, w, c, t)
        self.vline(x, y, h, c, t)
        self.vline(x + w - t, y, h, c, t)

    def circle(self, cx, cy, r, c, t=2):
        import math
        steps = max(48, r * 6)
        for i in range(steps):
            a = 2 * math.pi * i / steps
            self.fill_rect(cx + int(r * math.cos(a)) - t // 2,
                           cy + int(r * math.sin(a)) - t // 2, t, t, c)

    def text_w(self, text, s):
        text = text.upper()
        return len(text) * 6 * s - s if text else 0

    def text(self, x, y, text, s, c):
        text = text.upper()
        cx = x
        for ch in text:
            glyph = FONT.get(ch, FONT[" "])
            for r in range(7):
                row = glyph[r]
                for col in range(5):
                    if row[col] == "#":
                        self.fill_rect(cx + col * s, y + r * s, s, s, c)
            cx += 6 * s
        return cx

    def text_center(self, y, text, s, c):
        self.text((self.w - self.text_w(text, s)) // 2, y, text, s, c)

    def wrap(self, text, s, max_w):
        """Greedy word wrap; every returned line fits in max_w pixels."""
        lines, cur = [], ""
        for word in text.upper().split(" "):
            trial = word if not cur else cur + " " + word
            if self.text_w(trial, s) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, text, s, max_w, c, leading=6):
        lines = self.wrap(text, s, max_w)
        for ln in lines:
            self.text(x, y, ln, s, c)
            y += 7 * s + leading
        return y


def draw_globe(cv, cx, cy, r, c):
    """Simple line globe: outer circle, two meridian ellipses, two parallels."""
    import math
    cv.circle(cx, cy, r, c, t=3)
    steps = 72
    for k, f in ((0.45, 1.0), (0.9, 1.0)):
        for i in range(steps):
            a = 2 * math.pi * i / steps
            ex, ey = cx + int(r * f * math.cos(a)), cy + int(r * math.sin(a))
            cv.fill_rect(ex - 1, ey - 1, 3, 3, c)
    for dy in (-r // 2, r // 2):
        half = int((r * r - dy * dy) ** 0.5)
        cv.hline(cx - half, cy + dy, half * 2, c, t=2)
    cv.hline(cx - r, cy, r * 2, c, t=2)


def story_block(cv, x, y, w, kicker, headline, summary, head_s, sum_s):
    cv.text(x, y, kicker, 2, RED)
    y += 7 * 2 + 8
    y = cv.para(x, y, headline, head_s, w, INK, leading=4)
    y += 2
    y = cv.para(x, y, summary, sum_s, w, INK, leading=5)
    return y


def main():
    cv = Canvas(W, H, PAPER)
    M = 36  # margin
    content_w = W - 2 * M

    # --- masthead ---
    cv.hline(0, 0, W, RED, t=8)
    cv.text_center(26, "THE WORLD TODAY", 8, INK)
    cv.text_center(96, "WEDNESDAY 18 NOVEMBER 2026", 3, RED)
    cv.text_center(122, "THE DAY'S WORLD NEWS IN ONE PAGE", 2, GREY)
    cv.hline(M, 150, content_w, INK, t=3)
    cv.hline(M, 156, content_w, INK, t=1)

    # --- lead story: APEC opens in Shenzhen (layout flows from content height) ---
    y = 176
    cv.text(M, y, "LEAD  •  ASIA-PACIFIC SUMMIT", 2, RED)
    y += 7 * 2 + 10
    lead_w = 700
    y = cv.para(M, y, "APEC OPENS IN SHENZHEN", 5, lead_w, INK, leading=4)
    y = cv.para(M, y, "TRUMP, XI AND PUTIN TO MEET", 5, lead_w, INK, leading=4)
    y += 4
    y = cv.para(
        M, y,
        "Leaders of 21 Pacific economies open their summit in China. "
        "Trump and Xi will talk trade, tariffs and AI, and a three-way "
        "meeting with Putin is planned for Thursday.",
        3, lead_w, INK, leading=6)
    draw_globe(cv, 880, 290, 92, BLUE)
    cap = "SHENZHEN, CHINA"
    cv.text(880 - cv.text_w(cap, 2) // 2, 398, cap, 2, BLUE)

    y += 16
    cv.hline(M, y, content_w, INK, t=2)
    y += 20

    # --- second row: two stories ---
    col_w = (content_w - 40) // 2
    end_l = story_block(cv, M, y, col_w,
                        "GULF  •  STRAIT OF HORMUZ",
                        "TANKER HIT IN HORMUZ, CREW EVACUATED",
                        "A tanker is struck as it leaves the strait and its crew "
                        "is evacuated. Iran claims a supertanker carrying two "
                        "million barrels of oil has sunk.",
                        4, 2)
    end_r = story_block(cv, M + col_w + 40, y, col_w,
                        "BRITAIN  •  WEST BANK",
                        "UK SANCTIONS ISRAELI SETTLEMENT FIRMS",
                        "Britain freezes the assets of eight Israeli construction "
                        "firms building West Bank settlements, in a push to protect "
                        "the two-state solution.",
                        4, 2)
    y = max(end_l, end_r) + 16
    cv.hline(M, y, content_w, INK, t=2)
    y += 20

    # --- third row: three stories ---
    col3 = (content_w - 2 * 32) // 3
    e1 = story_block(cv, M, y, col3,
                     "TAIWAN  •  DEFENCE",
                     "TAIWAN SEEKS $14BN IN US ARMS",
                     "Taipei says it urgently needs $14 billion of American "
                     "weapons as tensions with Beijing grow. The deal is now "
                     "up to President Trump.",
                     3, 2)
    e2 = story_block(cv, M + col3 + 32, y, col3,
                     "WEATHER  •  BAY OF BENGAL",
                     "CYCLONE AKVAN BEARS DOWN",
                     "A cyclonic storm strengthens over the Bay of Bengal and "
                     "is likely to turn severe by Thursday, India's weather "
                     "office warns.",
                     3, 2)
    e3 = story_block(cv, M + 2 * (col3 + 32), y, col3,
                     "USA  •  WASHINGTON",
                     "TRUMP RUBBISHES DIRTY-BOMB PLOT",
                     "Trump dismisses US intelligence reports that Iran is "
                     "weighing a dirty-bomb attack in Washington: \"They are "
                     "crazy,\" he says.",
                     3, 2)
    y = max(e1, e2, e3) + 24

    # --- footer ---
    cv.hline(M, y, content_w, INK, t=1)
    cv.text_center(y + 12, "SOURCES: REUTERS, AP, BBC, XINHUA, UKMTO - ALL EVENTS OF 18 NOVEMBER 2026", 2, GREY)

    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "entry.png")
    write_png(path, cv)
    print("wrote", path, os.path.getsize(path), "bytes")


def write_png(path, cv):
    raw = b"".join(
        b"\x00" + bytes(cv.buf[y * cv.w * 3:(y + 1) * cv.w * 3])
        for y in range(cv.h)
    )

    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)


if __name__ == "__main__":
    main()

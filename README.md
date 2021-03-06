# advent-py 🎄🐍
Advent of Code problems solved in Python (3.9+)

- [Advent of Code](https://adventofcode.com/)

## Running

I work on these using [PyCharm](https://www.jetbrains.com/pycharm/)

But you can run manually with:

```shell
$ export PYTHONPATH=.
$ python advent/year2020/day1.py
Part 1: <spoilers!>
Part 2: <spoilers!>
```

Just simple scripts: Each day's script runs solo (no top-level runner) and reads input from a .txt file with the same prefix in the same directory: `day1.py` reads `day1.txt`

## What's interesting?

- What's Advent of Code?
  - See Advent of Code's ["About"](https://adventofcode.com/2021/about)
- Why Advent of Code?
  - It's fun! As opposed to grinding LeetCode, AoC has fun "flavor" and lets you solve however you want (any language or even none!). Lots of hidden easter eggs and nerdy references.
  - Non-prescriptive: you decide how you want to solve the problem: use whatever language, editor/IDE, debuggers, or libraries you want.
  - "Sneaky" concepts: I like how Advent questions are a bit subtle and uniquely challenging. What works for part 1 may not scale for part 2. Sometimes all it takes is some refactoring; other times a full rewrite might be necessary.
- Why Python?
  - I've used AoC to get more familiar with other languages (Go, Clojure) and it's been a fun and useful approach.
  - I'm now looking to get more familiar with Python
  - Python is the #1 language for Advent of Code, and for good reason IMO. Most problems are solved in less than 100 lines of python
  - Compare to other languages, Python has significant advantages:
    - Python emphasizes the developer's time, which for these problems is a more crucial resource vs execution time 
    - vs Java: Python is succinct, direct, and operates on a higher level (and just more fun!)
    - vs Go, Crystal, or Clojure: Python has a better debugger (or has one at all!)
    - vs Go or Java: Python's `int` (and dynamic typing in-general) is nicer than strict typing 
    - Python is the slowest language to execute, but that's still fast enough. A "correct" solution typically comes down to using the right algorithm or data structures. 
- [elf.py](advent/elf.py) - Santa's little helper! Where I put helper functions
  - For example, using `__file__` within a python script gives the script filename. Then, changing the `.py` to `.txt` makes it simple to put the input file next to the script

##  My Advent Progress

What I've completed **in any language**

- Year 2021: 🌟 IN PROGRESS!
- Year 2020: 🎄 DONE! All done in Python here: [advent/year2020](advent/year2020)
- Year 2019: ❄️ On ice. On day 2.
- Year 2018: ❄️ On ice. On day 6.
- Year 2017: ❄️ On ice. On day 7.
  - Days 1-5 in [Crystal](https://crystal-lang.org/)
- Year 2016: ❄️ On ice. On day 20.
  - Days 1-7 and day 19 in Python here: [advent/year2016](advent/year2016)
  - Days 8-18 in Java: [github.com/valbaca/advent](https://github.com/valbaca/advent)
- Year 2015: 🎄 DONE! 
  - Days 1-19 in Go: [github.com/valbaca/AdventOfCode2015-Go](https://github.com/valbaca/AdventOfCode2015-Go)
  - Days 19-22 in Python here: [advent/year2015](advent/year2015)
  - Again in Clojure, to learn Clojure: [github.com/valbaca/advent](https://github.com/valbaca/advent)





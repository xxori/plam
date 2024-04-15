# plam

Simple tree-walking interpreter with a C-like syntax.

Python implementation of a slightly modified version of the language from Crafting Interpreters. I'll probably make some changes once I finish this part of the book, perhaps to make it follow more functional style i.e. pattern matching, a type system, etc..

After I finish the simple tree-walking interpreter, I plan to implement the bytecode VM from the book using Zig and then research and play around with type systems.

Currently implemented:
- Arithmetic operators with runtime type checking
- Number and string literals
- Global variable declarations and assignment
- Simple REPL and file running
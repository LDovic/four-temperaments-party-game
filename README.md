Published under MIT license:

Copyright (c)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

End license.

This is a game based on the <a href="https://en.wikipedia.org/wiki/Four_temperaments" target="_blank">Hippocratic four temperaments personality model</a>. The aim of the game is to throw a successful party with a mix of the four personalities outlined by the model.

Dependencies: pygame, simpleaudio, wavinfo

- pygame - important: pip install pygame==2.0.0.dev6 (developer pygame version) if working with Python 3.8
The standard pygame will not work with <= Python 3.7
More info: https://pythonprogramming.altervista.org/how-to-install-pygame-in-python-3-8/

- simpleaudio - simpleaudio plays audio files

- wavinfo - wavinfo gets metadata from wav audiofiles

Built with pyinstaller
https://www.pyinstaller.org/

To build:
- Add dependencies to main.spec
- Terminal command: pyinstaller --onedir --noupx main.spec (from same dist as main.spec)

Executable location is dist/main/main

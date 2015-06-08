# spaceship
Python terminal utility for chat and streaming files across two Linux machines on the same network.

##Installation

To install the latest stable release with [pip](https://pip.pypa.io/en/stable/)
```
$ pip install spaceship
```

You can also install the development version (may have bugs):
```
$ pip install git+git://github.com/antoan-angelov/spaceship.git#egg=spaceship
```

##How to use

You must have two Linux machines running on the same network.

On the first one run:
```
$ echo omg spaceship! | spaceship
```

On the second one run:
```
$ spaceship
```

This way the two machines pair and the second one receives `omg spaceship!`

You can also name the channel like so:
```
$ echo omg named channel! | spaceship --channel Enterprise
```

That way, another machine can only receive data if it runs `spaceship` with the same channel name:
```
$ spaceship --channel Enterprise
```

##File streaming

The above example barely scratched the surface.

Let's say you want to stream a video from machine 1 to machine 2.

On machine 1 run:
```
$ spaceship < myvideo.mp4
```

And on machine 2:
```
$ spaceship | mplayer -
```

That way the video will be streamed from machine 1 straight to [mplayer](https://www.mplayerhq.hu/) on machine 2. 
This can be achieved with any player that supports streaming to stdin.

##Chat
Two machines can also send messages to each other.

Both machines must either run:
```
$ spaceship chat
```

or with a named channel:
```
$ spaceship chat --channel Spock
```

When one of the machines writes a message, it gets sent to the other machine.

##License
```
The MIT License (MIT)

Copyright (c) 2015 Antoan Angelov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

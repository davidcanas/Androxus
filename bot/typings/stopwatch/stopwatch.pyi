"""
MIT License

Copyright (c) 2018 Free TNT

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
"""
from __future__ import annotations

from typing import Optional


class Stopwatch:
    _start: float
    _end: Optional[float]

    def __init__(self) -> None:
        ...

    @property
    def duration(self) -> float:
        """
        The duration of this stopwatch since start or start to end if this
        stopwatch has stopped.

        Returns:
            float: The duration of the stopwatch in seconds.

        """
        ...

    @property
    def running(self) -> bool:
        """
        Check if the stopwatch is running or not.

        Returns:
            bool: True if the stopwatch is running, False if stopped.

        """
        ...

    def restart(self) -> Stopwatch:
        """
        Reset and start the stopwatch.

        Returns:
            Stopwatch: The restarted stopwatch.

        """
        ...

    def reset(self) -> Stopwatch:
        """
        Resets the Stopwatch to 0 duration.

        Returns:
            Stopwatch: The resetted stopwatch.

        """
        ...

    def start(self) -> Stopwatch:
        """
        Starts the stopwatch.

        Returns:
            Stopwatch: The started stopwatch.

        """
        ...

    def stop(self) -> Stopwatch:
        """
        Stops the stopwatch, freezing the duration.

        Returns:
            Stopwatch: The stopped stopwatch.

        """
        ...

    def __str__(self) -> str:
        ...

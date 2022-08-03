from __future__ import annotations


__all__ = ['Fmt']


class Fmt(object):

    @staticmethod
    def float(_: int, cs: str) -> list[float]:
        return list(map(float, cs.split()))
# -*- coding: utf-8 -*-
from typing import Dict


def _get_params(params: Dict, *exclude) -> Dict:
    check = lambda k, v: v is not None and k[0].isalpha() and k not in exclude
    return {k: v for k, v in params.items() if check(k, v) and k != 'self'}


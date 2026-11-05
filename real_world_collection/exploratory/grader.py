"""Strict JSON outcome grading. Numeric absolute tolerance 1e-6 in requested units."""
import json
import math

def parse(text):
    def pairs(items):
        d = {}
        for k, v in items:
            if k in d:
                raise ValueError('duplicate key')
            d[k] = v
        return d
    def bad_constant(s):
        raise ValueError('nonfinite number')
    return json.loads(text, object_pairs_hook=pairs, parse_constant=bad_constant)

def grade(text, reference):
    try:
        answer = parse(text)
    except (ValueError, TypeError, RecursionError):
        return dict(passed=False, score=0.0, fields={}, error='invalid JSON')
    if not isinstance(answer, dict) or set(answer) != set(reference):
        return dict(passed=False, score=0.0, fields={}, error='exact key set required')
    fields = {}
    for k, expected in reference.items():
        value = answer[k]
        if expected is None:
            ok = value is None
        elif isinstance(expected, bool):
            ok = type(value) is bool and value is expected
        elif isinstance(expected, (int, float)):
            try:
                ok = type(value) in (int, float) and math.isfinite(value) and abs(value-expected) <= 1e-6
            except OverflowError:
                ok = False
        else:
            ok = type(value) is type(expected) and value == expected
        fields[k] = ok
    return dict(passed=all(fields.values()), score=sum(fields.values())/len(fields), fields=fields)

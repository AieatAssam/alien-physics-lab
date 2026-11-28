#!/bin/sh
# Judge scores behind the 2026-11-28 reviews (P-0036 narrowed, P-0037 replicated).
# Needs numpy (P-0036's model imports it). Setup used here:
#   python3 -m venv /tmp/lab-b-venv && /tmp/lab-b-venv/bin/pip install numpy
# Run from the repo root.
J=labs/lab-b/analysis/judge_generic_2026-11-24.py
PY=/tmp/lab-b-venv/bin/python

# P-0036 narrowed: all mixed-pair runs of lab-b with two particles, r0 in [3, 5], T <= 2
$PY -I $J "$PWD" papers/P-0036 '{"species":["A","B","C"],"r_range":[3,5],"max_particles":2}' \
  2026-11-18/r2/lab-b/013 2026-11-18/r2/lab-b/014 2026-11-18/r2/lab-b/015 \
  2026-11-18/r3/lab-b/009 2026-11-18/r3/lab-b/010 2026-11-18/r3/lab-b/011 \
  2026-11-18/r3/lab-b/012 2026-11-18/r3/lab-b/013 2026-11-18/r3/lab-b/014 \
  2026-11-18/r3/lab-b/015 2026-11-18/r3/lab-b/016 \
  2026-11-22/r1/lab-b/002 2026-11-22/r1/lab-b/003 2026-11-22/r2/lab-b/006 \
  2026-11-22/r2/lab-b/007 2026-11-22/r2/lab-b/009 2026-11-22/r3/lab-b/003 \
  2026-11-23/r3/lab-b/001 2026-11-25/r2/lab-b/005 2026-11-25/r2/lab-b/006 \
  2026-11-28/r2/lab-b/001 2026-11-28/r2/lab-b/002 2026-11-28/r2/lab-b/003

# P-0037 replicated: review runs
$PY -I $J "$PWD" papers/P-0037 '{"species":["A"],"r_range":[3.5,9],"max_particles":2}' \
  2026-11-28/r2/lab-b/004 2026-11-28/r2/lab-b/005 2026-11-28/r2/lab-b/006

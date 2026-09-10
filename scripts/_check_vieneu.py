#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiểm tra API VieNeu v3 Turbo - chạy trực tiếp để xem preset voices."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from vieneu import Vieneu

v = Vieneu(mode="v3turbo")
print(f"Sample rate: {v.sample_rate}")
presets = v.list_preset_voices()
print(f"Total presets: {len(presets)}")
for p in presets:
    print(f"  - {p}")

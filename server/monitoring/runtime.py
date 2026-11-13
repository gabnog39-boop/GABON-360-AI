"""Shared process-level instances for monitoring and central APIs.

A single monitor instance prevents alert and situation helpers from keeping
separate in-memory views during the same application process.
"""
from .continuous_monitor import ContinuousMonitor

monitor = ContinuousMonitor()

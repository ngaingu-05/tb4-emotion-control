"""Bounded, edge-triggered emotion behaviors, independent of ROS."""
import math


# label: linear velocity (m/s), angular velocity (rad/s), action duration (s)
ACTIONS = {
    'happy': (0.10, 0.30, 4.0),
    'sad': (0.10, -0.30, 4.0),
    'angry': (-0.08, 0.0, 1.5),
    'surprise': (0.0, 0.50, 2.0 * math.pi / 0.50),
    'fear': (0.08, 0.0, 1.5),
}
EMOTIONS = frozenset((*ACTIONS, 'neutral'))


class EmotionController:
    """Require stable labels and trigger only once per emotion transition."""

    def __init__(self, stable_frames=3):
        self.stable_frames = stable_frames
        self.candidate = None
        self.count = 0
        self.current = None
        self.action = None
        self.action_started = 0.0

    def observe(self, emotion, now):
        if emotion not in EMOTIONS:
            self.candidate, self.count = None, 0
            self.current, self.action = None, None
            return
        if emotion == self.candidate:
            self.count += 1
        else:
            self.candidate, self.count = emotion, 1
        if self.count < self.stable_frames or emotion == self.current:
            return
        self.current = emotion
        if emotion == 'neutral':
            self.action = None
        else:
            self.action = emotion
            self.action_started = now

    def velocity(self, now):
        if self.action is None:
            return 0.0, 0.0
        linear, angular, duration = ACTIONS[self.action]
        if now - self.action_started >= duration:
            self.action = None
            return 0.0, 0.0
        return linear, angular

    def lost(self):
        self.candidate, self.count = None, 0
        self.current, self.action = None, None

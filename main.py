from example.TestActivity2 import TestActivity2
from openparticle.api.activity.activity import ActivityManager

if __name__ == '__main__':
    manager = ActivityManager()
    # manager.add(TestActivity())
    manager.add(TestActivity2())
    manager.run()
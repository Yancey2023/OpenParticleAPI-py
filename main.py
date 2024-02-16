from example.TestActivity import TestActivity
from openparticle.api.activity.activity import ActivityManager

manager = ActivityManager()
manager.add(TestActivity())
manager.run()

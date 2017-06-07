import os
import shutil
from com.flyme.anranalyser.mainstate.Basestate import Basestate


class Sleeping(Basestate):
    def __init__(self, anrobj):
        Basestate.__init__(self, anrobj)

    def generate_bug_and_undetermined_if_needed(self, bug, undetermined,
                                                nonbug):
        Basestate.generate_bug(self, bug)

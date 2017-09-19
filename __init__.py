import sys
import datetime

old_out = sys.stdout


class St_ampe_dOut:
    """Stamped stdout."""

    nl = True

    def write(self, x):
        """Write function overloaded."""
        if x == '\n':
            old_out.write(x)
            self.nl = True
        elif self.nl:
            old_out.write('%s> %s' % (str(datetime.now()), x))
            self.nl = False
        else:
            old_out.write(x)

sys.stdout = St_ampe_dOut()
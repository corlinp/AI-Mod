import os, sys
"""

Contains random utilities for AI Mod

"""

def combine_reports_max(*args):
    # if isinstance(args[0], list):
    #     args = args[0]
    master_dict = {'notes': []}
    for dic in args:
        for k, v in dic.items():
            if k in master_dict:
                if k == 'notes':
                    for note in v:
                        if note not in master_dict['notes']:
                            master_dict['notes'].append(note)
                else:
                    master_dict[k] = max(v, master_dict[k])
            else:
                master_dict[k] = v

    return master_dict

# Lower bound of Wilson score confidence interval for a Bernoulli parameter
# This is for things like, likelihood that a user is a troll given this many troll comments and this many non-troll comments
def confidence(ups, downs):
    n = ups + downs
    if n == 0:
        return 0
    z = 1.90 #1.44 = 85%, 1.96 = 95%
    phat = float(ups) / n
    return ((phat + z*z/(2*n) - z * ((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n))**0.5



# the absolute path of AI Mod. Good for working with files.
def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")

def module_path():
    if we_are_frozen():
        out = str(os.path.dirname(sys.executable))
    out = str(os.path.dirname(__file__))
    out = out.replace('\\', '/')
    # Remove the utils part
    return '/'.join(out.split('/')[:-2])

root_path = module_path() + '/'

if __name__ == "__main__":
    print(root_path)

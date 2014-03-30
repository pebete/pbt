"""The setup plugin: when the meta-problem counter reaches a high level"""
import pbt
import os


def writeln(file, line=""):
    "Pascal's turning in its grave."
    file.write(line)
    file.write(os.linesep)


@pbt.command(name="setup")
def main(ctx, args, p):
    """Generates a valid setup.py file.
    It uses the info found in project.pbt."""

    # NOTE: yes, short names, 'cause I'm gonna write them a gazillion times
    f = open('setup.py', 'w+')
    s = p.settings

    # TODO: support other major versions
    writeln(f, "#! /usr/bin/env python3")
    writeln(f, "from distutils.core import setup")
    writeln(f)
    writeln(f, "setup(")

    # lazy, me?
    def kv(k, v):
        writeln(f, "    %s='%s'," % (k, v))

    def kvs(k, vs):
        writeln(f, "    %s=%s," % (k, vs))

    kv('name', p.name)
    kv('version', p.version)
    kv('description', p.description)
    # TODO: author
    kv('url', p.url)
    kvs('packages', s.packages)
    # TODO: run the plugin that generates the binary from the entry point
    kvs('scripts', s.scripts)
    kv('license', p.license['name'])
    # TODO: classifiers

    writeln(f, "    )")
    f.close()

    print("setup.py file written.")

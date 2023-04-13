from __future__ import annotations

import os
import os.path
from glob import glob

import click
import pkg_resources
from tutor import hooks

from .__about__ import __version__

########################################
# CONFIGURATION
########################################

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Add your new settings that have default values here.
        # Each new setting is a pair: (setting_name, default_value).
        # Prefix your setting names with 'MYPLUGIN_'.
        ("MYPLUGIN_VERSION", __version__),
    ]
)

config = {
    "defaults": {
        "COURSES_MFE_APP":{
            "name": "courses",
            "repository": "https://github.com/ahmed-arb/frontend-app-courses.git",
            "port": 2010,
        }
    },
}

MY_MFES = [
    {
        "name": "courses",
        "tag":  "ahmedkhalid19/course-mfe-dev"
    }
]

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"MFE_{key}", value) for key, value in config.get("defaults", {}).items()]
)

for mfe in MY_MFES:
    name = f"{mfe['name']}-dev"
    tag = mfe['tag']
    hooks.Filters.IMAGES_BUILD.add_item(
        (
            name,
            ("plugins", "mfe", "build", "mfe"),
            tag,
            (f"--target={mfe}-dev",),
        )
    )
    hooks.Filters.IMAGES_PULL.add_item((name, tag))
    hooks.Filters.IMAGES_PUSH.add_item((name, tag))




########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        pkg_resources.resource_filename("tutormyplugin", "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
    # For example, ``tutormyplugin/templates/myplugin/build``
    # will be rendered to ``$(tutor config printroot)/env/plugins/myplugin/build``.
    [
        ("myplugin/build", "plugins"),
        ("myplugin/apps", "plugins"),
    ],
)


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutormyplugin/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutormyplugin", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))


########################################
# CUSTOM JOBS (a.k.a. "do-commands")
########################################

# A job is a set of tasks, each of which run inside a certain container.
# Jobs are invoked using the `do` command, for example: `tutor local do importdemocourse`.
# A few jobs are built in to Tutor, such as `init` and `createuser`.
# You can also add your own custom jobs:

# To add a custom job, define a Click command that returns a list of tasks,
# where each task is a pair in the form ("<service>", "<shell_command>").
# For example:
### @click.command()
### @click.option("-n", "--name", default="plugin developer")
### def say_hi(name: str) -> list[tuple[str, str]]:
###     """
###     An example job that just prints 'hello' from within both LMS and CMS.
###     """
###     return [
###         ("lms", f"echo 'Hello from LMS, {name}!'"),
###         ("cms", f"echo 'Hello from CMS, {name}!'"),
###     ]


# Then, add the command function to CLI_DO_COMMANDS:
## hooks.Filters.CLI_DO_COMMANDS.add_item(say_hi)

# Now, you can run your job like this:
#   $ tutor local do say-hi --name="John Doe"


#######################################
# CUSTOM CLI COMMANDS
#######################################

# Your plugin can also add custom commands directly to the Tutor CLI.
# These commands are run directly on the user's host computer
# (unlike jobs, which are run in containers).

# To define a command group for your plugin, you would define a Click
# group and then add it to CLI_COMMANDS:


### @click.group()
### def myplugin() -> None:
###     pass


### hooks.Filters.CLI_COMMANDS.add_item(myplugin)


# Then, you would add subcommands directly to the Click group, for example:


### @myplugin.command()
### def example_command() -> None:
###     """
###     This is helptext for an example command.
###     """
###     print("You've run an example command.")


# This would allow you to run:
#   $ tutor myplugin example-command

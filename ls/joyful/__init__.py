# ------------------------------------------------------------------------------
# Joyful initialization
# ------------------------------------------------------------------------------
name = "joyful"
try:
    from ._version import version as __version__
except ImportError:  # pragma: no cover
    __version__ = '0.1'

#default_app_config = 'ls.joyful.apps.JoyfulAppConfig'

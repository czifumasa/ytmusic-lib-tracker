import sys
import traceback
from timeit import default_timer as timer

from ytmusiclibtracker.common import log
from ytmusiclibtracker.create_library_changelog import create_library_changelog
from ytmusiclibtracker.export_playlists import export_to_file
from ytmusiclibtracker.import_playlists import import_from_file


def changelog():
    create_library_changelog()


def export():
    export_to_file()


def reverse():
    import_from_file()


def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, None)
    input('\nPress Enter to exit...')
    sys.exit(-1)


def main():
    sys.excepthook = show_exception_and_exit
    log('Welcome in YTMusic-Lib-Tracker!\n')
    start = timer()
    export_to_file()
    create_library_changelog()
    end = timer()
    log('END')
    log('-----------------------------------------------------------------------', True)
    log('All tasks has been completed. Time: ' + str(end - start) + ' sec.', True)
    input("Press Enter to continue...")
    sys.exit()


if __name__ == "__main__":
    main()

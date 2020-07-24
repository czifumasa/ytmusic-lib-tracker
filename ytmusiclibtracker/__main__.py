from ytmusiclibtracker.create_library_changelog import create_library_changelog
from ytmusiclibtracker.export_playlists import export_to_csv
from ytmusiclibtracker.list_duplicates import list_duplicates


def changelog():
    create_library_changelog()


def export():
    export_to_csv()


def duplicates():
    list_duplicates()


if __name__ == "__main__":
    changelog()

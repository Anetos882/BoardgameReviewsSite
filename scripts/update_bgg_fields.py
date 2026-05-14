import csv
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = PROJECT_ROOT / "boardgames_ranks.csv"
GAMES_DIR = PROJECT_ROOT / "src" / "content" / "games"

FIELDS_MAP = {
    "title": "name",
    "year": "yearpublished",
    "bgg_rank": "rank",
    "bayes_rating": "bayesaverage",
    "average_rating": "average",
    "users_rated": "usersrated",
}


def quote_yaml_string(value: str) -> str:
    value = value.replace('"', '\\"')
    return f'"{value}"'


def format_value(field: str, value: str) -> str:
    if value is None or value == "":
        return ""

    if field == "title":
        return quote_yaml_string(value)

    if field in {"year", "bgg_rank", "users_rated"}:
        return str(int(float(value)))

    if field in {"bayes_rating", "average_rating"}:
        return str(round(float(value), 1))

    return str(value)


def load_bgg_data():
    data = {}

    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            bgg_id = str(row["id"]).strip()
            data[bgg_id] = row

    return data


def update_frontmatter(text: str, bgg_data: dict, file_path: Path) -> tuple[str, bool]:
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, flags=re.DOTALL)

    if not match:
        print(f"Пропущен файл без frontmatter: {file_path}")
        return text, False

    frontmatter = match.group(1)
    body = match.group(2)

    bgg_id_match = re.search(r"^bgg_id:\s*(\d+)\s*$", frontmatter, flags=re.MULTILINE)

    if not bgg_id_match:
        print(f"Нет bgg_id: {file_path}")
        return text, False

    bgg_id = bgg_id_match.group(1)

    if bgg_id not in bgg_data:
        print(f"Не найден bgg_id {bgg_id} в CSV: {file_path}")
        return text, False

    row = bgg_data[bgg_id]
    updated = frontmatter

    for md_field, csv_field in FIELDS_MAP.items():
        new_value = format_value(md_field, row[csv_field])
        pattern = rf"^{md_field}:\s*.*$"
        replacement = f"{md_field}: {new_value}"

        if re.search(pattern, updated, flags=re.MULTILINE):
            updated = re.sub(pattern, replacement, updated, flags=re.MULTILINE)
        else:
            updated += f"\n{replacement}"

    new_text = f"---\n{updated}\n---\n{body}"

    return new_text, new_text != text


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Не найден файл: {CSV_PATH}")

    if not GAMES_DIR.exists():
        raise FileNotFoundError(f"Не найдена папка: {GAMES_DIR}")

    bgg_data = load_bgg_data()

    updated_count = 0

    for file_path in sorted(GAMES_DIR.glob("*.md")):
        old_text = file_path.read_text(encoding="utf-8")
        new_text, changed = update_frontmatter(old_text, bgg_data, file_path)

        if changed:
            file_path.write_text(new_text, encoding="utf-8")
            updated_count += 1
            print(f"Обновлён: {file_path.name}")

    print(f"\nГотово. Обновлено файлов: {updated_count}")


if __name__ == "__main__":
    main()

# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "elf",
#     "tabulate"
# ]
# ///

from datetime import datetime

from elf import OutputFormat, get_user_status
from tabulate import tabulate

current_year = datetime.now().year
years = list(range(2015, current_year + 1))

# Fetch progress via elf
progress_by_year: dict[int, dict[int, int]] = {}
for year in years:
    try:
        status = get_user_status(year, fmt=OutputFormat.MODEL)
    except ValueError as e:
        if "Invalid year" in str(e):
            continue
        else:
            raise
    progress_by_year[year] = {day.day: day.stars for day in status.days}

# Create table columns
headers = ["**Year**", "🌟"] + [f"**{d}**" for d in range(1, 26)]
table_data = []

# Add table rows
for year in sorted(progress_by_year.keys()):
    year_progress = progress_by_year.get(year, {})
    year_stars_available = len(year_progress) * 2
    year_stars_obtained = sum(year_progress.values())
    row = [f"**{year}**"]
    if year_stars_obtained == year_stars_available:
        row.append(f"**{year_stars_obtained}/{year_stars_available}**&nbsp;🌟")
    else:
        row.append(f"{year_stars_obtained}/{year_stars_available}")
    for day in range(1, 26):
        stars = year_progress.get(day, None)
        if stars is None:
            icon = "⬛"
        elif stars == 0:
            icon = "⬜"
        elif stars == 1:
            icon = "🟨"
        elif stars == 2:
            icon = "🟩"
        else:
            assert False, "unexpected number of stars"
        row.append(icon)

    table_data.append(row)

timestamp = datetime.now().strftime("%Y-%m-%d")

# Generate markdown table
markdown_table = tabulate(table_data, headers=headers, tablefmt="github")

# Update README.md
readme_path = "README.md"
with open(readme_path, "r") as f:
    readme_content = f.read()

# Find markers and replace content between them
start_marker = "<!-- PROGRESS_START -->"
end_marker = "<!-- PROGRESS_END -->"

if start_marker in readme_content and end_marker in readme_content:
    before_start = readme_content.split(start_marker)[0]
    after_end = readme_content.split(end_marker)[1]

    new_progress = (
        f"{start_marker}\nUpdated {timestamp}.\n\n{markdown_table}\n{end_marker}"
    )
    new_content = f"{before_start}{new_progress}{after_end}"

    with open(readme_path, "w") as f:
        f.write(new_content)

    print(f"README.md updated with progress as of {timestamp}.")
else:
    print("Warning: Could not find progress markers in README.md")

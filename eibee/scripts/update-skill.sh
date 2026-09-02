#!/usr/bin/env bash
set -euo pipefail

ref="${1:-main}"
skill_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repository="coconut4210/eibee-content-factory"
raw_base="https://raw.githubusercontent.com/${repository}/${ref}/eibee"
temporary_skill="$(mktemp)"
temporary_version="$(mktemp)"

cleanup() {
  rm -f "$temporary_skill" "$temporary_version"
}
trap cleanup EXIT

curl -fsSL "${raw_base}/SKILL.md" -o "$temporary_skill"
curl -fsSL "${raw_base}/VERSION" -o "$temporary_version"

if ! grep -qx 'name: eibee' "$temporary_skill"; then
  echo "Downloaded file is not the eibee Skill. Nothing was changed." >&2
  exit 1
fi

new_version="$(tr -d '\r\n' < "$temporary_version")"
if ! [[ "$new_version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Downloaded version is invalid. Nothing was changed." >&2
  exit 1
fi

cp "$skill_root/SKILL.md" "$skill_root/SKILL.md.bak"
cp "$temporary_skill" "$skill_root/SKILL.md"
printf '%s' "$new_version" > "$skill_root/VERSION"
echo "eibee updated to ${new_version} from ${ref}. Backup: ${skill_root}/SKILL.md.bak"

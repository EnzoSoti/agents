#!/usr/bin/env bash
# Detect stack, tooling, and git state. Read-only. Usage: scripts/preflight.sh [dir]
set -u
cd "${1:-.}" || exit 1
echo "== PREFLIGHT: $(pwd) =="
echo
echo "-- Git --"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
  echo "commit: $(git rev-parse --short HEAD 2>/dev/null)"
  n=$(git status --porcelain | wc -l | tr -d ' ')
  echo "uncommitted changes: $n"
  [ "$n" -gt 0 ] && git status --short | head -20
  echo "worktrees:"; git worktree list 2>/dev/null | sed 's/^/  /'
else
  echo "not a git repository"
fi
echo
echo "-- Stack detection --"
has() { [ -e "$1" ] && echo "  found: $1"; }
for f in package.json pnpm-lock.yaml yarn.lock package-lock.json tsconfig.json \
         pyproject.toml requirements.txt setup.py Pipfile poetry.lock \
         go.mod Cargo.toml pom.xml build.gradle build.gradle.kts \
         Gemfile composer.json mix.exs *.csproj *.sln \
         Dockerfile docker-compose.yml docker-compose.yaml Makefile \
         .github/workflows .gitlab-ci.yml Jenkinsfile \
         prisma/schema.prisma alembic.ini migrations db/migrate \
         AGENTS.md CONTRIBUTING.md README.md .editorconfig \
         .eslintrc* .prettierrc* ruff.toml .flake8 .golangci.yml; do
  for m in $f; do has "$m"; done
done
echo
echo "-- Likely commands --"
if [ -f package.json ]; then
  echo "  node scripts:"
  python3 - << 'PY' 2>/dev/null
import json
try:
    s=json.load(open("package.json")).get("scripts",{})
    for k in ("install","build","lint","typecheck","test","test:unit","test:e2e","dev","start"):
        if k in s: print(f"    npm run {k}  ->  {s[k]}")
except Exception as e: print("    (could not parse package.json)")
PY
fi
[ -f pyproject.toml ] || [ -f requirements.txt ] && echo "  python: pytest / ruff / mypy (check config)"
if ls ./*.sln ./*.csproj >/dev/null 2>&1 || [ -n "$(find . -maxdepth 3 -name '*.sln' -o -maxdepth 3 -name '*.csproj' 2>/dev/null | head -1)" ]; then
  echo "  dotnet: dotnet restore && dotnet build && dotnet test  (EF: dotnet ef migrations list)"
fi
for d in frontend client web ui src/frontend; do [ -f "$d/package.json" ] && echo "  frontend folder: $d  -> scripts/verify.sh $d"; done
for d in backend api server src/backend; do [ -n "$(find "$d" -maxdepth 3 \( -name '*.sln' -o -name '*.csproj' \) 2>/dev/null | head -1)" ] && echo "  backend folder:  $d  -> scripts/verify.sh $d"; done
[ -f go.mod ] && echo "  go: go build ./... && go vet ./... && go test ./..."
[ -f Cargo.toml ] && echo "  rust: cargo build && cargo clippy && cargo test"
[ -f pom.xml ] && echo "  maven: mvn -q verify"
[ -f build.gradle ] || [ -f build.gradle.kts ] && echo "  gradle: ./gradlew build test"
[ -f Makefile ] && { echo "  make targets:"; grep -E '^[a-zA-Z0-9_-]+:' Makefile | cut -d: -f1 | head -15 | sed 's/^/    /'; }
echo
echo "-- Tools on PATH --"
for t in git node npm pnpm yarn python3 pip go cargo mvn gradle docker psql mysql sqlite3 rg; do
  command -v "$t" >/dev/null 2>&1 && echo "  $t: $(command -v $t)"
done
echo
echo "-- Agent coordination --"
[ -d .agent ] && { echo "  .agent/ present"; ls .agent 2>/dev/null | sed 's/^/    /'; } || echo "  no .agent/ directory (single-agent mode)"
echo
echo "Next: record BASELINE (run verify.sh before changing anything)."

#!/usr/bin/env bash
# Auto-detect and run lint / typecheck / build / tests.
# Usage: scripts/verify.sh [dir] [--fast]
#   dir: subfolder to verify (e.g. frontend, backend). Default: current directory.
# Exit non-zero if any detected step fails; exit 2 if no project type was detected.
FAST=0; DIR="."
for a in "$@"; do [ "$a" = "--fast" ] && FAST=1 || DIR="$a"; done
cd "$DIR" || { echo "cannot cd to $DIR"; exit 2; }
echo "verifying in: $(pwd)"
NAMES=(); RESULTS=()
run() { local name="$1"; shift; echo; echo ">>> $name: $*"
  if "$@"; then NAMES+=("$name"); RESULTS+=("PASS"); else NAMES+=("$name"); RESULTS+=("FAIL"); fi; }
npm_has() { python3 -c "import json,sys;sys.exit(0 if '$1' in json.load(open('package.json')).get('scripts',{}) else 1)" 2>/dev/null; }

# Node / React
if [ -f package.json ]; then
  pm=npm; [ -f pnpm-lock.yaml ] && pm=pnpm; [ -f yarn.lock ] && pm=yarn
  [ -d node_modules ] || echo "NOTE: node_modules missing - run '$pm install' first"
  npm_has lint && run "node:lint" $pm run lint
  if npm_has typecheck; then run "node:typecheck" $pm run typecheck
  elif [ -f tsconfig.json ] && command -v npx >/dev/null; then run "node:tsc" npx --no-install tsc --noEmit; fi
  npm_has test && run "node:test" env CI=true $pm run test
  [ $FAST -eq 0 ] && npm_has build && run "node:build" $pm run build
fi
# .NET
if ls ./*.sln ./*.slnx ./*.csproj >/dev/null 2>&1 || [ -n "$(find . -maxdepth 3 -name '*.sln' -o -maxdepth 3 -name '*.csproj' 2>/dev/null | head -1)" ]; then
  if command -v dotnet >/dev/null; then
    run "dotnet:build" dotnet build --nologo -v q
    [ $FAST -eq 0 ] && run "dotnet:format" dotnet format --verify-no-changes --no-restore -v q
    run "dotnet:test" dotnet test --nologo --no-build -v q
  else echo "NOTE: .NET project detected but 'dotnet' CLI not on PATH"; fi
fi
# Python
if [ -f pyproject.toml ] || [ -f requirements.txt ] || [ -f setup.py ]; then
  command -v ruff >/dev/null && run "py:ruff" ruff check .
  command -v mypy >/dev/null && [ $FAST -eq 0 ] && run "py:mypy" mypy .
  command -v pytest >/dev/null && run "py:pytest" pytest -q
fi
# Go / Rust / Java
[ -f go.mod ] && { run "go:vet" go vet ./...; run "go:test" go test ./...; }
[ -f Cargo.toml ] && command -v cargo >/dev/null && { run "rust:clippy" cargo clippy -q; run "rust:test" cargo test -q; }
[ -f pom.xml ] && run "maven:verify" mvn -q verify
[ -f gradlew ] && run "gradle:build" ./gradlew build

echo; echo "== VERIFY SUMMARY =="
if [ ${#NAMES[@]} -eq 0 ]; then
  echo "No known project type detected here. Try a subfolder (e.g. verify.sh frontend) or run the project's own commands and report them."
  exit 2
fi
fail=0
for i in "${!NAMES[@]}"; do printf '  %-18s %s\n' "${NAMES[$i]}" "${RESULTS[$i]}"; [ "${RESULTS[$i]}" = FAIL ] && fail=1; done
[ $fail -eq 0 ] && echo "ALL PASS" || echo "FAILURES PRESENT (compare with baseline before blaming your change)"
exit $fail

for f in gemini-code-*.py; do
  target=$(head -n 2 "$f" | sed -n 's|^# *models/binding/membrane/||p' | tr -d '[:space:]')
  [[ -n "$target" ]] && mv -v "$f" "$target"
done

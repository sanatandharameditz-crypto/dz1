# DuelZone Bundler — PowerShell
# Embeds ALL external <script src="..."> tags inline into each HTML file

$BASE = "c:\Users\Aashish\Desktop\DUELZONE DESIGN"

$GAME_HTMLS = @(
  "pong.html","pingpong.html","snake.html","airhockey.html",
  "tanks.html","bomberman.html","minesweeper.html","sudoku.html",
  "memory.html","connect4.html","game2048.html","battleship.html",
  "spacedodge.html","starcatcher.html","reaction.html","wordduel.html",
  "territory.html","darts.html","blackjack.html","pool.html","checkers.html"
)

function Embed-Scripts($htmlFile) {
  $html = [System.IO.File]::ReadAllText($htmlFile, [System.Text.Encoding]::UTF8)
  
  # Match <script src="..."></script> but not http(s):// ones
  $pattern = '<script\s+src=[''"](?!https?://)([^''"]+)[''"]><\/script>'
  $regex = [regex]$pattern
  
  $result = $regex.Replace($html, {
    param($match)
    $src = $match.Groups[1].Value
    $jsPath = Join-Path $BASE ($src -replace '/', '\')
    if (Test-Path $jsPath) {
      $jsContent = [System.IO.File]::ReadAllText($jsPath, [System.Text.Encoding]::UTF8)
      Write-Host "    + Embedded: $src"
      return "<script>`n$jsContent`n</script>"
    } else {
      Write-Host "    ! Missing (kept external): $src"
      return $match.Value
    }
  })
  
  [System.IO.File]::WriteAllText($htmlFile, $result, [System.Text.Encoding]::UTF8)
  Write-Host "  OK: $(Split-Path $htmlFile -Leaf)"
}

Write-Host "=== DuelZone Bundler ==="
foreach ($name in $GAME_HTMLS) {
  $fullPath = Join-Path $BASE $name
  if (Test-Path $fullPath) {
    Write-Host "`nProcessing: $name"
    Embed-Scripts $fullPath
  } else {
    Write-Host "SKIP (not found): $name"
  }
}

Write-Host "`n=== DONE! All game HTML files are now fully self-contained ==="

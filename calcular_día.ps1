param($p1)

#Componer fecha
if ($p1){
      $mydate = $p1
} else {
      $mydate = -join($(Get-Date -Format "dd-MM-yyyy"), ".", "txt")
}

if (Test-Path $mydate -PathType Leaf){
      python .\timem.py $mydate
} else {
      New-Item -Name $mydate -ItemType "file"
}
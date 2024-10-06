param($p1)
if ($p1){
      $mydate = $p1
} else {
      $mydate = -join($(Get-Date -Format "dd-MM-yyyy"), ".", "txt")
}
python .\timem.py $mydate
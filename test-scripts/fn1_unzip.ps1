$inFolder = "Z:\DataETL\FileCont1-mpd\test\0_in"
$outFolder = "Z:\DataETL\FileCont1-mpd\test\1_unzip"

#=== get ZIP folder content + extract to next dir
$zipFiles = Get-ChildItem -Path $inFolder -Recurse -File | Where-Object { $_.Extension -eq ".zip" } 
foreach($zipFile in $zipFiles) 
{ 
    Expand-Archive -Path $zipFile.FullName -DestinationPath $outFolder
}

$fileExtensions = @('.csv', '.xlsx', '.tsv', '.txt')
$files = Get-ChildItem -Path $inFolder -Recurse | Where-Object { $_.Extension -in $fileExtensions }

foreach($file in $files) 
{
    Copy-Item -Path $file.FullName -Destination $outFolder
}

Write-Host "files unzipped." -ForegroundColor Green
# keep .ps1+.bat in dir "C:\Users\r.unteregger\Documents"

$SourceFolder = "Z:\inbox"
$BackupFolder = "Z:\(databackup)\inbox_backup"
$AlreadyCopied = @{}

$Watcher = New-Object System.IO.FileSystemWatcher
$Watcher.Path = $SourceFolder
$Watcher.Filter = "*"
$Watcher.IncludeSubdirectories = $true
$Watcher.EnableRaisingEvents = $true

$MappedFiles = "Z:\QuickHMNY\data_in"
$BackupFiles = "Z:\(databackup)\files_backup"
$AlreadyCopied2 = @{}

$Watcher2 = New-Object System.IO.FileSystemWatcher
$Watcher2.Path = $MappedFiles
$Watcher2.Filter = "*"
$Watcher2.IncludeSubdirectories = $true
$Watcher2.EnableRaisingEvents = $true

# action to take when new file created
$action = {
    $path = $Event.SourceEventArgs.FullPath
    Copy-ItemIfNew -path $path
}

#===========================================
#=== BackupFunctions(inboxSourceFolder) ===
#=========================================

Function Copy-ItemIfNew {
    param ( [string]$path )

    # check if item is a subfolder
    if (Test-Path -Path $path -PathType Container) {
        $destPath = $path -replace [regex]::Escape($SourceFolder), $BackupFolder
        if (-not $AlreadyCopied.ContainsKey($destPath)) {
            # check if item already exists in BackupFolder
            if (-not (Test-Path -Path $destPath)) {
                Copy-Item -Path $path -Destination $destPath -Recurse
                $AlreadyCopied[$destPath] = $true
            }
        }
    }
}

# unregister existing event associated with NewFileCreated before moving on
$existingEvent = Get-EventSubscriber -SourceIdentifier NewFileCreated -ErrorAction SilentlyContinue
if ($existingEvent) {
    Unregister-Event -SubscriptionId $existingEvent.SubscriptionId
}

# register event for newly created files
Register-ObjectEvent -InputObject $Watcher -EventName Created -SourceIdentifier NewFileCreated -Action $action

# copy existing items when script is run if not already copied
Get-ChildItem -Path $SourceFolder -Recurse | ForEach-Object {
    Copy-ItemIfNew -path $_.FullName
}

#=====================================
#=== BackupFunctions(MappedFiles) ===
#===================================

Function Copy-ItemIfNew {
    param ( [string]$path2 )

    # check if item is a subfolder
    if (Test-Path -Path $path2 -PathType Container) {
        $destPath2 = $path2 -replace [regex]::Escape($MappedFiles), $BackupFiles
        if (-not $AlreadyCopied2.ContainsKey($destPath2)) {
            # check if item already exists in BackupFolder
            if (-not (Test-Path -Path $destPath2)) {
                Copy-Item -Path $path2 -Destination $destPath2 -Recurse
                $AlreadyCopied2[$destPath2] = $true
            }
        }
    }
}

# unregister existing event associated with NewFileCreated2 before moving on
$existingEvent = Get-EventSubscriber -SourceIdentifier NewFileCreated2 -ErrorAction SilentlyContinue
if ($existingEvent) {
    Unregister-Event -SubscriptionId $existingEvent.SubscriptionId
}

# register event for newly created files
Register-ObjectEvent -InputObject $Watcher2 -EventName Created -SourceIdentifier NewFileCreated2 -Action $action

# copy existing items when script is run if not already copied
Get-ChildItem -Path $MappedFiles -Recurse | ForEach-Object {
    Copy-ItemIfNew -path $_.FullName
}
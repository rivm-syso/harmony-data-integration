#=== checkOS=Windows?
if ([System.Environment]::OSVersion.Platform -ne 'Win32NT')
{
    Write-Host `n "ERROR: Intended to run on Windows only. Script exit."`n -ForegroundColor Red
    exit
}

#=========================================
#====== FunctionInputs/defintions ======
#=====================================

###param ( [string] $studyPrefix )

$scriptRoot = $PSScriptRoot #/script root-dir.
$initialDir = "Z:\DataETL\FileCont1-mpd\test\2.2_convert" #/dir.for selecting files
$outFolder = "Z:\DataETL\FileCont1-mpd\test\3_prefix" #/output-dir.


#=====================================
#====== MainFunction - GUI... ======
#=================================

#=== Load(Sys.Win.Forms)
[System.Reflection.Assembly]::LoadWithPartialName("System.Drawing") | Out-Null
[System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms") | Out-Null

#=== GUI(WindowsForm)
$inForm = New-Object System.Windows.Forms.Form
$inForm.Text = "Selecting files"
$inForm.Size = New-Object System.Drawing.Size(800,600)
$inForm.StartPosition = "CenterScreen"
$inForm.FormBorderStyle = [System.Windows.Forms.FormBorderStyle]::FixedSingle

#-------------------------------
#=== InputForm StudyPrefixes ===
#-------------------------------

#=== Load list of prefixes
$scriptPath = Join-Path -Path $scriptRoot\fn-inputs -ChildPath 'study-prefixes.ps1' 
.$scriptPath

#=== GUI(ComboBox)
$itemList1 = @($prefixList)
$CB1 = New-Object System.Windows.Forms.ComboBox
$CB1.Location = New-Object System.Drawing.Size(200,50)
$CB1.Size = New-Object System.Drawing.Size(400,40)
$CB1.Font = New-Object System.Drawing.Font("Segoe UI",12,[System.Drawing.FontStyle]::Regular)
$CB1.Text = "<select Study-Prefix from list>"
foreach($item in $itemList1)
{
    $CB1.Items.Add($item) | Out-Null
}

#=== GUI(Button-OK)
$BT1 = New-Object System.Windows.Forms.Button
$BT1.Location = New-Object System.Drawing.Size(300,450)
$BT1.Size = New-Object System.Drawing.Size(200,40)
$BT1.Font = New-Object System.Drawing.Font("Segoe UI",12,[System.Drawing.FontStyle]::Regular)
$BT1.Text = "Confirm"
$BT1.Add_Click({
    $inForm.DialogResult = [System.Windows.Forms.DialogResult]::OK
    $inForm.Close()
})

#=== GUI(add ElementsToForm)
$inForm.Controls.AddRange(@($CB1,$BT1))

#=== GUI(show WindowsForm)
$inForm.TopMost = $true
$inForm.Add_Shown({ 
    $inForm.Activate()
})
$showForm = $inForm.ShowDialog()

#==== checkIfChancelled
if ($showForm -ne [System.Windows.Forms.DialogResult]::OK) { exit }

#-----------------------------
#=== InputForm SelectFiles ===
#-----------------------------

#=== GUI(create OpenFileDialog)
$oFD = New-Object System.Windows.Forms.OpenFileDialog
$oFD.InitialDirectory = $initialDir
$oFD.Multiselect = $true

#=== GUI(show OpenFileDialog)
$showFD = $oFD.ShowDialog()

if ($showFD -eq [System.Windows.Forms.DialogResult]::OK)
{
    $selectedFiles = $oFD.FileNames
}

#==== checkIfChancelled
if ($showFD -ne [System.Windows.Forms.DialogResult]::OK) { exit }

#=============================================
#====== MainFunction - FileProcess... ======
#=========================================

#=== Prefix from InputForm
$studyPrefix = $CB1.SelectedItem

#=== create StudySubfolders + checkIfAlreadyExist
$subfolderPath = Join-Path -Path $outFolder -ChildPath $studyPrefix
if (-not (Test-Path -Path $subfolderPath -PathType Container)) 
{
    New-Item -Path $subfolderPath -ItemType Directory
}

#=== Load array of HeaderNames to find in files
$scriptPath = Join-Path -Path $scriptRoot\fn-inputs -ChildPath 'headername-patterns.ps1' 
.$scriptPath

#=== Suffix for multiple files per dataset
$suffixNr = 0

#=== scan HeaderNames(selectedFiles)->rename->copy
foreach ($file in $selectedFiles)
{
    $content = Get-Content -Path $file -First 2 #/first 2x rows

    $matches = 0 #/counter to track headername-matches

    if($content -match $regexImmun) {
        $midname = "immun_data"
        $matches++
    }
    if($content -match $regexDemog) {
        $midname = "demog_dim"
        $matches++
    }
    if($content -match $regexVaccin) {
        $midname = "vaccin_dim"
        $matches++
    }
    if($content -match $regexInfect) {
        $midname = "infect_dim"
        $matches++
    }

    #/check count of matches
    if($matches -gt 1) {
        $midname = "mixed_data"
    }
    elseif($matches -eq 0) {
        $midname = "other_tbl"
    }
    
    #/rename & copy to new subdir. 
    $suffixNr++
    $renameFile = $studyPrefix + "_" + $midname + "_" + $suffixNr + ".csv"
    Copy-Item -Path $file -Destination $subfolderPath\$renameFile
}
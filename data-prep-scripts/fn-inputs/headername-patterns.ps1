#=== Array of HeaderStrings to check
$stringsImmun = "anti_sval", "anti_ag", "MIA_CoV19_S", "IgG_S", "titer_Final"
$stringsDemog = "demo_age", "Age_Vacc_", "age_on_vac", "AGE"
$stringsVaccin = "vacdate", "Vacc_COVID_", "vaccinatie datum", "vacc_date_" 
$stringsInfect = "cov_01_2_", "positive_date", "Positive_Date", "Posdate_", "RI_"
#=== create RegEx patterns to check
$regexImmun = ($stringsImmun | ForEach-Object { [regex]::Escape($_) }) -join '|'
$regexDemog = ($stringsDemog | ForEach-Object { [regex]::Escape($_) }) -join '|'
$regexVaccin = ($stringsVaccin | ForEach-Object { [regex]::Escape($_) }) -join '|'
$regexInfect = ($stringsInfect | ForEach-Object { [regex]::Escape($_) }) -join '|'

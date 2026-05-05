#!powershell

# Copyright: (c) 2024, Chris Arceneaux <carcenea@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

param(
    [string]$state = "present",
    [string]$exclusion_type = "path",
    [string]$exclusions = ""
)

$ErrorActionPreference = "Stop"

try {
    $exclusionList = @()
    if ($exclusions -ne "") {
        $exclusionList = $exclusions -split ";"
    }

    $changed = $false

    $prefs = Get-MpPreference

    switch ($exclusion_type) {
        "path"      { $currentExclusions = @($prefs.ExclusionPath) }
        "process"   { $currentExclusions = @($prefs.ExclusionProcess) }
        "extension" { $currentExclusions = @($prefs.ExclusionExtension) }
    }

    if ($null -eq $currentExclusions) {
        $currentExclusions = @()
    }

    if ($state -eq "present") {
        foreach ($item in $exclusionList) {
            if ($currentExclusions -notcontains $item) {
                switch ($exclusion_type) {
                    "path"      { Add-MpPreference -ExclusionPath $item }
                    "process"   { Add-MpPreference -ExclusionProcess $item }
                    "extension" { Add-MpPreference -ExclusionExtension $item }
                }
                $changed = $true
            }
        }
    }
    elseif ($state -eq "absent") {
        foreach ($item in $exclusionList) {
            if ($currentExclusions -contains $item) {
                switch ($exclusion_type) {
                    "path"      { Remove-MpPreference -ExclusionPath $item }
                    "process"   { Remove-MpPreference -ExclusionProcess $item }
                    "extension" { Remove-MpPreference -ExclusionExtension $item }
                }
                $changed = $true
            }
        }
    }

    # Get final state of exclusions after changes
    $finalPrefs = Get-MpPreference

    switch ($exclusion_type) {
        "path"      { $finalExclusions = @($finalPrefs.ExclusionPath) }
        "process"   { $finalExclusions = @($finalPrefs.ExclusionProcess) }
        "extension" { $finalExclusions = @($finalPrefs.ExclusionExtension) }
    }

    if ($null -eq $finalExclusions) {
        $finalExclusions = @()
    }

    if ($changed) {
        $msg = "Exclusions have been updated."
    }
    else {
        $msg = "No changes required."
    }

    @{changed=$changed; msg=$msg; exclusions=$finalExclusions} | ConvertTo-Json -Compress
    exit 0
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}

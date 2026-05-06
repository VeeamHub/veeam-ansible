#!powershell

# Copyright: (c) 2024, Chris Arceneaux <carcenea@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#Requires -Module Ansible.ModuleUtils.Legacy

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$params = Parse-Args $args -supports_check_mode $false

$state           = Get-AnsibleParam -obj $params -name "state"          -type "str"  -default "present" -ValidateSet "present", "absent"
$exclusion_type  = Get-AnsibleParam -obj $params -name "exclusion_type" -type "str"  -failifempty $true  -ValidateSet "path", "process", "extension"
$exclusion_value = Get-AnsibleParam -obj $params -name "exclusions"     -type "list" -failifempty $true

$result = @{
    changed = $false
    changes = [System.Collections.Generic.List[string]]::new()
}

Try {
    if ($exclusion_type -eq "path") {
        $current = (Get-MpPreference).ExclusionPath
    } elseif ($exclusion_type -eq "process") {
        $current = (Get-MpPreference).ExclusionProcess
    } elseif ($exclusion_type -eq "extension") {
        $current = (Get-MpPreference).ExclusionExtension
    }

    foreach ($value in $exclusion_value) {
        $exists = $current -contains $value

        if ($state -eq "present" -and -not $exists) {
            if ($exclusion_type -eq "path") {
                Add-MpPreference -ExclusionPath $value -ErrorAction Stop
            } elseif ($exclusion_type -eq "process") {
                Add-MpPreference -ExclusionProcess $value -ErrorAction Stop
            } elseif ($exclusion_type -eq "extension") {
                Add-MpPreference -ExclusionExtension $value -ErrorAction Stop
            }
            $result.changes.Add("Added $exclusion_type exclusion: $value")
            $result.changed = $true
        } elseif ($state -eq "absent" -and $exists) {
            if ($exclusion_type -eq "path") {
                Remove-MpPreference -ExclusionPath $value -ErrorAction Stop
            } elseif ($exclusion_type -eq "process") {
                Remove-MpPreference -ExclusionProcess $value -ErrorAction Stop
            } elseif ($exclusion_type -eq "extension") {
                Remove-MpPreference -ExclusionExtension $value -ErrorAction Stop
            }
            $result.changes.Add("Removed $exclusion_type exclusion: $value")
            $result.changed = $true
        }
    }
}
Catch {
    Fail-Json -obj $result -message "Failed to modify Windows Defender Exclusions - $($_.Exception.Message)"
}

Exit-Json -obj $result

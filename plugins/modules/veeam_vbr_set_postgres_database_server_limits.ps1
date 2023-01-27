#!powershell

# Copyright: (c) 2020, Chris Arceneaux <carcenea@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#Requires -Module Ansible.ModuleUtils.Legacy
#AnsibleRequires -OSVersion 6.2
#AnsibleRequires -CSharpUtil Ansible.Basic

$spec = @{
    options = @{
        os_type = @{ type = "str"; choices = "windows", "linux" }
        cpu_count = @{ type = "int" }
        ram_gb = @{ type = "int" }
        dump_to_file = @{ type = "str" }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version 2.0

# Functions
Function Connect-VeeamServer {
    try {
        # Accounts for switch from PSSnapin to Module in v11
        if (-Not (Get-Module -ListAvailable -Name Veeam.Backup.PowerShell)){
            Add-PSSnapin -PassThru VeeamPSSnapIn -ErrorAction Stop | Out-Null
        }
    }
    catch {
        Fail-Json -obj @{} -message  "Failed to load Veeam SnapIn on the target: $($_.Exception.Message)"
    }

    try {
        Connect-VBRServer -Server localhost
    }
    catch {
        Fail-Json -obj @{} -message "Failed to connect VBR Server on the target: $($_.Exception.Message)"
    }
}
Function Disconnect-VeeamServer {
    try {
        Disconnect-VBRServer
    }
    catch {
        Fail-Json -obj @{} -message "Failed to disconnect VBR Server on the target: $($_.Exception.Message)"
    }
}

# Connect
Connect-VeeamServer

# Processing input parameters
$os_type = $module.Params.os_type
$cpu_count = $module.Params.cpu_count
$ram_gb = $module.Params.ram_gb
$dump_to_file = $module.Params.dump_to_file

# If dump_to_file is specified, PostgreSQL server is not currently running the VBR DB
if ($dump_to_file) {
    # Checking for missing parameters...
    switch ($null) {
        $os_type {
            Fail-Json -obj @{} -message  "Missing 'os_type' parameter. Please refer to Veeam PowerShell documentation for more information on required parameters for the Set-VBRPSQLDatabaseServerLimits cmdlet."
        }
        $cpu_count {
            Fail-Json -obj @{} -message  "Missing 'cpu_count' parameter. Please refer to Veeam PowerShell documentation for more information on required parameters for the Set-VBRPSQLDatabaseServerLimits cmdlet."
        }
        $ram_gb {
            Fail-Json -obj @{} -message  "Missing 'ram_gb' parameter. Please refer to Veeam PowerShell documentation for more information on required parameters for the Set-VBRPSQLDatabaseServerLimits cmdlet."
        }
        Default {}
    }
    Set-VBRPSQLDatabaseServerLimits -OSType $os_type -CPUCount $cpu_count -RamGb $ram_gb -DumpToFile "$dump_to_file"
}
# If os_type is specified, a remote PostgreSQL server is currently running the VBR DB
elseif ($os_type) {
    # Checking for missing parameters...
    switch ($null) {
        $cpu_count {
            Fail-Json -obj @{} -message  "Missing 'cpu_count' parameter. Please refer to Veeam PowerShell documentation for more information on required parameters for the Set-VBRPSQLDatabaseServerLimits cmdlet."
        }
        $ram_gb {
            Fail-Json -obj @{} -message  "Missing 'ram_gb' parameter. Please refer to Veeam PowerShell documentation for more information on required parameters for the Set-VBRPSQLDatabaseServerLimits cmdlet."
        }
        Default {}
    }
    Set-VBRPSQLDatabaseServerLimits -OSType $os_type -CPUCount $cpu_count -RamGb $ram_gb
}
# Local PostgreSQL server currently running the VBR DB
else {
    Set-VBRPSQLDatabaseServerLimits
}

# Disconnect
Disconnect-VeeamServer

# Return result
$module.ExitJson()

#!powershell

# Copyright: (c) 2020, Chris Arceneaux <carcenea@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#Requires -Module Ansible.ModuleUtils.Legacy
#AnsibleRequires -OSVersion 6.2
#AnsibleRequires -CSharpUtil Ansible.Basic

$spec = @{
    options = @{
        state = @{ type = "str"; choices = "present", "absent", "adhoc"; default = "present" }
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

switch ( $module.Params.state) {
    "present" {
        Set-VBRConfigurationBackupJob -Enable:$true
    }
    "absent" {
        Set-VBRConfigurationBackupJob -Enable:$false
    }
    "adhoc" {
        Start-VBRConfigurationBackupJob | Out-Null
    }
    Default {}
}

# Disconnect
Disconnect-VeeamServer

# Return result
$module.ExitJson()

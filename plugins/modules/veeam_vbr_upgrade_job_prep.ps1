#!powershell

# Copyright: (c) 2020, Chris Arceneaux <carcenea@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#Requires -Module Ansible.ModuleUtils.Legacy
#AnsibleRequires -OSVersion 6.2
#AnsibleRequires -CSharpUtil Ansible.Basic

$spec = @{
    options = @{
        state = @{ type = "str"; choices = "disable", "enable"; required = $true }
        jobs_file = @{ type = "str"; required = $true }
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

# Setting Disabled Jobs csv file
$file = $module.Params.jobs_file

switch ( $module.Params.state) {
    "disable" {
        try {
            # Stopping all running Backup Jobs
            Get-VBRJob | Where-Object { $_.GetLastState() -eq 'Working' } | Stop-VBRJob

            # Backing up scheduled Backup Jobs
            Get-VBRJob | Where-Object { $_.IsScheduleEnabled -eq $True } | Select-Object Name | Export-Csv $file

            # Disabling schedule Backup Jobs
            $jobs = @()
            foreach ($job in Import-Csv $file){
                $jobs += $job | Disable-VBRJob -Job { $_.Name } | Select-Object Id,Name,@{Name = "Enabled"; Expression = {$false}}
            }

            # Saving info to output
            $module.Result.msg = "Backup Job names of all disabled jobs have been saved."
            $module.Result.file = $file
        }
        catch {
            Fail-Json -obj @{} -message "Failed to disable backup jobs: $($_.Exception.Message)"
        }
    }
    "enable" {
        try {
            $jobs = @()
            foreach ($job in Import-Csv $file){
                $jobs += $job | Enable-VBRJob -Job { $_.Name } | Select-Object Id,Name,@{Name = "Enabled"; Expression = {$true}}
            }

            # Saving info to output
            $module.Result.msg = "Backup Jobs in the specified file have been enabled."
            $module.Result.file = $file
            $module.Result.output = $jobs | ConvertTo-Json
        }
        catch {
            Fail-Json -obj @{} -message "Failed to enable backup jobs: $($_.Exception.Message)"
        }
    }
    Default {}
}

# Disconnect
Disconnect-VeeamServer

# Return result
$module.ExitJson()

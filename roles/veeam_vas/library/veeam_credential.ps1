#!powershell

# Copyright: (c) 2019, Markus Kraus <markus.kraus@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#Requires -Module Ansible.ModuleUtils.Legacy
#AnsibleRequires -OSVersion 6.2
#AnsibleRequires -CSharpUtil Ansible.Basic

$spec = @{
    options = @{
        type = @{ type = "str"; choices = "windows", "linux", "standard"; default = "standard" }
        username = @{ type = "str" }
        password = @{ type = "str" }
        state = @{ type = "str"; choices = "absent", "present"; default = "present" }
        description = @{ type = "str"; default = "Created by Ansible"}
        id = @{ type = "str"}

    }
    required_if = @(@("state", "present", @("username", "password")),
                    @("state", "absent", @("id")))
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version 2.0

# Functions
Function Connect-VeeamServer {
    try {
        Add-PSSnapin -PassThru VeeamPSSnapIn -ErrorAction Stop | Out-Null
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
    "present" { if ($module.Params.type -eq "standard") {
                    $Cred = Add-VBRCredentials -User $module.Params.username -Password "$($module.Params.password)" -Description "$($module.Params.description)"
                    }
                    else {
                        $Cred = Add-VBRCredentials -Type $module.Params.type -User $module.Params.username -Password "$($module.Params.password)" -Description "$($module.Params.description)"
                    }
                $module.Result.changed = $true
                $module.Result.id = $Cred.id
                }
    "absent" { $RemoveCred = Get-VBRCredentials | Where-Object {$_.id -eq $module.Params.id}
               $Cred = Remove-VBRCredentials -Credential $RemoveCred
               $module.Result.changed = $true
            }
    Default {}
}

# Disconnect
Disconnect-VeeamServer

# Return result
$module.ExitJson()

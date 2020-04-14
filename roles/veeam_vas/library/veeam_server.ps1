#!powershell

# Copyright: (c) 2019, Markus Kraus <markus.kraus@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#Requires -Module Ansible.ModuleUtils.Legacy
#AnsibleRequires -OSVersion 6.2
#AnsibleRequires -CSharpUtil Ansible.Basic

$spec = @{
    options = @{
        type = @{ type = "str"; choices = "esxi", "vcenter", "windows"; default = "esxi" }
        credential_id = @{ type = "str" }
        state = @{ type = "str"; choices = "absent", "present"; default = "present" }
        name = @{ type = "str" }
        id = @{ type = "str" }

    }
    required_if = @(@("state", "present", @("type", "name", "credential_id")),
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
    "present" { $Cred = Get-VBRCredentials | Where-Object {$_.id -eq $module.Params.credential_id}
                    switch ($module.Params.type) {
                        "esxi" {    $Server = Add-VBRESXi –Name $module.Params.name -Credentials $Cred
                                    $module.Result.changed = $true
                                    $module.Result.id = $Server.id  
                                }
                        "vcenter" { $Server = Add-VBRvCenter –Name $module.Params.name -Credentials $Cred
                                    $module.Result.changed = $true
                                    $module.Result.id = $Server.id   
                            
                                    }
                        "windows" {Fail-Json -obj @{} -message "Type not yet implemented."
                                    }
                        Default { }
                    }
                }
    "absent" { Fail-Json -obj @{} -message "State not yet implemented."
                }
    Default {}
}

# Disconnect
Disconnect-VeeamServer

# Return result
$module.ExitJson()

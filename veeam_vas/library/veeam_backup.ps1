#!powershell

# Copyright: (c) 2019, Markus Kraus <markus.kraus@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#Requires -Module Ansible.ModuleUtils.Legacy
#AnsibleRequires -OSVersion 6.2
#AnsibleRequires -CSharpUtil Ansible.Basic

$spec = @{
    options = @{
        type = @{ type = "str"; choices = "vi", "hv"; default = "vi" }
        entity = @{ type = "str"; choices = "tag", "vm"; default = "tag" }
        tag = @{ type = "str" }
        state = @{ type = "str"; choices = "absent", "present"; default = "present" }
        name = @{ type = "str" }
        repository = @{ type = "str" }
        id = @{ type = "str" }

    }
    required_if = @(@("state", "present", @("type", "entity", "name", "repository")),
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
    "present" { $Repositroy = Get-VBRBackupRepository -Name $module.Params.repository
                    switch ($module.Params.type) {
                        "vi" {      switch ($module.Params.entity) {
                                        "tag" { $Entity = Find-VBRViEntity -Tags | Where-Object {$_.Path -match "$($module.Params.tag)"} }
                                        "vm" { Fail-Json -obj @{} -message "Type not yet implemented."}
                                        Default { }
                                    }
                            
                                    $Backup = Add-VBRViBackupJob -Name $module.Params.name -Entity $Entity -BackupRepository $Repositroy
                                    $module.Result.changed = $true
                                    $module.Result.id = $Backup.id  
                                }
                        "hv" { Fail-Json -obj @{} -message "Type not yet implemented."
                            
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

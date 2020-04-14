#!powershell

# Copyright: (c) 2019, Markus Kraus <markus.kraus@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#Requires -Module Ansible.ModuleUtils.Legacy
#AnsibleRequires -OSVersion 6.2

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

# Create a new result object
$result = @{
    changed = $false
    veeam_facts = @{
        veeam_connection = @()
        veeam_repositories = @()
        veeam_servers = @()
        veeam_credentials = @()
        veeam_backups = @()
    }
}

# Get Veeam Connection
try {
    $Connection = Get-VBRServerSession
} catch {
    Fail-Json -obj $result -message "Failed to get connection details on the target: $($_.Exception.Message)"
}

# Get Veeam Server
try {
    [Array]$ServerList = Get-VBRServer
}
catch {
    Fail-Json -obj $result -message "Failed to get server details on the target: $($_.Exception.Message)"   
}

# Get Veeam Repositories
try {
    [Array]$RepoList = Get-VBRBackupRepository | Where-Object {$_.Type -ne "SanSnapshotOnly"} 
}
catch {
    Fail-Json -obj $result -message "Failed to get repository details on the target: $($_.Exception.Message)"   
}

# Get Veeam Credentials
try {
    [Array]$CredList = Get-VBRCredentials    
}
catch {
    Fail-Json -obj $result -message "Failed to get credential details on the target: $($_.Exception.Message)"   
}

# Get Veeam Backup Jobs
try {
    [Array]$BackupJobList = Get-VBRJob | Where-Object {$_.JobType -eq "Backup"}  
}
catch {
    Fail-Json -obj $result -message "Failed to get backup job details on the target: $($_.Exception.Message)"   
}

# Create result
$connection_info = @{}
$connection_info["user"] = $Connection.user
$connection_info["server"] = $Connection.server
$connection_info["port"] = $Connection.port

$result.veeam_facts.veeam_connection += $connection_info

foreach ($Repo in $RepoList) {
    $repo_info = @{}
    $repo_info["name"] = $repo.name
    $repo_info["type"] = $repo.typedisplay
    $repo_info["host"] = $($ServerList | Where-Object {$_.Id -eq $repo.HostId}).name
    $repo_info["friendlypath"] = $repo.friendlypath
    $repo_info["description"] = $repo.description

    $result.veeam_facts.veeam_repositories += $repo_info
}

foreach ($Server in $ServerList) {
    $server_info = @{}
    $server_info["id"] = $server.id
    $server_info["name"] = $server.name
    $server_info["description"] = $server.description
    $server_info["type"] = $server.info.typedescription

    $result.veeam_facts.veeam_servers += $server_info
}

foreach ($Cred in $CredList) {
    $cred_info = @{}
    $cred_info["id"] = $cred.id
    $cred_info["name"] = $cred.name
    $cred_info["username"] = $cred.username
    $cred_info["encryptedpassword"] = $cred.encryptedpassword
    $cred_info["description"] = $cred.description

    $result.veeam_facts.veeam_credentials += $cred_info
}

foreach ($backup in $BackupJobList) {
    $backup_info = @{}
    $backup_info["id"] = $backup.id
    $backup_info["name"] = $backup.name
    $backup_info["jobtype"] = $backup.JobType
    $backup_info["description"] = $backup.description

    $result.veeam_facts.veeam_backups += $backup_info
}

# Disconnect
Disconnect-VeeamServer

# Return result
Exit-Json -obj $result

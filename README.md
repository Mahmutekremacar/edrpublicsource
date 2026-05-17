[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12


$url = "https://raw.githubusercontent.com/ansible/ansible-documentation/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"


Invoke-Expression ((New-Object System.Net.WebClient).DownloadString($url))

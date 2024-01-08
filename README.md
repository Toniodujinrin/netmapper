**Netmapper** \n
Usage:\n
-d --discover: perform host discovery \n
-t<1-3> --timing<1-3> : set timing and decretion( 1-slow but very discrete, 3-fast but not discrete)\n
-g --gui: open GUI( still in production)\n
-s --scan: scan host host open ports \n
-r --response: show average response times and TTL \n
-o --os: perform os detection(still in production)\n
-h --hard: gather hardware details\n

Example: python3 netmapper -d -t 3 -s -r -o -h \n
Output:\n
![Screenshot_2024-01-08_16_02_44](https://github.com/Toniodujinrin/netmapper/assets/93059939/3b30bb3a-4ba6-46d9-9ac5-bce1dcef6222)

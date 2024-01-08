**Netmapper**
Usage:
-d --discover : perform host discovery 
-t<1-3> --timing<1-3> : set timing and decretion( 1-slow but very descrete, 3-fast but not decrete)
-g --gui: open GUI( still in production)
-s --scan: scan host host open ports 
-r --response: show average response times and ttl 
-o --os: perform os detection(still in production)
-h --hard: gather hardware details

Example: python3 netmapper -d -t 3 -s -r -o -h 
Output:
![Screenshot_2024-01-08_16_02_44](https://github.com/Toniodujinrin/netmapper/assets/93059939/3b30bb3a-4ba6-46d9-9ac5-bce1dcef6222)

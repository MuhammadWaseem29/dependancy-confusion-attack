#!/bin/bash
echo -e "\e[1;36m" ''' 
███╗   ███╗ ██████╗  ██████╗ ██████╗ ██╗    ██╗    ██╗    ██╗ █████╗ ███████╗██╗
████╗ ████║██╔═══██╗██╔═══██╗██╔══██╗██║    ██║    ██║    ██║██╔══██╗██╔════╝██║
██╔████╔██║██║   ██║██║   ██║██║  ██║██║ █╗ ██║    ██║ █╗ ██║███████║███████╗██║
██║╚██╔╝██║██║   ██║██║   ██║██║  ██║██║███╗██║    ██║███╗██║██╔══██║╚════██║╚═╝
██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██████╔╝╚███╔███╔╝    ╚███╔███╔╝██║  ██║███████║██╗
╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝  ╚══╝╚══╝      ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚═╝  v1.0.0
            Created by Muhammad Waseem  
\e[1;31mWarning:\e[0m \e[1;33mVerify results manually to avoid false positives.\e[0m 
\e[1;31mUse responsibly. Developer is not liable for misuse.\e[0m
'''
echo -e "\e[0m"

if [ -d $1 ];then
    echo '' >/dev/null 2>&1
else 
    mkdir $PWD/$1;
fi

echo -e "\e[1;34mChecking PyPI packages in $1\e[0m"
waybackurls $1 | sort -u | grep .py | sed 's/?.*//' | grep -v '/static/\|/media/\|.jpg\|.png\|.css\|.js' | sort -u | tee -a $PWD/$1/$1-py-urls.txt >/dev/null 2>&1;

echo -e "\e[1;35mRunning gau on $1\e[0m"
gau $1 | sort -u | grep .py | sed 's/?.*//' | grep -v '/static/\|/media/\|.jpg\|.png\|.css\|.js' | sort -u | tee -a $PWD/$1/$1-py-urls.txt >/dev/null 2>&1;

cd $PWD/$1;
echo -e "\e[1;32mFound $(cat $1-py-urls.txt | sort -u | wc -l) Python files\e[0m"
cat $1-py-urls.txt | sort -u | while read url;do
    wget $url.map >/dev/null 2>&1;
done

grep -oriahE "[^\"\'> ]+" | grep 'site-packages' | sed 's:.*/site-packages::' | cut -d '/' -f 1 | sort -u | grep -v '.py' | egrep '\b[a-z]+\b' | tee -a $1-py-packages.txt >/dev/null 2>&1;

rm $1-py-urls.txt;
if [ -s $1-py-packages.txt ];then
    echo -e "\e[1;33mFound some packages, verifying on PyPI\e[0m"
    cat $1-py-packages.txt | sort -u | while read pkg;do
        if $(curl -o /dev/null -s -w "%{http_code}\n" "https://pypi.org/project/$pkg" | grep "404" >/dev/null 2>&1); then
            echo -e "\e[1;31m$pkg - Private or unregistered package found!\e[0m" && echo $pkg >> $1-py-vuln.txt;
            echo -e "\e[1;31mPotential takeover: https://pypi.org/project/$pkg\e[0m"
        else
            echo -e "\e[1;32m$pkg - Available on PyPI\e[0m";
        fi
    done
else
    echo -e "\e[1;31mNo Python packages found.\e[0m"
fi

rm $1-py-packages.txt *.map.* *.map;

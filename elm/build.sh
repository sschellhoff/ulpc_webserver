#!/bin/bash
elm make src/Main.elm --output=main.js
if [ $? -eq 0 ];
then
    mv main.js ../js/main.js
    echo "moved output to ../js/"
fi

#!/bin/bash

rm getEntries
g++ getEntries.C `root-config --libs --cflags` -o getEntries

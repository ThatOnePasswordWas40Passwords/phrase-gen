export SHELL := /usr/bin/env TZ=UTC bash

all: build

include ./t1pw40p-common/makefiles/Makefile.python.in

export VERSION=$(shell ./t1pw40p-common/scripts/get-version)

build: package


.PHONY: all $(python-phonies)

#!/bin/bash

touch ~/.kube/config

"test" >> ~/.kube/config

cat ~/.kube/config

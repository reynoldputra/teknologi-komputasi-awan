#!/bin/bash

/entrypoint.sh mysqld &

npm run start &

wait -n

exit $?

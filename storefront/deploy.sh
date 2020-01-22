#!/bin/bash

## DESCRIPTION:
#  ███████╗███╗   ██╗██╗   ██╗██╗███████╗████████╗ █████╗
#  ██╔════╝████╗  ██║██║   ██║██║██╔════╝╚══██╔══╝██╔══██╗
#  █████╗  ██╔██╗ ██║██║   ██║██║███████╗   ██║   ███████║
#  ██╔══╝  ██║╚██╗██║╚██╗ ██╔╝██║╚════██║   ██║   ██╔══██║
#  ███████╗██║ ╚████║ ╚████╔╝ ██║███████║   ██║   ██║  ██║
#  ╚══════╝╚═╝  ╚═══╝  ╚═══╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝
#
## AUTHOR: Arrathilar

# get variables
NAME="Envista"
OWNER="apache:apache"
PROJECT_DIRECTORY="/home/arrathilar/development/envista/storefront/"
BUILD_DIRECTORY="build/"
WELCOME_TEXT="4paI4paI4paI4paI4paI4paI4paI4pWX4paI4paI4paI4pWXICAg4paI4paI4pWX4paI4paI4pWXICAg4paI4paI4pWX4paI4paI4pWX4paI4paI4paI4paI4paI4paI4paI4pWX4paI4paI4paI4paI4paI4paI4paI4paI4pWXIOKWiOKWiOKWiOKWiOKWiOKVlyAK4paI4paI4pWU4pWQ4pWQ4pWQ4pWQ4pWd4paI4paI4paI4paI4pWXICDilojilojilZHilojilojilZEgICDilojilojilZHilojilojilZHilojilojilZTilZDilZDilZDilZDilZ3ilZrilZDilZDilojilojilZTilZDilZDilZ3ilojilojilZTilZDilZDilojilojilZcK4paI4paI4paI4paI4paI4pWXICDilojilojilZTilojilojilZcg4paI4paI4pWR4paI4paI4pWRICAg4paI4paI4pWR4paI4paI4pWR4paI4paI4paI4paI4paI4paI4paI4pWXICAg4paI4paI4pWRICAg4paI4paI4paI4paI4paI4paI4paI4pWRCuKWiOKWiOKVlOKVkOKVkOKVnSAg4paI4paI4pWR4pWa4paI4paI4pWX4paI4paI4pWR4pWa4paI4paI4pWXIOKWiOKWiOKVlOKVneKWiOKWiOKVkeKVmuKVkOKVkOKVkOKVkOKWiOKWiOKVkSAgIOKWiOKWiOKVkSAgIOKWiOKWiOKVlOKVkOKVkOKWiOKWiOKVkQrilojilojilojilojilojilojilojilZfilojilojilZEg4pWa4paI4paI4paI4paI4pWRIOKVmuKWiOKWiOKWiOKWiOKVlOKVnSDilojilojilZHilojilojilojilojilojilojilojilZEgICDilojilojilZEgICDilojilojilZEgIOKWiOKWiOKVkQrilZrilZDilZDilZDilZDilZDilZDilZ3ilZrilZDilZ0gIOKVmuKVkOKVkOKVkOKVnSAg4pWa4pWQ4pWQ4pWQ4pWdICDilZrilZDilZ3ilZrilZDilZDilZDilZDilZDilZDilZ0gICDilZrilZDilZ0gICDilZrilZDilZ0gIOKVmuKVkOKVnQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg"

#color red - errors, default and yellow
R=$(tput setaf 1)
N=$(tput sgr0)
Y=$(tput setaf 3)

echo ${WELCOME_TEXT} | base64 --decode
printf "\n"

# check attributes
if [ -z "${OWNER}" ]; then
  printf "%-$(expr 80 - ${#b})s %-40s\n" $R"apache:apache owner:group are required" "[error]"$N
  exit 1
fi

# got to project dir
cd $PROJECT_DIRECTORY || exit

# check build dir
ls $BUILD_DIRECTORY || (
  mkdir -p build
  printf "$Y""Created build dir""$N"
)

# run build
npm run build || exit 0

# change owner to apache
chown $OWNER $BUILD_DIRECTORY

# restart apache
sudo systemctl restart httpd || exit

printf '%s%s%s%s' "$(tput setaf 3)" "$(tput blink)" "${NAME} was deployed" "$(tput sgr0)"
printf "\n"

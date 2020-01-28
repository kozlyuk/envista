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
APACHE_OWNER="apache:apache"
DEFAULT_ROOT_USER_WITH_ROOT="arrathilar"
PROJECT_OWNER_USERNAME="envista"
PROJECT_ROOT_DIRECTORY="/home/envista/envista/"
PROJECT_DIRECTORY="/home/envista/envista/storefront/"
BUILD_DIRECTORY="build/"
WELCOME_TEXT="4paI4paI4paI4paI4paI4paI4paI4pWX4paI4paI4paI4pWXICAg4paI4paI4pWX4paI4paI4pWXICAg4paI4paI4pWX4paI4paI4pWX4paI4paI4paI4paI4paI4paI4paI4pWX4paI4paI4paI4paI4paI4paI4paI4paI4pWXIOKWiOKWiOKWiOKWiOKWiOKVlyAK4paI4paI4pWU4pWQ4pWQ4pWQ4pWQ4pWd4paI4paI4paI4paI4pWXICDilojilojilZHilojilojilZEgICDilojilojilZHilojilojilZHilojilojilZTilZDilZDilZDilZDilZ3ilZrilZDilZDilojilojilZTilZDilZDilZ3ilojilojilZTilZDilZDilojilojilZcK4paI4paI4paI4paI4paI4pWXICDilojilojilZTilojilojilZcg4paI4paI4pWR4paI4paI4pWRICAg4paI4paI4pWR4paI4paI4pWR4paI4paI4paI4paI4paI4paI4paI4pWXICAg4paI4paI4pWRICAg4paI4paI4paI4paI4paI4paI4paI4pWRCuKWiOKWiOKVlOKVkOKVkOKVnSAg4paI4paI4pWR4pWa4paI4paI4pWX4paI4paI4pWR4pWa4paI4paI4pWXIOKWiOKWiOKVlOKVneKWiOKWiOKVkeKVmuKVkOKVkOKVkOKVkOKWiOKWiOKVkSAgIOKWiOKWiOKVkSAgIOKWiOKWiOKVlOKVkOKVkOKWiOKWiOKVkQrilojilojilojilojilojilojilojilZfilojilojilZEg4pWa4paI4paI4paI4paI4pWRIOKVmuKWiOKWiOKWiOKWiOKVlOKVnSDilojilojilZHilojilojilojilojilojilojilojilZEgICDilojilojilZEgICDilojilojilZEgIOKWiOKWiOKVkQrilZrilZDilZDilZDilZDilZDilZDilZ3ilZrilZDilZ0gIOKVmuKVkOKVkOKVkOKVnSAg4pWa4pWQ4pWQ4pWQ4pWdICDilZrilZDilZ3ilZrilZDilZDilZDilZDilZDilZDilZ0gICDilZrilZDilZ0gICDilZrilZDilZ0gIOKVmuKVkOKVnQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg"

#color red - errors, default and yellow
R=$(tput setaf 1)
N=$(tput sgr0)
Y=$(tput setaf 3)

echo ${WELCOME_TEXT} | base64 --decode
printf "\n"

# check existing DEFAULT_ROOT_USER_WITH_ROOT
if [ $(getent passwd $DEFAULT_ROOT_USER_WITH_ROOT) ]; then
  printf $Y"${DEFAULT_ROOT_USER_WITH_ROOT} exist\n"$N
else
  printf $R"${DEFAULT_ROOT_USER_WITH_ROOT} does not exist\n"$N
  exit 0
fi

# check existing PROJECT_OWNER_USERNAME
if [ $(getent passwd $PROJECT_OWNER_USERNAME) ]; then
  printf $Y"${PROJECT_OWNER_USERNAME} exist\n"$N
else
  printf $R"${PROJECT_OWNER_USERNAME} does not exist\n"$N
  exit 0
fi

# check attributes
if [ -z "${APACHE_OWNER}" ]; then
  printf "%-$(expr 80 - ${#b})s %-40s\n" $R"apache:apache owner:group are required" "[error]"$N
  exit 1
fi

# move to project root dir
cd $PROJECT_ROOT_DIRECTORY || exit

# pull from git
sudo -u ${PROJECT_OWNER_USERNAME} git pull origin master

# move to project dir
cd $PROJECT_DIRECTORY || exit

# delete or create build dir
if [ -d "$BUILD_DIRECTORY" ]; then
  sudo rm -rfv $BUILD_DIRECTORY
  mkdir --verbose $BUILD_DIRECTORY
else
  mkdir --verbose $BUILD_DIRECTORY
fi

# run install
npm install || exit 0

# run build
npm run build || exit 0

# change owner to apache
chown $APACHE_OWNER $BUILD_DIRECTORY

# restart apache
sudo systemctl restart httpd || exit

# restart celery
sudo systemctl restart celeryd.service || exit

printf '%s%s%s%s' "$(tput setaf 3)" "$(tput blink)" "${NAME} was deployed" "$(tput sgr0)"
printf "\n"

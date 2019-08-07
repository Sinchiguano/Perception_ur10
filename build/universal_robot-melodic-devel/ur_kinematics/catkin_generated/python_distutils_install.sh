#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/casch/ws_moveit/src/universal_robot-melodic-devel/ur_kinematics"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/casch/ws_moveit/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/casch/ws_moveit/install/lib/python2.7/dist-packages:/home/casch/ws_moveit/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/casch/ws_moveit/build" \
    "/usr/bin/python2" \
    "/home/casch/ws_moveit/src/universal_robot-melodic-devel/ur_kinematics/setup.py" \
    build --build-base "/home/casch/ws_moveit/build/universal_robot-melodic-devel/ur_kinematics" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/casch/ws_moveit/install" --install-scripts="/home/casch/ws_moveit/install/bin"

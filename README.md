# Autonomous_Bot_Navigation
 * This is a directory of programs written for an indoor navigation bot.
 * A kinect attached on the roof captures the image of the floor and sends it to the server. 
 * The python script on the server uses openCV libraries to detect the obstacles on the floor and convert the image in to a maze.
 * Then a simple BFS is run on the maze for finding the path. The start and end are recognised by the color coding.
 * The directions are then sent to the Raspberrypi attached to the bot that drives the bot to the destination.

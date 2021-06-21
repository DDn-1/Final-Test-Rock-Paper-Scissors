# Final-Test-Rock-Paper-Scissors

- Daniel Arturo Bustillos Vila

# Problem

---

For this problem, you will have to implement the well-known Rock Paper Scissors game without
using any neural network based method. Your camera will have to recognize the movement of
your hands as rock, paper, or scissors in any light conditions. After your turn, your computer
should logically play the game in a consistent manner. Although you should uniquely use basic
libraries for this problem (OpenCV), you can use the rock paper scissors dataset at
Roboflow.com to speed up your coding. A complete game should consist of three turns for you,
three turns for the computer, and a clear message of who is the winner. Now, your chances to
get a good mark will rise if you develop a meaningful game where the computer always wins.
To submit your answer to this problem, you must hand in a python file capable of playing the
game through a webcam. Also, a github repository where you commit frequently.

# Method to recognize

---

The method is use the funcition of OpenCV which is matchTemplate. This function find or search the location of a template image in a large image. 
About the classication, the images used to compare are 10 for each class (rock, paper, scissors), the code always compare the frame of the video 
with all images of the datasets. And with the function cv.minMaxLoc(), it's possible to find the maximun values of the prediction of each class.
Then, it compares the max value of each class and find the max value which is the prediction. To improve this method, is good to put a threshold 
to limit the possibilities to find a class.
A disadvantage of use match Template() is the number of comparisons that can be made in a period of time, because the more comparisons or 
images you have, the longer it will take to classify. 

# Calibration

---

On the dataset, this is a calibration that can be performed at any time, that is, new images are taken for each class. So this game can be adapted
 to each situation that arises. In addition, The movements made by the computer also come from an image of the dataset of each class.

# Rules

---

The rules that the computer follows are simple, but widely used for this game. The first rule is that if the player wins, they will generally get
 the same class. The second rule is that if it loses then it will switch to the next class found in the loop (rock - paper - scissors), for example,
If your previous play was rock and you lost, your next play may be paper. And the third rule is if the first or second rule is not met, then a random
 number is generated between 0 and 1, if this number is greater than 0.7 but less than 0.8 then the computer puts rock, if it is between 0.8 and 0.9
 the computer puts paper, and if it is between 0.9 and 1 the computer puts scissors.

# References

---

[1]  .  Much of this code was based on this github.  https://github.com/TolgaGolet/Rock-Paper-Scissors_OpenCV-Python

[2]  .  https://www.youtube.com/watch?v=T-0lZWYWE9Y

[3]  .  https://docs.opencv.org/4.5.2/d4/dc6/tutorial_py_template_matching.html

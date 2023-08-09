# Real-time 3D Screen Illusion: Computer Vision & Perspective Projection with PyGame
Author: [Avi Shah](https://www.linkedin.com/in/-avishah/) (2023)

Create a captivating 3D digital illusion using computer vision techniques and perspective projection. This project utilizes Python, Pygame, OpenCV, MediaPipe, and your webcam to simulate a 3D space in 2D, providing an immersive visual experience that responds to the user's movement in real-time.

## Video Demonstration
https://github.com/avishah3/3D-Screen-Illusion/assets/115107522/1c21f686-8c66-4c99-ac25-36731cb316c6

## How it Works
* The main script, screen_effect.py, calls track_eyes.py to begin webcam recording and creates a new PyGame window. 
* The track_eyes.py script employs the MediaPipe and OpenCV library to create a face mesh and updates eye location data in real-time.
* screen_effect.py utilizes rectangles.py to create thousands of rectangles at different z locations (this creates the infinite tunnel)
* screen_effect.py utilizes the graphics.py script to create multiple image planes at different z locations
* rectangles.py and graphics.py have similar .draw() functions that renders a single object based on its location and the current eye location
* The further away the z distance, the darker and smaller the objects are (this is expressed logarithmically to achieve perspective projection)
* screen_effect.py loops through all the rectangles and graphics and calls their draw functions

## Getting Started
1. Clone the repository to your local machine.
2. Install the required libraries in requirements.txt
3. Run screen_effect.py and customize to your preference

## Final Thoughts
The inspiration behind this project comes from the world of visual effects, particularly the use of After Effects' camera tools to transform 2D layers into a 3D scene. Looking ahead, I hope to create a website that showcases this illusion or see others use this technique to create immersive visuals.

I have not encountered other projects that achieve a similar interactive 3D-depth illusion within a 2D renderer (this might be one of the first projects related to this topic). The most related project I found involved the rotation of 3D objects in your web browser [here](https://github.com/vivien000/trompeloeil).

Any feedback and contributions to refine and expand this project's potential are welcome!

# LS Detection from Stock Graph

## Install dependencies
```
opencv-python
```
In windows, we're using 4.6.0.66 version, and 4.2.0.32 in Ubuntu.

## How to run
Check the connection of camera.
After installation of opencv, please run the below command.

```commandline
python main.py --camera --show
```
In case that several cameras are available, Please select one of them. Default camera index is 0.
 
If you need to process the video file, please point the video path.
```commandline
python main.py --video "path/to/video" --show
```
Here, argument **_show_** is for displaying the detection result.

    usage: main.py [-h] [-c] [-v VIDEO] [--show]
    
    optional arguments:
      -h, --help            show this help message and exit
      -c, --camera          camera to be processed. (default: False)
      -v VIDEO, --video VIDEO
                            Path for video file to be processed. (default: None)
      --show                Showing process and result frame. (default: False)


You can check the result in this video - video_output.mp4



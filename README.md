# LS Detection from Stock Graph

## Install dependencies
    opencv-python
    python-dotenv
    requests
    mss
`python-dotenv` is for **_slack-notification_**. For slack-notification, please create `.env` file.

## How to run
Check the connection of camera.
After installation of opencv, please run main.py.

Here, argument **_show_** is for displaying the detection result.

    usage: main.py [-h] [-i INPUT_TYPE] [-c CONFIG] [-v VIDEO] [--show] [--log_file LOG_FILE]

    optional arguments:
    -h, --help            show this help message and exit
    -i INPUT_TYPE, --input_type INPUT_TYPE
                            input type to be processed. (default: capture)
    -c CONFIG, --config CONFIG
                            config file path of ticker (default: ticker.config)
    -v VIDEO, --video VIDEO
                            Path for video file to be processed when input type is video. (default: None)
    --show                Showing process and result frame. (default: False)
    --log_file LOG_FILE   log file path (default: None)

### Camera
```commandline
python main.py --camera --show
```
In case that several cameras are available, Please select one of them. Default camera index is 0.
 
### Video
If you need to process the video file, please point the video path.
```commandline
python main.py --video "path/to/video" --show
```
### Screen Capture
In case of screen capture, Please use the below command. The number of ticker in config file and the number of user-selected rectangles should be same. Otherwise, error message will be displayed.
```commandline
python main.py -i capture -c ticker.config
```

https://user-images.githubusercontent.com/96384530/184595640-47954005-1199-4cfd-bf85-2fa601dcf57a.mp4

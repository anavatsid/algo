# LS Detection from Stock Graph

## Install dependencies
    opencv-python
    python-dotenv
    requests
    mss
    ibapi
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
    --trade               process order placement. (default: False)
    

### Screen Capture
In case of screen capture, Please use the below command. If so, the available ticker names will be displayed from config file. From there, select one of them and select the specific area on screeen.
```commandline
python main.py -i capture --show --trade
```


https://user-images.githubusercontent.com/96384530/184595640-47954005-1199-4cfd-bf85-2fa601dcf57a.mp4

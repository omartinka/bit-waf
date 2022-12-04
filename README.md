# BIT-WAF 

> Disclaimer: This is a school project. Barely works. Use at your own risk.

## What's this

This is a web application firewall. Instead of the traditional approach using regular expressions, we decided to use machine learning to determine whether an input is malicious or not. So far, we have two classification models, one for xss and one for sqli.

Unfortunately, we decided to use our own datasets, which lack a lot of possible inputs and are filled with lots of noise. Therefore the trained models are not good, and if they encounter something slightly different than what they are used to, the outcome is unpredictable. A classbook example of overfitting. But the classification reports report accuraccy >90%, so the product is easy to sell 😎.

On the other hand, it has a neat little management interface in which you can manage rules for each endpoint separately. 

## Installation and usage:

1. Create and initialize a python virtual environment somewhere
     - `python -m venv bitwaf` 
     - `source /path/to/venv/bin/activate` 
2. Clone the repository and install requirements using `pip install -r requirements.txt`
3. Add example hostnames to `/etc/hosts` file:
      ```bash
      # BIT
      127.0.0.1  derave1.local
      127.0.0.1  derave2.local
      127.0.0.1  api.fw-management.local
      ```
4. Everything is ready to use. Start the vulnerable applications by naviganting into their respective directories (`cd ./derave` and `cd ./derave2`) and running them by `python run.py`
   
   If you wish to change the port or IP addresses, change the `PORT` and `HOST` variables directly in the `run.py` file.

## WAF startup instructions

WAF is located in the `./firewall` directory. 

To run it, it needs a few command line arguments:
  - `--xss <name>` - specifies name of classification model to use for XSS detection
  - `--sqli <name>` - specifies name of classification model to use for SQLi detection
  - `--train-xss <data>` - trains the xss detection model on startup. needs dataset name `<data>` placed in `./data` folder. takes a few seconds.')
  - `--train-sqli <data> ` - trains the sqli detection model on startup. needs dataset name `<data>` placed in `./data` directory. takes a few seconds.

Both the models and the datasets we used are provided in the repository in the `./firewall/data` folder, so the app can be started right away by `python main.py --xss xss.bin --sqli sqli.bin`

If you wish to train the datasets, an example would be `python main.py --train-xss dataset.txt --train-sqli dataset_sqli.txt`

## Management interface

By default, the WAF has no rules and does not redirect to any internal applications. To change that, you can either manually rewrite the `.ruleset` file, or you can use our web interface written in `vue.js`

1. Navigate into the `fw-management` directory
2. Install dependencies using `npm install`
3. Run the management using `npm run dev`

It should become available at `http://localhost:5173`

![](/media/1.png)

You can add which host maps to which internall IP address by the `Hostname` and `Internal IP` fields. In each application, you can specify what rules should apply in what endpoints.

Do not forget to click `Apply` after every configuration change.  The `Load` button does not work yet.

I also planned to dockerize all this but i'm lazy.
# WSB-Tracker

### Dependencies 
python 3.7 or higher  
pip install numpy  
pip install pandas  
pip install yfinance  
pip install matplotlib  

### Usage

from the command line enter 
```bash 
python main.py MM/DD/YYYY [# of iterations] [top X stocks]
```

The below example will run for October 10th, 2020. It will go througn 10,000 posts and obtain the top 20 stocks
```bash
python main.py 10/10/2020 10000 20
```

Here is the output for the above example:
![image](https://user-images.githubusercontent.com/52977770/147697811-2fb3e8e1-3d7b-491c-bc52-c79b2e135b97.png)


![image](https://user-images.githubusercontent.com/52977770/147697833-bff653e2-55a7-44da-af48-c8e4d19b4da0.png)


Due to deprecation of PSAW, the first version no longer works, version 2 has been uploaded, rate limit has decreased significantly.

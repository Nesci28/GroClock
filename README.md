# GroClock

The idea behind this little Python Script is to copy the behavior of a GroClock (https://gro.co.uk/product/gro-clock/) without paying the astronomous price of it, at the end of the day, it is a clock...

I had a RPi collecting dust and have wanted to find something to do with it for about 4 years.

Bought some LEDs and learnt how to plug everything together:

[![IMG-0038.jpg](https://i.postimg.cc/0jSLYYL2/IMG-0038.jpg)](https://postimg.cc/fSw2Z9z6)

In Action:

[![IMG-0039.jpg](https://i.postimg.cc/43KwHfCX/IMG-0039.jpg)](https://postimg.cc/qtT29dMF)

### Behavior:

The 5 red lights lights up then, every 1/5th of the time between the red and yellow configs, one of them turns off.  
At the yellow config time, the four yellow lights turn on then every 15 minutes one of them turns off, during that time, the baby can play in his/her bedroom.  
Finally, the green one lights up and the baby can finally go wake everybody up!

### Configs:

```json
{
  "GPIO": {
    "red": [22, 10, 9, 11, 5],
    "yellow": [3, 4, 17, 27],
    "green": [2]
  },
  "time": {
    "red": {
      "hour": 19,
      "minute": 30
    },
    "yellow": {
      "hour": 6,
      "minute": 0
    },
    "green": {
      "hour": 7,
      "minute": 0
    }
  }
}
```

Set up the GPIO numbers in order from the first one to turn off to the last one.

### How to Run

```bash
git clone https://github.com/Nesci28/GroClock.git

sudo apt-get update
sudo apt-get install tmux

tmux new-session -d -s groclock 'python main.py'

tmux kill-session -t groclock
```

# Five Chungus

FiveChungus is a peer-to-peer file sharing/distribution application that lets users to share their files via localhost.

This was a school project from Bahcesehir University, Introduction to Computer Networks course. Main program is written in Python, UI is added via Electron.js

## Requirements
- Node.js
- Python


## Installation

```bash
# Clone this repo
git clone https://github.com/Kaaleyah/FiveChungus.git

# Navigate to the project
cd FiveChungus/gui

#Install dependencies
npm install
```

## Usage
Move the file you want to share to `files` folder. Enter the file name in Announce part to share it. App will share it to other devices. Make sure the app is open in other devices when you announce the file. 

Available files will be shown under Discover section with IPs

To download a file, enter its name and the app will download it. Downloaded files will be in `files` folder and they will be shared too.
![alt text](https://i.ibb.co/HXV48yR/Screenshot-2022-07-04-184136.png)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

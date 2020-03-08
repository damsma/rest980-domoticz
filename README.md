# rest980-domoticz
Domoticz plugin to control your iRobot Roomba with koalazak/rest980 (https://github.com/koalazak/rest980)

Instructiuons:
<h1>1. Install rest980</h1>

<pre><code>apt-get install npm nodejs
git clone https://github.com/koalazak/rest980.git
cd rest980
npm install
nano config/default.json
</code></pre>

Type in the right values for your Roomba, should look something like this:
<pre><code>  ...
  "blid": "1234567890123456",
  "password": ":1:1234567890:abcDEFghiJKMnopR",
  "robotIP": "192.168.100.90",
  "firmwareVersion": 2,
  ...
</code></pre>

and save the config file

see <a href="https://github.com/koalazak/dorita980#how-to-get-your-usernameblid-and-password" target="_blank">dorita980</a> for more information and instructions for obtaining blid and password.

Start rest980 forever with with PM2
<pre><code>npm i -g pm2
pm2 startup
pm2 start npm --name "rest980-roomba" -- start
pm2 save
</code></pre>

check if everything works fine
<pre><code>wget http://127.0.0.1:3000/api/local/action/start > /dev/null
</code></pre>

if your roomba started cleanig, you can install the plugin now.


<h1>2. Install this plugin</h1>

<pre><code>cd domoticz/plugins
git clone https://github.com/damsma/rest980-domoticz.git
systemctl restart domoticz
</code></pre>

<h1>3. Configure the plugin</h1>
You can now add "iRobot Roomba (rest980-domoticz)" on the hardware page in domoticz. The device will be created automatically.

If you installed rest980 on the same machnie as domoticz, you can leave the default plugin settings, otherwise, type in the IP adress of the machnie you installed rest980 on.
